from anthropic import Anthropic

from app.config import ANTHROPIC_API_KEY
# from app.constants import PROPERTY_CONTEXT

client = Anthropic(
    api_key=ANTHROPIC_API_KEY
)


def generate_reply(
    guest_name: str,
    message: str,
    query_type: str,
    property_context
):

    prompt = f"""
You are a luxury villa hospitality assistant.

Use ONLY the provided property context.

Do not hallucinate details.

Keep replies short, natural, and conversational.

Prefer WhatsApp-style hospitality replies.

Maximum 4-5 sentences.

Do not over-explain.

Do not use marketing language.

If information is missing, say a team member will confirm.

PROPERTY CONTEXT:
{property_context}

QUERY TYPE:
{query_type}

GUEST NAME:
{guest_name}

GUEST MESSAGE:
{message}

Generate a guest-ready reply.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text