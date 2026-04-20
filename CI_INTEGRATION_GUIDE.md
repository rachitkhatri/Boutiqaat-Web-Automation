# CI/CD Integration Guide

## 🎯 Running Tests in CI Environments

This guide explains how to run the Boutiqaat automation tests in CI/CD pipelines with proper logging.

---

## 🚀 Quick Start

### **Option 1: Using the CI Script (Recommended)**

```bash
# Run all tests
./run_tests_ci.sh

# Run specific test file
./run_tests_ci.sh tests/test_cart.py

# Run specific test
./run_tests_ci.sh tests/test_cart.py::test_add_to_cart
```

### **Option 2: Direct Pytest Command**

```bash
# Run with CI-friendly options
python3 -m pytest tests/ -v --capture=no --log-cli-level=INFO -s
```

---

## 📊 What Gets Logged

### **1. Console Output (Real-time)**
- Test collection results
- Test execution progress (X/Y tests, Z% complete)
- Test results (PASS/FAIL/SKIP)
- Test duration
- Estimated time remaining
- Final summary with statistics

### **2. Log Files**
- `logs/pytest_execution.log` - Pytest logs with DEBUG level
- `logs/ci_execution.log` - Full console output (when using script)
- `logs/latest.log` - Framework logs with timestamps
- `logs/test_run_*.log` - Timestamped execution logs

### **3. HTML Report**
- `reports/latest_report.html` - Comprehensive test report
- `reports/report_*.html` - Timestamped reports

### **4. Failure Artifacts**
- `screenshots/fail_*.png` - Screenshots of failed tests
- `videos/*.webm` - Video recordings of test execution

---

## 🔧 CI Configuration Examples

### **GitHub Actions**

```yaml
name: Boutiqaat Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Run tests
        run: ./run_tests_ci.sh
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: |
            logs/
            reports/
            screenshots/
      
      - name: Upload HTML report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: html-report
          path: reports/latest_report.html
```

---

### **Jenkins**

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install chromium'
            }
        }
        
        stage('Test') {
            steps {
                sh './run_tests_ci.sh'
            }
        }
    }
    
    post {
        always {
            // Archive test results
            archiveArtifacts artifacts: 'logs/**, reports/**, screenshots/**', allowEmptyArchive: true
            
            // Publish HTML report
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'latest_report.html',
                reportName: 'Test Report'
            ])
        }
    }
}
```

---

### **GitLab CI**

```yaml
test:
  image: python:3.9
  
  before_script:
    - pip install -r requirements.txt
    - playwright install chromium
  
  script:
    - ./run_tests_ci.sh
  
  artifacts:
    when: always
    paths:
      - logs/
      - reports/
      - screenshots/
    reports:
      junit: logs/pytest_execution.log
```

---

### **Travis CI**

```yaml
language: python
python:
  - "3.9"

install:
  - pip install -r requirements.txt
  - playwright install chromium

script:
  - ./run_tests_ci.sh

after_script:
  - cat logs/pytest_execution.log
```

---

## 📝 Pytest Configuration for CI

The `pytest.ini` file is configured for CI-friendly output:

```ini
[pytest]
# Show output in real-time (no buffering)
addopts = -v --tb=short -p no:warnings --capture=no --log-cli-level=INFO

# Enable live logging
log_cli = true
log_cli_level = INFO

# File logging
log_file = logs/pytest_execution.log
log_file_level = DEBUG
```

---

## 🔍 Troubleshooting CI Issues

### **Issue 1: Logs Not Appearing**

**Problem:** Logs don't show up in CI console

**Solution:**
```bash
# Use unbuffered Python output
export PYTHONUNBUFFERED=1

# Run with -s flag (don't capture stdout)
python3 -m pytest tests/ -v -s --capture=no
```

---

### **Issue 2: Tests Timeout in CI**

**Problem:** Tests timeout in CI but work locally

**Solution:**
```python
# Increase timeouts in config/settings.py
DEFAULT_TIMEOUT = 60_000  # 60 seconds
PAYMENT_TIMEOUT = 300_000  # 5 minutes
```

---

### **Issue 3: Browser Not Found**

**Problem:** Playwright can't find browser in CI

**Solution:**
```bash
# Install browsers before running tests
playwright install chromium

# Or install all browsers
playwright install
```

---

### **Issue 4: Permission Denied**

**Problem:** Can't execute run_tests_ci.sh

**Solution:**
```bash
# Make script executable
chmod +x run_tests_ci.sh

# Or run with bash
bash run_tests_ci.sh
```

---

## 📊 Understanding Exit Codes

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | All tests passed | ✅ Success |
| 1 | Some tests failed | ❌ Check logs |
| 2 | Test execution interrupted | ⚠️ Check CI timeout |
| 3 | Internal pytest error | 🔥 Check pytest installation |
| 4 | Pytest usage error | ⚠️ Check command syntax |
| 5 | No tests collected | ⚠️ Check test path |

---

## 🎯 Best Practices for CI

### **1. Use Headless Mode**

For CI environments, run browser in headless mode:

```python
# conftest.py
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": True,  # ← Headless for CI
        "args": ["--no-sandbox", "--disable-dev-shm-usage"],  # CI-friendly args
    }
```

---

### **2. Parallel Execution**

Run tests in parallel for faster CI:

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest tests/ -n auto  # Auto-detect CPU cores
pytest tests/ -n 4     # Use 4 workers
```

---

### **3. Retry Failed Tests**

Retry flaky tests automatically:

```bash
# Install pytest-rerunfailures
pip install pytest-rerunfailures

# Retry failed tests up to 2 times
pytest tests/ --reruns 2 --reruns-delay 5
```

---

### **4. Generate JUnit XML**

For CI integration:

```bash
# Generate JUnit XML report
pytest tests/ --junitxml=logs/junit.xml
```

---

### **5. Set Timeouts**

Prevent tests from hanging:

```bash
# Install pytest-timeout
pip install pytest-timeout

# Set 10-minute timeout per test
pytest tests/ --timeout=600
```

---

## 📈 Monitoring Test Results

### **View Logs in CI**

```bash
# GitHub Actions
cat logs/pytest_execution.log

# Jenkins
cat $WORKSPACE/logs/pytest_execution.log

# GitLab CI
cat logs/pytest_execution.log
```

---

### **Download Artifacts**

All CI platforms allow downloading:
- Test logs
- HTML reports
- Screenshots
- Videos

Check your CI platform's documentation for artifact download.

---

## 🚀 Advanced CI Features

### **Conditional Test Execution**

Run different tests based on branch:

```yaml
# GitHub Actions
- name: Run tests
  run: |
    if [ "${{ github.ref }}" == "refs/heads/main" ]; then
      ./run_tests_ci.sh tests/  # All tests on main
    else
      ./run_tests_ci.sh tests/test_smoke.py  # Smoke tests on branches
    fi
```

---

### **Scheduled Runs**

Run tests on a schedule:

```yaml
# GitHub Actions - Run daily at 2 AM
on:
  schedule:
    - cron: '0 2 * * *'
```

---

### **Matrix Testing**

Test on multiple Python versions:

```yaml
# GitHub Actions
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11']
```

---

## 📞 Support

If logs still don't appear in CI:

1. Check `logs/pytest_execution.log` file
2. Verify `pytest.ini` has `log_cli = true`
3. Ensure `--capture=no` flag is used
4. Set `PYTHONUNBUFFERED=1` environment variable
5. Use `-s` flag with pytest
6. Check CI platform's log settings

---

## ✅ Checklist for CI Setup

- [ ] Install Python 3.9+
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Install Playwright browsers (`playwright install chromium`)
- [ ] Make run_tests_ci.sh executable (`chmod +x run_tests_ci.sh`)
- [ ] Set PYTHONUNBUFFERED=1 environment variable
- [ ] Configure artifact upload for logs/reports/screenshots
- [ ] Set appropriate timeouts
- [ ] Enable headless mode for browsers
- [ ] Configure test result reporting

---

**Your tests are now CI-ready with comprehensive logging!** 🎉
