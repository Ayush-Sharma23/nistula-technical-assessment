from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.config import APP_NAME, ENVIRONMENT
from app.database import SessionLocal
from app.models import GuestMessage
from app.schemas import IncomingMessage, UnifiedMessage
from app.classifier import classify_query
from app.ai_service import generate_reply
from app.confidence import calculate_confidence

app = FastAPI(title = APP_NAME)

VALID_SOURCES = {
	"whatsapp",
	"booking_com",
	"airbnb",
	"instagram",
	"direct"
}

@app.get("/")
def root():
	return {
	"message":"Backend Running",
	"environment":ENVIRONMENT
	}

@app.get("/health")
def health_check():
	return {
	"status":"healthy"
	}

@app.post("/webhook/message")
def handle_message(payload : IncomingMessage):

	#initiating session to store the incoming message
	db: Session = SessionLocal()

	try:
		# validating the source of incoming data 
		if payload.source not in VALID_SOURCES:
			raise HTTPException(
				status_code=400,
				detail = "Invalid Source"
			)

		#creating a unified model from the payload
		query_type = classify_query(payload.message)

		unified = UnifiedMessage.build(payload,query_type)

		

		db_message = GuestMessage(
				message_id = unified.message_id,
				source=unified.source,
				guest_name=unified.guest_name,
				message_text=unified.message_text,
				timestamp =unified.timestamp,
				booking_ref=unified.booking_ref,
				property_id=unified.property_id,
				query_type=unified.query_type
			)

		db.add(db_message)

		db.commit()

		drafted_reply = generate_reply(
			guest_name = unified.guest_name,
			message=unified.message_text,
			query_type=unified.query_type
		)

		confidence_score, action = calculate_confidence(
			unified.query_type,
			unified.message_text
		)

		return{
			"message_id": unified.message_id,
			"query_type": unified.query_type,
			"drafted_reply": drafted_reply,
			"confidence_score": confidence_score,
			"action": action
		}

	except HTTPException:
		raise

	except Exception as e:

		raise HTTPException(
			status_code=500,
			detail=str(e)
		)

	finally:
		db.close()