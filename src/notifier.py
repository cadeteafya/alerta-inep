"""
Sends Adaptive Cards to Microsoft Teams via Power Automate webhook.
"""
import requests


def send_card(webhook_url: str, card_content: dict) -> bool:
    """
    Wraps an Adaptive Card in the Teams message envelope and POSTs it.
    Returns True on success (2xx), False otherwise.
    """
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_content,
            }
        ],
    }
    try:
        response = requests.post(webhook_url, json=payload, timeout=15)
        if response.status_code in (200, 202):
            return True
        print(f"[Notifier] Unexpected status {response.status_code}: {response.text}")
        return False
    except requests.RequestException as e:
        print(f"[Notifier] Request failed: {e}")
        return False
