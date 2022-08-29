DROP TABLE IF EXISTS police_department_calls_for_service;
DROP TABLE IF EXISTS original_crime_type_name;
DROP TABLE IF EXISTS disposition;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS agency_id;
DROP TABLE IF EXISTS address_type;

CREATE TABLE original_crime_type_name
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE
);

CREATE TABLE disposition
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE
);

CREATE TABLE city
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE
);

CREATE TABLE state
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE
);

CREATE TABLE agency_id
(
  id SERIAL PRIMARY KEY,
  name INTEGER UNIQUE
);

CREATE TABLE address_type
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE
);

CREATE table police_department_calls_for_service
(
  id SERIAL PRIMARY KEY,
  crime_id BIGINT,
  original_crime_type_name_id INTEGER,
  FOREIGN key (original_crime_type_name_id) REFERENCES original_crime_type_name(id),
  report_date TIMESTAMP,
  call_date TIMESTAMP,
  offense_date TIMESTAMP,
  call_time TIME,
  call_date_time TIMESTAMP,
  disposition_id INTEGER,
  FOREIGN KEY (disposition_id) REFERENCES disposition(id),
  address VARCHAR(100),
  city_id INTEGER,
  FOREIGN KEY (city_id) REFERENCES city(id),
  state_id INTEGER,
  FOREIGN KEY (state_id) REFERENCES state(id),
  agency_id INTEGER,
  FOREIGN KEY (agency_id) REFERENCES agency_id(id),
  address_type_id INTEGER,
  FOREIGN KEY (address_type_id) REFERENCES address_type(id),
  common_location VARCHAR(100)
);