from app.database import SessionLocal
from app.models import Property

# retrieves property data from db
def get_property(property_id: str):

    db = SessionLocal()

    property_obj = (
        db.query(Property)
        .filter(Property.property_id == property_id)
        .first()
    )

    db.close()

    return property_obj

#builds a string about property context for AI
def build_property_context(property_obj):

    if not property_obj:
        return None

    return f"""
Property: {property_obj.property_name}
Location: {property_obj.location}

Bedrooms: {property_obj.bedrooms}
Max guests: {property_obj.max_guests}
Private pool: {property_obj.private_pool}

Check-in: {property_obj.check_in}
Check-out: {property_obj.check_out}

Base rate:
{property_obj.base_rate}

Extra guest rate:
{property_obj.extra_guest_rate}

WiFi password:
{property_obj.wifi_password}

Caretaker:
{property_obj.caretaker_hours}

Chef on call:
{property_obj.chef_on_call}

Availability:
{property_obj.availability}

Cancellation:
{property_obj.cancellation_policy}
"""