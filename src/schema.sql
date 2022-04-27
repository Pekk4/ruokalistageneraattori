CREATE TABLE meals (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE users (id SERIAL PRIMARY KEY, username UNIQUE TEXT, password TEXT);
--CREATE TABLE menus (id SERIAL PRIMARY KEY, meal_ids INTEGER REFERENCES meals, user_id INTEGER REFERENCES users, date DATE);
--CREATE TABLE menus (id SERIAL PRIMARY KEY, meal_ids INTEGER[], user_id INTEGER, date DATETIME);
--CREATE TABLE menus (id SERIAL PRIMARY KEY, meal_ids INTEGER[], user_id INTEGER, TIMESTAMP TIMESTAMP);
CREATE TABLE menus (id SERIAL PRIMARY KEY, user_id INTEGER, timestamp TIMESTAMP, week_number, INTEGER);
create table menu_meals (id SERIAL PRIMARY KEY, menu_id INTEGER REFERENCES menus, meal_id INTEGER REFERENCES meals);

CREATE TABLE menus (id SERIAL PRIMARY KEY, user_id INTEGER, timestamp TIMESTAMP);
CREATE UNIQUE INDEX test ON menus (user_id, DATE_PART('week', timestamp), DATE_PART('year', timestamp));

--INSERT INTO menus (user_id, timestamp) VALUES (1, now()) ON CONFLICT (user_id, DATE_PART('week', timestamp), DATE_PART('year', timestamp)) DO UPDATE SET timestamp = '2022-04-19 16:30:30.416533';

--menu_meals:ille indexi poistoa varten?
