#!/usr/bin/env python3
"""MDM Backend API Health Check"""
import urllib.request
import urllib.error
import json

def test_api():
    base_url = "http://127.0.0.1:8080"
    
    print("=" * 50)
    print("MDM Backend Health Check Report")
    print("=" * 50)
    print()
    
    # 1. Health check
    print("[1] Testing GET /health endpoint...")
    try:
        with urllib.request.urlopen(f"{base_url}/health", timeout=5) as resp:
            status = resp.status
            body = resp.read().decode('utf-8')
            print(f"    ✅ Status: {status}")
            print(f"    Response: {body}")
    except urllib.error.URLError as e:
        print(f"    ❌ ERROR: {e.reason}")
    
    print()
    
    # 2. Device list
    print("[2] Testing GET /api/v1/devices (device list)...")
    try:
        with urllib.request.urlopen(f"{base_url}/api/v1/devices", timeout=5) as resp:
            status = resp.status
            body = resp.read().decode('utf-8')
            print(f"    ✅ Status: {status}")
            data = json.loads(body)
            print(f"    Code: {data.get('code')}")
            print(f"    Message: {data.get('message')}")
            if 'data' in data and 'pagination' in data['data']:
                pagination = data['data']['pagination']
                print(f"    Pagination: {pagination}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"    ⚠️  Status: {e.code}")
        print(f"    Response: {body}")
    except urllib.error.URLError as e:
        print(f"    ❌ ERROR: {e.reason}")
    
    print()
    
    # 3. Device register
    print("[3] Testing POST /api/v1/devices/register...")
    data = {
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "sn_code": "TEST123456",
        "hardware_model": "M5_CoreS3",
        "firmware_version": "1.0.0"
    }
    try:
        req = urllib.request.Request(
            f"{base_url}/api/v1/devices/register",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            body = resp.read().decode('utf-8')
            print(f"    ✅ Status: {status}")
            result = json.loads(body)
            print(f"    Code: {result.get('code')}")
            print(f"    Message: {result.get('message')}")
            if 'data' in result:
                print(f"    Data: {result['data']}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"    ⚠️  Status: {e.code}")
        print(f"    Response: {body}")
    except urllib.error.URLError as e:
        print(f"    ❌ ERROR: {e.reason}")
    
    print()
    
    # 4. Get non-existent device
    print("[4] Testing GET /api/v1/devices/test-nonexistent-id...")
    try:
        with urllib.request.urlopen(f"{base_url}/api/v1/devices/test-nonexistent-id", timeout=5) as resp:
            status = resp.status
            body = resp.read().decode('utf-8')
            print(f"    ✅ Status: {status}")
            print(f"    Response: {body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"    ⚠️  Status: {e.code} (Expected 404)")
        print(f"    Response: {body}")
    except urllib.error.URLError as e:
        print(f"    ❌ ERROR: {e.reason}")
    
    print()
    print("=" * 50)
    print("Backend API Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    test_api()
