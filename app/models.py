from sqlalchemy import Column, String, Text, DateTime

from app.database import Base

class GuestMessage(Base):
    __tablename__ = "guest_messages"
    
    # Defining the db model

    message_id = Column(String, primary_key = True)
    
    source = Column(String, nullable=False)
    
    guest_name = Column(String, nullable=False)
    
    message_text = Column(Text, nullable=False)
    
    timestamp = Column(DateTime, nullable=False)
    
    booking_ref = Column(String)

    property_id = Column(String)

    query_type = Column(String)
