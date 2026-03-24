#!/bin/sh
RESP=$(cat /tmp/l.json | curl -s -X POST "http://localhost:8080/api/v1/auth/login" -H "Content-Type: application/json" -d @-)
TOKEN=$(echo "$RESP" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

echo "Token: $TOKEN"
echo ""
echo "=== /api/v1/pet-social/feed ==="
curl -s "http://localhost:8080/api/v1/pet-social/feed" -H "Authorization: Bearer $TOKEN"
