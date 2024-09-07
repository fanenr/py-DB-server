CREATE TABLE IF NOT EXISTS teacher (
  id serial PRIMARY KEY,
  username varchar UNIQUE NOT NULL,
  password varchar NOT NULL,
  name varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS student (
  id serial PRIMARY KEY,
  username varchar UNIQUE NOT NULL,
  password varchar NOT NULL,
  name varchar NOT NULL,
  start date NOT NULL
);

CREATE TABLE IF NOT EXISTS course (
  id serial PRIMARY KEY,
  tid integer REFERENCES teacher (id),
  name varchar NOT NULL,
  start date NOT NULL
);

CREATE TABLE IF NOT EXISTS grade (
  id serial PRIMARY KEY,
  cid integer REFERENCES course (id),
  sid integer REFERENCES student (id),
  tid integer REFERENCES teacher (id),
  score integer CHECK (score BETWEEN 0 AND 100)
);
