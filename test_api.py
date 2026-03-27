# MDM API Verification Test Script
import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://localhost:8080/api/v1"
TOKEN = None
TENANT_ID = None

def make_request(method, path, data=None, token=None, expect_fail=False):
    url = BASE_URL + path
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            status = "✅ PASS" if result.get("code") == 0 or result.get("code") == "SUCCESS" else f"⚠️  CODE={result.get('code')}"
            if expect_fail and result.get("code") != 0:
                status = "✅ EXPECTED_FAIL"
            return status, result, None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            result = json.loads(body)
            return f"❌ HTTP {e.code}", result, str(e)
        except:
            return f"❌ HTTP {e.code}", {"raw": body[:200]}, str(e)
    except Exception as e:
        return f"❌ ERROR", {}, str(e)

def login():
    global TOKEN, TENANT_ID
    status, resp, err = make_request("POST", "/auth/login", {"username": "admin", "password": "admin123"})
    print(f"[AUTH] POST /auth/login -> {status}")
    if resp.get("data"):
        TOKEN = resp["data"].get("token")
        TENANT_ID = resp["data"].get("tenant_id")
        print(f"   Token: {TOKEN[:50]}...")
        print(f"   TenantID: {TENANT_ID}")
    return TOKEN is not None

def test_apis():
    results = []
    
    print("\n" + "="*60)
    print("MDM API VERIFICATION REPORT")
    print("="*60)
    print(f"Backend: http://localhost:8080")
    print(f"Tested at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    # Test 1: Login
    print("[1] AUTH MODULE")
    if not login():
        print("❌ Login failed, cannot proceed with other tests")
        return results
    
    # Test 2: User APIs
    print("\n[2] USER MODULE")
    path = f"/tenants/{TENANT_ID}/users"
    
    # GET users list
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    if resp.get("data"):
        print(f"      Total users: {resp['data'].get('total', len(resp['data'].get('list', [])))}")
    
    # POST create user
    status, resp, err = make_request("POST", path, {"username": "testuser", "real_name": "Test User", "phone": "13800138001", "role": "normal_user"}, token=TOKEN)
    print(f"   POST {path} -> {status}")
    created_user_id = None
    if resp.get("data") and resp["data"].get("user_id"):
        created_user_id = resp["data"]["user_id"]
        print(f"      Created user_id: {created_user_id}")
    
    # PUT update user
    if created_user_id:
        status, resp, err = make_request("PUT", f"{path}/{created_user_id}", {"real_name": "Test User Updated"}, token=TOKEN)
        print(f"   PUT {path}/{created_user_id} -> {status}")
    
    # Test 3: Store APIs
    print("\n[3] STORE MODULE")
    path = f"/tenants/{TENANT_ID}/stores"
    
    # GET stores
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # POST create store
    status, resp, err = make_request("POST", path, {
        "store_name": "Test Store",
        "store_code": f"TEST{int(time.time())}",
        "province": "Beijing",
        "city": "Beijing",
        "district": "Chaoyang",
        "address": "Test Address",
        "contact_phone": "010-12345678"
    }, token=TOKEN)
    print(f"   POST {path} -> {status}")
    created_store_id = None
    if resp.get("data") and resp["data"].get("store_id"):
        created_store_id = resp["data"]["store_id"]
        print(f"      Created store_id: {created_store_id}")
    
    # PUT update store
    if created_store_id:
        status, resp, err = make_request("PUT", f"{path}/{created_store_id}", {"store_name": "Test Store Updated"}, token=TOKEN)
        print(f"   PUT {path}/{created_store_id} -> {status}")
    
    # DELETE store
    if created_store_id:
        status, resp, err = make_request("DELETE", f"{path}/{created_store_id}", token=TOKEN)
        print(f"   DELETE {path}/{created_store_id} -> {status}")
    
    # Test 4: Device APIs
    print("\n[4] DEVICE MODULE")
    path = f"/tenants/{TENANT_ID}/devices"
    
    # GET devices
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # POST register device
    status, resp, err = make_request("POST", path, {
        "device_name": "Test Device",
        "device_code": f"DEV{int(time.time())}",
        "hardware_model": "CoreS3"
    }, token=TOKEN)
    print(f"   POST {path} -> {status}")
    
    # Test 5: Member APIs
    print("\n[5] MEMBER MODULE")
    path = f"/tenants/{TENANT_ID}/members"
    
    # GET members
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # Test 6: Role APIs
    print("\n[6] ROLE MODULE")
    path = "/roles"
    
    # GET roles
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # Test 7: Alert APIs
    print("\n[7] ALERT MODULE")
    path = f"/tenants/{TENANT_ID}/alerts/rules"
    
    # GET alert rules
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # Test 8: Settings APIs
    print("\n[8] SETTINGS MODULE")
    path = f"/tenants/{TENANT_ID}/settings"
    
    # GET settings
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # PUT settings
    status, resp, err = make_request("PUT", path, {"tenant_name": "Updated via API Test"}, token=TOKEN)
    print(f"   PUT {path} -> {status}")
    
    # Test 9: AI Chat API
    print("\n[9] AI CHAT MODULE")
    path = "/ai/chat"
    
    # POST chat
    status, resp, err = make_request("POST", path, {"message": "Hello, this is a test"}, token=TOKEN)
    print(f"   POST {path} -> {status}")
    if resp.get("data"):
        print(f"      AI Response: {str(resp['data'])[:100]}...")
    
    # Test 10: Dashboard Stats API
    print("\n[10] DASHBOARD MODULE")
    path = "/dashboard/stats"
    
    # GET dashboard stats
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    if resp.get("data"):
        print(f"      Stats keys: {list(resp['data'].keys()) if isinstance(resp['data'], dict) else 'N/A'}")
    
    # Test 11: Additional APIs
    print("\n[11] ADDITIONAL APIs")
    
    # Departments
    path = f"/tenants/{TENANT_ID}/departments"
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # Stores tree
    path = f"/tenants/{TENANT_ID}/stores/tree"
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # Logs
    path = f"/tenants/{TENANT_ID}/logs"
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # System health
    path = "/system/health"
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # System version
    path = "/system/version"
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # Dicts
    path = "/dicts"
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # Plans (admin)
    path = "/admin/plans"
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    # Tenants (admin)
    path = "/admin/tenants"
    status, resp, err = make_request("GET", path, token=TOKEN)
    print(f"   GET {path} -> {status}")
    
    print("\n" + "="*60)
    print("API VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_apis()
