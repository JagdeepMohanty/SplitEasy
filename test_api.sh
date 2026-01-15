#!/bin/bash

# EasyXpense API Test Script
# Tests all endpoints to verify backend is working correctly

BASE_URL="https://easyxpense.onrender.com"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "🧪 EasyXpense API Test Suite"
echo "=========================================="
echo ""
echo "Backend URL: $BASE_URL"
echo ""

# Counter for passed/failed tests
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        echo "   Response: $body" | head -c 100
        echo ""
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code)"
        echo "   Response: $body"
        FAILED=$((FAILED + 1))
    fi
    echo ""
}

# Test 1: Root endpoint
test_endpoint "Root Endpoint" "GET" "/"

# Test 2: Health check
test_endpoint "Health Check" "GET" "/health"

# Test 3: API Health
test_endpoint "API Health" "GET" "/api/health"

# Test 4: Test endpoint
test_endpoint "Test Endpoint" "GET" "/api/test"

# Test 5: Test POST
test_endpoint "Test POST" "POST" "/api/test" '{"test":"data"}'

# Test 6: Get Friends (empty is OK)
test_endpoint "Get Friends" "GET" "/api/friends"

# Test 7: Add Friend
TIMESTAMP=$(date +%s)
test_endpoint "Add Friend" "POST" "/api/friends" "{\"name\":\"Test User $TIMESTAMP\",\"email\":\"test$TIMESTAMP@example.com\"}"

# Test 8: Get Friends (should have at least one now)
test_endpoint "Get Friends Again" "GET" "/api/friends"

# Test 9: Get Expenses (empty is OK)
test_endpoint "Get Expenses" "GET" "/api/expenses"

# Test 10: Add Expense
test_endpoint "Add Expense" "POST" "/api/expenses" "{\"description\":\"Test Expense\",\"amount\":100,\"payer\":\"Test User $TIMESTAMP\",\"participants\":[\"Test User $TIMESTAMP\"]}"

# Test 11: Get Expenses (should have at least one now)
test_endpoint "Get Expenses Again" "GET" "/api/expenses"

# Test 12: Get Debts
test_endpoint "Get Debts" "GET" "/api/debts"

# Test 13: Get Settlements
test_endpoint "Get Settlements" "GET" "/api/settlements"

# Summary
echo "=========================================="
echo "📊 Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Backend is fully operational.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Check the errors above.${NC}"
    exit 1
fi
