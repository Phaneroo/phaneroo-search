# Phaneroo Search

This is a project made with the purpose of testing sematic search of devotionals and sermons using ChromaDB

## Installation

To install Phaneroo Search, you need to have python 3.8 or higher, pip, and virtualenv installed on your system. You can follow these steps to install the project:

1. Clone this repository.
2. Create a virtual environment and activate it:
```bash
virtualenv venv && source venv/bin/activate
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. For mac incase chroma is not builing run the command below:
```bash
export HNSWLIB_NO_NATIVE=1
```
5. Then install chroma:
```bash
pip install chroma-hnswlib  
```
6. Run the migrations to create the database tables:
```bash
python manage.py migrate
```
7. Populate the chroma database:
```bash
--For users include the python version
python3 pupulate_db.py
```
8. Edit the path to the DB :
On **line 5** In the **schema.py** edit the path to the DB folder
```bash
client = chromadb.PersistentClient(path="relative_path/db")
```
9. Run the server:
```bash
python manage.py runserver
```

## Usage

To use Phaneroo Search, you can access the graphql endpoint at http://localhost:8000/graphql/. You can use the graphical interface to explore the schema and execute queries and mutations. Here are the graphql queries and mutations that you can try:
1. Get a sermon by ID 
```graphql
query {
  getSermon(sermonId: 2322)
}
```
**Finding The Results**
To view the results navigate to the right and press cmd **+** F(mac), ctrl **+** F and input **"title"** in the search bar.

2. Get all sermons 
```graphql
query {
  getSermons
}
```
3. Search sermons by text 
```graphql
query {
  searchSermons(searchText: 'Knowing God')
}
```
4. Get a devotional by ID 
```graphql
query {
  getDevotional(devotionalId: 2322)
}
```
2. Get all devotionals
```graphql
query {
  getDevotionals
}
```
3. Search devotionals by text 
```graphql
query {
  searchDevetionals(searchText: 'Knowing God')
}
```"

