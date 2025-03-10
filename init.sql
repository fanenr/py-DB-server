DROP TABLE IF EXISTS grade CASCADE;
DROP TABLE IF EXISTS course CASCADE;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS teacher CASCADE;

CREATE TABLE IF NOT EXISTS teacher (
  id SERIAL PRIMARY KEY,
  username VARCHAR UNIQUE NOT NULL,
  password VARCHAR NOT NULL,
  name VARCHAR NOT NULL,
  start DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS student (
  id SERIAL PRIMARY KEY,
  username VARCHAR UNIQUE NOT NULL,
  password VARCHAR NOT NULL,
  name VARCHAR NOT NULL,
  start DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS course (
  id SERIAL PRIMARY KEY,
  tid INTEGER REFERENCES teacher (id),
  name VARCHAR NOT NULL,
  start DATE NOT NULL,
  UNIQUE (tid, name)
);

CREATE TABLE IF NOT EXISTS grade (
  id SERIAL PRIMARY KEY,
  cid INTEGER NOT NULL REFERENCES course (id),
  sid INTEGER NOT NULL REFERENCES student (id),
  score INTEGER CHECK (score BETWEEN 0 AND 100),
  UNIQUE (cid, sid)
);
