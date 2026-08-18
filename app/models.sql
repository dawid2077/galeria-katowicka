CREATE TABLE authors(
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    name TEXT NOT NULL ,
    surname TEXT NOT NULL
);

CREATE TABLE test (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    name VARCHAR(150) NOT NULL,
    author_id UUID REFERENCES authors(id) ON DELETE CASCADE,
    release_year INTEGER NOT NULL,
    quantity INTEGER NOT NULL

);
