import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("path/to/your-service-account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_day_log(symbol, data):
    doc_id = f"{symbol}_{datetime.now().strftime('%Y-%m-%d')}"
    db.collection("trade_logs").document(doc_id).set(data)

def fetch_latest(symbol):
    doc_id = f"{symbol}_{datetime.now().strftime('%Y-%m-%d')}"
    return db.collection("trade_logs").document(doc_id).get().to_dict()
