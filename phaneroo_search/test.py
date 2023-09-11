# Import chromadb
import chromadb

# Create a client object
client = chromadb.PersistentClient(path="db")

# Create a collection object
collection = client.get_collection("sermons")

# Query the collection for the most similar document to a given query
result = collection.query(
    query_texts=[""],
    n_results=2,
    include=["metadatas"]
)

# Print the result
print(result)
