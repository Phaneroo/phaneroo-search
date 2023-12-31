import json
import graphene
import chromadb

# Create a client object
client = chromadb.PersistentClient(path="db")

# Create collection objects
sermons_collection = client.get_collection("sermons")
devotionals_collection = client.get_collection("devotionals")

class Query(graphene.ObjectType):
    get_sermon = graphene.String(sermon_id=graphene.String(required=True))
    get_sermons = graphene.String()
    search_sermons = graphene.String(search_text=graphene.String(required=True))
    get_devotional = graphene.String(devotional_id=graphene.String(required=True))
    get_devotionals = graphene.String()
    search_devotionals = graphene.String(search_text=graphene.String(required=True))


    def resolve_get_sermon(self, info, sermon_id):
        return json.dumps(sermons_collection.get(ids=[sermon_id], limit=1, include=["metadatas"]).__getitem__('metadatas'))
    
    def resolve_get_sermons(self, info):
        return json.dumps(sermons_collection.get(include=["metadatas"]).__getitem__('metadatas'))
    
    def resolve_search_sermons(self, info, search_text):
        # Query the collection for the most similar document to a given query
        result = sermons_collection.query(
            query_texts=[search_text],
            include=["metadatas"]
        )
        return json.dumps(result.__getitem__('metadatas'))
    def resolve_get_devotional(self, info, devotional_id):
        return json.dumps(devotionals_collection.get(ids=[devotional_id], limit=1, include=["metadatas"]).__getitem__('metadatas'))
    
    def resolve_get_devotionals(self, info):
        return json.dumps(devotionals_collection.get(include=["metadatas"]).__getitem__('metadatas'))
    
    def resolve_search_devotionals(self, info, search_text):
        # Query the collection for the most similar document to a given query
        result = devotionals_collection.query(
            query_texts=[search_text],
            include=["metadatas"]
        )

        return json.dumps(result.__getitem__('metadatas'))

schema = graphene.Schema(query=Query)
