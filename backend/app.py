from flask import Flask, request, jsonify
from web3 import Web3
import requests

app = Flask(__name__)

# Initialize Web3 and contract
infura_url = 'https://mainnet.infura.io/v3/5205460d35d8456cbdf517ec0a73fa15'
web3 = Web3(Web3.HTTPProvider(infura_url))
contract_address = 'address dalna hai'
contract_abi = [ {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "predictedPrice",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_price",
          "type": "uint256"
        }
      ],
      "name": "updatePredictedPrice",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/api/predict', methods=['GET'])
def get_prediction():
    try:
        # Fetch prediction from the model API
        response = requests.get('http://localhost:4000/predict')
        data = response.json()
        predicted_price = data.get('predicted_price')
        return jsonify({'predicted_price': predicted_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/updatePrice', methods=['POST'])
def update_price():
    data = request.json
    price = data.get('price')
    
    if price is None:
        return jsonify({'error': 'Price is required'}), 400

    # Get the account to send the transaction from
    account = 'YOUR_ACCOUNT_ADDRESS'
    private_key = 'YOUR_PRIVATE_KEY'
    
    try:
        # Build the transaction
        txn = contract.functions.updatePredictedPrice(price).buildTransaction({
            'from': account,
            'gas': 2000000,
            'gasPrice': web3.toWei('1', 'gwei'),
            'nonce': web3.eth.getTransactionCount(account),
        })
        
        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
        
        # Send the transaction
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        web3.eth.waitForTransactionReceipt(txn_hash)
        return jsonify({'status': 'Price updated on blockchain'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)
