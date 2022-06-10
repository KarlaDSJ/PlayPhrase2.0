from collections import Counter
import pickle
from tqdm import tqdm 
import numpy as np
from .utils import *

class TFIDF():
    """
    Clase que dado un corpus calcula el valor TFIDF de cada palabra 
    Crea vectores TFIDF y recupera documentos

    Args:
        data (Data): objeto de tipo data con los subtítulos en una lista
    """
    def __init__(self, data):
        self.data = data #Objeto de tipo data
        self.__term_list = self.data.get_frequencies()
        self.__tfidf = []
    
    @property
    def term_list(self):
        """Regresa el tf e idf de cada palabra (objeto pandas)"""
        return self.__term_list
    
    @term_list.setter
    def term_list(self, path):
        """Carga los valores previamente calculados"""
        with open(path, "rb") as f:
            self.__term_list = pickle.load(f)

    @property
    def tfidf(self):
        """Regresa el tfidf de cada palabra"""
        return self.__tfidf
    
    @tfidf.setter
    def tfidf(self, path):
        """Carga los valores previamente calculados"""
        with open(path, "rb") as f:
            self.__tfidf = pickle.load(f)

    def get_idf(self, path, document = True):
        """
        Realiza el cálculo de idf para cada palabra en el corpus
        y lo guarda

        Args:
            path (str): ruta del archivo 
        """
        idf = {}
        corpus = self.data.documents.values() if document else self.data.all_subtitles
        num_documents = len(corpus)
        for term in tqdm(self.__term_list.index):
            total_documents = 0
            for token_list in corpus:
                if term in token_list:
                    total_documents += 1
                    
            #Asignación de idf
            idf[term] = -np.log2(total_documents/num_documents)
        self.__save_idf(path, idf)

    def __save_idf(self, path, idf):
        """
        Método auxiliar para guardar los valores tf, idf de cada palabra

        Args:
            path (str): ruta del archivo 
            idf (dic): valores idf de cada palabra
        """
        #Agregamos el idf al dataframe
        self.term_list['idf'] = idf.values()
        self.term_list = self.term_list.sort_values(by='idf', ascending=False)
        #Lo guardamos
        pickle.dump(self.term_list, open(path, "wb"))

    def __do_padding(self, vector, t):
        '''
        Agrega 0 al vector si no es del tamaño t 
        Args:
            vector (lst): lista de tamaño diferente
            t (int): Tamaño esperado del vector
        '''
        for _ in range(0, t - len(vector)):
            vector.append(0)

    def get_tfidf(self, path, a=0.5, document=True):
        """
        Realiza el calculo del valor tfidf para cada palabra en el corpus
        y lo guarda en un archivo

        Args:
            path (str): ruta del archivo
            a (float): valor entre 0 y 1 para calcular tf relativo
        """
        self.__tfidf = {} if document else []
        corpus = self.data.documents.items() if document else self.data.all_subtitles
        #Guarda los tfidf
        for token_list in tqdm(corpus):
            if document:
                doc = token_list[0]
                token_list = token_list[1]
            if token_list != []:
                #Cuenta la frecuencia del término en el documento
                term_freq_doc = Counter(token_list)
                #Obtiene la frecuencia mayor
                max_freq = np.max(list(term_freq_doc.values()))
                #Guarda tfidf por documento
                tfidf_doc = {}
                for term in term_freq_doc:
                    #Valor de TF
                    tf = a + (1-a)*(self.term_list["Frequency"][term]/max_freq)
                    #Valor de tfidf
                    tfidf_doc[term] = tf*self.term_list["idf"][term]
                
                if document:
                    self.__tfidf[doc] = tfidf_doc
                else:
                    self.__tfidf.append(tfidf_doc)
        pickle.dump(self.__tfidf, open(path, "wb"))
    
    def get_tfid_vectors(self, document=True):
        '''
        Por cada palabra de cada subtítulo se 
        busca su valor tfidf y se crea un vector con esos valores

        Args:
            do
        '''
        i = 0
        #Iteramos sobre los canales
        for chanel in tqdm(self.data.corpus):
            for video in chanel:
                #Cada texto se guarda por oraciones
                if 'subtitles' in video:
                    for s in video['subtitles']:
                        vector = []
                        if document:
                            for t in s["text"]:
                                vector.append(self.tfidf[video['id']][t])
                        elif s['text'] != []:
                            vector = list(self.tfidf[i].values())
                            self.__do_padding(vector, len(s['text']))
                            i += 1
                        s["tfid"] = vector
    
    def recover_documents(self, query):
        """
        Función para recuperar documentos en base a su valor de TFIDF.
        
        Args:
            query (str): Cadena a buscar
        """
        #Obtener términos en query y procesarlos
        proc_query = flatten([get_tokens_clean(w) for w in query.split()])
        #Iteramos sobre los canales
        for chanel in self.data.corpus:
            for video in chanel:
                #Cada texto se guarda por oraciones
                if 'subtitles' in video:
                    for i,s in enumerate(video['subtitles']):
                        score = 0
                        for w in proc_query:
                            #Revisa si todos los terminos de la query que están en el documento
                            if w in s["text"]:
                                index = s["text"].index(w)
                                score += s["tfid"][index]
                        yield (video['id'], i), score