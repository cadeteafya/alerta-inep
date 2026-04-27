"""
Adaptive Card builder for ABMES editais (Type 3).
Similar to card_edital, but with specific ABMES labels and buttons.
Color: Blue gov.br (#1351B4) to match editais.
"""

def build(title: str, post_url: str, download_url: str = None, summary: str = "") -> dict:
    """
    Build a Teams Adaptive Card for a new edital from ABMES.

    Args:
        title: Title of the post (e.g. "EDITAL INEP Nº 49")
        post_url: Direct link to the ABMES post
        download_url: Link to download the PDF/file (if available)
        summary: Context text from the post
    """
    actions = [
        {
            "type": "Action.OpenUrl",
            "title": "📄 Página de Editais INEP - ABMES",
            "url": post_url,
        }
    ]

    if download_url:
        actions.append({
            "type": "Action.OpenUrl",
            "title": "⬇️ Baixar Documento do ABMES",
            "url": download_url,
            "style": "positive",
        })

    return_dict = {
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
                        "text": "🏛️  NOVO DOCUMENTO INEP · ABMES",
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
                        "text": "EDITAL / RETIFICAÇÃO",
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
                    }
                ],
            },
        ],
        "actions": actions,
    }

    if summary:
        # Add the summary as a new TextBlock after the title
        card_body_items = return_dict["body"][1]["items"]
        card_body_items.append({
            "type": "TextBlock",
            "text": summary,
            "wrap": True,
            "size": "Default",
            "spacing": "Small",
        })

    return return_dict
