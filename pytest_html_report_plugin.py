# ============================================================
# pytest_html_report_plugin.py — Comprehensive HTML report
# with all modules, page objects, and detailed coverage.
# ============================================================

import pytest, time, os, base64, platform, traceback
from datetime import datetime
from pathlib import Path

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


class _Result:
    __slots__ = ("nodeid", "name", "status", "duration", "error_msg",
                 "short_tb", "screenshot", "markers", "params", "module")

    def __init__(self, nodeid, name):
        self.nodeid = nodeid
        self.name = name
        self.status = "unknown"
        self.duration = 0.0
        self.error_msg = ""
        self.short_tb = ""
        self.screenshot = ""
        self.markers = []
        self.params = ""
        self.module = ""


_results: list[_Result] = []
_start_times: dict[str, float] = {}
_session_start = 0.0


def _format_duration(seconds):
    """Format duration as Xm Ys or Xs"""
    if seconds >= 60:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"
    return f"{seconds:.1f}s"


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    global _session_start
    _session_start = time.time()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    _start_times[item.nodeid] = time.time()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" and not (report.when == "setup" and report.failed):
        return

    r = _Result(item.nodeid, item.name)
    r.duration = report.duration if report.duration else (time.time() - _start_times.pop(item.nodeid, time.time()))
    r.markers = [m.name for m in item.iter_markers()]
    
    if "::" in item.nodeid:
        module_path = item.nodeid.split("::")[0]
        r.module = os.path.basename(module_path).replace(".py", "")

    if "[" in item.name:
        r.params = item.name.split("[", 1)[1].rstrip("]")

    if report.passed:
        r.status = "passed"
    elif report.skipped:
        r.status = "skipped"
        r.error_msg = str(report.longrepr[-1]) if isinstance(report.longrepr, tuple) else str(report.longrepr)
    elif report.failed:
        r.status = "failed"
        if report.longrepr:
            r.short_tb = str(report.longrepr)
            lines = r.short_tb.strip().splitlines()
            r.error_msg = lines[-1] if lines else ""

    safe = item.name.replace("[", "_").replace("]", "")
    shot = f"screenshots/fail_{safe}.png"
    if os.path.isfile(shot):
        try:
            r.screenshot = base64.b64encode(Path(shot).read_bytes()).decode()
        except Exception:
            pass

    _results.append(r)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    # Calculate total duration from actual test durations instead of wall clock time
    total_dur = sum(r.duration for r in _results) if _results else (time.time() - _session_start)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fname = datetime.now().strftime("report_%Y%m%d_%H%M%S.html")

    passed  = sum(1 for r in _results if r.status == "passed")
    failed  = sum(1 for r in _results if r.status == "failed")
    skipped = sum(1 for r in _results if r.status == "skipped")
    total   = len(_results)
    rate    = f"{passed/total*100:.1f}" if total else "0"
    
    modules = {}
    for r in _results:
        if r.module not in modules:
            modules[r.module] = []
        modules[r.module].append(r)

    module_info = {
        "test_e2e_flow": {
            "name": "End-to-End Purchase Flow",
            "icon": "🛒",
            "description": "Complete user journey from registration to payment",
            "coverage": [
                "User registration via REST API",
                "Login with email/password authentication",
                "Product search functionality",
                "Product detail page (PDP) navigation",
                "Add to cart from PDP",
                "Cart page verification and navigation",
                "Address form filling (area, block, street, villa, phone)",
                "Dynamic block dropdown based on area selection",
                "Address validation and save confirmation",
                "Payment method selection (KNET, Credit Card, Tabby, Amex)",
                "Wallet selection if balance available",
                "Place order and redirect to payment gateway",
                "Payment success flow (manual completion required)",
                "Payment cancellation flow on KNET gateway",
                "Failure screen capture with all transaction details"
            ]
        },
        "test_registration": {
            "name": "User Registration",
            "icon": "👤",
            "description": "New user account creation and validation",
            "coverage": [
                "Registration form field validation",
                "Email uniqueness check (timestamp-based)",
                "Password strength validation",
                "Mobile number format validation (Kuwait format)",
                "Gender selection (men/women)",
                "Terms & Conditions acceptance",
                "Registration REST API endpoint testing",
                "Auto-retry mechanism on transient failures (up to 3 attempts)",
                "Screenshot capture on each failed attempt for debugging"
            ]
        },
        "test_cart": {
            "name": "Shopping Cart Management",
            "icon": "🛍️",
            "description": "Cart operations - add, remove, and verify items",
            "coverage": [
                "Add multiple products to cart",
                "Search and add specific product (Matte Black Sippii Bottle)",
                "Cart page navigation and loading",
                "Remove item from cart using trash icon",
                "Cart item count verification",
                "Cart persistence across sessions",
                "Multiple product handling in cart",
                "Empty cart detection"
            ]
        },
        "test_wishlist": {
            "name": "Wishlist Management",
            "icon": "❤️",
            "description": "Add and manage wishlist items",
            "coverage": [
                "Add to wishlist from Product Detail Page (PDP)",
                "Wishlist icon interaction and state change",
                "Wishlist state persistence after page reload",
                "User authentication requirement for wishlist",
                "Wishlist item verification"
            ]
        },
        "test_address": {
            "name": "Address Management (CRUD)",
            "icon": "📍",
            "description": "Delivery address create, read, update, delete operations",
            "coverage": [
                "Add new delivery address",
                "Area dropdown selection (132 Kuwait areas)",
                "Block dropdown (dynamic load based on selected area)",
                "Street, avenue, villa/building number fields",
                "Floor and flat number (optional fields)",
                "Phone number validation (Kuwait format)",
                "Delivery notes field (optional)",
                "Edit existing address functionality",
                "Add second/multiple addresses to account",
                "Address validation and save confirmation",
                "Continue to payment button verification",
                "Address form field persistence"
            ]
        },
        "test_navigation": {
            "name": "Navigation & Category Pages",
            "icon": "🧭",
            "description": "Public pages, categories, and site navigation",
            "coverage": [
                "Homepage load and rendering (women section)",
                "Makeup category page with product grid",
                "Fragrance category page with product listings",
                "Skincare category page navigation",
                "Haircare category page verification",
                "Brands listing page (all brands)",
                "Search results page (perfume query)",
                "Search results page (lipstick query)",
                "Product grid rendering (minimum 5-10 items per page)",
                "Page title verification (no 404/error pages)",
                "Category navigation without login requirement"
            ]
        }
    }
    
    # Page Objects section
    page_objects_info = {
        "base_page.py": {
            "name": "BasePage",
            "icon": "🔧",
            "description": "Foundation class with shared utilities",
            "methods": [
                "dismiss_overlays() - Remove blocking popups/modals",
                "type_like_user() - Human-like typing simulation",
                "screenshot_on_failure() - Auto-capture on errors"
            ]
        },
        "login_page.py": {
            "name": "LoginPage",
            "icon": "🔐",
            "description": "User authentication and login",
            "methods": [
                "open() - Navigate to login page",
                "login() - Fill credentials and submit",
                "Validates successful login by URL change"
            ]
        },
        "registration_page.py": {
            "name": "RegistrationPage",
            "icon": "📝",
            "description": "New user registration via API and UI",
            "methods": [
                "register() - Create account via REST API",
                "register_and_login() - Combined registration + login",
                "Retry logic for transient failures"
            ]
        },
        "search_page.py": {
            "name": "SearchPage",
            "icon": "🔍",
            "description": "Product search and autocomplete",
            "methods": [
                "search() - Open search overlay and type query",
                "select_first_product() - Click first result",
                "Handles autocomplete dropdown and fallback"
            ]
        },
        "cart_page.py": {
            "name": "CartPage",
            "icon": "🛒",
            "description": "Shopping cart operations",
            "methods": [
                "add_to_cart() - Add product from PDP",
                "open_cart() - Navigate to cart page",
                "get_cart_item_count() - Count items in cart",
                "remove_first_item() - Delete item via trash icon",
                "is_cart_empty() - Check if cart has no items"
            ]
        },
        "address_page.py": {
            "name": "AddressPage",
            "icon": "🏠",
            "description": "Delivery address management",
            "methods": [
                "open() - Navigate to address page",
                "fill_address() - Fill all form fields",
                "save_address() - Submit and save",
                "add_new_address() - Add additional address",
                "edit_address() - Update existing address",
                "has_saved_address() - Verify address saved",
                "continue_to_payment() - Proceed to checkout"
            ]
        },
        "payment_page.py": {
            "name": "PaymentPage",
            "icon": "💳",
            "description": "Payment gateway and order placement",
            "methods": [
                "dismiss_modal() - Close promotional popup",
                "select_payment_method() - Choose KNET/Card/Tabby",
                "select_wallet() - Use wallet balance",
                "place_order() - Submit payment",
                "cancel_payment() - Cancel on KNET gateway",
                "capture_failure_details() - Extract error info",
                "wait_for_payment_success() - Wait for completion"
            ]
        },
        "wishlist_page.py": {
            "name": "WishlistPage",
            "icon": "💝",
            "description": "Wishlist add and remove operations",
            "methods": [
                "add_to_wishlist_from_pdp() - Add from product page",
                "Handles wishlist icon interaction"
            ]
        },
        "navigation_page.py": {
            "name": "NavigationPage",
            "icon": "🗺️",
            "description": "Category and page navigation verification",
            "methods": [
                "verify_page_loads() - Check page loads correctly",
                "get_page_title() - Extract page title",
                "Validates product grid rendering"
            ]
        }
    }
    
    # Page Objects section HTML
    page_objects_section = "<div class='section'><h2>📄 Page Object Model (POM)</h2>"
    page_objects_section += "<p class='pom-desc'>Modular page classes following the Page Object Model pattern for maintainability and reusability.</p>"
    for po_key, po_info in page_objects_info.items():
        methods_list = "".join([f"<li>{m}</li>" for m in po_info["methods"]])
        page_objects_section += f"""
        <div class="pom-card">
          <div class="pom-header">
            <span class="pom-icon">{po_info['icon']}</span>
            <div>
              <h4>{po_info['name']}</h4>
              <p class="pom-file">{po_key}</p>
            </div>
          </div>
          <p class="pom-desc-text">{po_info['description']}</p>
          <ul class="pom-methods">{methods_list}</ul>
        </div>"""
    page_objects_section += "</div>"
    
    # Module coverage section
    module_section = "<div class='section'><h2>📦 Test Modules & Coverage</h2>"
    for mod_key in sorted(modules.keys()):
        if not mod_key:
            continue
        mod_results = modules[mod_key]
        mod_passed = sum(1 for r in mod_results if r.status == "passed")
        mod_failed = sum(1 for r in mod_results if r.status == "failed")
        mod_skipped = sum(1 for r in mod_results if r.status == "skipped")
        mod_total = len(mod_results)
        mod_rate = f"{mod_passed/mod_total*100:.0f}" if mod_total else "0"
        
        info = module_info.get(mod_key, {
            "name": mod_key.replace("test_", "").replace("_", " ").title(),
            "icon": "📝",
            "description": "Test module",
            "coverage": []
        })
        
        status_badge = "pass" if mod_failed == 0 else "fail"
        coverage_list = "".join([f"<li>{item}</li>" for item in info["coverage"]])
        
        module_section += f"""
        <div class="module-card">
          <div class="module-header">
            <div class="module-title">
              <span class="module-icon">{info['icon']}</span>
              <div>
                <h3>{info['name']}</h3>
                <p class="module-desc">{info['description']}</p>
              </div>
            </div>
            <div class="module-stats">
              <span class="badge {status_badge}">{mod_rate}% PASS</span>
              <span class="stat-detail">{mod_passed}✅ {mod_failed}❌ {mod_skipped}⏭️</span>
            </div>
          </div>
          <div class="module-body">
            <h4>Test Coverage ({mod_total} test{'s' if mod_total != 1 else ''}):</h4>
            <ul class="coverage-list">{coverage_list}</ul>
            <div class="test-list">
              <strong>Tests in this module:</strong>
              <ul>{''.join([f"<li><span class='mini-badge {('pass' if r.status=='passed' else 'fail' if r.status=='failed' else 'skip')}'>{r.status[0].upper()}</span> {_esc(r.name)} <span class='test-dur'>({_format_duration(r.duration)})</span></li>" for r in mod_results])}</ul>
            </div>
          </div>
        </div>"""
    module_section += "</div>"

    rows = ""
    for i, r in enumerate(_results, 1):
        badge = {"passed": "pass", "failed": "fail", "skipped": "skip"}.get(r.status, "skip")
        dur = _format_duration(r.duration)
        reason = _esc(r.error_msg) if r.error_msg else "—"

        detail_block = ""
        if r.short_tb and r.status == "failed":
            detail_block += f'<pre class="tb">{_esc(r.short_tb)}</pre>'
        if r.screenshot:
            detail_block += f'<img src="data:image/png;base64,{r.screenshot}" class="shot"/>'

        toggle = ""
        if detail_block:
            toggle = f"""
            <tr class="detail" id="d{i}" style="display:none">
              <td colspan="7">{detail_block}</td>
            </tr>"""

        click = f' class="clickable" onclick="toggle({i})"' if detail_block else ""
        rows += f"""
        <tr{click}>
          <td>{i}</td>
          <td class="module-col">{_esc(r.module)}</td>
          <td class="name">{_esc(r.name)}</td>
          <td><span class="badge {badge}">{r.status.upper()}</span></td>
          <td>{dur}</td>
          <td class="markers">{', '.join(r.markers) or '—'}</td>
          <td class="reason">{reason}</td>
        </tr>{toggle}"""

    failed_section = ""
    if failed:
        frows = ""
        for r in _results:
            if r.status != "failed":
                continue
            frows += f"""
            <div class="fail-card">
              <h4>❌ {_esc(r.name)}</h4>
              <p><strong>Module:</strong> {r.module}</p>
              <p><strong>Duration:</strong> {_format_duration(r.duration)}</p>
              <p><strong>Error:</strong></p>
              <pre class="tb">{_esc(r.short_tb)}</pre>
              {"<p><strong>Screenshot:</strong></p><img src='data:image/png;base64," + r.screenshot + "' class='shot'/>" if r.screenshot else ""}
            </div>"""
        failed_section = f"""
        <div class="section">
          <h2>❌ Failed Tests — Detailed Analysis</h2>
          {frows}
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Boutiqaat Test Report — {ts}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f0f2f5;color:#1a1a2e;padding:24px}}
.container{{max-width:1400px;margin:auto}}
h1{{font-size:1.8rem;margin-bottom:4px}}
.subtitle{{color:#666;margin-bottom:24px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:28px}}
.card{{background:#fff;border-radius:12px;padding:20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.card .num{{font-size:2.2rem;font-weight:700}}
.card .lbl{{font-size:.85rem;color:#666;margin-top:4px}}
.card.total .num{{color:#1a1a2e}}.card.pass .num{{color:#22c55e}}.card.fail .num{{color:#ef4444}}.card.skip .num{{color:#f59e0b}}.card.dur .num{{color:#6366f1}}.card.rate .num{{color:#0ea5e9}}
.bar{{height:10px;border-radius:5px;background:#e5e7eb;margin-bottom:28px;overflow:hidden;display:flex}}
.bar .g{{background:#22c55e}}.bar .r{{background:#ef4444}}.bar .y{{background:#f59e0b}}
.section{{background:#fff;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.section h2{{font-size:1.2rem;margin-bottom:16px}}
.pom-desc{{font-size:.9rem;color:#666;margin-bottom:16px}}
.pom-card{{border:1px solid #e5e7eb;border-radius:8px;padding:16px;margin-bottom:12px;background:#fafbfc}}
.pom-header{{display:flex;gap:12px;align-items:center;margin-bottom:8px}}
.pom-icon{{font-size:1.8rem}}
.pom-header h4{{font-size:1rem;color:#1a1a2e;margin-bottom:2px}}
.pom-file{{font-size:.75rem;color:#6366f1;font-family:monospace}}
.pom-desc-text{{font-size:.85rem;color:#555;margin-bottom:8px}}
.pom-methods{{margin:8px 0 0 20px;font-size:.82rem;line-height:1.6}}
.pom-methods li{{margin-bottom:3px;color:#444}}
.module-card{{border:1px solid #e5e7eb;border-radius:8px;margin-bottom:16px;overflow:hidden}}
.module-header{{background:#f8f9fa;padding:16px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e5e7eb}}
.module-title{{display:flex;gap:12px;align-items:center}}
.module-icon{{font-size:2rem}}
.module-title h3{{font-size:1.1rem;margin-bottom:4px;color:#1a1a2e}}
.module-desc{{font-size:.82rem;color:#666}}
.module-stats{{text-align:right}}
.stat-detail{{display:block;font-size:.75rem;color:#666;margin-top:4px}}
.module-body{{padding:16px}}
.module-body h4{{font-size:.9rem;margin-bottom:8px;color:#444}}
.coverage-list{{margin:8px 0 16px 20px;font-size:.85rem;line-height:1.6}}
.coverage-list li{{margin-bottom:4px;color:#555}}
.test-list{{margin-top:16px;padding-top:16px;border-top:1px solid #f0f0f0}}
.test-list ul{{margin:8px 0 0 20px;font-size:.82rem}}
.test-list li{{margin-bottom:4px}}
.test-dur{{color:#888;font-size:.75rem}}
.mini-badge{{display:inline-block;width:18px;height:18px;line-height:18px;text-align:center;border-radius:50%;font-size:.7rem;font-weight:700;color:#fff;margin-right:6px}}
.mini-badge.pass{{background:#22c55e}}.mini-badge.fail{{background:#ef4444}}.mini-badge.skip{{background:#f59e0b}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:left;padding:10px 12px;background:#f8f9fa;font-size:.8rem;text-transform:uppercase;color:#666;border-bottom:2px solid #e5e7eb}}
td{{padding:10px 12px;border-bottom:1px solid #f0f0f0;font-size:.88rem;vertical-align:top}}
tr.clickable{{cursor:pointer}}tr.clickable:hover{{background:#f8f9fa}}
.badge{{padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:600;color:#fff}}
.badge.pass{{background:#22c55e}}.badge.fail{{background:#ef4444}}.badge.skip{{background:#f59e0b}}
.module-col{{font-weight:500;color:#6366f1;font-size:.82rem}}
.name{{font-weight:500;max-width:280px;word-break:break-word}}
.reason{{max-width:350px;word-break:break-word;color:#555;font-size:.82rem}}
.markers{{font-size:.78rem;color:#888}}
.tb{{background:#1e1e2e;color:#cdd6f4;padding:14px;border-radius:8px;font-size:.78rem;overflow-x:auto;white-space:pre-wrap;word-break:break-word;max-height:400px;overflow-y:auto;margin:8px 0}}
.shot{{max-width:100%;border-radius:8px;margin-top:8px;border:1px solid #e5e7eb}}
.fail-card{{border-left:4px solid #ef4444;padding:16px;margin-bottom:16px;background:#fef2f2;border-radius:0 8px 8px 0}}
.fail-card h4{{margin-bottom:8px;color:#dc2626}}
.env-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}}
.env-grid div{{padding:8px 12px;background:#f8f9fa;border-radius:6px;font-size:.85rem}}
.env-grid strong{{color:#444}}
.filter-bar{{margin-bottom:16px;display:flex;gap:8px}}
.filter-bar button{{padding:6px 16px;border-radius:20px;border:1px solid #ddd;background:#fff;cursor:pointer;font-size:.82rem;font-weight:500}}
.filter-bar button.active{{background:#1a1a2e;color:#fff;border-color:#1a1a2e}}
footer{{text-align:center;color:#999;font-size:.78rem;margin-top:32px;padding:16px}}
</style></head><body>
<div class="container">
<h1>🧪 Boutiqaat Automation — Comprehensive Test Report</h1>
<p class="subtitle">Generated: {ts} &nbsp;|&nbsp; Website: <a href="https://www.boutiqaat.com" target="_blank">boutiqaat.com</a></p>

<div class="cards">
  <div class="card total"><div class="num">{total}</div><div class="lbl">Total Tests</div></div>
  <div class="card pass"><div class="num">{passed}</div><div class="lbl">Passed</div></div>
  <div class="card fail"><div class="num">{failed}</div><div class="lbl">Failed</div></div>
  <div class="card skip"><div class="num">{skipped}</div><div class="lbl">Skipped</div></div>
  <div class="card dur"><div class="num">{_format_duration(total_dur)}</div><div class="lbl">Duration</div></div>
  <div class="card rate"><div class="num">{rate}%</div><div class="lbl">Pass Rate</div></div>
</div>

<div class="bar">
  <div class="g" style="width:{passed/total*100 if total else 0}%"></div>
  <div class="r" style="width:{failed/total*100 if total else 0}%"></div>
  <div class="y" style="width:{skipped/total*100 if total else 0}%"></div>
</div>

{module_section}

{page_objects_section}

<div class="section">
  <h2>🖥️ Test Environment</h2>
  <div class="env-grid">
    <div><strong>OS:</strong> {platform.system()} {platform.release()}</div>
    <div><strong>Python:</strong> {platform.python_version()}</div>
    <div><strong>Machine:</strong> {platform.machine()}</div>
    <div><strong>Target:</strong> boutiqaat.com</div>
    <div><strong>Browser:</strong> Chromium (Playwright)</div>
    <div><strong>Run Date:</strong> {ts}</div>
  </div>
</div>

{failed_section}

<div class="section">
  <h2>📋 All Test Results</h2>
  <div class="filter-bar">
    <button class="active" onclick="filterRows('all',this)">All ({total})</button>
    <button onclick="filterRows('passed',this)">✅ Passed ({passed})</button>
    <button onclick="filterRows('failed',this)">❌ Failed ({failed})</button>
    <button onclick="filterRows('skipped',this)">⏭️ Skipped ({skipped})</button>
  </div>
  <table id="results">
    <thead><tr><th>#</th><th>Module</th><th>Test Name</th><th>Status</th><th>Duration</th><th>Markers</th><th>Reason / Error</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<footer>Boutiqaat Automation Framework — Playwright + Pytest &nbsp;|&nbsp; Report auto-generated</footer>
</div>
<script>
function toggle(i){{var e=document.getElementById('d'+i);e.style.display=e.style.display==='none'?'table-row':'none'}}
function filterRows(s,btn){{
  document.querySelectorAll('.filter-bar button').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  var rows=document.querySelectorAll('#results tbody tr');
  rows.forEach(r=>{{
    if(r.classList.contains('detail'))return;
    var badge=r.querySelector('.badge');
    if(!badge)return;
    var st=badge.textContent.trim().toLowerCase();
    r.style.display=(s==='all'||st===s)?'':'none';
    var next=r.nextElementSibling;
    if(next&&next.classList.contains('detail'))next.style.display='none';
  }});
}}
</script></body></html>"""

    out = os.path.join(REPORT_DIR, fname)
    Path(out).write_text(html, encoding="utf-8")

    latest = os.path.join(REPORT_DIR, "latest_report.html")
    Path(latest).write_text(html, encoding="utf-8")

    print(f"\n📊 HTML Report: {os.path.abspath(out)}")
    print(f"📊 Latest:      {os.path.abspath(latest)}")


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
