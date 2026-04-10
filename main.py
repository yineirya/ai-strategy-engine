import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from agents import llm, governance_agent, analyst_agent, ProcessDesign, ProcessStep
from finance import ValueModeler
from agents import ProcessDesign

load_dotenv()

# 1. Define the Shared State
class StrategyState(TypedDict):
    business_process: str
    proposed_design: List[dict]
    critique_history: List[str]
    is_ready: bool
    iterations: int
    value_hypothesis: str

# 2. Node: The Architect
def architect_node(state: StrategyState):
    print("--- ARCHITECT IS DESIGNING ---")
    
    system_message = (
        "You are an IBM Strategy Consultant. Deconstruct the process into "
        "technical steps using Zero-based design principles."
    )
    
    user_input = f"Process: {state['business_process']}. Critique: {state.get('critique_history', 'None')}"
    
    # Use ProcessDesign (the container) instead of List[ProcessStep]
    structured_llm = llm.with_structured_output(ProcessDesign)
    
    response = structured_llm.invoke([
        ("system", system_message),
        ("human", user_input)
    ])
    
    # Extract the steps from the container and convert to dicts
    return {
    "proposed_design": [step.model_dump() for step in response.steps],
    "iterations": state.get("iterations", 0) + 1
}
def value_node(state: StrategyState):
    print("--- CALCULATING VALUE CREATION ---")
    modeler = ValueModeler()
    # We'll assume a volume of 1,000 requests per month for the demo
    stats = modeler.calculate_roi(state["proposed_design"], 1000)
    return {"value_hypothesis": f"Projected ROI: {stats['net_roi']}"}
def build_buy_node(state: StrategyState):
    print("--- EVALUATING BUILD VS BUY ---")
    
    prompt = (
        "Based on this design, should we build a custom solution or buy an enterprise platform? "
        "Consider speed-to-market and total cost of ownership. "
        f"Design: {state['proposed_design']}"
    )
    
    decision = analyst_agent.invoke(prompt)
    
    report = f"Decision: {decision.decision} | Rationale: {decision.rationale} | Platform: {decision.recommended_platform}"
    # We will store this in the value_hypothesis to show in the final output
    return {"value_hypothesis": state["value_hypothesis"] + "\n" + report}

# 3. Node: The Governance Critic
def governance_node(state: StrategyState):
    print("--- GOVERNANCE IS EVALUATING RISK ---")
    design = state["proposed_design"]
    
    # We call the structured output agent we built in the last step
    assessment = governance_agent.invoke(f"Evaluate this design for risk: {design}")
    
    return {
        "is_ready": assessment.is_safe_to_proceed,
        "critique_history": [assessment.mitigation_strategy]
    }

# 4. Conditional Logic: The "Decision Point"
def should_continue(state: StrategyState):
    if state["is_ready"] or state["iterations"] >= 3:
        return "value_analysis"
    return "rework"

# 5. Assemble the Graph
workflow = StateGraph(StrategyState)

workflow.add_node("architect", architect_node)
workflow.add_node("governance", governance_node)
workflow.add_node("value_engine", value_node)

workflow.set_entry_point("architect")

# The Critique Loop
workflow.add_edge("architect", "governance")
workflow.add_conditional_edges(
    "governance",
    should_continue,
    {
        "rework": "architect", # Loop back to fix design
	"value_analysis": "value_engine"    }
)
# 1. Add the node
workflow.add_node("build_buy_analyst", build_buy_node)

# 2. Change the final edge
# Old: workflow.add_edge("value_engine", END)
workflow.add_edge("value_engine", "build_buy_analyst") # New path
workflow.add_edge("build_buy_analyst", END)           # Final stop

workflow.add_edge("value_engine", END)
app = workflow.compile()

if __name__ == "__main__":
    inputs = {
        "business_process": "Manual review of customer refund requests for a retail chain.",
        "iterations": 0
    }
    for output in app.stream(inputs):
        print(output)