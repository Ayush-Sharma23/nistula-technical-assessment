## Scenario

It is 3am. A guest at Villa B1 sends a WhatsApp message:

> "There is no hot water and we have guests arriving for breakfast in 4 hours. This is unacceptable. I want a refund for tonight."

---

# Question A — The Immediate Response

## AI Reply

Hi, I’m very sorry about this — this is not the experience we wanted for you. I’ve escalated this to our on-call support team immediately and marked it as urgent. Our staff will contact you shortly to resolve the hot water issue as quickly as possible.

I understand your frustration regarding tonight’s experience. Once the immediate issue is addressed, our team will review the refund request with priority.

## Reasoning

This wording achieves the following things:
- acknowledgment and empathy
- reassurance
- avoiding premature promises about refunds before human review
- tells the guest that their query will be handled by a human being

The AI should not autonomously approve compensation or speculate about repair timelines.

---

# Question B — The System Design

The platform should immediately classify this as:
- complaint
- high_priority

## System Actions

1. Escalate to human operations staff.
2. Trigger urgent notifications:
   - WhatsApp/email/SMS to on-call property manager
   - push notification in internal dashboard
   - raise a ticket to the on-call support team
3. Create incident ticket with:
   - property ID
   - guest details
   - complaint category
   - complaint message
   - timestamp
4. Log the conversation and escalation decision in PostgreSQL.
5. Mark AI auto_send as disabled for this thread until human takeover.

## Escalation Logic

If no human responds within 30 minutes, the system should
- escalate to secondary manager
- log the complaint into unresolved category with a flag like time-elapsed till resolution
- trigger repeat alerts
- flag a report internally
- optionally send a follow up acknowledgement to guest such as 

> “Our team is still actively working on this issue.”

---

# Question C — The Learning

Three similar complaints in two months indicates a recurring operational failure, not an isolated support issue.

We can setup a complaint tracking system that seeks for recurring patterns and raises them as an issue once it sees
a trend in the complaints. This trend could be decided by
- threshold amount of certain complaints on a certain property
- checking with the service log to see if the property was services within that time

The system should:
- aggregate complaint trends by property and category
- detect repeated “hot water” incidents
- automatically raise a maintenance-risk flag for the property

Preventative measures like as-follows can be taken:

1. Complaint pattern analytics
2. Property health scoring
3. Preventive maintenance workflows
4. Raise maintainance issues if not resolved
