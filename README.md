# 🌊 InsightFlow AI - Agentic Research Dashboard

**InsightFlow AI** is an advanced autonomous agent ecosystem designed for deep executive research. It utilizes a **State Graph (LangGraph)** architecture to orchestrate multiple specialized agents that collaborate, analyze, and draft structured reports with real-time validation.

This project focuses on **Enterprise-grade LLMOps**, integrating real-world execution metrics, token consumption, and full traceability via LangSmith.

---

## 🚀 Key Features

* **Multi-Agent Orchestration**: A cyclic workflow powered by **LangGraph** featuring:
    * 🔍 **Researcher Agent**: Performs web-based fact-finding and data extraction.
    * 🧠 **Analyzing Agent**: Evaluates information density and manages iteration logic.
    * ⚖️ **Critical Agent**: Verifies for hallucinations and ensures logical consistency.
    * ✍️ **Writing Agent**: Generates professional, structured Markdown reports.
* **Real-Time LLMOps Observability**: 
    * **LangSmith Deep Integration**: Every execution generates a unique `trace_id` linked directly to the monitoring platform.
    * **Dynamic Trace Access**: An interactive UI button to inspect the agents' internal reasoning (prompts, nodes, and metadata).
* **Performance Metrics Dashboard**:
    * **Token Efficiency**: Smart estimation of token usage for cost optimization.
    * **Real Latency**: Exact execution time fetched directly from the LangSmith API.
* **Structured Outputs**: Pydantic-validated schemas to ensure consistent, professional reporting formats.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Orchestration** | [LangChain](https://www.langchain.com/) / [LangGraph](https://www.langchain.com/langgraph) |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Frontend** | [Gradio](https://gradio.app/) |
| **Observability** | [LangSmith](https://www.langchain.com/langsmith) |
| **AI Models** | Gemini 3.1 Flash Lite / Pro |
| **Infrastructure** | Docker & Docker Compose |

---

## 📐 Agentic Workflow

The system operates on a **Self-Correction** logic:



1.  **Entry Node**: Receives the research task.
2.  **Research Node**: Gathers facts based on the query.
3.  **Analyst Node**: Evaluates data density. If information is insufficient (fewer than 3 facts or low iterations), it loops back to the Researcher.
4.  **Writer Node**: Once approved, it generates a final report including Executive Summary, Key Findings, and Verified Sources.

---

## 📊 Observability & Metrics

Unlike traditional chatbots, **InsightFlow AI** exposes its internal telemetry:

* **Execution Link**: Upon completion, the system generates a custom CSS-styled button: `🔗 Open in LangSmith`.
* **System Metrics**: The Gradio dashboard displays real-time data:
    * **Execution Time**: Total time from input to final report.
    * **Sources Used**: Count of unique sources processed by the agents.
    * **Token Usage**: Efficiency metrics for cost-tracking.

---

## ⚙️ Installation & Setup

Follow these steps to deploy the dashboard locally using Docker:

### 1. Clone the repository
```bash
git clone [https://github.com/PaoloSebastian12/InsightFlow_AI.git](https://github.com/PaoloSebastian12/InsightFlow_AI.git)
cd InsightFlow_AI

### 2. Configure Environment Variables
Create a .env file in the root directory:
    GOOGLE_API_KEY=your_google_api_key
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_API_KEY=your_langsmith_api_key
    LANGCHAIN_PROJECT=insightflow-ai-test
```
### 3. Deploy with Docker Compose
```bash
docker-compose up --build
```
### 4. Access the Application
```bash
Frontend (Gradio): http://localhost:8501

Backend (FastAPI Docs): http://localhost:8000/docs
```
📈 Quality & Validation
```bash
The project integrates automated validations to ensure agent reliability:

 - API Response Schema: Enforced through defined types to prevent integration failures.

 - System Status Monitoring: Visual feedback on the dashboard regarding the agentic flow status.
 ```

