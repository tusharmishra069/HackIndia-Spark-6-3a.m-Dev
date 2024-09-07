// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract PredictionMarket {
    address public owner;
    uint public predictionFee;

    constructor() {
        owner = msg.sender;
        predictionFee = 0.01 ether;
    }

    struct Prediction {
        address predictor;
        uint amount;
        uint predictedValue;
        bool resultFetched;
        uint actualValue;
    }

    Prediction[] public predictions;

    event NewPrediction(address indexed predictor, uint amount, uint predictedValue);
    event PredictionResultFetched(uint indexed predictionId, uint actualValue);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    function makePrediction(uint predictedValue) public payable {
        require(msg.value >= predictionFee, "Insufficient fee");
        predictions.push(Prediction(msg.sender, msg.value, predictedValue, false, 0));
        emit NewPrediction(msg.sender, msg.value, predictedValue);
    }

    function fetchPredictionResult(uint predictionId, uint actualValue) public onlyOwner {
        require(!predictions[predictionId].resultFetched, "Result already fetched");
        predictions[predictionId].actualValue = actualValue;
        predictions[predictionId].resultFetched = true;
        emit PredictionResultFetched(predictionId, actualValue);
    }

    function getPrediction(uint predictionId) public view returns (address, uint, uint, bool, uint) {
        Prediction memory p = predictions[predictionId];
        return (p.predictor, p.amount, p.predictedValue, p.resultFetched, p.actualValue);
    }

    function withdraw() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
}
