CREATE TABLE teacher (
  id serial PRIMARY KEY,
  username varchar UNIQUE NOT NULL,
  password varchar NOT NULL,
  name varchar NOT NULL
);

CREATE TABLE student (
  id serial PRIMARY KEY,
  username varchar UNIQUE NOT NULL,
  password varchar NOT NULL,
  semester integer NOT NULL,
  name varchar NOT NULL
);

CREATE TABLE course (
  id serial PRIMARY KEY,
  tid integer REFERENCES teacher (id),
  semester integer NOT NULL,
  name varchar NOT NULL
);

CREATE TABLE grade (
  id serial PRIMARY KEY,
  sid integer REFERENCES student (id),
  tid integer REFERENCES teacher (id),
  cid integer REFERENCES course (id),
  score integer
);
