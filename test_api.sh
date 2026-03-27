#!/bin/sh
# Login first
LOGIN=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')
# Extract token manually (no python)
TOKEN=$(echo "$LOGIN" | sed -n 's/.*"token":"([^"]*)".*/\1/p')
echo "=== Login result ==="
echo "$LOGIN"
echo ""
echo "=== Token ==="
echo "$TOKEN"
echo ""
echo "=== Menu API ==="
curl -s http://localhost:8080/api/v1/menus -H "Authorization: Bearer $TOKEN"
echo ""
echo ""
echo "=== Dashboard Stats ==="
curl -s http://localhost:8080/api/v1/dashboard/stats -H "Authorization: Bearer $TOKEN"
