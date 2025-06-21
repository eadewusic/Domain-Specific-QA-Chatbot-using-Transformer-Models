import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter 
import json
from datetime import datetime

# Path to Firebase service account key
SERVICE_ACCOUNT_FILE = "ayikabot-v1-firebase-adminsdk-fbsvc-ad7ae9cf65.json"

# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Helper function to serialize Firestore data
def serialize_firestore_data(data):
    if isinstance(data, dict):
        return {k: serialize_firestore_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_firestore_data(item) for item in data]
    elif isinstance(data, datetime):
        # Convert datetime objects to ISO format strings
        return data.isoformat()
    else:
        return data

def download_training_data_from_firestore(output_file="ayikabot_full_training_data.json"):
    print(f"Downloading climate-related interactions for training data...")
    
    # Query the 'interactions' collection
    interactions_ref = db.collection('interactions')
    
    # Only include climate-related Q&A where the bot provided a climate_answer
    query = interactions_ref.where(filter=FieldFilter('is_climate_related', '==', True))\
                            .where(filter=FieldFilter('response_type', '==', 'climate_answer'))
    
    docs = query.stream() # Get all documents matching the query
    
    training_data_list = []
    for doc in docs:
        entry = doc.to_dict()
        # Format the entry to match desired training data structure
        training_data_list.append({
            'input': f"question: {entry.get('user_question', '')}",
            'output': entry.get('bot_response', ''),
            'metadata': {
                'confidence': entry.get('confidence_score', 0.0),
                # Ensure timestamp is stringified, as it's datetime object in Firestore
                'timestamp': entry.get('timestamp', datetime.now()).isoformat()
            }
        })

    if training_data_list:
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(training_data_list, f, indent=2, ensure_ascii=False)
        print(f"Successfully downloaded {len(training_data_list)} training examples to {output_file}")
    else:
        print("No climate-related training data found in Firestore to download.")

if __name__ == "__main__":
    # download training data from Firestore
    download_training_data_from_firestore(output_file="training_data_logs.json")
