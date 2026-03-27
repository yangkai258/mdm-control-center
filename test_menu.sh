#!/bin/sh
TOKEN=$(curl -s -X POST http://localhost:8080/api/v1/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}' | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('token',''))")
echo "Token: $TOKEN"
echo ""
echo "Menus API:"
curl -s http://localhost:8080/api/v1/menus -H "Authorization: Bearer $TOKEN"
echo ""
echo ""
echo "Dashboard API:"
curl -s http://localhost:8080/api/v1/dashboard/stats -H "Authorization: Bearer $TOKEN"
