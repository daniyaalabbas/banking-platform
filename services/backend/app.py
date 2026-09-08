from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "banking-backend"
    })

@app.route("/api/account")
def account():
    return jsonify({
        "account": "ACC-1001",
        "balance": 50000,
        "currency": "INR"
    })

@app.route("/api/payment", methods=["POST"])
def payment():
    return jsonify({
        "status": "SUCCESS",
        "transaction_id": "TXN-10001"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
