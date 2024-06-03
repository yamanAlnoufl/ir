import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import load_npz
from flask import Flask, request, jsonify
from implment_cluster import readFileCluster, implmentClusterAlg
from query_processing import perform_query_search
from implment_topic import readFileTopic,implmentTopicAlg
from eval import eval
from eval2 import eval2
from get_queries import getQueries 
from suggistions import refine_query
# Create an instance of Flask
app = Flask(__name__)
# Provide the path to your JSONL file
# Initialize variables
dff = pd.DataFrame()
temp = pd.DataFrame()
queries={}
data_title = {}
data_text = {}
cluster_labels = {}
topic_weights = {}
documents = []
keys = []
tfidf_matrix = None
vectorizer = TfidfVectorizer()


def set_variables(data_set, jsonl_file_path, corpus_json_path, tfidf_matrix_path, documents_path, keys_path, id, text_or_abstract):
    global dff, temp, data_title, data_text, cluster_labels, topic_weights, documents, keys, tfidf_matrix, vectorizer,queries
    # Initialize variables
    print(jsonl_file_path)
    if data_set == 1:
        dff = pd.read_json(jsonl_file_path, lines=True)
    elif data_set == 2:
        dff = pd.read_csv(r'C:\Users\omer\.ir_datasets\cord19\2020-06-19\metadata.csv')
    queries=getQueries(data_set)
    # Create dictionaries for data_title and data_text
    data_title = {}
    data_text = {}
    if data_set == 2:
        d = 0
        for i, row in dff.iterrows():
            if d < 10 and d>=0:
                d += 1
            data_title[str(row[id])] = str(row['title'])
            data_text[str(row[id])] = str(row[text_or_abstract])

    if data_set == 1:
        k = 0
        for i, row in dff.iterrows():
            if k < 10 and k>=0:
                k += 1
    # Add the tokenized title and abstract to the dictionary
            data_title[str(row[id])] = str(row['title']) 
            data_text[str(row[id])]=str(row[text_or_abstract])

    # Load the corpus JSON
    #temp = pd.read_json(corpus_json_path, lines=True)
    # Read cluster labels
    cluster_labels = readFileCluster(data_set)
    topic_weights = readFileTopic(data_set)
    with open(documents_path, 'r') as f:
        documents = json.load(f)
    with open(keys_path, 'r') as f:
        keys = json.load(f)
    #tfidf_matrix = load_npz(tfidf_matrix_path)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
@app.route('/refine_query', methods=['POST'])
def api_refine_query():
    user_query = request.json['user_query']
    suggested_queries = refine_query(user_query, queries)

    response = {
        'suggested_queries': suggested_queries
    }
    return jsonify(response)
    
@app.route('/set_dataset', methods=['POST'])
def set_dataset():
    global data_set, jsonl_file_path, corpus_json_path, documents, keys, tfidf_matrix,tfidf_matrix_path,documents_path,keys_path,id,text_or_abstract,dff,queries
    

    dataset = request.form ['dataset']
    if dataset == '1':
        data_set = 1
        jsonl_file_path = r'C:/Users/omer/.ir_datasets/beir/webis-touche2020/webis-touche2020/corpus.jsonl'
        corpus_json_path = 'C:/Users/omer/.ir_datasets/beir/webis-touche2020/webis-touche2020/corpus.jsonl'
        documents_path = r'C:/Users/omer/.ir_datasets/beir/webis-touche2020/webis-touche2020/documents.json'
        keys_path = r'C:/Users/omer/.ir_datasets/beir/webis-touche2020/webis-touche2020/keys.json'
        tfidf_matrix_path = 'C:/Users/omer/.ir_datasets/beir/webis-touche2020/webis-touche2020/tfidf_matrix.npz'
        id='_id'
        text_or_abstract='text'
        set_variables(data_set, jsonl_file_path, corpus_json_path,tfidf_matrix_path,documents_path,keys_path,id,text_or_abstract)
    elif dataset == '2':
        data_set = 2
        jsonl_file_path = r'C:/Users/omer/.ir_datasets/cord19/2020-06-19/corpus.jsonl'
        corpus_json_path = 'C:/Users/omer/.ir_datasets/cord19/2020-06-19/corpus.jsonl'
        documents_path = r'C:/Users/omer/.ir_datasets/cord19/2020-06-19/documents.json'
        keys_path = r'C:/Users/omer/.ir_datasets/cord19/2020-06-19/keys.json'
        tfidf_matrix_path = 'C:/Users/omer/.ir_datasets/cord19/2020-06-19/tfidf_matrix.npz'
        id='cord_uid'
        text_or_abstract='abstract'
        set_variables(data_set, jsonl_file_path, corpus_json_path,tfidf_matrix_path,documents_path,keys_path,id,text_or_abstract)

    else:
        return jsonify({'error': 'Invalid dataset value. Choose 1 or 2.'})
    

    return jsonify({'message': 'Dataset set successfully.', 'dataset': data_set})



@app.route('/get_query', methods=['POST'])
def predict():
    result = {
        "data": [],
        "evaluation": [],
        "count_result": 0
    }
    
    query = request.form['kewword']
    predicted_documents = perform_query_search(query, tfidf_matrix, documents, keys, vectorizer)
    
    for key in predicted_documents['predicted_documents']:
        data_entry = {
            "title": data_title[key],
            "abstract": data_text[key]
        }
        result['data'].append(data_entry)

    if data_set == 1:
        evaluations = eval(query, predicted_documents['predicted_documents'])
    if data_set == 2:
        evaluations = eval2(query, predicted_documents['predicted_documents'])
    print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
    print(evaluations)
    result['evaluation']=evaluations
    result['count_result'] = predicted_documents['count_result']

    return jsonify(result)









@app.route('/get_query_with_cluster', methods=['POST'])
def predictWithCluster():
    result = {
        "data": [],
        "evaluation": [],
        "count_result": 0
    }   
    query = request.form['kewword']
    predicted_documents = implmentClusterAlg(query, tfidf_matrix, temp, data_title, cluster_labels,keys,vectorizer)
     
    for key in predicted_documents['predicted_documents']:
        data_entry = {
            "title": data_title[key],
            "abstract": data_text[key]
        }
        result['data'].append(data_entry)

    #if data_set == 1:
     #   evaluations=eval(query,predicted_documents['predicted_documents'])
    #if data_set == 2:
     #   evaluations=eval2(query,predicted_documents['predicted_documents'])
        
    #result['evaluation']=evaluations
    result['count_result']=predicted_documents['count_result']
    return jsonify(result)

@app.route('/get_query_with_topic', methods=['POST'])
def predictWithTopic():
    result = {
        "data": [],
        "evaluation": [],
        "count_result": 0
    }       
    query = request.form['kewword']
    predicted_documents = implmentTopicAlg(query, tfidf_matrix, temp, data_title, topic_weights,keys,vectorizer)

    for key in predicted_documents['predicted_documents']:
        data_entry = {
            "title": data_title[key],
            "abstract": data_text[key]
        }
        result['data'].append(data_entry)

    if data_set == 1:
        evaluations=eval(query,predicted_documents['predicted_documents'])
    if data_set == 2:
        evaluations=eval2(query,predicted_documents['predicted_documents'])
    result['evaluation']=evaluations
    result['count_result']=predicted_documents['count_result']
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='192.168.252.207',port=8080)

