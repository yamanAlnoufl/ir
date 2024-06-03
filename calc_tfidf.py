import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz

def convert_corpus(tokenized_dict):
    temp = {}
    for key, value in tokenized_dict.items():
        my_string = " ".join(value)
        temp[key] = my_string

    return temp


def create_tfidf_matrix(documents, file_path):
   

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    save_npz(file_path, tfidf_matrix)
