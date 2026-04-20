#!/bin/bash
# ============================================================
# run_tests_ci.sh — Run tests in CI/CD environment
#
# PURPOSE:
#   Execute tests with CI-friendly logging and output.
#   Ensures logs are visible in CI console and saved to files.
#
# USAGE:
#   ./run_tests_ci.sh                    # Run all tests
#   ./run_tests_ci.sh tests/test_cart.py # Run specific test file
#
# CI ENVIRONMENTS SUPPORTED:
#   - GitHub Actions
#   - Jenkins
#   - GitLab CI
#   - Travis CI
#   - CircleCI
#   - Any CI with CI=true environment variable
#
# OUTPUT:
#   - Console: Real-time logs with progress
#   - File: logs/pytest_execution.log
#   - Report: reports/latest_report.html
# ============================================================

set -e  # Exit on error
set -o pipefail  # Exit on pipe failure

# Colors for output (if terminal supports it)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log with timestamp
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}"
}

# Print header
echo "============================================================"
log "Boutiqaat Automation - CI Test Execution"
echo "============================================================"

# Detect CI environment
if [ ! -z "$CI" ] || [ ! -z "$GITHUB_ACTIONS" ] || [ ! -z "$JENKINS_HOME" ] || [ ! -z "$GITLAB_CI" ]; then
    log "CI environment detected"
    export PYTHONUNBUFFERED=1  # Force unbuffered output
    export PYTEST_CURRENT_TEST=""  # Show current test in output
else
    log_warning "Not running in CI environment (local execution)"
fi

# Create necessary directories
log "Creating output directories..."
mkdir -p logs
mkdir -p reports
mkdir -p screenshots
mkdir -p videos

# Check Python version
log "Checking Python version..."
python3 --version || { log_error "Python 3 not found"; exit 1; }

# Check if pytest is installed
log "Checking pytest installation..."
python3 -m pytest --version || { log_error "Pytest not installed"; exit 1; }

# Get test path (default to all tests)
TEST_PATH="${1:-tests/}"
log "Test path: $TEST_PATH"

# Count tests
log "Collecting tests..."
TEST_COUNT=$(python3 -m pytest --collect-only -q "$TEST_PATH" 2>/dev/null | tail -1 | grep -oE '[0-9]+' | head -1)
log "Found $TEST_COUNT tests to execute"

# Run tests with CI-friendly options
log "Starting test execution..."
echo "============================================================"

# Run pytest with:
# -v: Verbose output
# --tb=short: Short traceback
# --capture=no: Show output in real-time
# --log-cli-level=INFO: Show INFO logs
# -s: Don't capture stdout (show print statements)
# --maxfail=5: Stop after 5 failures (optional, remove if you want all tests to run)

python3 -m pytest "$TEST_PATH" \
    -v \
    --tb=short \
    --capture=no \
    --log-cli-level=INFO \
    -s \
    2>&1 | tee logs/ci_execution.log

# Capture exit code
EXIT_CODE=${PIPESTATUS[0]}

echo "============================================================"

# Check results
if [ $EXIT_CODE -eq 0 ]; then
    log_success "All tests passed!"
    log_success "Exit code: $EXIT_CODE"
elif [ $EXIT_CODE -eq 1 ]; then
    log_error "Some tests failed"
    log_error "Exit code: $EXIT_CODE"
elif [ $EXIT_CODE -eq 2 ]; then
    log_error "Test execution interrupted"
    log_error "Exit code: $EXIT_CODE"
elif [ $EXIT_CODE -eq 5 ]; then
    log_warning "No tests collected"
    log_warning "Exit code: $EXIT_CODE"
else
    log_error "Test execution error"
    log_error "Exit code: $EXIT_CODE"
fi

# Show log file location
echo "============================================================"
log "Logs saved to:"
log "  - logs/pytest_execution.log (pytest logs)"
log "  - logs/ci_execution.log (full console output)"
log "  - logs/latest.log (framework logs)"

# Show report location
if [ -f "reports/latest_report.html" ]; then
    log "HTML report generated:"
    log "  - reports/latest_report.html"
fi

# Show screenshots if any failures
if [ -d "screenshots" ] && [ "$(ls -A screenshots/*.png 2>/dev/null)" ]; then
    log_warning "Failure screenshots available in screenshots/"
fi

echo "============================================================"

# Exit with pytest's exit code
exit $EXIT_CODE
