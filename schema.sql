-- Nistula Unified Messaging Platform Schema

-- I will first define core entities
-- Phyical : 1. Guest 2. Property 3. Reservation 4. Message
-- Logical : Channel Identites, Conversations, 

-- Why am I using different tables for guest and channel identites?
-- Because storing all channel handles in guest will require a
-- column for each channel and it would not be scalable.

-- guests table 
-- contains basic guest info - id, name, email(if exists), phone(if exists)
CREATE TABLE guests(
	guest_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	full_name VARCHAR(50),
	email VARCHAR(255) UNIQUE,
	phone VARCHAAR(20),
	created_at TIMESTAMPZ NOT NULL DEFUALT now(),
	updated_at TIMESTAMPZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_guests_email ON guests (email);
CREATE INDEX idx_guest_phone ON guests (phone);

-- channel_name enumerated so that we can fill this and only this in channel column

CREATE TYPE channel_name AS ENUM(
	'whatsapp',
	'booking_com',
	'airbnb',
	'instagram',
	'direct'
);

-- channel identities pivot table
-- maps a guest to their handle on each channel
-- a guest may have a whatsapp no., an airbnb profile - all linked to one guest row.
-- lookup path: (channel, channel_handle) -> guest_id
CREATE TABLE channel_identities (
	identity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	guest_id UUID NOT NULL REFERENCES guests (guest_id) ON DELETE CASCADE,
	channel channel_name NOT NULL,
	channel_handle VARCHAR(255) NOT NULL,
	created_at TIMESTAMPZ NOT NULL DEFAULT now(),

	UNIQUE (channel, channel_handle)
);

CREATE INDEX idx_channel_identities_guest ON channel_identities (guest_id);
CREATE INDEX idx_channel_identities_lookup ON channel_identities (channel, channel_handle);

-- properties table
-- operational context per property.
-- i have taken some context from from the first problem , although this is different
-- that the properties table i have used in the first problen statement.
-- this table is made so that guests can be linked to a property after reservation
CREATE TABLE properties (
    property_id VARCHAR(100) PRIMARY KEY,
    property_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    bedrooms SMALLINT,
    max_guests SMALLINT,
    private_pool BOOLEAN DEFAULT FALSE,
    check_in_time TIME,
    check_out_time TIME,
    base_rate_usd NUMERIC(10, 2),
    extra_guest_rate_usd NUMERIC(10, 2),
    wifi_password VARCHAR(255),
    caretaker_hours VARCHAR(100),
    chef_on_call BOOLEAN DEFAULT FALSE,
    availability TEXT,
    cancellation_policy TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- reservations_status enumerate for the same reason as channel_name
CREATE TYPE reservation_status AS ENUM (
    'confirmed',
    'checked_in',
    'checked_out',
    'cancelled'
);

-- reservations table 
CREATE TABLE reservations (
    reservation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id VARCHAR(100) NOT NULL REFERENCES properties (property_id),
    guest_id UUID NOT NULL REFERENCES guests (guest_id),
    booking_ref VARCHAR(100) UNIQUE,
    status reservation_status NOT NULL DEFAULT 'confirmed',
    check_in_date DATE,
    check_out_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_reservations_guest ON reservations (guest_id);
CREATE INDEX idx_reservations_property ON reservations (property_id);
CREATE INDEX idx_reservations_booking_ref ON reservations (booking_ref);

-- Conversation status enumarated to classify conversations
CREATE TYPE conversation_status AS ENUM (
    'open',
    'resolved',
    'escalated'
);

-- conversation table groups messages from one guest on one channel around one reservation
-- reservation_id is nullable as pre_sales_enquiries also arrive before booking. 
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id UUID NOT NULL REFERENCES guests (guest_id),
    reservation_id UUID REFERENCES reservations (reservation_id),
    channel channel_name NOT NULL,
    status conversation_status NOT NULL DEFAULT 'open',
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_message_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_conversations_guest ON conversations (guest_id);
CREATE INDEX idx_conversations_reservation ON conversations (reservation_id);
CREATE INDEX idx_conversations_status ON conversations (status);

-- Messages 
-- Every inbound and outbound message in one table .
-- using the same table for tracking the message, AI confidence score and query type
CREATE TYPE message_direction AS ENUM ('inbound', 'outbound');

CREATE TYPE query_type AS ENUM (
    'pre_sales_availability',
    'pre_sales_pricing',
    'post_sales_checkin',
    'special_request',
    'complaint',
    'general_enquiry'
);

CREATE TYPE action_type AS ENUM (
    'auto_send',
    'agent_review',
    'escalate'
);

CREATE TYPE draft_origin AS ENUM (
    'ai_drafted',
    'agent_written',
-- this is actually part of future scalability at the time of writing this    
    'template'
);


CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations (conversation_id),

    -- keeping inbound outbound messages in same table helps retrieve compete threads faster
    direction message_direction NOT NULL,
    channel channel_name NOT NULL,

    -- the exact message sent by the guest, used for DeBERTa
    raw_text TEXT NOT NULL,

    -- Classification (inbound only; NULL on outbound rows)
    query_type query_type,
    operational_confidence NUMERIC(4, 3),

    -- tracking what action was taken (was the message Auto_sent, Agent_reviewed or Escalated)
    action_taken action_type,

    -- Reply tracking
    draft_origin draft_origin,
    drafted_reply TEXT,
    sent_reply TEXT,
    -- this is useful to know in which queries , an agent edited the text for further training of our model
    agent_edited BOOLEAN DEFAULT FALSE,

    received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    sent_at TIMESTAMPTZ
);

CREATE INDEX idx_messages_conversation ON messages (conversation_id);
CREATE INDEX idx_messages_direction ON messages (direction);
CREATE INDEX idx_messages_query_type ON messages (query_type);
CREATE INDEX idx_messages_action ON messages (action_taken);
CREATE INDEX idx_messages_received_at ON messages (received_at DESC);


-- I have tried to keep the least amount of tables while maintaining normalization
-- and honestly it was the hardest part of my design decision. I had to choose between 
-- making my schema this way or in a much more modular way. One can tell by looking at
-- my schema design the lack of joins. It was one of the major considerations I made during 
-- the design. If you look at the messages table, you'd notice that there are two columns 
-- that stay null always when a message direction is inbound. Now it is not ideal but the other 
-- solution was to seperate inbound and outbound messages. The problem with that is that for 
-- recreating any message thread, it would require a lot of joins. And if the table size grows huge 
-- , those joins would go slower and slower.
-- My current design is more suited for monolithic applications where we don't have to worry much about
-- very large traffic, which I assume is the case for Nistula right now. 