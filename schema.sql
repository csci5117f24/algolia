CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    details TEXT NOT NULL,
    sport TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);