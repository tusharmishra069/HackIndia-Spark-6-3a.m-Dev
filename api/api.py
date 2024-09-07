from flask import Flask, request, jsonify
import ipfshttpclient
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Connect to IPFS
client = ipfshttpclient.connect('http://127.0.0.1:8080')
model_cid = "QmWvFgPaZAKfZu7hmG3Z7Fc7oGejewmUrw3bvXBLHbP8PW"

# Load the model from IPFS
def load_model_from_ipfs():
    client.get(model_cid, target='Google_stock_predict.h5')
    model = load_model('Google_stock_predict.h5')
    return model

model = load_model_from_ipfs()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = np.array(data['input']).reshape(-1, 1)
    
    sc = MinMaxScaler(feature_range=(0, 1))
    input_data = sc.fit_transform(input_data)

    # Make prediction
    prediction = model.predict(input_data)
    predicted_price = sc.inverse_transform(prediction)

    return jsonify({'predicted_price': predicted_price.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
