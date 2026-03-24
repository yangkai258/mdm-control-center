#!/bin/sh
RESP=$(cat /tmp/l.json | curl -s -X POST "http://localhost:8080/api/v1/auth/login" -H "Content-Type: application/json" -d @-)
TOKEN=$(echo "$RESP" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

echo "=== /api/v1/compliance/policies ==="
curl -s "http://localhost:8080/api/v1/compliance/policies" -H "Authorization: Bearer $TOKEN"
echo ""
echo "=== /api/v1/device-shadow/1 ==="
curl -s "http://localhost:8080/api/v1/device-shadow/1" -H "Authorization: Bearer $TOKEN"