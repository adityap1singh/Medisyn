import streamlit as st
import google.generativeai as genai
from memory import HealthcareMemory
from agents import medical_llm

# memory.py
from collections import deque

class HealthcareMemory:
    def __init__(self, max_short_term=7):
        self.short_term = deque(maxlen=max_short_term)
        self.long_term = []

    def add_short_term(self, query, response):
        self.short_term.append({
            "query": query,
            "response": response
        })

    def add_long_term(self, content, disease, approved):
        self.long_term.append({
            "content": content,
            "disease": disease,
            "approved": approved
        })

    def get_context(self):
        return "\n".join(
            [f"Q: {m['query']}\nA: {m['response']}" for m in self.short_term]
        )
		
# agents.py

from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def medical_llm(query, disease_focus, context):
    prompt = f"""
You are a clinical research assistant.

Disease Focus: {disease_focus}

Previous Context:
{context}

Task:
- Summarize medical literature
- Compare treatments if applicable
- Be factual and cautious

Query:
{query}
"""
    response = model.generate_content(prompt)
    return response.text
	

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = HealthcareMemory()

st.title("🧬 MediSyn Labs – AI Healthcare Research Assistant")

# Sidebar metadata
with st.sidebar:
    researcher_id = st.text_input("Researcher ID", "R-001")
    project_id = st.text_input("Project ID", "P-Clinical-01")
    disease_focus = st.text_input("Disease Focus", "COPD")

st.divider()

query = st.text_area(
    "Enter Clinical Research Query",
    placeholder="What does recent literature say about mRNA vaccines?"
)

if st.button("Run Analysis"):
    if len(query.strip()) < 10:
        st.warning("Please enter a valid medical query.")
    else:
        with st.spinner("Analyzing medical literature..."):
            context = st.session_state.memory.get_context()
            response = medical_llm(query, disease_focus, context)

            st.session_state.memory.add_short_term(query, response)

            st.subheader("📄 Generated Medical Summary")
            st.write(response)

            # HITL Approval
            st.subheader("🧑‍⚕️ Human-in-the-Loop Approval")
            approval = st.radio(
                "Approve this summary?",
                ["Approve", "Reject"],
                horizontal=True
            )

            if approval == "Approve":
                st.session_state.memory.add_long_term(
                    content=response,
                    disease=disease_focus,
                    approved=True
                )
                st.success("Summary approved and stored in long-term memory.")

            # Download
            st.download_button(
                "Download Report",
                data=response,
                file_name="clinical_summary.txt"
            )

st.divider()

# Display Memory
with st.expander("📚 Session Memory"):
    st.write(list(st.session_state.memory.short_term))

with st.expander("🗄️ Long-Term Memory"):
    st.write(st.session_state.memory.long_term)
	
	