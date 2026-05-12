from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4

# we are using BaseModel to validate the source message

class IncomingMessage(BaseModel):

	source: str

	guest_name: str

	message: str

	timestamp: datetime

	booking_ref: str

	property_id: str

class UnifiedMessage(BaseModel):

	message_id:str

	source: str

	guest_name: str

	message_text: str

	timestamp: datetime

	booking_ref: str

	property_id: str

	query_type: str | None = None

	@staticmethod
	def build(payload):

		return UnifiedMessage(
			message_id=str(uuid4()),
			source=payload.source,
			guest_name=payload.guest_name,
			message_text=payload.message,
			timestamp=payload.timestamp,
			booking_ref=payload.booking_ref,
			property_id=payload.property_id,
			query_type=None
		)