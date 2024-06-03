import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from data_processing import preprocess_text
# Create a TfidfVectorizer object
def readFileCluster(data_set):
# Specify the file path for the CSV file
    if data_set == 1:
        file_path = 'C:/Users/omer/.ir_datasets/beir/webis-touche2020/webis-touche2020/cluster_labels.csv'
    elif data_set == 2:
        file_path = 'C:/Users/omer/.ir_datasets/cord19/2020-06-19/files/cluster_labels.csv'

# Read the CSV file into a DataFrame
    cluster_data = pd.read_csv(file_path)

# Access the cluster labels from the DataFrame
    cluster_labels = cluster_data['Cluster Label'].values
    return cluster_labels


def implmentClusterAlg(query,tfidf_matrix, temp, data_title,cluster_labels,keys,vectorizer):
    predicted_documents = []
    pureQuery = query

    query=preprocess_text(query)

    # Transform the query into a TF-IDF vector
    query_vector = vectorizer.transform([query])

    # Cosine Similarity
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)
    most_similar_document_index = cosine_similarities.argmax()
    similarity_score = cosine_similarities[0, most_similar_document_index]

    # Cluster Algorithm
    query_cluster = cluster_labels[most_similar_document_index]
    cluster_indices = [i for i, label in enumerate(cluster_labels) if label == query_cluster]
    print("The result of Cluster Algorithm search : ",len(cluster_indices))
    cluster_similarities = cosine_similarities[0, cluster_indices]
    sorted_indices = np.array(cluster_indices)[np.argsort(cluster_similarities)[::-1]]
    # Get the predicted documents
    

    top_indices = sorted_indices[:20]
    predicted_documents += [list(keys)[idx] for idx in top_indices]
    result={}
    result['predicted_documents']=predicted_documents
    result['count_result']=len(cluster_indices)
    
   

    return result   


