# Import requests and chromadb modules
import requests
import chromadb
# Import logging module
import logging

# Create a logger object
logger = logging.getLogger(__name__)

# Set the level of the logger
logger.setLevel(logging.DEBUG)

# Create a handler object for standard output
stream_handler = logging.StreamHandler()
# Set the level of the handler
stream_handler.setLevel(logging.DEBUG)
# Create a formatter object for standard output
stream_formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
# Attach the formatter to the handler
stream_handler.setFormatter(stream_formatter)
# Attach the handler to the logger
logger.addHandler(stream_handler)

# Create a handler object for file output
file_handler = logging.FileHandler('chromadb.log')
# Set the level of the handler
file_handler.setLevel(logging.ERROR)
# Create a formatter object for file output
file_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
# Attach the formatter to the handler
file_handler.setFormatter(file_formatter)
# Attach the handler to the logger
logger.addHandler(file_handler)

# Define a function that takes an API endpoint URL and returns a chroma db object


def populate_devotionals(url):
    logger.info(f'Populating Devotionals')
    # Get the devotionals from api
    devotionals = fetch_devotionals_from_api(url)
    # Log a message with JSON data size
    logger.info(f'Devotionals data size: {len(devotionals)}')
    # Create a list of documents from the JSON data

    documents = []
    metadatas = []
    ids = []

    for doc in devotionals:
        documents.append(f"{doc['title']}")
        metadatas.append({  # Use any other fields as metadata
                "id": str(doc["id"]),
                "title": str(doc["title"]),
                "body": str(doc["body"]),
                "artlink": str(doc["artlink"]),
                "date": str(doc["date"])
            })
        ids.append(str(doc["id"]))

    # Log an info message with documents size
    logger.info(f'Documents size: {len(documents)}')
    logger.info(f'Metadatas size: {len(metadatas)}')
    logger.info(f'IDs size: {len(ids)}')
    # Create a chroma db object using Chroma constructor without passing embeddings parameter
    logger.info(f'Adding data to db and creating embeddings...')
    db = chromadb.PersistentClient(
        path="db",  # Specify a directory to save the database on disk
        )
    devotionals_collection = db.get_or_create_collection("devotionals")
    # Add documents to chroma db using add_documents method
    devotionals_collection.add(documents=documents, metadatas=metadatas, ids=ids)
    # Return the chroma db object
    return db
    
def populate_sermons(url):
    logger.info(f'Populating Sermons')
    # Log an info message with input parameter
    logger.info(f'Creating chroma db from API endpoint: {url}')
    # Make a GET request to the API endpoint and store the response object
    response = requests.get(url)
    # Check if the response status code is 200
    if response.status_code == 200:
        # Log an info message with successful request
        logger.info(
            f'Request successful with status code {response.status_code}')
        # Parse the JSON data from the response
        json_data = response.json()
        # Log a debug message with JSON data size
        logger.info(f'JSON data size: {len(json_data["data"])}')
        # Create a list of documents from the JSON data

        documents = []
        metadatas = []
        ids = []

        for doc in json_data["data"]:
            documents.append(f"{doc['title']} {doc['description']}")
            metadatas.append({  # Use any other fields as metadata
                    "id": str(doc["id"]),
                    "title": str(doc["title"]),
                    "description": str(doc["description"]),
                    "duration": str(doc["duration"]),
                    "media_link": str(doc["media_link"]),
                    "artlink": str(doc["artlink"]),
                    "published_date": str(doc["published_date"])
                })
            ids.append(str(doc["id"]))

        # Log an info message with documents size
        logger.info(f'Documents size: {len(documents)}')
        logger.info(f'Metadatas size: {len(metadatas)}')
        logger.info(f'IDs size: {len(ids)}')
        # Create a chroma db object using Chroma constructor without passing embeddings parameter
        logger.info(f'Adding data to db and creating embeddings...')
        db = chromadb.PersistentClient(
            path="db",  # Specify a directory to save the database on disk
            )
        sermons_collection = db.get_or_create_collection("sermons")
        # Add documents to chroma db using add_documents method
        sermons_collection.add(documents=documents, metadatas=metadatas, ids=ids)
        # Return the chroma db object
        return db
    else:
        # Log an error message with failed request and status code
        logger.error(f'Request failed with status code {response.status_code}')
        # Raise an exception or handle the error if the response status code is not 200
        raise Exception(
            f'Request failed with status code {response.status_code}')


def fetch_devotionals_from_api(url):
    devotionals = []

    try:
        page_meta_data = requests.get(url)
        if page_meta_data.status_code == 200:
            no_of_pages = page_meta_data.json()['last_page']
            logger.info(f"found {no_of_pages} pages")
            for i in range(1, no_of_pages + 1):
                response = None
                new_url = f"{url}?page={i}"
                logger.info(f"working on {new_url}")

                try:
                    response = requests.get(new_url)
                    if response.status_code == 200:
                        json_response = response.json()
                        logger.info(
                            f"found {len(json_response['data']) or 0} devotionals")
                        for element in json_response['data']:
                            devotionals.append(element)
                        logger.info(f"appended devotionals. Current length is {len(devotionals)}")
                    else:
                        raise Exception("An error occurred")
                except Exception as e:
                    logger.info(e)
            return devotionals
        else:
            raise Exception("An error occurred")
    except Exception as e:
        logger.info(e)
 

populate_sermons("https://phaneroo.a23.us/api/v1/sermons")
populate_devotionals("https://phaneroo.a23.us/api/v1/devotionals")