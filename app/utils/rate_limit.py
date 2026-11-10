
from slowapi import Limiter
from slowapi.util import get_remote_address


# Apply a shared limit of 10 requests per minute per client IP.
limiter = Limiter(
    key_func=get_remote_address,
    application_limits=["10/minute"],
)