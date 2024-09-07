// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PricePrediction {
    address public owner;
    uint256 public predictedPrice;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    function updatePredictedPrice(uint256 _price) public onlyOwner {
        predictedPrice = _price;
    }
}
