# Building an Automated Trading System; Part 1
![Image](https://uint32.xyz/_next/image?url=%2Fstatic%2Fimages%2Fmonkeys.webp&w=3840&q=75)

## Overview
This project explores building automated trading systems using Amazon Web Services (AWS). Part 1 covers the initial setup, strategy development, and model training.

> **Disclaimer:** This project is educational and not intended as financial advice.

## Part 1: Building the Trading System

### Project Highlights
1. **Trading Strategy**: The goal is to identify small-cap tokens with potential breakout trends using machine learning.
2. **Model**: A RandomForest model is used to identify price breakouts based on technical indicators like RSI, MACD, VWRSI, and others.
3. **Data Collection**: Using AWS S3, Glue, and Athena, price and volume data are collected and processed.
5. **Training & Evaluation**: Models are trained and evaluated using accuracy, precision, recall, F1 score, and AUC-ROC.

### Getting Started

1. **Prerequisites**
   - Python 3.x
   - An AWS Account
   - Relevant AWS services (S3, Glue, Athena, Lambda)

2. **Installation**
   - Clone the repository: `git clone https://github.com/uint32xyz/automated-trading-system-part-1.git`
   - Install dependencies: `pip install -r requirements.txt`

3. **Setup AWS Services**
   - Configure your S3 bucket, Glue crawler, and Athena.
   - Update the provided AWS Lambda function with your S3 bucket name and API key.
   - Modify the Lambda trigger schedule as required.

4. **Data Processing**
   - Set up an hourly Lambda function to fetch the latest data.
   - Execute Glue crawlers to map S3 data for SQL queries.
   - Use Athena queries to refine data and calculate technical indicators.

5. **Model Training**
   - Run the Python scripts to train the RandomForest model.
   - Evaluate the model performance using the included metrics.

### Features
- **Multi-Token Strategy**: Analyzes multiple tokens to predict breakouts.
- **Single-Token Strategy**: Focuses on individual tokens for a refined approach.
- **Technical Indicators**: Incorporates over 10 indicators, including RSI, MACD, and VWRSI.

### Results
- **Multi-Token Strategy**: Moderate performance with accuracy of 0.62 and AUC-ROC of 0.62.
- **Single-Token Strategy (SOL)**: High performance with accuracy of 0.91 and AUC-ROC of 0.89.

## Comprehensive Lesson on How to Build the System
For detailed instructions and a comprehensive lesson on how to build this system, check out the full article [here](https://uint32.xyz/writing/building-an-automated-trading-system).

### Part 2 (Coming Soon)
- Deploying the model to the cloud using Docker containers.
- Automating predictions and trade execution.
- Setting up email alerts.

## Resources
- [AWS Cloud Technical Essentials](https://www.aws.com)
- [Architecting Solutions on AWS](https://aws.amazon.com/architecture/)
- [DeepLearning.AI](https://www.deeplearning.ai/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details..


