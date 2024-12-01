--To set up a foundational schema for the database intended to store RDF triples efficiently in a relational structure

CREATE TABLE IF NOT EXISTS triples (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    predicate VARCHAR(255) NOT NULL,
    object TEXT NOT NULL,
    UNIQUE (subject, predicate, object) --to prevent duplicate triples

-- Create indexes on the 'subject' and 'predicate' columns to improve query performance
CREATE INDEX IF NOT EXISTS idx_subject ON triples (subject);
CREATE INDEX IF NOT EXISTS idx_predicate ON triples (predicate);

--without scanning every row, these can accelerate queries like SEARCH queries and sorting related queries