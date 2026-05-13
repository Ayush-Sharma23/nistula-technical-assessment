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


class Property(Base):

    __tablename__ = "properties"

    property_id = Column(String, primary_key=True)

    property_name = Column(String, nullable=False)

    location = Column(String)

    bedrooms = Column(String)

    max_guests = Column(String)

    private_pool = Column(String)

    check_in = Column(String)

    check_out = Column(String)

    base_rate = Column(String)

    extra_guest_rate = Column(String)

    wifi_password = Column(String)

    caretaker_hours = Column(String)

    chef_on_call = Column(String)

    availability = Column(String)

    cancellation_policy = Column(String)