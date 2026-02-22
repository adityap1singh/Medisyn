import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def medical_llm(query, disease_focus, context):
    prompt = f"""
You are a clinical research assistant.
You do NOT provide medical advice or diagnosis.

Disease Focus: {disease_focus}

Conversation Context:
{context}

Instructions:
- Summarize peer-reviewed medical literature
- Compare treatments only at a high level
- Use cautious, evidence-based language
- Include uncertainty when evidence is limited

User Query:
{query}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"