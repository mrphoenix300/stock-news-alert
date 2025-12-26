

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Twilio](https://img.shields.io/badge/API-Twilio-red)
![AlphaVantage](https://img.shields.io/badge/Data-AlphaVantage-orange)

An automated Python script designed to monitor stock market volatility and deliver real-time intelligence via SMS. 

> **Note:** This project is part of my journey learning to work with APIs, manage environment variables, and automate real-world tasks with Python.

## 📋 Project Overview

This system monitors the daily stock performance of a target company (default: Tesla/TSLA). It calculates the percentage difference between the closing price of the last two trading days. 

If a significant fluctuation is detected (defined as a **>5% increase or decrease**), the system triggers an alert sequence:
1.  **Data Retrieval:** Fetches the top 3 relevant news articles via NewsAPI.
2.  **Notification:** Constructs and dispatches an SMS via Twilio containing the stock movement percentage and news headlines/briefs.

## ⚙️ Technical Architecture

### Core Libraries
* **`requests`**: Handles HTTP GET requests to external API endpoints.
* **`twilio`**: Manages the SMS dispatch client.
* **`os`**: Implements secure environment variable retrieval.

### Data Providers
* **Alpha Vantage**: Provides Time Series Daily stock data (JSON).
* **NewsAPI**: Provides query-based article retrieval (JSON).

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mrphoenix300/stock-news-alert.git
cd stock-news-alert
```
### 2. Create Virtual EnvironmentIt is recommended to use a virtual environment to manage dependencies.
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```
### 3. Install Dependencies
* requests
* twilio
### 4. Configuration
Security is a priority for this project. API keys are not hardcoded. You must export the following environment variables in your terminal or use a .env file. 
| Variable | Description |
| :--- | :--- |
| `ACCOUNT_SID` | Twilio Account SID |
| `AUTH_TOKEN` | Twilio Authentication Token |
| `API_KEY1` | Alpha Vantage API Key |
| `API_KEY2` | NewsAPI Key |
| `TEMP_NUMBER_NUMBER` | Phone number of receiver (virtual) |
| `MESSAGING_SERVICE_SID` | ID of this conversation (SENDER -> RECEIVER) |
## 🚀 Usage
Execute the script from the root directory:
```bash
python main.py
```
Expected Output (Console):If the threshold is met, the script will print the percentage change and the status of the sent message.
```
-5.234
queued
queued
queued
```
**Expected Output (SMS)**: \
&emsp;TSLA: 🔻5%Headline: Why Tesla Stock Dropped Today...Brief: Shares of the EV maker slid following...
## 💡 Key Competencies Demonstrated
This project highlights the following technical skills:
* **RESTful API Consumption**: Constructing parameterized queries and handling JSON responses from multiple distinct providers.
* **Data Processing**: Parsing complex nested dictionaries and performing list slicing/comprehensions to extract relevant metrics.
* **Security Best Practices**: Utilizing os.environ to decouple sensitive credentials (API Keys/Auth Tokens) from the codebase.
* **Algorithmic Logic**: Implementing conditional control flow based on mathematical thresholds (volatility > 5%).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Created by $$Mr. Phoenix300$$