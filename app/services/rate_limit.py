from collections import deque
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.config import settings

_request_times: deque[datetime] = deque()


def enforce_rate_limit() -> None:
    now = datetime.now(timezone.utc)
    one_minute_ago = now - timedelta(minutes=1)

    while _request_times and _request_times[0] < one_minute_ago:
        _request_times.popleft()

    if len(_request_times) >= settings.max_requests_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again shortly.",
        )

    _request_times.append(now)
