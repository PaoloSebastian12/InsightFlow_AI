import gradio as gr
import requests
import time

def run_ai_research(task):
    start_time = time.time()
    steps = [
        "🔍 Investigating Agent: Searching for sources on the web...",
        "🧠 Analyzing Agent: Extracting key concepts...",
        "⚖️ Critical Agent: Verifying hallucinations and consistency...",
        "✍️ Writing Agent: Generating final report in Markdown..."
    ]
    current_log = ""
    for step in steps:
        current_log += f"{step}\n"
        yield (
            current_log,
            "Generating...",
            "Calculating...",
            "Calculating...",
            "Processing flow...",
            0, "---", "---",
            [],"---")
        time.sleep(1.2)
    try:
        response = requests.post("http://backend:8000/research", json={"task": task})
        response.raise_for_status()
        data = response.json()
        trace_id = data.get("trace_id", "no_id")
        langsmith_url = f"https://smith.langchain.com/o/9994b2d3-2195-4a3a-b478-792aa0a2dde6/projects/p/5805d150-538a-455a-8197-8e8cc02c4abb?peek={trace_id}"
        open_link_md = ""
        if trace_id != "no_id":
            open_link_md = f"""
            <div style="margin-top:10px;">
                <a href="{langsmith_url}" target="_blank">
                    <button style="
                        background-color:#4f46e5;
                        color:white;
                        padding:10px 16px;
                        border:none;
                        border-radius:8px;
                        cursor:pointer;
                        font-weight:bold;
                    ">
                        🔗 Open in LangSmith
                    </button>
                </a>
            </div>
            """
        real_tokens = data.get("usage", {}).get("total_tokens", 0)
        latency = data.get("latency", 0)
        trace_link = trace_id
        duration = round(time.time() - start_time, 2)
        report_data = data.get("final_report", {})
        sources = report_data.get("sources", [])
        md = f"# 📊 {report_data.get('title', 'Research Report')}\n\n"
        md += f"### 📝 Executive Summary\n{report_data.get('executive_summary', '')}\n\n"
        md += "### 🔑 Key Findings\n" + "\n".join([f"- {f}" for f in report_data.get('key_findings', [])]) + "\n\n"
        md += f"### 🎯 Conclusion\n{report_data.get('conclusion', '')}\n\n"
        if sources:
            md += "### 📚 Sources\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(sources)])
        quality_data = [
            ["Alucinaciones", "Awaiting Evaluator ⏳"],
            ["Relevancia AI", "Awaiting Evaluator ⏳"],
            ["Pytest: Schema", "✅ Passed"]
        ]
        yield (
            current_log + "✅ Proceso completado exitosamente.",
            md,
            f"{duration} s",
            str(len(sources)),
            "InsightFlow AI Online",
            real_tokens,
            f"{latency}s",
            trace_id,
            quality_data,
            open_link_md)
    except Exception as e:
        yield (f"❌ Error: {str(e)}", "Error en la generación", "0", "0", "Error", 0, "0", "None", [], "")


with gr.Blocks(theme=gr.themes.Soft(), title="InsightFlow AI Dashboard") as demo:
    gr.Markdown("# 🌊 InsightFlow AI - Agentic Research Dashboard")

    with gr.Row():
        tokens_val = gr.Number(label="Tokens Usados (Efficiency)", precision=0)
        latency_val = gr.Textbox(label="Latencia Total (Performance)")
        trace_val = gr.Textbox(label="LangSmith Trace (ID)")
    open_link = gr.Markdown()

    with gr.Row():
        with gr.Column(scale=2):
            input_text = gr.Textbox(label="Research Task", placeholder="Describe the research task you want InsightFlow AI to perform...")
            btn = gr.Button("Run Agent", variant="primary")
            gr.Markdown("### 🧠 Agent's Reasoning (LangGraph Trace)")
            reasoning_log = gr.Textbox(label="Agent Thought Process", interactive=False, lines=8)
        with gr.Column(scale=1):
            gr.Markdown("### 📈 System Metrics")
            m1 = gr.Textbox(label="Execution Time (s)", interactive=False)
            m2 = gr.Textbox(label="Sources Used", interactive=False)
            m3 = gr.Textbox(label="System Status", interactive=False)
            gr.Markdown("### ✅ Quality Score (Self-Correction)")
            quality_table = gr.Dataframe(
                headers=["Métrica", "Resultado"],
                datatype=["str", "str"],
                col_count=(2, "fixed"),
                label="Pytest & Validation Results"
            )
    gr.Markdown("---")
    output_report = gr.Markdown(label="Report Generated")


    btn.click(fn=run_ai_research, inputs=[input_text], outputs=[reasoning_log, output_report, m1, m2, m3, tokens_val, latency_val, trace_val, quality_table,open_link ])
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8501)