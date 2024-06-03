import string
import nltk
from nltk import pos_tag
from collections import defaultdict
import re

from nltk.corpus import stopwords, words
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import pycountry
import pandas as pd
from textblob import TextBlob

def preprocess_text(text):
    def replace_percent_text(text):
        return text.replace('%', ' percent')
    
    def expand_country_names(text):
        if isinstance(text, str):
            for country in pycountry.countries:
                text = text.replace(country.alpha_2, country.name)
                text = text.replace(country.alpha_3, country.name)
        return text
    
    def clean_text(text):
        return re.sub(r'[^\w\s]', ' ', text)
    
    def lower_text(text):
        return text.lower()
    
    def stem_text(text):
        stemmer = PorterStemmer()
        tokens = nltk.word_tokenize(text)
        stems = [stemmer.stem(token) for token in tokens]
        return ' '.join(stems)
    
    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        words = nltk.word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in stop_words and word.isalpha()]
        return ' '.join(filtered_words)
    
    def correct_spelling(text):
        blob = TextBlob(text)
        return str(blob.correct())
    
    text = replace_percent_text(text)
    text = expand_country_names(text)
    text = clean_text(text)
    text = lower_text(text)
    text = stem_text(text)
    text = remove_stopwords(text)
    text = correct_spelling(text)
    
    return text

def tokenize_and_remove_stop_words(text):
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words and word.isalpha()]
    return filtered_words

def process_data(jsonl_file_path):
    df = pd.read_json(jsonl_file_path, lines=True)
    
    data_title = {}
    data_text = {}
    
    for i, row in df.iterrows():
        title = preprocess_text(row['title'])
        text = preprocess_text(row['text'])
        data_title[str(row['_id'])] = title 
        data_text[str(row['_id'])] = text
    
    tokenized_dict = {}
    
    for key, value in data_title.items():
        title_tokens = tokenize_and_remove_stop_words(value)
        text_tokens = tokenize_and_remove_stop_words(data_text[key])
        tokenized_dict[key] = title_tokens + text_tokens
    
    return tokenized_dict
