import streamlit as st
from memory import HealthcareMemory
from agents import medical_llm

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = HealthcareMemory()

st.set_page_config(page_title="MediSyn Labs", layout="wide")

st.title("🧬 MediSyn Labs – AI Healthcare Research Assistant")

# Sidebar
with st.sidebar:
    st.subheader("Research Metadata")
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
        st.warning("Please enter a detailed clinical research query.")
    else:
        with st.spinner("Analyzing medical literature..."):
            context = st.session_state.memory.get_context()
            response = medical_llm(query, disease_focus, context)

            st.session_state.memory.add_short_term(query, response)

            st.subheader("📄 Generated Medical Summary")
            st.write(response)

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
                st.success("Summary approved and stored.")

            st.download_button(
                "📥 Download Report",
                data=response,
                file_name="clinical_summary.txt"
            )

st.divider()

with st.expander("📚 Session Memory"):
    st.json(list(st.session_state.memory.short_term))

with st.expander("🗄️ Long-Term Memory"):
    st.json(st.session_state.memory.long_term)