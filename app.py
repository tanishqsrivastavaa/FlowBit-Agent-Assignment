import streamlit as st
import asyncio
from main import classifier_agent, json_agent, email_agent, memory
import json

st.set_page_config(page_title="FlowBit Multi-Agent Demo", layout="centered")

st.title("📄 FlowBit Multi-Agent AI System")
st.subheader("Made by Tanishq Srivastava")
st.markdown(
    """
    This demo classifies your input (Email, JSON, or PDF/text), routes it to the right agent, and logs all steps for traceability.
    """
)

input_type = st.radio(
    "Select input type:",
    ("Email", "JSON", "Text File"),
    horizontal=True
)

user_input = ""
uploaded_file = None

if input_type == "Email":
    user_input = st.text_area("Paste your email content here:", height=200)
elif input_type == "JSON":
    user_input = st.text_area("Paste your JSON payload here:", height=200)
else:
    #Having issues with the PDF upload ): - FIX!
    uploaded_file = st.file_uploader("Upload a text or PDF file", type=["txt", "pdf"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            user_input = "\n".join(page.extract_text() for page in pdf_reader.pages)
        else:
            user_input = uploaded_file.read().decode("utf-8")

if st.button("Process Input", type="primary"):
    if not user_input.strip():
        st.warning("Please provide some input.")
    else:
        with st.spinner("Processing..."):
            async def run_agents():
                # Classify
                classifier_result = await classifier_agent.run(user_prompt=user_input)
                try:
                    if isinstance(classifier_result.output, str):
                        classification = json.loads(classifier_result.output)
                    else:
                        classification = classifier_result.output
                except Exception as e:
                    st.error(f"Classifier agent did not return valid JSON. Output was:\n\n{classifier_result.output}")
                    return None, None
                memory.log("user", "classification", classification)

                # Routing the 
                route_to = classification.route_to
                route_map = {
                    "json_agent": json_agent,
                    "email_agent": email_agent
                }
                agent = route_map.get(route_to)
                if agent is None:
                    return classification, None

                agent_result = await agent.run(user_prompt=user_input)
                memory.log("user", route_to, agent_result.output)
                return classification, agent_result.output

            classification, agent_output = asyncio.run(run_agents())

        st.subheader("🔎 Classification")
        try:
            if isinstance(classification, str):
                st.json(json.loads(classification))
            else:
                st.json(classification)
        except Exception:
            st.write(classification)

        if agent_output:
            st.subheader("🤖 Routed Agent Output")
            try:
                if isinstance(agent_output, str):
                    st.json(json.loads(agent_output))
                else:
                    st.json(agent_output)
            except Exception:
                st.write(agent_output)
        else:
            st.info("No suitable agent found for this input.")

        st.subheader("📝 Memory Log")
        for entry in memory.get_all():
            st.markdown(f"""
            - **Type:** {entry['type']}
            - **Timestamp:** {entry['timestamp']}
            - **Extracted:** `{entry['extracted']}`
            - **Thread ID:** {entry['thread_id']}
            ---
            """)

st.caption("FlowBit Multi-Agent Demo • Made by Tanishq Srivastava")