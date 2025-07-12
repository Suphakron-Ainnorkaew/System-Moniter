import requests
import json

# Update this URL to your deployed server URL
API_URL = "https://your-app-name.onrender.com"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_submit():
    """Test submitting data"""
    test_data = {
        "model_name": "Test Device",
        "cpu_brand": "Intel",
        "cpu_model": "Core i7-10700K",
        "gpu_brand": "NVIDIA",
        "gpu_model": "RTX 3080",
        "ram_gb": 16,
        "test_details": {
            "test_type": "ai",
            "mode": "all",
            "total_time": 120.5,
            "avg_score": 85.2,
            "scores": {"test1": 90, "test2": 80}
        }
    }
    
    try:
        response = requests.post(f"{API_URL}/submit", json=test_data)
        print(f"Submit test: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Submit test failed: {e}")
        return False

def test_list():
    """Test listing data"""
    try:
        response = requests.get(f"{API_URL}/list")
        print(f"List test: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} records")
        return response.status_code == 200
    except Exception as e:
        print(f"List test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing System Monitor API...")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    health_ok = test_health()
    
    # Test submit endpoint
    print("\n2. Testing submit endpoint...")
    submit_ok = test_submit()
    
    # Test list endpoint
    print("\n3. Testing list endpoint...")
    list_ok = test_list()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Health: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Submit: {'✅ PASS' if submit_ok else '❌ FAIL'}")
    print(f"List: {'✅ PASS' if list_ok else '❌ FAIL'}")
    
    if all([health_ok, submit_ok, list_ok]):
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️ Some tests failed. Check your deployment and environment variables.") 