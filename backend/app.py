from flask import Flask, request, jsonify
from web3 import Web3
import requests

app = Flask(__name__)

# Initialize Web3 and contract
infura_url = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'
web3 = Web3(Web3.HTTPProvider(infura_url))
contract_address = 'address dalna hai'
contract_abi = [ 0x608060405234801561000f575f80fd5b50335f806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506102eb8061005c5f395ff3fe608060405234801561000f575f80fd5b506004361061003f575f3560e01c80638da5cb5b14610043578063a27afd6714610061578063d9a7713c1461007f575b5f80fd5b61004b61009b565b604051610058919061019a565b60405180910390f35b6100696100be565b60405161007691906101cb565b60405180910390f35b61009960048036038101906100949190610212565b6100c4565b005b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60015481565b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610151576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161014890610297565b60405180910390fd5b8060018190555050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f6101848261015b565b9050919050565b6101948161017a565b82525050565b5f6020820190506101ad5f83018461018b565b92915050565b5f819050919050565b6101c5816101b3565b82525050565b5f6020820190506101de5f8301846101bc565b92915050565b5f80fd5b6101f1816101b3565b81146101fb575f80fd5b50565b5f8135905061020c816101e8565b92915050565b5f60208284031215610227576102266101e4565b5b5f610234848285016101fe565b91505092915050565b5f82825260208201905092915050565b7f4e6f7420617574686f72697a65640000000000000000000000000000000000005f82015250565b5f610281600e8361023d565b915061028c8261024d565b602082019050919050565b5f6020820190508181035f8301526102ae81610275565b905091905056fea2646970667358221220fc81dd3cf27efcfb084891c031fad9bc17e08280a577242a05926a63d532122564736f6c63430008150033 ]
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
