# 🚀 Enterprise AI Strategy & Value Engine

An agentic orchestration system designed to automate **Zero-Based Design** and **Financial ROI Modeling** for legacy business processes.

## 🛠️ Tech Stack
- **Orchestration:** LangGraph (State Machine)
- **Inference:** Groq / Llama-3.3-70b
- **Interface:** Streamlit
- **Logic:** Python (Pydantic, python-dotenv)

## 🛡️ Key Features
- **Governance Critic:** Autonomous agent audits designs for PII and policy risks.
- **Value Modeler:** Quantifies ROI based on monthly transaction volume and labor savings.
- **Build vs. Buy Analyst:** Recommends enterprise platforms (e.g., **IBM watsonx**) vs. custom builds.

## 📊 Quick Start
1. Clone the repo: `git clone https://github.com/yineirya/ai-strategy-engine.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `GROQ_API_KEY` to a `.env` file.
4. Run: `./venv/bin/python3 -m streamlit run app.py`
