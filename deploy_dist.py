#!/usr/bin/env python3
"""
Deploy script for System Monitor application
This script helps update the API URL in the executable and provides deployment instructions
"""

import os
import shutil
import json
import requests
from pathlib import Path

def update_api_url_in_exe():
    """Update the API URL in the executable file"""
    dist_path = Path("dist/system_monitor.exe")
    
    if not dist_path.exists():
        print("❌ system_monitor.exe not found in dist folder")
        print("Please build the application first using PyInstaller")
        return False
    
    print("📁 Found system_monitor.exe in dist folder")
    print("⚠️ Note: Updating API URL in executable requires rebuilding")
    print("Please update the API_URL in system_monitor_db.py and rebuild")
    return True

def test_api_connection(api_url):
    """Test connection to the deployed API"""
    try:
        print(f"🔗 Testing connection to: {api_url}")
        response = requests.get(f"{api_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ API connection successful")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def create_deployment_guide():
    """Create a deployment guide"""
    guide = """
# 🚀 System Monitor Deployment Guide

## 1. Web API Deployment (Render.com)

### Step 1: Deploy the Flask API
1. Push your code to GitHub
2. Go to Render.com and create a new Web Service
3. Connect your GitHub repository
4. Set the following environment variables:
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `PORT`: 5000 (optional, Render sets this automatically)

### Step 2: Get your API URL
- After deployment, Render will give you a URL like: `https://your-app-name.onrender.com`
- Test the API: `https://your-app-name.onrender.com/health`

## 2. Update API URL in Application

### Step 1: Update system_monitor_db.py
Change the API_URL in `system_monitor_db.py`:
```python
API_URL = "https://your-app-name.onrender.com/submit"
```

### Step 2: Rebuild the executable
```bash
pyinstaller system_monitor.spec
```

## 3. Test the Connection

### Step 1: Test API locally
```bash
cd app
python test_api.py
```

### Step 2: Test from the application
1. Run the executable: `dist/system_monitor.exe`
2. Go to AI Test or Program Test tab
3. Run a benchmark test
4. Check if data is saved to MongoDB Atlas

## 4. Troubleshooting

### Common Issues:
1. **API not responding**: Check if the service is running on Render
2. **MongoDB connection failed**: Verify MONGODB_URI environment variable
3. **Data not saving**: Check the API logs on Render dashboard
4. **Timeout errors**: Increase timeout in system_monitor_db.py

### Debug Steps:
1. Check Render logs: Dashboard > Your Service > Logs
2. Test API endpoints manually
3. Verify MongoDB Atlas connection
4. Check firewall/network settings

## 5. MongoDB Atlas Setup

### Step 1: Create Database
1. Go to MongoDB Atlas dashboard
2. Create a new database named `system-monitor`
3. Create a collection named `process`

### Step 2: Get Connection String
1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Copy the connection string
4. Replace `<password>` with your database password
5. Add this as MONGODB_URI environment variable

## 6. Final Checklist

- [ ] Flask API deployed on Render.com
- [ ] MONGODB_URI environment variable set
- [ ] API URL updated in system_monitor_db.py
- [ ] Application rebuilt with new API URL
- [ ] API health check passes
- [ ] Test data submission works
- [ ] Data appears in MongoDB Atlas
"""
    
    with open("DEPLOYMENT_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("📋 Created DEPLOYMENT_GUIDE.md")

def main():
    print("🚀 System Monitor Deployment Helper")
    print("=" * 50)
    
    # Check if dist folder exists
    if not os.path.exists("dist"):
        print("❌ dist folder not found")
        print("Please build the application first:")
        print("  pyinstaller system_monitor.spec")
        return
    
    # Check executable
    exe_exists = update_api_url_in_exe()
    
    # Create deployment guide
    create_deployment_guide()
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. Deploy the Flask API to Render.com")
    print("2. Update API_URL in system_monitor_db.py")
    print("3. Rebuild the executable")
    print("4. Test the connection")
    print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main() 