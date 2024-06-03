
import json


def get_id_from_text(text):
    with open(r'C:\Users\omer\.ir_datasets\beir\webis-touche2020\webis-touche2020\queries.jsonl', 'r') as file:
        for line in file:
            data = json.loads(line)
            if data['text'] == text:
                return data['_id']
    return 1








def readQrels(query_number):
    data=[]
    i = 0
    with open(r'C:\Users\omer\.ir_datasets\beir\webis-touche2020\webis-touche2020\qrels\test.tsv', 'r') as file:
        for line in file:
            query_parts = line.strip().split('\t')
            if i == 0:
                print(query_parts)
            try:
                if int(query_parts[0]) == int(query_number):
                    data.append(i)
            except ValueError:
                pass  # Skip non-integer lines
            i += 1


    return data





# Read the relevance judgments from the file
 # List of relevant document IDs for the query

def precision_at_k(actual, predicted, k):
    
    if len(predicted) > k:
        predicted = predicted[:k]
    tp = len(set(actual) & set(predicted))
    precision = tp / len(predicted)
    return precision

def eval(pureQuery,predicted_documents):
    data=readQrels( get_id_from_text(pureQuery))
    relevant_documents = [] 
    with open(r'C:\Users\omer\.ir_datasets\beir\webis-touche2020\webis-touche2020\qrels\test.tsv', 'r') as file:
        i = 0   
        for line in file:
            query_id, corpus_id, score = line.split()
            if i >= data[0] and i <= data[-1]:
                relevant_documents.append(corpus_id)     
            i += 1   


    # Calculate Precision@10, Precision, and Recall
    precision_10 = precision_at_k(relevant_documents,predicted_documents, 10)
    precision = precision_at_k(relevant_documents, predicted_documents, len(predicted_documents))
    recall = len(set(relevant_documents) & set(predicted_documents)) / len(relevant_documents)



    # Calculate Mean Average Precision (MAP)
    average_precision = 0
    relevant_count = 0
    for i, doc in enumerate(predicted_documents):
        if doc in relevant_documents:
            relevant_count += 1
            precision_at_i = relevant_count / (i + 1)
            average_precision += precision_at_i
    if relevant_count > 0:
        average_precision /= relevant_count



    # Calculate Mean Reciprocal Rank (MRR)
    reciprocal_rank = 0
    for i, doc in enumerate(predicted_documents):
        if doc in relevant_documents:
            reciprocal_rank = 1 / (i + 1)
            break
    result=[]
    result.append(precision_10)
    result.append(precision)
    result.append(recall)
    result.append(average_precision)
    result.append(reciprocal_rank)
    
    # Print the metrics
    print("Precision@10:", precision_10)
    print("Precision:", precision)
    print("Recall:", recall)
    print("MAP:", average_precision)
    print("MRR:", reciprocal_rank)
    return result



