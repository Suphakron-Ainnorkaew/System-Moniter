
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
