import os
import fitz
from pymongo import MongoClient
from dotenv import load_dotenv

def pdf_to_json(filename, doc_id):
    """
    Parses a PDF file and converts it into JSON format.
    
    :param filename: Path to the PDF file
    :param doc_id: The ID to assign to the document
    :return: JSON representation of the PDF
    """
    pdf_document = fitz.open(filename)
    pdf_json = {
        'id': doc_id,
        'filename': os.path.basename(filename),
        'content': []
    }

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        pdf_json['content'].append({
            'page_number': page_num + 1,
            'text': text
        })

    return pdf_json

def store_in_mongodb(json_data, db_name, collection_name, mongo_url):
    """
    Stores JSON data into a MongoDB collection.
    
    :param json_data: JSON data to store
    :param db_name: Name of the database
    :param collection_name: Name of the collection
    :param mongo_url: MongoDB connection URI
    """
    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(json_data)

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    directory_path = './Documents'
    mongo_url = os.getenv('MONGO_URL')
    db_name = os.getenv('DB_NAME')
    collection_name = os.getenv('COLLECTION_NAME')

    for index, filename in enumerate(os.listdir(directory_path), start=1):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            doc_id = f"doc_{index}"
            pdf_json = pdf_to_json(pdf_path, doc_id)
            # Store JSON in MongoDB
            store_in_mongodb(pdf_json, db_name, collection_name, mongo_url)
            print(f"PDF {filename} parsed and stored in MongoDB successfully with ID {doc_id}.")
