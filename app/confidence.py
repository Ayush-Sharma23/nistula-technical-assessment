def has_information_for_query(
    query_type: str,
    property_obj,
    message: str
):

    text = message.lower()

    if query_type == "complaint":
        return False

    if query_type == "pre_sales_availability":
        return bool(property_obj.availability)

    if query_type == "pre_sales_pricing":
        return bool(property_obj.base_rate)

    if query_type == "post_sales_checkin":

        keywords = [
            "check in",
            "check-in",
            "wifi",
            "wi-fi"
        ]

        if any(k in text for k in keywords):

            return (
                bool(property_obj.check_in)
                or bool(property_obj.wifi_password)
            )

    if query_type == "general_enquiry":

        enquiry_fields = [
            property_obj.private_pool,
            property_obj.chef_on_call,
            property_obj.caretaker_hours,
            property_obj.cancellation_policy
        ]

        return any(enquiry_fields)

    if query_type == "special_request":

        request_keywords = {
            "chef": property_obj.chef_on_call,
            "early check in": property_obj.check_in,
            "early check-in": property_obj.check_in
        }

        for keyword, value in request_keywords.items():

            if keyword in text and value:
                return True

        return False

    return False


def calculate_confidence(
    query_type: str,
    message: str,
    property_obj
):

    if query_type == "complaint":
        return 0.30, "escalate"

    score = 0.50

    information_available = has_information_for_query(
        query_type,
        property_obj,
        message
    )

    if information_available:
        score += 0.35

    else:
        score -= 0.20

    low_risk_queries = [
        "pre_sales_availability",
        "pre_sales_pricing",
        "post_sales_checkin"
    ]

    if query_type in low_risk_queries:
        score += 0.10

    ambiguity_markers = [
        "not sure",
        "maybe",
        "something",
        "urgent",
        "help me"
    ]

    text = message.lower()

    if any(marker in text for marker in ambiguity_markers):
        score -= 0.15

    score = max(0.0, min(score, 0.99))

    if score > 0.85:
        action = "auto_send"

    elif score >= 0.65:
        action = "agent_review"

    else:
        action = "escalate"

    return score, action