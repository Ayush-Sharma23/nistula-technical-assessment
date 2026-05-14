# Nistula Guest Message Handler

An asynchronous backend system designed to handle guest message processing, normalization, classification, and response drafting across multiple communication platforms, such as WhatsApp, Airbnb, Booking.com, Instagram, and Nistula's website.

This project leverages **FastAPI** for its asynchronous capabilities, strong validation via Pydantic, and lightweight production environment.

---

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Database Initialization and Seeding](#database-initialization-and-seeding)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [Overview](#overview)
  - [Payload Testing](#payload-testing)
- [Processing Flow](#processing-flow)
  - [Architectural Diagram](#architectural-diagram)
- [Model Setup](#model-setup)
- [Future Improvements](#future-improvements)
  - [Completed Improvements](#completed-improvements)
- [Notes](#notes)
- [Confidence Scoring System](#confidence-scoring-system)

---

## About

This backend system is developed to achieve the following objectives:
1. Receive inbound messages from multiple communication platforms.
2. Normalize messages into a unified schema.
3. Categorize messages into predefined categories using semantic classification with AI.
4. Process the normalized messages and categories via the Claude API to draft intelligent responses.
5. Calculate confidence scores to determine the reliability of responses and route them accordingly.
6. Safely return responses to clients while adhering to business rules and context limitations.

Key Features:
- **Built with FastAPI**: Enables async-readiness and strong data validation.
- **Semantic Classification**: Leverages the DeBERTA model for accurate message categorization.
- **AI-Powered Responses**: Integrates with Claude for generating contextual replies.
- **Confidence Scoring**: Determines the response reliability through contextual and heuristic methods.

---

## Getting Started

Follow the instructions below to set up and test the project.

### Prerequisites

- **Python**: Version 3.9 or higher.
- **ASGI Server**: Uvicorn.
- **Classifier Model**: Download from [HuggingFace](https://huggingface.co/zuccyzucc/guest_message_classifier).
- **Supported Databases**: SQLite (default) or PostgreSQL.

---

### Environment Setup

1. **Set up and activate a virtual environment**:

   #### Linux/macOS
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   #### Windows
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

### Database Initialization and Seeding

1. **Database Initialization**:
   Run the following command to create the necessary tables:
   ```bash
   python -m app.init_db
   ```

2. **Seed Property Data**:
   To populate the database with property data, execute:
   ```bash
   python -m app.seed_properties
   ```

---

## Running the Server

Start the FastAPI server with the following command:

```bash
uvicorn app.main:app --reload
```

This will start the server at `http://127.0.0.1:8000`

---

## API Endpoints

### Overview

1. **Root**:
   - `GET /`
   - Returns a welcome message.

2. **Health Check**:
   - `GET /health`
   - Verifies that the server is up and running.

3. **Payload**:
   - `POST /webhook/message`
   - Accepts a payload of guest message data for processing and classification.
   - Refer to the **Payload Testing** section for usage examples.

4. **Documentation (Swagger UI)**:
   - `GET /docs`
   - Interactive API documentation for testing endpoints directly.

---

### Payload Testing

#### PowerShell Example
```powershell
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

#### Bash Example
```bash
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

## Processing Flow

The following steps describe how webhook requests are processed:

1. **Webhook Request**:
   - Validate incoming requests.
   - Normalize message data into a unified schema.

2. **Classification**:
   - Classify the message using the **DeBERTA** model.
   - Persist the classified message in the database under `guest_messages`.

3. **AI Drafting**:
   - Use Claude AI to create a message response draft.
   - Attach property context and guardrails for secure data handling.

4. **Confidence Scoring**:
   - Assess confidence in responses using contextual metrics.
   - Decide the next action (e.g., notify staff, auto-reply).

5. **Response**:
   - Return the processed and classified data in an appropriate structure.

---

### Architectural Diagram

```text
                         ┌───────────────────────┐
                         │   Guest Channels      │
                         │───────────────────────│
                         │ • WhatsApp            │
                         │ • Booking.com         │
                         │ • Airbnb              │
                         │ • Instagram           │
                         │ • Direct              │
                         └──────────┬────────────┘
                                    │
                                    ▼
                     ┌───────────────────────────┐
                     │ FastAPI Webhook Endpoint  │
                     │ POST /webhook/message     │
                     └──────────┬────────────────┘
                                │
                                ▼
                   ┌──────────────────────────────┐
                   │ Payload Validation (Pydantic)│
                   └──────────┬───────────────────┘
                              │
                              ▼
                ┌──────────────────────────────────┐
                │ Message Normalization Layer      │
                │──────────────────────────────────│
                │ Unified Message Schema           │
                │ • message_id                     │
                │ • source                         │
                │ • guest_name                     │
                │ • message_text                   │
                │ • timestamp                      │
                │ • booking_ref                    │
                │ • property_id                    │
                │ • query_type                     │
                └──────────┬───────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼

┌──────────────────────────┐   ┌──────────────────────────┐
│ DeBERTa Intent Classifier│   │ PostgreSQL Database      │
│──────────────────────────│   │──────────────────────────│
│ Query Classification     │   │ guest_messages           │
│ • availability           │   │ properties               │
│ • pricing                │   └──────────┬───────────────┘
│ • complaints             │              │
│ • checkin                │              ▼
│ • special requests       │   ┌──────────────────────────┐
└──────────┬───────────────┘   │ Property Service Layer   │
           │                   │──────────────────────────│
           │                   │ Dynamic Property Context │
           │                   │ Retrieval                │
           │                   └──────────┬───────────────┘
           │                              │
           └──────────────┬───────────────┘
                          │
                          ▼
            ┌──────────────────────────────┐
            │ Operational Confidence Engine│
            │──────────────────────────────│
            │ Factors:                     │
            │ • context availability       │
            │ • ambiguity                  │
            │ • business risk              │
            │ • query type                 │
            └──────────┬───────────────────┘
                       │
                       ▼
               ┌──────────────────┐
               │ Claude AI Service│
               │──────────────────│
               │ Reply Drafting   │
               │ using:           │
               │ • guest message  │
               │ • query type     │
               │ • property data  │
               └────────┬─────────┘
                        │
                        ▼
              ┌───────────────────────┐
              │ Final API Response    │
              │───────────────────────│
              │ • drafted_reply       │
              │ • confidence_score    │
              │ • action              │
              │   - auto_send         │
              │   - agent_review      │
              │   - escalate          │
              └───────────────────────┘
```

---

## Model Setup

### Classifier Model

1. **Download**:
   - Download the classifier model from [HuggingFace](https://huggingface.co/zuccyzucc/guest_message_classifier).

2. **Extract**:
   - Place the model files inside the `app/` directory.

3. **Rename**:
   - Ensure the model folder is named `villa_bert_model` (or update the path in `app/classifier.py` as needed).

---

## Future Improvements

### Completed Improvements

1. **Smarter Classification**:
   - Integrated semantic classification using the DeBERTA model to enhance accuracy.

2. **Better Confidence Scoring**:
   - Developed a dedicated confidence scoring engine based on:
     - Operational coverage
     - Query ambiguity
     - Business risk

---

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


## Confidence Scoring System
The first implementation of the confidence scoring system was a very basic heuristical system. It used simple rules to determine the confidence score. 
The current system is a major improvement over the previous one. It uses the property context available to see whether the current query can be resolved completely from the information available in the context. If it does and the query is not a complaint(which always requires human escalation) it calculates the confidence score based on that. It also checks whether the query is too vague to for AI. Now all these systems are implemented mathematically but with more time (and ClaudeAPI balance) I would move forward from this to a similar implementation but with the help of ClaudeAPI itself. I can have the scoring system get some of the obscure details such as query clarity from ClaudeAPI itself as part of the reply message, then extract that information from the message, remove the information part from the message and pass forward the clean message. Using that information to improve the scoring system. 
