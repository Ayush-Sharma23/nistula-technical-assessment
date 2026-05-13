def calculate_confidence(
	query_type:str,
	message: str
):
	
	score = 0.70

	if query_type in [
		"pre_sales_availability",
		"pre_sales_pricing",
		"post_sales_checkin"
	]:

		score+=0.20

	if len(message.split())>5:
			score+=0.05

	if query_type == "complaint":
			score=0.40

	score = min(score,0.99)

	if score < 0.60:
		action = "escalate"

	elif score < 0.85:
		action = "agent_review"

	else:
		action = "auto_send"

	return score,action