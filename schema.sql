CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password VARCHAR(100) NOT NULL, is_admin BOOLEAN);
CREATE TABLE meals (id SERIAL PRIMARY KEY, name TEXT, user_id INTEGER REFERENCES users);
CREATE TABLE ingredients (id SERIAL PRIMARY KEY, name TEXT, user_id INTEGER REFERENCES users);
CREATE TABLE menus (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, timestamp TIMESTAMP);
CREATE TABLE menu_meals (menu_id INTEGER REFERENCES menus, meal_id INTEGER REFERENCES meals ON DELETE SET NULL, day_of_week INTEGER);
CREATE TABLE meal_ingredients (meal_id INTEGER REFERENCES meals ON DELETE CASCADE, ingredient_id INTEGER REFERENCES ingredients, quantity TEXT, qty_unit TEXT);
CREATE TABLE news (id SERIAL PRIMARY KEY, topic TEXT, news TEXT, date DATE);

CREATE UNIQUE INDEX unique_menus_per_week_for_user ON menus (user_id, DATE_PART('week', timestamp), DATE_PART('year', timestamp));
CREATE UNIQUE INDEX unique_ingredients_for_user ON ingredients (name, user_id);
CREATE UNIQUE INDEX unique_meals_for_user ON meals (name, user_id);
CREATE UNIQUE INDEX unique_meal_ingredients_for_user ON meal_ingredients (meal_id, ingredient_id);

CREATE FUNCTION after_delete()
  RETURNS trigger AS
$$
BEGIN
IF NOT EXISTS(SELECT 1 FROM meal_ingredients WHERE ingredient_id = OLD.ingredient_id) THEN
    DELETE FROM ingredients WHERE id = OLD.ingredient_id;
END IF;
RETURN OLD;
END;

$$
LANGUAGE 'plpgsql';

CREATE TRIGGER delete_ingredient_when_no_more_references
    AFTER DELETE ON meal_ingredients
    FOR EACH ROW
    EXECUTE PROCEDURE after_delete();