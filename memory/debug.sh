#!/bin/sh
RESP=$(cat /tmp/l.json | curl -s -X POST "http://localhost:8080/api/v1/auth/login" -H "Content-Type: application/json" -d @-)
TOKEN=$(echo "$RESP" | sed 's/.*"token":"\([^"]*\)".*/\1/')

echo "Token: $TOKEN"
echo ""

echo "=== Health Exercise ==="
curl -s "http://localhost:8080/api/v1/health/1/exercise" -H "Authorization: Bearer $TOKEN"
echo ""

echo "=== Digital Twin Vitals ==="
curl -s "http://localhost:8080/api/v1/digital-twin/1/vitals" -H "Authorization: Bearer $TOKEN"
