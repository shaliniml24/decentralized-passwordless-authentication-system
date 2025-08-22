from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
import json, uuid

app = Flask(__name__)
CORS(app)

# -----------------------------
# Blockchain connection
# -----------------------------
w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/<YOUR_INFURA_KEY>"))


# Your deployed contract address (from Hardhat deployment logs)
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# Load ABI from compiled contract JSON
with open("contracts/DIDRegistry.json") as f:
    contract_json = json.load(f)
    contract_abi = contract_json["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# -----------------------------
# Nonce store (in-memory for demo)
# -----------------------------
nonces = {}

@app.route("/api/auth/nonce", methods=["POST"])
def get_nonce():
    """Generate and return a nonce for a given wallet address"""
    data = request.json
    address = data["address"]

    nonce = str(uuid.uuid4())
    nonces[address.lower()] = nonce

    return jsonify({"nonce": nonce})


@app.route("/api/auth/verify", methods=["POST"])
def verify_signature():
    """Verify the wallet signature of the nonce"""
    from eth_account.messages import encode_defunct
    from eth_account import Account

    data = request.json
    address = data["address"]
    signature = data["signature"]
    nonce = data["nonce"]

    expected_nonce = nonces.get(address.lower())
    if expected_nonce != nonce:
        return jsonify({"error": "Invalid nonce"}), 400

    message = encode_defunct(text=nonce)
    recovered_address = Account.recover_message(message, signature=signature)

    if recovered_address.lower() == address.lower():
        return jsonify({"success": True, "address": recovered_address})
    else:
        return jsonify({"error": "Signature verification failed"}), 400


# -----------------------------
# DID Registry endpoints
# -----------------------------
@app.route("/api/did/register", methods=["POST"])
def register_did():
    """Register a DID on the blockchain"""
    data = request.json
    address = data["address"]
    did = data["did"]

    try:
        tx = contract.functions.registerDID(did).build_transaction({
            "from": address,
            "nonce": w3.eth.get_transaction_count(address),
            "gas": 3000000,
            "gasPrice": w3.to_wei("20", "gwei"),
        })

        # For demo we sign with Hardhat's first account (replace with private key mgmt in prod)
        PRIVATE_KEY = " 0xd5fB5F201db6A9dCD3DAECDFf805211501d4F53b"
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({"success": True, "txHash": tx_hash.hex()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/did/get", methods=["POST"])
def get_did():
    """Fetch DID for an address"""
    data = request.json
    address = data["address"]

    try:
        did = contract.functions.getDID(address).call()
        return jsonify({"did": did})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
