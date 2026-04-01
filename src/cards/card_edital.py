"""
Adaptive Card builder for official INEP editais and portarias (Type 1).
Color: Blue gov.br (#1351B4)
Buttons: direct DOU link + fixed INEP editais page link
"""

EDITAIS_PAGE_URL = "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida"


def _detect_type(title: str) -> tuple[str, str]:
    """Returns (icon, type_label) based on document title."""
    title_lower = title.lower()
    if "portaria" in title_lower:
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
                "style": "emphasis",
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
                "backgroundImage": {
                    "fillMode": "Cover",
                    "horizontalAlignment": "Center",
                    "verticalAlignment": "Center",
                    "url": "data:image/png;base64,",  # solid color via style
                },
                "style": "accent",
            },
            {
                "type": "Container",
                "items": [
                    {
                        "type": "FactSet",
                        "facts": [
                            {"title": "Tipo", "value": type_label},
                            {"title": "Fonte", "value": "Diário Oficial da União"},
                        ],
                    },
                    {
                        "type": "TextBlock",
                        "text": title,
                        "wrap": True,
                        "weight": "Bolder",
                        "size": "Medium",
                        "spacing": "Medium",
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
