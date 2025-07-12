# System Monitor API

Flask API for storing system benchmark data in MongoDB Atlas.

## Environment Variables

You need to set these environment variables in your Render.com dashboard:

### Required:
- `MONGODB_URI`: Your MongoDB Atlas connection string
  - Format: `mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority`
  - Get this from your MongoDB Atlas dashboard

### Optional:
- `PORT`: Port number (Render sets this automatically)

## API Endpoints

### POST /submit
Submit benchmark data to MongoDB.

**Required fields:**
- `model_name`: Device model name
- `cpu_brand`: CPU brand
- `cpu_model`: CPU model
- `gpu_brand`: GPU brand
- `gpu_model`: GPU model
- `ram_gb`: RAM in GB

**Optional fields:**
- `test_details`: Additional test information

### GET /list
Retrieve all stored benchmark data.

### GET /health
Health check endpoint.

## Deployment on Render.com

1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy the app
4. Update the API_URL in `system_monitor_db.py` with your deployed URL

## Local Development

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables
3. Run: `python app.py` 