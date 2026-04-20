-- tables
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    region TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    event_type TEXT NOT NULL,
    location TEXT,
    event_date DATE NOT NULL,
    attendees INTEGER,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- sets index for attributes for future measurement
CREATE INDEX idx_events_event_type ON events(event_type);
CREATE INDEX idx_events_event_date ON events(event_date);
CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_type_date ON events(event_type, event_date);
CREATE INDEX idx_events_status_attendees ON events(status, attendees);

-- sets optimizer cost parameter
ALTER DATABASE event_analytics SET random_page_cost = 2.0;

-- collects statistics
ANALYZE users;
ANALYZE events;