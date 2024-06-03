import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation



#Algorithms

# Clustering
num_clusters = 5  # Set the number of clusters as desired
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(tfidf_matrix)







# Topic Detection
num_topics = 3  # Set the number of topics as desired
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
topic_weights = lda.fit_transform(tfidf_matrix)


