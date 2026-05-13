KNOWN_CAPABILITIES = {
    "availability",
    "pricing",
    "wifi",
    "checkin",
    "checkout",
    "pets",
    "parking",
    "chef",
    "pool",
    "cancellation"
}

def has_required_context(message: str)->bool:

    text = message.lower()

    capability_keywords = {
        "availability": ["available", "availability"],
        "pricing": ["price", "rate", "cost"],
        "wifi": ["wifi", "wi-fi"],
        "checkin": ["check in", "check-in"],
        "checkout": ["check out", "check-out"],
        "pets": ["pets", "pet friendly"],
        "parking": ["parking"],
        "chef": ["chef", "cook"],
        "pool": ["pool"],
        "cancellation": ["cancel", "refund"]    
    }

    for capability, keywords in capability_keywords.items():
        if any(keyword in text for keyword in keywords):
            if capability in KNOWN_CAPABILITIES:
                return True

    return False

def calculate_confidence(
    query_type: str,
    message: str
):
    if query_type == "complaint":
        return 0.30, "escalate"

    score = 0.50

    if has_required_context(message):
        score += 0.35

    if query_type in [
        "pre_sales_availability",
        "pre_sales_pricing",
        "post_sales_checkin",
        "general_enquiry"
    ]:
        score+=0.10

    if query_type == "special_request":
        score -= 0.15

    text = message.lower()

    ambiguity_markers = [
        "maybe",
        "not sure",
        "can you help",
        "something",
        "urgent"
    ]

    if any(marker in text for marker in ambiguity_markers):
        score -=0.15

    score = max(0.0, min(score,0.99))

    if score>0.85:
        action = "auto_send"

    elif score>0.60:
        action = "agent_review"

    else:
        action = "escalate"

    return score,action