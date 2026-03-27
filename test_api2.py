# MDM API Verification Test Script
import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://localhost:8080/api/v1"
TOKEN = None
TENANT_ID = "e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2"  # extracted from JWT

def make_request(method, path, data=None, token=None):
    url = BASE_URL + path
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return "PASS", result, None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            result = json.loads(body)
            return "HTTP_" + str(e.code), result, str(e)
        except:
            return "HTTP_" + str(e.code), {"raw": body[:200]}, str(e)
    except Exception as e:
        return "ERROR", {}, str(e)

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print("[" + ts + "] " + str(msg))

log("Starting MDM API Verification")

# Login
status, resp, err = make_request("POST", "/auth/login", {"username": "admin", "password": "admin123"})
log("LOGIN -> " + status + ": " + json.dumps(resp)[:200])
if resp.get("data"):
    import base64
    TOKEN = resp["data"].get("token")
    payload = TOKEN.split('.')[1]
    payload += '=' * (4 - len(payload) % 4)
    decoded = json.loads(base64.b64decode(payload))
    TENANT_ID = decoded.get("tenant_id", "e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2")
    log("Token: " + TOKEN[:30] + "... TenantID: " + str(TENANT_ID))
else:
    log("FATAL: Login failed")
    exit(1)

tests = [
    # (module, method, path, data)
    ("USER_LIST", "GET", "/tenants/" + TENANT_ID + "/users", None),
    ("USER_CREATE", "POST", "/tenants/" + TENANT_ID + "/users", {"username": "testuser", "real_name": "Test User", "phone": "13800138001", "role": "normal_user"}),
    ("STORE_LIST", "GET", "/tenants/" + TENANT_ID + "/stores", None),
    ("STORE_CREATE", "POST", "/tenants/" + TENANT_ID + "/stores", {"store_name": "Test Store", "store_code": "TEST" + str(int(time.time())), "province": "Beijing", "city": "Beijing", "district": "Chaoyang", "address": "Test Address", "contact_phone": "010-12345678"}),
    ("DEVICE_LIST", "GET", "/tenants/" + TENANT_ID + "/devices", None),
    ("DEVICE_CREATE", "POST", "/tenants/" + TENANT_ID + "/devices", {"device_name": "Test Device", "device_code": "DEV" + str(int(time.time())), "hardware_model": "CoreS3"}),
    ("MEMBER_LIST", "GET", "/tenants/" + TENANT_ID + "/members", None),
    ("ROLE_LIST", "GET", "/roles", None),
    ("ALERT_RULES", "GET", "/tenants/" + TENANT_ID + "/alerts/rules", None),
    ("SETTINGS_GET", "GET", "/tenants/" + TENANT_ID + "/settings", None),
    ("SETTINGS_PUT", "PUT", "/tenants/" + TENANT_ID + "/settings", {"tenant_name": "Updated via API Test"}),
    ("AI_CHAT", "POST", "/ai/chat", {"message": "Hello, this is a test"}),
    ("DASHBOARD", "GET", "/dashboard/stats", None),
    ("DEPT_LIST", "GET", "/tenants/" + TENANT_ID + "/departments", None),
    ("STORES_TREE", "GET", "/tenants/" + TENANT_ID + "/stores/tree", None),
    ("LOGS", "GET", "/tenants/" + TENANT_ID + "/logs", None),
    ("SYS_HEALTH", "GET", "/system/health", None),
    ("SYS_VERSION", "GET", "/system/version", None),
    ("DICTS", "GET", "/dicts", None),
    ("ADMIN_PLANS", "GET", "/admin/plans", None),
    ("ADMIN_TENANTS", "GET", "/admin/tenants", None),
]

for name, method, path, data in tests:
    status, resp, err = make_request(method, path, data, TOKEN)
    code = resp.get("code", "N/A") if isinstance(resp, dict) else "N/A"
    data_keys = list(resp.get("data", {}).keys()) if isinstance(resp.get("data"), dict) else "N/A"
    short_resp = json.dumps(resp)[:100]
    log(name + ": " + method + " " + path + " -> status=" + str(status) + " code=" + str(code) + " resp=" + short_resp)

log("Verification complete")
