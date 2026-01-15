@echo off
REM EasyXpense API Test Script for Windows
REM Tests all endpoints to verify backend is working correctly

setlocal enabledelayedexpansion

set BASE_URL=https://easyxpense.onrender.com
set PASSED=0
set FAILED=0

echo ==========================================
echo EasyXpense API Test Suite
echo ==========================================
echo.
echo Backend URL: %BASE_URL%
echo.

REM Test 1: Root endpoint
echo Testing Root Endpoint...
curl -s %BASE_URL%/
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Root Endpoint
    set /a PASSED+=1
) else (
    echo [FAILED] Root Endpoint
    set /a FAILED+=1
)
echo.

REM Test 2: Health check
echo Testing Health Check...
curl -s %BASE_URL%/health
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Health Check
    set /a PASSED+=1
) else (
    echo [FAILED] Health Check
    set /a FAILED+=1
)
echo.

REM Test 3: API Health
echo Testing API Health...
curl -s %BASE_URL%/api/health
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] API Health
    set /a PASSED+=1
) else (
    echo [FAILED] API Health
    set /a FAILED+=1
)
echo.

REM Test 4: Test endpoint
echo Testing Test Endpoint...
curl -s %BASE_URL%/api/test
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Test Endpoint
    set /a PASSED+=1
) else (
    echo [FAILED] Test Endpoint
    set /a FAILED+=1
)
echo.

REM Test 5: Get Friends
echo Testing Get Friends...
curl -s %BASE_URL%/api/friends
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Get Friends
    set /a PASSED+=1
) else (
    echo [FAILED] Get Friends
    set /a FAILED+=1
)
echo.

REM Test 6: Add Friend
echo Testing Add Friend...
curl -s -X POST %BASE_URL%/api/friends -H "Content-Type: application/json" -d "{\"name\":\"Test User\",\"email\":\"test@example.com\"}"
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Add Friend
    set /a PASSED+=1
) else (
    echo [FAILED] Add Friend
    set /a FAILED+=1
)
echo.

REM Test 7: Get Expenses
echo Testing Get Expenses...
curl -s %BASE_URL%/api/expenses
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Get Expenses
    set /a PASSED+=1
) else (
    echo [FAILED] Get Expenses
    set /a FAILED+=1
)
echo.

REM Test 8: Get Debts
echo Testing Get Debts...
curl -s %BASE_URL%/api/debts
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Get Debts
    set /a PASSED+=1
) else (
    echo [FAILED] Get Debts
    set /a FAILED+=1
)
echo.

REM Test 9: Get Settlements
echo Testing Get Settlements...
curl -s %BASE_URL%/api/settlements
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Get Settlements
    set /a PASSED+=1
) else (
    echo [FAILED] Get Settlements
    set /a FAILED+=1
)
echo.

REM Summary
echo ==========================================
echo Test Summary
echo ==========================================
echo Passed: %PASSED%
echo Failed: %FAILED%
set /a TOTAL=%PASSED%+%FAILED%
echo Total:  %TOTAL%
echo.

if %FAILED% EQU 0 (
    echo All tests passed! Backend is fully operational.
    exit /b 0
) else (
    echo Some tests failed. Check the errors above.
    exit /b 1
)
