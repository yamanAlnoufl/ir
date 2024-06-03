import nltk
from collections import defaultdict
import json

def create_inverted_index(tokenized_dict):
    inverted_index = defaultdict(list)
    for x, doc_content in tokenized_dict.items():
        # Combine the "title" and "abstract" fields
        text = " ".join(doc_content)
        
        # Tokenize the text and apply any desired text preprocessing steps
        terms = [term.lower() for term in nltk.word_tokenize(text) if term.isalnum()]

        # Add the doc_id to the list associated with each term in the inverted index
        for term in terms:
            inverted_index[term].append(x)
    
    return dict(inverted_index)
