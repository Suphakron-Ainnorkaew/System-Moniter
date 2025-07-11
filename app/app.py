from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB Atlas connection (use environment variable for security)
import os
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client["system-moniter"]
collection = db["process"]

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    # Validate required fields
    required = ['model_name', 'cpu_brand', 'cpu_model', 'gpu_brand', 'gpu_model', 'ram_gb']
    for field in required:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'Missing field: {field}'}), 400

    # Prepare document
    doc = {
        'model_name': data['model_name'],         # ชื่อรุ่นที่ใช้ทดสอบ
        'cpu_brand': data['cpu_brand'],           # ยี่ห้อ CPU
        'cpu_model': data['cpu_model'],           # รุ่น CPU
        'gpu_brand': data['gpu_brand'],           # ยี่ห้อ GPU
        'gpu_model': data['gpu_model'],           # รุ่น GPU
        'ram_gb': data['ram_gb'],                 # จำนวนแรม (GB)
        'test_details': data.get('test_details'), # ข้อมูลอื่นๆ (optional)
        'created_at': datetime.utcnow()           # เวลาบันทึก
    }

    # Insert to MongoDB
    collection.insert_one(doc)
    return jsonify({'status': 'ok', 'message': 'Data saved.'})

@app.route('/list', methods=['GET'])
def list_data():
    # ดึงข้อมูลทั้งหมด
    results = list(collection.find({}, {'_id': 0}))
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)