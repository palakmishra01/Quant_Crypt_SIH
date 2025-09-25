from flask import Flask, jsonify, request
import base64
import secrets
import datetime

app = Flask(__name__)

@app.route("/api/v1/qkd/keys/new", methods=["GET"])
def new_key():
    # Generate a random 256-bit key
    key_bytes = secrets.token_bytes(32)
    key_b64 = "base64:" + base64.b64encode(key_bytes).decode()

    # Generate a fake key_id
    key_id = "QK-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    return jsonify({
        "key_id": key_id,
        "key_material": key_b64,
        "length_bits": 256,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "usage": "test",
        "lifetime_seconds": 3600
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
