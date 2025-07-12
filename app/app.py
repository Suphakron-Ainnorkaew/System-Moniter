from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
import logging

app = Flask(__name__)

# MongoDB Atlas connection (use environment variable for security)
MONGODB_URI = os.environ.get('MONGODB_URI')

if not MONGODB_URI:
    app.logger.error("MONGODB_URI environment variable not set!")
    raise ValueError("MONGODB_URI environment variable is required")

try:
    client = MongoClient(MONGODB_URI)
    # Test the connection
    client.admin.command('ping')
    app.logger.info("Successfully connected to MongoDB Atlas")
    db = client["system-monitor"]  # Fixed typo: was "system-moniter"
    collection = db["process"]
except Exception as e:
    app.logger.error(f"Failed to connect to MongoDB: {e}")
    raise

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400

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
        result = collection.insert_one(doc)
        app.logger.info(f"Successfully inserted document with ID: {result.inserted_id}")
        
        return jsonify({
            'status': 'ok', 
            'message': 'Data saved successfully.',
            'document_id': str(result.inserted_id)
        })
        
    except Exception as e:
        app.logger.error(f"Error in submit endpoint: {e}")
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500

@app.route('/list', methods=['GET'])
def list_data():
    try:
        # ดึงข้อมูลทั้งหมด
        results = list(collection.find({}, {'_id': 0}))
        app.logger.info(f"Retrieved {len(results)} documents")
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Error in list endpoint: {e}")
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({'status': 'ok', 'message': 'Service is healthy'})
    except Exception as e:
        app.logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'error', 'message': f'Service unhealthy: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))