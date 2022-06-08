from operator import itemgetter
from os import listdir
from os.path import isfile, join
#Para ver las palabras
from collections import Counter, defaultdict
# nltk
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords #Listas de stopwords
from nltk.tokenize import word_tokenize#Tokens
import re #regex
from tqdm import tqdm #Medir el progreso del entrenamiento
import json
import pandas as pd
import pickle

class Data ():
    """
    Clase para cargar y manipular los datos para ese proyecto

    En caso de no pasarle la ruta del archivo pickle con los datos limpios 
    se cargaran de la ruta ../corpus/data
    """
    def __init__(self, path):
        # tokens que necesitan ser limpiados del corpus y que no
        # se encuentran en la lista de stopwords
        self.more = ["si", "bien", "ahora", "así", "aquí", "pues"]
        self.stopwords_list = stopwords.words('spanish') + self.more
        self.all_subtitles = []
        self.documents = defaultdict(list)

        if path == "../corpus/data":
            self.__corpus = self.__get_txt(path)
        else:
            with open(path, "rb") as f:
                self.__corpus = pickle.load(f)

    @property
    def corpus(self):
        """Variable que contiene todo el corpus d ela carpeta corpus/data"""
        return self.__corpus

    def __get_txt(self, path):
        """
        Regresa una lista con el contenido de todos los archivos de un directorio

        Args:
            path (str): ruta de la carpeta
        """
        txt = []
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

        for file in onlyfiles:
            with open(path+"/"+file, 'rb') as f:
                txt.append(json.loads(f.read().decode('utf-8', 'replace')))
        return txt

    def clean_videos(self):
        '''
        Limpia el corpus de cada video mantiendo la estructura.
        '''
        #Iteramos sobre los canales
        for chanel in tqdm(self.corpus):
            for video in chanel:
                #Cada texto se guarda por oraciones
                if 'subtitles' in video:
                    for sub_key in range(len(video['subtitles'])):
                        video['subtitles'][sub_key]['text']=self.__get_tokens_clean(video['subtitles'][sub_key]['text'])
        
        pickle.dump(self.corpus, open("../pkl/clean_videos.pkl", "wb"))


    def __get_tokens_clean(self, text, stop_words=True):
        '''
        Genera los tokens de una cadena y los limpia
        (quita símbolos raros y stopwords)
        
        Args:
            text (str): cadena
        '''
        tokens = word_tokenize(text)
        clean = []
        pattern = r'[-_{}(),;:"#\/.¡!¿?·\[\]\'`]'
        for w in tokens:
            #quita stopwords y convierte a minúsculas
            w = re.sub(pattern,'', w.lower())
            if w not in self.stopwords_list and w != '':
                clean.append(w)
            elif not stop_words and w != '':
                clean.append(w)
        return clean

    def get_all_subtitles(self):
        '''
        Mezcla el corpus de cada video en una entrada del
        diccionario movies en un solo corpus, 
        guarda los diálogos por línea tokenizados y limpios
        '''
        self.all_subtitles = []
        #Iteramos sobre los canales
        for chanel in tqdm(self.corpus):
            for video in chanel:
                #Cada texto se guarda por oraciones
                if 'subtitles' in video:
                    self.all_subtitles += [s['text'] for s in video['subtitles']]
                    for s in video['subtitles']:
                        self.documents[video['id']] += s["text"]
        return self.all_subtitles

    def flatten(self):
        """Junta todos los subtítulos de los vídeos en una sola lista"""
        return [item for sub in self.all_subtitles for item in sub]
    
    def get_frequencies(self):
        """
        Regresa un onjeto pandas con el número de veces que 
        aparece cada palabra en el corpus
        """
        if self.all_subtitles == []: self.get_all_subtitles()
        frequencies = Counter(self.flatten())
        term_list = pd.DataFrame(sorted(frequencies.items(), key=itemgetter(1), reverse=True), 
                                columns=['Token','Frequency'])

        term_list = term_list.set_index(term_list['Token'])
        term_list.pop('Token')
        return term_list