# nltk
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords #Listas de stopwords
from nltk.tokenize import word_tokenize#Tokens
import re #regex

# tokens que necesitan ser limpiados del corpus y que no
# se encuentran en la lista de stopwords
more = ["si", "bien", "ahora", "así", "aquí", "pues"]
stopwords_list = stopwords.words('spanish') + more

def get_tokens_clean(text, stop_words=False):
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
        if w not in stopwords_list and w != '':
            clean.append(w)
        elif not stop_words and w != '':
            clean.append(w)
    return clean

def flatten(lst):
    '''
    Junta las listas anidadas en una 

    Args:
        lst (list): Lista de listas
    '''
    return [item for sub in lst for item in sub]