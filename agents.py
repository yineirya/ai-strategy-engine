# agents.py

import os
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# --- ADD THIS CLASS BELOW ---
class ProcessStep(BaseModel):
    step_name: str = Field(description="Name of the process step")
    is_agentic: bool = Field(description="True if it requires complex reasoning")
    strategy: str = Field(description="The AI-native approach for this step")
# ----------------------------
class BuildVsBuy(BaseModel):
    decision: str = Field(description="'Build', 'Buy', or 'Enhance'")
    rationale: str = Field(description="The strategic reason for this choice")
    recommended_platform: str = Field(description="e.g., IBM watsonx, Custom Python, or AWS Bedrock")

# This is the line your error was complaining about!
analyst_agent = llm.with_structured_output(BuildVsBuy)
class RiskAssessment(BaseModel):
    risk_score: int
    governance_flags: List[str]
    mitigation_strategy: str
    is_safe_to_proceed: bool
# agents.py

# ... existing code ...

class ProcessDesign(BaseModel):
    """Container for the full list of process steps."""
    steps: List[ProcessStep] = Field(description="A list of technical steps for the workflow")

# No change needed to governance_agent
governance_agent = llm.with_structured_output(RiskAssessment)