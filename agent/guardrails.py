import os

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

POLICY = {
    "web_search": {"rate_limit": 30, "window_s": 60},
    "send_email": {"requires_confirm": True},
}

def enforce(plan, step):
    # Placeholder pour quotas/confirmations/règles
    return True
