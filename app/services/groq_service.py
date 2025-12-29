from langchain_groq import ChatGroq
from app.schemas.claim import ClaimExtraction
from app.core.config import settings

class GroqService:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model="llama-3.3-70b-versatile", groq_api_key=settings.GROQ_API_KEY)
        self.structured_llm = self.llm.with_structured_output(ClaimExtraction)

    def process_claim_email(self, subject: str, body: str) -> ClaimExtraction:
        prompt = f"""
            Você é um analista de sinistros sênior em uma corretora de seguros. 
            Sua tarefa é ler e-mails de clientes e extrair dados estruturados.
            
            Assunto do E-mail: {subject}
            Corpo do E-mail: {body}
            
            Instrução Extra: Se o cliente estiver muito nervoso, aumente o nível de urgência.
        """

        return self.structured_llm.invoke(prompt)