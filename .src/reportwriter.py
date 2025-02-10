import os
import logfire
from pydantic import BaseModel, Field
from pydantic_ai.models.groq import GroqModel
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from typing import List

load_dotenv()
logfire.configure()

# Model Setup
GROQ_API_KEY = os.getenv("GROQ_API_KE")
llama_model = GroqModel("llama-3.3-70b-versatile", api_key=GROQ_API_KEY)


# Define System Prompt Output Model
class SystemPrompt(BaseModel):
    """System prompt generated dynamically for the investment report agent."""

    prompt: str
    tags: List[str]


# Define Investment Report Output Model
# class InvestmentReport(BaseModel):
#     """AI-generated Investment Report."""
#     # report: List[str] = Field(..., description="List of AI-generated investment report sections.")

# Define Prompt Generator Agent
prompt_agent = Agent(
    model=llama_model,
    result_type=SystemPrompt,
    system_prompt=(
        "You an expert prompt writer. Create a system prompt to be used for an AI agent that will help a user based on the user's input. "
        "Must be very descriptive and include step by step instructions on how the agent can best answer user's question. Do not directly answer the question. "
        "Start with 'You are a helpful assistant specialized in...'. "
        "Include any relevant tags that will help the AI agent understand the context of the user's input. Add Disclosures at last"
    ),
)

# Define Investment Report Agent
investment_agent = Agent(
    model=llama_model,
    # result_type=InvestmentReport,
    system_prompt="Use the system prompt and tags provided to generate a helpful response to the user's info.",
)


# Dynamic System Prompt Injection
@investment_agent.system_prompt
def add_prompt(ctx: RunContext[SystemPrompt]) -> str:
    return ctx.deps.prompt


@investment_agent.system_prompt
def add_tags(ctx: RunContext[SystemPrompt]) -> str:
    return f"Use these tags: {', '.join(ctx.deps.tags)}"


# Collect User Input

user_input = """I want an deatiled Investment report for Me - {Rahul ,Short term(3years) investor , Highrisktype , wealthgenerationfocus}"""

user_data = """Portfolio Details:

{ Stock: HDFCBANK.NS  ,Shares Owned: 50 ,Purchase Price: ₹1300.00,Current Price: ₹1677.30 ,Allocation Percentage: 25% }   
{ Stock: TCS.NS  ,Shares Owned: 80 ,Purchase Price: ₹3000.00, Current Price: ₹4099.80 ,Allocation Percentage: 30% }  
{ Stock: RELIANCE.NS  ,Shares Owned: 30 ,Purchase Price: ₹1200.00 ,Current Price: ₹1253.05 ,Allocation Percentage: 15%  }
{ Stock: ITC.NS ,Shares Owned: 100 ,Purchase Price: ₹370.00 ,Current Price: ₹453.20,Allocation Percentage: 10% }
{ Stock: L&T.NS , Shares Owned: 25 , Purchase Price: ₹2400.00  ,Current Price: ₹2850.55 , Allocation Percentage: 10% }
{ Stock: SUNPHARMA.NS, Shares Owned: 40 ,Purchase Price: ₹850.00 , Current Price: ₹1085.35, Allocation Percentage: 10% } 
"""
user_info = user_input + "\n\n" + user_data

# Step 1: Generate Dynamic System Prompt
logfire.info("📝 Generating system prompt dynamically...")
system_prompt = prompt_agent.run_sync(user_input).data

# Save Generated Prompt to Markdown File
prompt_filename = "prompt2.md"
with open(prompt_filename, "w", encoding="utf-8") as prompt_file:
    prompt_file.write(f"# AI-Generated System Prompt\n\n")
    prompt_file.write(f"**Prompt:**\n\n{system_prompt.prompt}\n\n")
    prompt_file.write(
        f"**Tags:** {', '.join(system_prompt.tags) if system_prompt.tags else 'No Tags'}\n"
    )

logfire.info(f"✅ System Prompt saved to {prompt_filename}")

# Step 2: Use Generated Prompt to Generate Investment Report
logfire.info("📊 Generating AI Investment Report...")
investment_result = investment_agent.run_sync(user_info, deps=system_prompt)


# Save Generated Investment Report to Markdown File
report_filename = "report2.md"
with open(report_filename, "w", encoding="utf-8") as report_file:
    report_file.write(f"# AI-Generated Investment Report\n\n")
    report_file.write(investment_result.data)  # Saving raw AI-generated text

logfire.info(f"✅ Investment Report saved to {report_filename}")
