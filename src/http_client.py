"""
Shared HTTP session with retry/backoff for transient network failures.

GitHub Actions runners occasionally return `[Errno 101] Network is unreachable`
when reaching www.gov.br. Retry with backoff turns those blips into successful
requests instead of failed workflow runs.
"""
from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def build_session() -> requests.Session:
    """Return a Session with retries on connect/read errors and 5xx responses."""
    retry = Retry(
        total=4,
        connect=4,
        read=4,
        backoff_factor=1.5,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
