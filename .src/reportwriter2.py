import os
import logfire
import yfinance as yf
import datetime
from typing import List, Dict
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pydantic_ai.models.groq import GroqModel

load_dotenv()

# Configure Logfire for AI Monitoring
logfire.configure()


# Portfolio Stock Structure
class PortfolioStock(BaseModel):
    """Structure for individual stock details in the user's portfolio."""

    stock_symbol: str = Field(
        ..., description="Stock ticker symbol (e.g., RELIANCE.NS)"
    )
    shares_owned: int = Field(..., description="Number of shares owned")
    purchase_price: float = Field(..., description="Purchase price per share")
    current_price: float = Field(..., description="Latest market price per share")
    allocation_percent: float = Field(
        ..., description="Portfolio allocation percentage"
    )
    profit_loss: float = Field(
        ..., description="Total profit/loss from this stock investment"
    )
    return_percentage: float = Field(
        ..., description="Percentage return on investment for this stock"
    )


class StockProfit(BaseModel):
    """Structure for stock profit details."""

    stock_symbol: str = Field(..., description="Stock ticker symbol")
    total_profit: float = Field(..., description="Total profit or loss from this stock")


# Investment Report Structure
class InvestmentReport(BaseModel):
    """AI-generated investment report containing portfolio analysis & recommendations."""

    investor_name: str = Field(..., description="Investor's full name")
    investment_goal: str = Field(
        ..., description="Investment objective (e.g., long-term growth, income)"
    )
    risk_profile: str = Field(
        ...,
        description="Investor's risk tolerance (e.g., conservative, moderate, aggressive)",
    )
    stocks_profit: List[StockProfit] = Field(
        ..., description=" provide Profit analysis for stocks"
    )
    portfolio_analysis: List[PortfolioStock] = Field(
        ..., description="do the Stock performance analysis"
    )
    portfolio_overview: List[str] = Field(
        ..., description=" give a  detailed summary of portfolio health"
    )
    risk_analysis: List[str] = Field(
        ...,
        description="do theRisk assessment based on diversification, volatility, and allocation",
    )
    investment_recommendations: List[str] = Field(
        ..., description="AI-generated investment suggestions"
    )
    benchmark_comparison: List[str] = Field(
        ..., description="Performance of portfolio compared to market benchmarks"
    )
    disclosure: List[str] = Field(
        ..., description="financial disclaimer mentioning SploreAI"
    )


# Model Setup
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# gemini_model = GeminiModel(model_name="gemini-1.5-pro-latest", api_key=GEMINI_API_KEY)


GROQ_API_KEY = os.getenv("GROQ_API_KE")

llama_model = GroqModel("llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

agent = Agent(
    model=llama_model,
    result_type=InvestmentReport,
    system_prompt=(
        "You are a Senior Finance Analyst at SploreAI India. Generate a structured investment report "
        "using the users portfolio details, investment goals, risk profile, and market conditions. "
        "Ensure the report is tailored to different client profiles."
    ),
)


# Fetch Latest Stock Prices with Date Handling
def get_latest_stock_price(stock_symbol):
    """
    Fetches the latest available stock price using the most recent trading day's data.
    Handles weekends & holidays by using the last available closing price.
    """
    today = datetime.date.today()
    ticker = yf.Ticker(stock_symbol)

    hist_data = ticker.history(start=today - datetime.timedelta(days=7), end=today)

    if hist_data.empty:
        return None  # Handle case when no data is available

    # Get the latest available closing price
    latest_price = hist_data["Close"].dropna().iloc[-1]
    return round(latest_price, 2)


# Collect User Input for Portfolio
def collect_user_portfolio():
    investor_name = input("Enter your name: ")
    investment_goal = input(
        "Enter your investment goal (e.g., Long-term Growth, Income, Retirement, etc.): "
    )
    risk_profile = input(
        "Enter your risk profile (Conservative, Moderate, Aggressive): "
    )

    portfolio = []
    num_stocks = int(input("How many different stocks do you own? "))

    for i in range(num_stocks):
        print(f"\nEntering details for Stock {i+1}:")
        stock_symbol = (
            input("Stock symbol (e.g., RELIANCE.NS, HDFCBANK.NS): ").strip().upper()
        )
        shares_owned = int(input("Number of shares owned: "))
        purchase_price = float(input("Purchase price per share: "))
        allocation_percent = float(
            input("Portfolio allocation percentage for this stock: ")
        )

        # Fetch latest stock price with date handling
        current_price = get_latest_stock_price(stock_symbol)

        # Calculate profit/loss and return percentage
        if current_price is not None:
            profit_loss = (current_price - purchase_price) * shares_owned
            return_percentage = (
                (current_price - purchase_price) / purchase_price
            ) * 100
        else:
            profit_loss = 0.0  # Default to zero if no data is available
            return_percentage = 0.0

        portfolio.append(
            PortfolioStock(
                stock_symbol=stock_symbol,
                shares_owned=shares_owned,
                purchase_price=purchase_price,
                current_price=current_price if current_price else 0.0,
                profit_loss=profit_loss,
                allocation_percent=allocation_percent,
                return_percentage=return_percentage,
            )
        )

    return {
        "investor_name": investor_name,
        "investment_goal": investment_goal,
        "risk_profile": risk_profile,
        "portfolio": portfolio,
    }


# Gather User Data
user_portfolio = collect_user_portfolio()


#  Improved System Prompt
@agent.system_prompt
def add_user_portfolio_details(ctx: RunContext[Dict]) -> str:
    """
    Ensures AI properly uses user portfolio details.
    """
    return f"""
    Investor Name: {ctx.deps['investor_name']}
    Investment Goal: {ctx.deps['investment_goal']}
    Risk Profile: {ctx.deps['risk_profile']}
    
    **Portfolio Breakdown:**
    {ctx.deps['portfolio']}
    
    - Structure **portfolio_analysis** as a list of objects containing:
      - Stock Symbol
      - Shares Owned
      - Purchase Price
      - Current Price
      - Allocation Percentage
      - Profit/Loss Calculation
      - Return Percentage
    - Compare the portfolio’s performance against benchmark indices.
    - Provide detailed investment recommendations based on performance.
    """


# System Prompt: Add Report Tags
@agent.system_prompt
def add_tags_for_report(ctx: RunContext[Dict]) -> str:
    return f"""
    Use the following structured format for the investment report:
    - Portfolio Overview
    - Portfolio Performance
    - Risk Analysis
    - Profit & Return Calculation
    - Investment Recommendations
    - Benchmark Comparison
    - Future Outlook

    **Ensure that portfolio_analysis is structured as a list of objects** instead of a dictionary.
    """


# Save AI Report to Markdown File
def save_report_to_markdown(report: InvestmentReport, filename="investment_report3.md"):
    """
    Saves the AI-generated investment report into a markdown (.md) file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"# 📊 AI-Generated Investment Report\n")
        file.write(f"**Investor Name:** {report.investor_name}\n\n")
        file.write(f"**Investment Goal:** {report.investment_goal}\n\n")
        file.write(f"**Risk Profile:** {report.risk_profile}\n\n")

        file.write("## 📌 Portfolio Overview\n")
        for item in report.portfolio_overview:
            file.write(f"- {item}\n")

        file.write("\n## 📈 Portfolio Performance\n")
        for stock in report.portfolio_analysis:
            file.write(f"- **{stock.stock_symbol}**\n")
            file.write(f"  - Shares Owned: {stock.shares_owned}\n")
            file.write(f"  - Purchase Price: ₹{stock.purchase_price}\n")
            file.write(f"  - Current Price: ₹{stock.current_price}\n")
            file.write(f"  - Allocation: {stock.allocation_percent}%\n")
            file.write(f"  - Profit/Loss: ₹{stock.profit_loss}\n")
            file.write(f"  - Return Percentage: {stock.return_percentage}%\n\n")

        file.write("\n## 📊 Profit Breakdown\n")
        for profit in report.stocks_profit:
            file.write(f"- **{profit.stock_symbol}:** ₹{profit.total_profit}\n")

        file.write("\n## ⚠️ Risk Analysis\n")
        for risk in report.risk_analysis:
            file.write(f"- {risk}\n")

        file.write("\n## 💡 Investment Recommendations\n")
        for recommendation in report.investment_recommendations:
            file.write(f"- {recommendation}\n")

        file.write("\n## 📏 Benchmark Comparison\n")
        for benchmark in report.benchmark_comparison:
            file.write(f"- {benchmark}\n")

        file.write("\n## 🔔 Disclaimer & Disclosure\n")
        for disclosure in report.disclosure:
            file.write(f"- {disclosure}\n")

    print(f"✅ Investment report saved successfully as '{filename}'")


with logfire.span("Generating AI Investment Report") as span:
    try:
        result = agent.run_sync(
            "Analyze this investor's portfolio and provide investment recommendations.",
            deps=user_portfolio,
        )
        span.set_attribute("AI Result", result.data)
        logfire.info("AI Result:", result=result.data)

        # ✅ Save AI report to Markdown file
        save_report_to_markdown(result.data)

    except Exception as e:
        logfire.error(f"AI Execution Error: {e}")
