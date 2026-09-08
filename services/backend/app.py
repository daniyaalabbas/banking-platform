from flask import Flask, jsonify, render_template_string
import os
import socket

app = Flask(__name__)

ACCOUNT_DATA = {
    "account_number": "IN91-HDFC-0019284711",
    "account_holder": "Daniyaal Abbas",
    "account_type": "Corporate Current Account",
    "currency": "INR",
    "available_balance": "50,000.00",
    "ledger_balance": "52,000.00",
    "status": "Active / Verified"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Global Core Banking Portal</title>
  <style>
    :root {
      --bg: #0b132b;
      --card-bg: #1c2541;
      --accent: #48cae4;
      --text: #ffffff;
      --muted: #8d99ae;
      --success: #06d6a0;
      --border: #3a506b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background-color: var(--bg); color: var(--text); display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
    .dashboard { width: 100%; max-width: 650px; background: var(--card-bg); border-radius: 16px; border: 1px solid var(--border); box-shadow: 0 20px 40px rgba(0,0,0,0.5); overflow: hidden; }
    .header { background: #0f1a36; padding: 24px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
    .logo { font-size: 20px; font-weight: 700; color: var(--accent); letter-spacing: 0.5px; }
    .badge { background: rgba(6, 214, 160, 0.15); color: var(--success); font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 20px; border: 1px solid var(--success); }
    .content { padding: 28px; }
    .label { font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
    .balance-box { background: rgba(72, 202, 228, 0.05); border: 1px dashed var(--accent); border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 24px; }
    .balance-amount { font-size: 38px; font-weight: 800; color: var(--text); margin-top: 4px; }
    .currency { color: var(--accent); font-size: 24px; font-weight: 600; margin-right: 4px; }
    .details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
    .detail-card { background: #131b31; padding: 14px; border-radius: 8px; border: 1px solid #23314f; }
    .detail-val { font-size: 14px; font-weight: 600; margin-top: 2px; }
    .telemetry { background: #0c1122; border-radius: 8px; padding: 14px; border: 1px solid #23314f; font-size: 12px; color: var(--muted); }
    .telemetry span { color: var(--accent); font-family: monospace; }
  </style>
</head>
<body>
  <div class="dashboard">
    <div class="header">
      <div class="logo">⚡ SecureCore Bank</div>
      <div class="badge">● Live Production TLS</div>
    </div>
    <div class="content">
      <div class="balance-box">
        <div class="label">Available Settlement Balance</div>
        <div class="balance-amount"><span class="currency">₹</span>{{ account.available_balance }}</div>
      </div>
      <div class="details-grid">
        <div class="detail-card">
          <div class="label">Account Holder</div>
          <div class="detail-val">{{ account.account_holder }}</div>
        </div>
        <div class="detail-card">
          <div class="label">Account Number</div>
          <div class="detail-val">{{ account.account_number }}</div>
        </div>
        <div class="detail-card">
          <div class="label">Ledger Balance</div>
          <div class="detail-val">₹{{ account.ledger_balance }}</div>
        </div>
        <div class="detail-card">
          <div class="label">Account Status</div>
          <div class="detail-val" style="color: var(--success);">{{ account.status }}</div>
        </div>
      </div>
      <div class="telemetry">
        Served by Pod: <span>{{ hostname }}</span> &nbsp;|&nbsp; DB Host: <span>{{ db_host }}</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

@app.route('/')
def home():
    hostname = socket.gethostname()
    db_host = os.getenv("DB_HOST", "banking-db.daniyaalabbas-dev.svc.cluster.local")
    return render_template_string(HTML_TEMPLATE, account=ACCOUNT_DATA, hostname=hostname, db_host=db_host)

@app.route('/health')
def health():
    return jsonify(status="UP", service="banking-backend"), 200

@app.route('/api/balance')
def balance():
    return jsonify(ACCOUNT_DATA), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
