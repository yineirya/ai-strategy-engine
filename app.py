import streamlit as st
from main import app # Import the compiled graph from your main.py

st.set_page_config(page_title="AI Strategy Engine", layout="wide")

st.title("🚀 Enterprise AI Strategy & Value Engine")
st.subheader("Transform legacy processes into AI-native workflows")

# Sidebar for inputs
with st.sidebar:
    st.header("Consultation Parameters")
    process_input = st.text_area("Describe the manual business process:", 
                                 placeholder="e.g., Manual review of employee expense reports...")
    volume = st.number_input("Monthly Transaction Volume:", value=1000)
    run_button = st.button("Generate Strategy")

if run_button and process_input:
    with st.spinner("Orchestrating Agents..."):
        # Run your LangGraph
        inputs = {"business_process": process_input, "iterations": 0}
        final_state = app.invoke(inputs)
        
        # Display results in Tabs
        tab1, tab2, tab3 = st.tabs(["📋 Process Design", "💰 Value Analysis", "🛡️ Governance"])
        
        with tab1:
            st.write("### AI-Native Workflow Design")
            st.table(final_state["proposed_design"])
            
            # Add a visual roadmap
            st.write("### Implementation Roadmap")
            roadmap_code = "graph LR\n"
            for i, step in enumerate(final_state["proposed_design"]):
                name = step['step_name'].replace(" ", "_")
                roadmap_code += f"    {name} --> "
            roadmap_code += "DONE"
            
            st.code(roadmap_code, language="mermaid")
            st.caption("Copy this code into a Mermaid Live Editor to visualize the full enterprise architecture.")
            
        with tab2:
            st.write("### Financial ROI & Value Hypothesis")
            # Extra safety: check if the string has a '$' before splitting
            if "$" in final_state['value_hypothesis']:
                savings = f"${final_state['value_hypothesis'].split('$')[1].split(' |')[0]}"
                st.metric(label="Projected Monthly Savings", value=savings)
            
            st.info(final_state["value_hypothesis"])
        with tab3:
            st.write("### Risk Mitigation & Governance")
            if final_state.get("critique_history"):
                for risk in final_state["critique_history"]:
                    st.warning(risk)
            else:
                st.success("No high-level risks identified by the Governance Agent.")

        # This section is now properly indented inside the 'if' block
        st.divider()
        st.download_button(
            label="📩 Download Executive Strategy Report",
            data=f"Process: {process_input}\n{final_state['value_hypothesis']}",
            file_name="AI_Strategy_Report.txt",
            mime="text/plain"
        )
