# Investment Report Generator (Approach 2 - Pydantic AI & Phi Agents)

## 📌 Project Overview

This **Investment Report Generator** is an AI-driven system that dynamically generates **personalized investment reports** using **Pydantic AI, Phi Data Agents, and Yahoo Finance (`yfinance`)**. It follows **Approach 2**, where a **two-agent system** creates structured prompts and generates AI-driven investment reports tailored to an investor’s portfolio.

## 🚀 Features

- **Two-Agent AI System**
  - **Prompt Generator Agent** → Creates structured prompts based on user portfolio data.
  - **Investment Analyst Agent** → Uses prompts + real-time data to generate reports.
- **Real-Time Stock Data Fetching** (`yfinance`)
- **Dynamic Prompt & Report Generation** (Saved as Markdown files `prompt.md` & `report.md`)
- **Automated AI Report Structuring**
- **Logfire UI Integration** to manage LLM interactions

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-repo/investment-report-generator.git
cd investment-report-generator
```

### 2️⃣ Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Set Up API Keys

Create a `.env` file in the project directory and add your Google Gemini API key:

```ini
GOOGLE_API_KEY=your_gemini_api_key
```

### 4️⃣ Run the Script

```bash
python investmentreportgenerator.py
```

## 📥 User Input Format

When you run the script, it will prompt you to enter:

1. **Stock tickers** (Comma-separated, e.g., `TCS.NS, RELIANCE.NS`)
2. **Shares held for each stock**
3. **Purchase price per share**
4. **Portfolio allocation percentage**
5. **Investment goal** (Growth, Retirement, Income)
6. **Risk tolerance** (Conservative, Moderate, Aggressive)
7. **Investment horizon** (Short-term, 5 years, 10+ years)

## 📊 Example Portfolio Input

```
Enter stock tickers: TCS.NS, RELIANCE.NS, HDFCBANK.NS, INFY.NS, ITC.NS
Enter number of shares held for TCS.NS: 50
Enter purchase price per share for TCS.NS: 3200
Enter portfolio allocation percentage for TCS.NS: 30
...
```

## 📄 Expected Output

### **Generated System Prompt**

![System Prompt](docs/prompt.png)

### **Generated Investment Report**

![Investment Report](docs/report1.png)
![Investment Report](docs/report2.png)

## 🛠️ Technologies Used

- **Python** 🐍
- **Pydantic AI** 🤖
- **Phi Agent Framework** 🔗
- **Google Gemini AI (via Phi Data)** 🧠
- **Yahoo Finance (`yfinance`)** 📈
- **Markdown for Report Formatting** 📄

## 🏗️ Future Enhancements

- ✅ **Stock News Sentiment Analysis**
- ✅ **Portfolio Risk Assessment**
- ✅ **Automated PDF Report Generation**

## 👨‍💻 Contributing

Want to improve this project? Feel free to submit PRs and suggestions!

## 📩 Contact

For questions or support, reach out via **Discord** or create an issue in the repository.

---

✅ **Now Run the Script and Generate Your Investment Report!** 🚀
