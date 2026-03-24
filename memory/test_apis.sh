#!/bin/sh
RESP=$(cat /tmp/l.json | curl -s -X POST "http://localhost:8080/api/v1/auth/login" -H "Content-Type: application/json" -d @-)
TOKEN=$(echo "$RESP" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

for api in \
    "/api/v1/alerts" \
    "/api/v1/subscriptions/plans" \
    "/api/v1/health/1/exercise" \
    "/api/v1/digital-twin/1/vitals" \
    "/api/v1/ai/models" \
    "/api/v1/research/datasets" \
    "/api/v1/simulation/virtual-pets"; do
    echo "=== $api ==="
    RESULT=$(curl -s "http://localhost:8080$api" -H "Authorization: Bearer $TOKEN")
    CODE=$(echo "$RESULT" | grep -o '"code":[0-9]*' | head -1 | cut -d':' -f2)
    if [ "$CODE" = "0" ] || [ "$CODE" = "200" ]; then
        echo "✅ PASS"
    elif [ -z "$CODE" ]; then
        echo "❌ 404/ERROR"
    else
        echo "⚠️  code=$CODE"
    fi
done
