#!/bin/sh
RESP=$(cat /tmp/l.json | curl -s -X POST "http://localhost:8080/api/v1/auth/login" -H "Content-Type: application/json" -d @-)
TOKEN=$(echo "$RESP" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

echo "Testing POST /api/v1/emotion/recognize/text"
curl -s -X POST "http://localhost:8080/api/v1/emotion/recognize/text" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"I am happy today"}'
