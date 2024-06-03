 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(query, document):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([query, document])
    similarity_matrix = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    similarity_score = similarity_matrix[0][0]
    return similarity_score


def refine_query(user_query, queries):
    similarity_threshold = 0.2
    suggested_queries = []

    for document in queries:
        similarity_score = calculate_similarity(user_query, document)
        if similarity_score > similarity_threshold:
            suggested_queries.append(document)
            print(document)

    return suggested_queries