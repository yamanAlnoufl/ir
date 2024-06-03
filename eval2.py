import xml.etree.ElementTree as ET

def get_query_indices(query):
    # Parse the XML file
    tree = ET.parse('C:/Users/omer/.ir_datasets/cord19/2020-06-19/queries.xml')
    root = tree.getroot()

    query_number = -1
    # Iterate over topic elements
    for index, topic in enumerate(root.findall('topic'), 1):
        topic_number = int(topic.get('number'))
        topic_query = topic.find('query').text
        if str(topic_query) == str(query):
            query_number = topic_number
    return query_number


def readQrle(query):
    with open('C:/Users/omer/.ir_datasets/cord19/trec-covid/round4/qrels', 'r') as file:
        print(query)

        data = []
        query_number = get_query_indices(query)
        print(query_number)
        i = 0
        for i, line in enumerate(file, 1):
            query_parts = line.strip().split()
            if int(query_parts[0]) == int(query_number):
                data.append(i)

       
        return data

# Read the relevance judgments from the file
# List of relevant document IDs for the query

def precision_at_k(actual, predicted, k):
    if len(predicted) > k:
        predicted = predicted[:k]
    tp = len(set(actual) & set(predicted))
    print(tp)
    precision = tp / len(predicted)
    return precision
def eval2(query,predicted_documents):
    relevant_documents = []  
    data=readQrle(query)
    with open(r'C:/Users/omer/.ir_datasets/cord19/trec-covid/round4/qrels', 'r') as file:
        i=0   
        for line in file:
            query_id, iteration, doc_id, relevance = line.split()
            if i>=data[0] and i <= data[-1]:
                relevant_documents.append(doc_id)     
            i+=1
            
        print('********************')
        print(relevant_documents[:10])
        print(predicted_documents)
        print(len(predicted_documents))
        print(len(relevant_documents))
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

