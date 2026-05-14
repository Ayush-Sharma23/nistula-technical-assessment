from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4

# Incoming webhook payload schema
# shared across all supported channels
class IncomingMessage(BaseModel):

	source: str

	guest_name: str

	message: str

	timestamp: datetime

	booking_ref: str

	property_id: str

# Standardized API response returned
# after AI orchestration pipeline completes
class UnifiedMessage(BaseModel):

	message_id:str

	source: str

	guest_name: str

	message_text: str

	timestamp: datetime

	booking_ref: str

	property_id: str

	query_type: str 

	@staticmethod
	def build(payload, query_type):

		return UnifiedMessage(
			message_id=str(uuid4()),
			source=payload.source,
			guest_name=payload.guest_name,
			message_text=payload.message,
			timestamp=payload.timestamp,
			booking_ref=payload.booking_ref,
			property_id=payload.property_id,
			query_type=query_type
		)