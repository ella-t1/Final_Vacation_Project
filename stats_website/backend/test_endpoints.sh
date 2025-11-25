#!/bin/bash
# Test script for backend API endpoints
# Make sure the server is running on http://localhost:5001

BASE_URL="http://localhost:5001"
COOKIE_FILE="cookies.txt"

echo "=== Testing Statistics Backend API ==="
echo ""

# Test 1: Health Check
echo "1. Testing Health Check..."
curl -s "$BASE_URL/health" | python -m json.tool
echo ""
echo ""

# Test 2: Login (should succeed for admin)
echo "2. Testing Login (Admin)..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin1234"}' \
  -c "$COOKIE_FILE" -w "\nHTTP_STATUS:%{http_code}")

HTTP_STATUS=$(echo "$LOGIN_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
BODY=$(echo "$LOGIN_RESPONSE" | sed '/HTTP_STATUS/d')

echo "Status: $HTTP_STATUS"
echo "$BODY" | python -m json.tool
echo ""
echo ""

# Test 3: Try to access stats without auth (should fail)
echo "3. Testing Protected Route Without Auth..."
curl -s "$BASE_URL/vacations/stats" | python -m json.tool
echo ""
echo ""

# Test 4: Get Statistics (with auth)
if [ -f "$COOKIE_FILE" ]; then
    echo "4. Testing Vacation Statistics..."
    curl -s "$BASE_URL/vacations/stats" -b "$COOKIE_FILE" | python -m json.tool
    echo ""
    echo ""
    
    echo "5. Testing Total Users..."
    curl -s "$BASE_URL/users/total" -b "$COOKIE_FILE" | python -m json.tool
    echo ""
    echo ""
    
    echo "6. Testing Total Likes..."
    curl -s "$BASE_URL/likes/total" -b "$COOKIE_FILE" | python -m json.tool
    echo ""
    echo ""
    
    echo "7. Testing Likes Distribution..."
    curl -s "$BASE_URL/likes/distribution" -b "$COOKIE_FILE" | python -m json.tool
    echo ""
    echo ""
    
    echo "8. Testing Logout..."
    curl -s -X POST "$BASE_URL/logout" -b "$COOKIE_FILE" | python -m json.tool
    echo ""
    echo ""
fi

# Cleanup
rm -f "$COOKIE_FILE"

echo "=== Testing Complete ==="

