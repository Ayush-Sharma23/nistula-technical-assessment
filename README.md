# Nistula Guest Message Handler 

### Note : At the end of the readme is my thought process between adding each feature and commiting it.

# Running the Project

## Activate venv

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Database Initialization

Run:

```bash
python -m app.init_db
```

---

## Run server

```bash
uvicorn app.main:app --reload
```

---

# Available Endpoints

## Root

GET /

## Health Check

GET /health

## Payload

POST /webhook/message

## Docs (TO TEST)

GET /docs

## Testing in PowerShell

```Text
$body = @{
    source      = "whatsapp"
    guest_name  = "Rahul Sharma"
    message     = "Is the villa available from April 20 to 24?"
    timestamp   = "2026-05-05T10:30:00Z"
    booking_ref = "NIS-2024-0891"
    property_id = "villa-b1"
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/webhook/message" -Method Post -Body ($body | ConvertTo-Json) -ContentType "application/json"
```

## Testing in Bash

```Text
curl -X POST "http://127.0.0.1:8000/webhook/message" \
-H "Content-Type: application/json" \
-d '{
  "source": "whatsapp",
  "guest_name": "Rahul Sharma",
  "message": "Is the villa available from April 20 to 24?",
  "timestamp": "2026-05-05T10:30:00Z",
  "booking_ref": "NIS-2024-0891",
  "property_id": "villa-b1"
}'
```

---

## Current Table

guest_messages

```text
Fields:
- message_id
- source
- guest_name
- message_text
- timestamp
- booking_ref
- property_id
- query_type
```

## Current Strategy

Rule-based keyword classification.
```text
Advantages:
- deterministic
- fast
- easy to debug
```
---

## Current Processing Flow

```text
Webhook Request
- Validate
- Normalize
- Classify
- Persist
```

# Future Improvements

## Smarter Classification

Current implementation uses deterministic keyword matching.
```text
Future upgrades may include:
- sentiment analysis
- transformer-based intent detection
- multilingual support
- semantic embeddings
```
---

## Better Confidence Scoring

Current scoring is heuristic-based.
```text
Future improvements:
- hallucination risk estimation
- ambiguity scoring
- LLM self-evaluation
- semantic uncertainty detection
```
---

## AI Guardrails
```text
Planned safeguards:
- structured outputs
- schema validation
- moderation layer
- prompt injection resistance
- hallucination prevention
```
---

## Scalability
```text
Potential future architecture:
- Redis queues
- async workers
- Kafka event streaming
- vector retrieval
- multi-property context retrieval
```
# Notes : 

The task in hand is to make a backend system to recieve guest messages from multiple channels such as :
Whatsapp, Airbnb, Booking.com, Instagram and Nistula's website

The goal for the backend is to achieve the following things :
1. Recieve inbound messages from multiple channels
2. Normalize them into a unified schema
3. Categorize those messages into vaious pre-defined categories
4. Send those normalized messages and category to Claude via API.
5. Have Claude draft a reply to the message.
6. Perform confidence score calculation, set an action according to the confidence score.
7. Route back the response safely.

I have decide to make the Backend in in FastAPI since I'm more profecient with Python and learning FastAPI seemed more comfortable. 
It also gives me some benefits like : async-readiness, strong validation via Pydantic and a lightweight production environment AND THAT BEAUTIFUL DOCS

I'm gonna breakdown the problem into incremental steps :
1. Make a persistent infrastructure that can correctly recieve/ fetch data from endpoints. 
2. Normalize the data into a unified schema so that all the data is same for the Claude API to work on regardless of the source.
3. Sentiment Analysis on message to classify it into one of the predefined categories.
4. Put down a Claude AI pipeline to send relevant information for Claude to process and produce a reply to. Also : Give claude the context of the property in question. /*I think this will be a very good database design challenge later. How to give claude the exact context of each property? How to design an efficient schema so that claude can quickly learn the context?*/ 
	I think it is also important to put down some guardrails for claude to prevent malicious prompt injections and hallucinations.
5. Get confidence score by performing whatever logic I decide for generating the score. /*Maybe something like LLM uncertainty estimation along with sentiment polarity*/
6. Return the whole thing in a neat structure. 

I'll worry about scalability and flexibility once our MVP works to a satifactory level.


## WHAT I'M DOING RIGHT NOW
```text
	Making test for the app. Improving Error Handling. Then branch out to a DeBERTa-based query classifier. 
```
