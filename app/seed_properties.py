from app.database import SessionLocal
from app.models import Property

db = SessionLocal()

property_data = Property(
    property_id="villa-b1",
    property_name="Villa B1",
    location="Assagao, North Goa",
    bedrooms="3",
    max_guests="6",
    private_pool="Yes",
    check_in="2pm",
    check_out="11am",
    base_rate="INR 18,000 per night",
    extra_guest_rate="INR 2,000 per guest",
    wifi_password="Nistula@2024",
    caretaker_hours="8am to 10pm",
    chef_on_call="Yes, pre-booking required",
    availability="April 20-24 Available",
    cancellation_policy="Free up to 7 days before check-in"
)

db.add(property_data)

db.commit()

db.close()

print("Property seeded.")