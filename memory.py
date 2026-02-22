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
            f"Q: {m['query']}\nA: {m['response']}"
            for m in self.short_term
        )