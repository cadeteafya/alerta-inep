"""
Adaptive Card builder for official INEP editais and portarias (Type 1).
Uses the same structure pattern as card_noticia (proven to work).
"""

EDITAIS_PAGE_URL = "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida"


def _detect_type(title: str) -> tuple:
    """Returns (icon, type_label) based on document title."""
    if "portaria" in title.lower():
        return "📋", "Portaria Oficial"
    return "🏛️", "Edital Oficial"


def build(title: str, dou_url: str) -> dict:
    """
    Build a Teams Adaptive Card for a new edital/portaria.

    Args:
        title: Full title from INEP page (e.g. "Edital nº 20, de 24 de março de 2026: ...")
        dou_url: Direct link to the DOU document
    """
    icon, type_label = _detect_type(title)

    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "Container",
                "style": "accent",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"{icon}  NOVO DOCUMENTO INEP · REVALIDA",
                        "weight": "Bolder",
                        "size": "Medium",
                        "color": "Light",
                        "wrap": True,
                    }
                ],
                "bleed": True,
            },
            {
                "type": "Container",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": type_label.upper(),
                        "size": "Small",
                        "weight": "Bolder",
                        "color": "Accent",
                        "spacing": "Medium",
                    },
                    {
                        "type": "TextBlock",
                        "text": title,
                        "wrap": True,
                        "weight": "Bolder",
                        "size": "Medium",
                        "spacing": "Small",
                    },
                ],
            },
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "📄 Ver Documento no DOU",
                "url": dou_url,
                "style": "positive",
            },
            {
                "type": "Action.OpenUrl",
                "title": "📂 Página de Editais INEP",
                "url": EDITAIS_PAGE_URL,
            },
        ],
    }
