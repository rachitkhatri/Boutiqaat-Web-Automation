# Quick Debugging Reference Card

## 🚨 Common Issues & How to Debug

### Issue 1: Cart Count Returns 0

**Symptoms:**
```
❌ ASSERTION FAILED
   Condition: Cart should have items
   Expected:  > 0
   Actual:    0
```

**Debug Steps:**
1. Check log for cart operations:
   ```bash
   grep -A 5 "Add To Cart" logs/latest.log
   ```

2. Look for timing issues:
   ```bash
   grep "wait_for_timeout" logs/latest.log | grep -A 2 "cart"
   ```

3. Check screenshot:
   ```bash
   open screenshots/fail_test_add_to_cart.png
   ```

4. Verify page URL:
   ```bash
   grep "PAGE INFO.*cart" logs/latest.log
   ```

**Common Causes:**
- API sync delay (increase wait time)
- Wrong selector (check screenshot)
- Session expired (check login logs)

---

### Issue 2: Login Failed

**Symptoms:**
```
❌ TEST FAILED: Login failed — check credentials or rate limiting
```

**Debug Steps:**
1. Check login attempts:
   ```bash
   grep "Login attempt" logs/latest.log
   ```

2. Check for rate limiting:
   ```bash
   grep "rate limiting" logs/latest.log
   ```

3. Verify credentials used:
   ```bash
   grep "DEBUG.*email" logs/latest.log
   ```

4. Check final URL:
   ```bash
   grep "current_url.*login" logs/latest.log
   ```

**Common Causes:**
- Rate limiting (increase wait between attempts)
- Wrong credentials (check test data)
- Page load timeout (increase timeout)

---

### Issue 3: Element Not Found

**Symptoms:**
```
🔥 ERROR OCCURRED
Type:     TimeoutError
Message:  Locator.wait_for: Timeout 30000ms exceeded
```

**Debug Steps:**
1. Find which element:
   ```bash
   grep -B 5 "TimeoutError" logs/latest.log
   ```

2. Check page state:
   ```bash
   grep "PAGE INFO" logs/latest.log | tail -5
   ```

3. View screenshot:
   ```bash
   ls -lt screenshots/*.png | head -1
   ```

4. Check selector in code:
   - Look at the line number in stack trace
   - Verify selector matches current page

**Common Causes:**
- Page not fully loaded (increase wait)
- Selector changed (update selector)
- Modal blocking element (dismiss modal first)

---

### Issue 4: Wishlist Count Not Updating

**Symptoms:**
```
🔍 DEBUG: wishlist_count = 0 (type: int)
❌ ASSERTION FAILED: Wishlist count should increase
```

**Debug Steps:**
1. Check API calls:
   ```bash
   grep "API CALL.*wishlist" logs/latest.log
   ```

2. Check retry attempts:
   ```bash
   grep "Wishlist API call failed" logs/latest.log
   ```

3. Verify add operation:
   ```bash
   grep "Added to Wishlist" logs/latest.log
   ```

4. Check timing:
   ```bash
   grep -A 3 "Added to Wishlist" logs/latest.log | grep "wait_for_timeout"
   ```

**Common Causes:**
- API slow to sync (increase retry attempts)
- Session expired (check login)
- Network issue (check API response)

---

### Issue 5: Address Edit Button Not Found

**Symptoms:**
```
🔥 ERROR OCCURRED
Context:  Edit button not found
```

**Debug Steps:**
1. Check if address was saved:
   ```bash
   grep "Address Saved" logs/latest.log
   ```

2. Check page state:
   ```bash
   grep "PAGE INFO.*address" logs/latest.log
   ```

3. View screenshot:
   ```bash
   open screenshots/fail_test_edit_address.png
   ```

4. Check for page reload:
   ```bash
   grep "reload" logs/latest.log | grep -A 2 "address"
   ```

**Common Causes:**
- Page not reloaded (add page reload)
- Different UI state (check screenshot)
- Selector changed (update selector)

---

## 📋 Quick Log Commands

### View Latest Test Run
```bash
cat logs/latest.log
```

### View Only Errors
```bash
grep "ERROR\|FAIL" logs/latest.log
```

### View Test Summary
```bash
grep "TEST.*PASSED\|TEST.*FAILED\|TEST.*SKIPPED" logs/latest.log
```

### View Specific Test
```bash
grep "test_add_to_cart" logs/latest.log
```

### View All Assertions
```bash
grep "ASSERTION" logs/latest.log
```

### View All Debug Info
```bash
grep "DEBUG" logs/latest.log
```

### View API Calls
```bash
grep "API CALL" logs/latest.log
```

### View Screenshots Taken
```bash
grep "Screenshot saved" logs/latest.log
```

### View Test Timing
```bash
grep "Duration:" logs/latest.log
```

### View All Steps
```bash
grep "STEP" logs/latest.log
```

---

## 🔍 Advanced Debugging

### Find Where Test Failed
```bash
# Get test name
grep "TEST FAILED" logs/latest.log

# Find last successful step before failure
grep -B 20 "ERROR OCCURRED" logs/latest.log | grep "STEP.*COMPLETE"
```

### Compare Two Test Runs
```bash
# List all log files
ls -lt logs/test_run_*.log

# Compare two runs
diff logs/test_run_20240115_143000.log logs/test_run_20240115_150000.log
```

### Extract All Errors from Multiple Runs
```bash
grep "ERROR OCCURRED" logs/test_run_*.log
```

### Find Slowest Tests
```bash
grep "Duration:" logs/latest.log | sort -t: -k2 -n -r | head -10
```

---

## 🛠️ Fixing Common Issues

### Issue: Tests Too Slow
**Solution:** Check wait times in logs
```bash
grep "wait_for_timeout" logs/latest.log | awk '{sum+=$NF} END {print sum/1000 "s total wait time"}'
```

### Issue: Flaky Tests
**Solution:** Check for timing issues
```bash
# Find tests that sometimes pass, sometimes fail
grep "test_name" logs/test_run_*.log | grep "PASSED\|FAILED"
```

### Issue: Rate Limiting
**Solution:** Check login frequency
```bash
grep "Login attempt" logs/latest.log | wc -l
```

### Issue: Stale Elements
**Solution:** Check for page reloads
```bash
grep "reload\|goto" logs/latest.log
```

---

## 📊 Log Analysis Tips

1. **Always check latest.log first**
   - Most recent run, easiest to find

2. **Use grep with context (-A, -B, -C)**
   - See what happened before/after error

3. **Check timestamps**
   - Identify slow operations

4. **Look for patterns**
   - Same error in multiple tests?

5. **Compare screenshots with logs**
   - Visual + text = full picture

6. **Check test duration**
   - Timeouts often cause failures

---

## 🎯 Quick Fixes Checklist

When a test fails:

- [ ] Check `logs/latest.log` for error details
- [ ] View screenshot in `screenshots/` folder
- [ ] Look for "ERROR OCCURRED" section
- [ ] Check "DEBUG" entries before error
- [ ] Verify "PAGE INFO" shows correct URL
- [ ] Check "ASSERTION" results
- [ ] Review "STEP" progression
- [ ] Check test "Duration" for timeouts
- [ ] Look for "WARN" messages
- [ ] Verify "API CALL" responses

---

## 💡 Pro Tips

1. **Keep logs directory clean**
   ```bash
   # Delete logs older than 7 days
   find logs/ -name "test_run_*.log" -mtime +7 -delete
   ```

2. **Create log aliases**
   ```bash
   alias viewlog="cat logs/latest.log"
   alias errors="grep 'ERROR\|FAIL' logs/latest.log"
   alias debug="grep 'DEBUG' logs/latest.log"
   ```

3. **Use log viewer tools**
   ```bash
   # Install bat for syntax highlighting
   brew install bat
   bat logs/latest.log
   ```

4. **Monitor logs in real-time**
   ```bash
   tail -f logs/latest.log
   ```

---

## 📞 Need More Help?

1. Check `LOGGING_GUIDE.md` for detailed documentation
2. Check `FIXES_APPLIED.md` for known issues and fixes
3. Review test code with log output side-by-side
4. Add more `log_debug()` calls to narrow down issues
