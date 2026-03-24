#!/bin/sh
RESP=$(cat /tmp/l.json | curl -s -X POST "http://localhost:8080/api/v1/auth/login" -H "Content-Type: application/json" -d @-)
TOKEN=$(echo "$RESP" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

echo "Token obtained"
echo ""

# Test previously failing APIs
for api in \
    "/api/v1/insurance/products" \
    "/api/v1/family/children/profiles" \
    "/api/v1/compliance/policies" \
    "/api/v1/devices/1/shadow" \
    "/api/v1/knowledge/articles" \
    "/api/v1/subscriptions/plans" \
    "/api/v1/ai/models"; do
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
