"""
AI Filter module using Gemini 2.5 Flash-Lite.
Determines if a news item is relevant to INEP Revalida.
"""
import json
import time
from google import genai

SYSTEM_PROMPT = """Você é um filtro para um sistema de alertas sobre o Revalida
(Exame Nacional de Revalidação de Diplomas Médicos Expedidos no Exterior).

Analise o título e o resumo da notícia e responda APENAS com JSON válido, sem markdown:
{"is_relevant": true, "reason": "motivo curto"}

is_relevant = true quando mencionar:
- "Revalida", "Revalidação de Diplomas", "diplomas médicos", "médico estrangeiro"
- Processo seletivo, edital, inscrição, resultado, gabarito do Revalida
- Portaria ou norma que impacte diretamente o Revalida

is_relevant = false para ruído:
- Enem, Saeb, Censo Escolar, Enade, Encceja, Celpe-Bras (sem menção ao Revalida)
- Notícias genéricas de educação, alfabetização, EPT
- Conteúdo administrativo interno do INEP sem relação com Revalida"""


def check_relevance(title: str, summary: str, api_key: str) -> dict:
    """
    Returns {"is_relevant": bool, "reason": str}.
    Includes rate limit protection (sleep between calls).
    """
    client = genai.Client(api_key=api_key)
    prompt = f"Título: {title}\nResumo: {summary}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite-preview-06-17",
            contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
        )
        raw = response.text.strip()
        # Strip markdown fences if present
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        time.sleep(15)  # respect 5 req/min free tier limit
        return result
    except json.JSONDecodeError:
        return {"is_relevant": False, "reason": "parse_error"}
    except Exception as e:
        print(f"[AI Filter] Error: {e}")
        return {"is_relevant": False, "reason": "api_error"}
