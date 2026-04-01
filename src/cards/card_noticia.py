"""
Adaptive Card builder for INEP homepage news/informativo items (Type 2).
Color: Green (#2E7D32) — visually distinct from edital cards.
"""

MAX_SUMMARY_CHARS = 150


def build(title: str, summary: str, url: str, category: str = "INEP · REVALIDA") -> dict:
    """
    Build a Teams Adaptive Card for a Revalida-relevant news item.

    Args:
        title: News headline
        summary: Short description (truncated to MAX_SUMMARY_CHARS)
        url: Link to the full news article on gov.br/inep
        category: Category label from the INEP page (e.g. "REVALIDA", "EPT")
    """
    short_summary = (
        summary[:MAX_SUMMARY_CHARS] + "..." if len(summary) > MAX_SUMMARY_CHARS else summary
    )

    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "Container",
                "style": "good",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "📰  NOVA NOTÍCIA INEP · REVALIDA",
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
                        "text": category.upper(),
                        "size": "Small",
                        "weight": "Bolder",
                        "color": "Good",
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
                    {
                        "type": "TextBlock",
                        "text": short_summary,
                        "wrap": True,
                        "color": "Default",
                        "spacing": "Small",
                    },
                ],
            },
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "🔗 Leia a Notícia Completa",
                "url": url,
                "style": "positive",
            }
        ],
    }
