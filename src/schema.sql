CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);

CREATE TABLE meals (id SERIAL PRIMARY KEY, name TEXT, user_id INTEGER REFERENCES users);
CREATE TABLE ingredients (id SERIAL PRIMARY KEY, name TEXT, user_id INTEGER REFERENCES users);
CREATE TABLE menus (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, timestamp TIMESTAMP);

CREATE TABLE menu_meals (menu_id INTEGER REFERENCES menus, meal_id INTEGER REFERENCES meals, day_of_week INTEGER);
CREATE TABLE meal_ingredients (meal_id INTEGER REFERENCES meals, ingredient_id INTEGER REFERENCES ingredients);

CREATE UNIQUE INDEX unique_menus_per_week ON menus (user_id, DATE_PART('week', timestamp), DATE_PART('year', timestamp));
CREATE UNIQUE INDEX unique_ingredients_for_user ON ingredients (name, user_id);
