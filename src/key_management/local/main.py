import requests
import secrets
import hashlib
import base64

# -----------------------------
# PART 1: Fetch from KME API
# -----------------------------
def fetch_qkd_key(api_url, token=None, key_id=None):
    headers = {
        "Accept": "application/json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    if key_id:
        # Fetch specific key
        url = f"{api_url}/qkd/keys?key_id={key_id}"
    else:
        # Request a new key
        url = f"{api_url}/qkd/keys/new"

    try:
        response = requests.get(url, headers=headers, verify=False)  # verify=False for local testing
        response.raise_for_status()
        key_info = response.json()

        print("\n[From KME]")
        print(f"Key ID: {key_info['key_id']}")
        print(f"Key (base64): {key_info['key_material']}")
        print(f"Length: {key_info['length_bits']} bits")

        # Convert key material into raw bytes
        raw_key = base64.b64decode(key_info["key_material"].split(":")[1])
        return key_info["key_id"], raw_key

    except Exception as e:
        print("⚠️ Could not reach KME, using simulated key instead.")
        key_id = "SIMULATED-KEY-001"
        raw_key = secrets.token_bytes(32)  # 256-bit key
        return key_id, raw_key

# -----------------------------
# PART 2: Simulate QKD post-processing
# -----------------------------
def qkd_post_processing(raw_alice_bits, raw_bob_bits):
    print("\n[QKD Simulation]")

    # Step 1: Sifting (keep only positions where bases match)
    sifted = [a for a, b in zip(raw_alice_bits, raw_bob_bits) if a is not None and b is not None and a == b]
    print(f"Sifted length: {len(sifted)} bits")

    # Step 2: Error correction (simulate by forcing them equal)
    corrected = sifted  # in real QKD use Cascade/LDPC
    print(f"Corrected length: {len(corrected)} bits")

    # Step 3: Privacy amplification (hash down to 256-bit key)
    key_bytes = "".join(map(str, corrected)).encode()
    final_key = hashlib.sha256(key_bytes).digest()
    print(f"Final key (hex): {final_key.hex()}")

    return final_key

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    # Local mock KME URL
    API_URL = "http://127.0.0.1:5000/api/v1"
    TOKEN = None  # No auth required for mock server

    # Fetch quantum key
    key_id, kme_key = fetch_qkd_key(API_URL, TOKEN)
    print(f"\nUsing key ID: {key_id}")
    print(f"Key bytes (hex): {kme_key.hex()}")

    # Simulate QKD post-processing
    alice_bits = [secrets.choice([0, 1]) for _ in range(128)]
    bob_bits   = alice_bits[:]  # simulate perfect channel
    final_key = qkd_post_processing(alice_bits, bob_bits)

    print("\n✅ Done.")
