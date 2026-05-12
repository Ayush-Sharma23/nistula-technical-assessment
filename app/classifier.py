def classify_query(message: str) -> str:
	text = message.lower()

	if any(word in text for word in[
		"available",
		"availability"
	]):
		return "pre_sales_availability"

	if any(word in text for word in [
		"rate",
		"price",
		"cost",
		"how much"
	]):
		return "pre_sales_pricing"

	if any(word in text for word in [
		"check in",
		"checkin",
		"check-in",
		"wifi",
		"wi-fi",
		"checkout",
		"check-out",
		"check out"
	]):
		return "post_sales_checkin"

	if any(word in text for word in [
		"early check",
		"early checkin",
		"early check-in",
		"early",
		"transfer",
		"pickup",
		"request"
	]):
		return "special_request"

	if any(word in text for word in [
		"not happy",
		"dissatisfactory",
		"dissatisfied",
		"annoying",
		"not working",
		"bad experince",
		"don't like"
	]):
		return "complaint"

	return "general_enquiry"