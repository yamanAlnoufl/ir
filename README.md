# ir
Information Retrieval System
my project focuses on creating a search engine for two datasets: COVID-19 and BIRE.
The project includes several preprocessing steps, the creation of a TF-IDF matrix, an inverted index, and various enhancements.
**Preprocessing Steps:**
List and describe each preprocessing step :
1. replace_percent_text for replace % with percent
2. expand_country_names usinr packeg pycountry
3. clean_text for Remove punctuations
4. lower_text for Convert to lowercase
5. lemmatize_text using WordNetLemmatizer
6. stem_text using PorterStemmer
7. remove_stopwords using stopwords
8. correct_spelling using TextBlob
**TF-IDF Matrix and Inverted Index:**
calculate tfidf for documints via TfidfVectorizer 
**Query Processing and Representation:**
query is processed and represented using the same steps as in the preprocessing section.
query is tokenized, cleaned, stemmed, and transformed to match the format of the TF-IDF matrix.
**Cosine Similarity Calculation:**
The cosine similarity is a measure that quantifies the similarity between two vectors in a high-dimensional space. In the context of a search engine, it is commonly used to calculate the similarity between a query and documents in the dataset.
**Enhancements:**
enhancement I mentioned (topic algorithm using LatentDirichletAllocation, cluster algorithm using KMeans, query suggestions).
 how each enhancement improves the search engine's performance or user experience:
 Rank the documents based on their cosine similarity values. Higher cosine similarity values indicate higher similarity to the query.
 suggistions:
 
