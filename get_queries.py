import json
import xml.etree.ElementTree as ET
def getQueries(data_set):
    texts = []
    if data_set == 1:
        with open(r'C:\Users\omer\.ir_datasets\beir\webis-touche2020\webis-touche2020\queries.jsonl', 'r') as file:
            for line in file:
                queries_dataset1 = json.loads(line.strip())
                text = queries_dataset1["text"]
                # Add the text to the list
                texts.append(text)
    if data_set == 2:
        tree = ET.parse('C:/Users/omer/.ir_datasets/cord19/2020-06-19/queries.xml')
        root = tree.getroot()
        for topic in root.findall("./topic"):
            query_element = topic.find("query")
            if query_element is not None:
                query = query_element.text.strip()
                texts.append(query)
    return texts

