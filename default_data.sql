INSERT INTO meals (id, name, user_id)
VALUES
    (1, 'Makaronilaatikko', 1),
    (2, 'Uunimakkara', 1),
    (3, 'Pinaattiletut', 1),
    (4, 'Kanakeitto', 1),
    (5, 'Pizza', 1),
    (6, 'Avokadopasta', 1),
    (7, 'Nakkikeitto', 1),
    (8, 'Kanaa ja riisiä', 1),
    (9, 'Soijarouhe-bolognese', 1);

SELECT setval('meals_id_seq', (SELECT MAX(id) FROM meals));

INSERT INTO ingredients (id, name, user_id)
VALUES
    (1, 'Jauheliha', 1),
    (2, 'Makaroni', 1),
    (3, 'Juustoraaste', 1),
    (4, 'Sipuli', 1),
    (5, 'Koskenlaskija', 1),

    (6, 'Lenkkimakkara', 1),
    (7, 'Juusto', 1),
    (8, 'Ketsuppi', 1),
    (9, 'Sinappi', 1),

    (10, 'Pinaatti', 1),
    (11, 'Maito', 1),
    (12, 'Vehnäjauhoja', 1),
    (13, 'Kananmuna', 1),
    (14, 'Suolaa', 1),
    (15, 'Öljyä', 1),

    (16, 'Kanan fileesuikale', 1),
    (17, 'Peruna', 1),
    (18, 'Porkkana', 1),
    (19, 'Kanaliemikuutio', 1),

    (20, 'Pizzajauho', 1),
    (21, 'Kuivahiiva', 1),
    (22, 'Pepperoni', 1),
    (23, 'Mozzarella', 1),

    (24, 'Avokado', 1),
    (25, 'Spaghetti', 1),
    (26, 'Lime', 1),

    (27, 'Nakki, kuoreton', 1),
    (28, 'Lihaliemikuutio', 1),

    (29, 'Kanan filee', 1),
    (30, 'Riisi', 1),

    (31, 'Soijarouhe', 1),
    (32, 'Tomaattimurska', 1),
    (33, 'Valkosipuli', 1);

SELECT setval('ingredients_id_seq', (SELECT MAX(id) FROM ingredients));

INSERT INTO meal_ingredients (meal_id, ingredient_id, quantity, qty_unit)
VALUES
    (1, 1, 400, 'g'),
    (1, 2, 5, 'dl'),
    (1, 3, 2, 'dl'),
    (1, 4, 1, 'kpl'),
    (1, 5, 1, 'pkt'),

    (2, 6, 1, 'pkt'),
    (2, 7, 1, 'kpl'),
    (2, 8, 1, 'kpl'),
    (2, 9, 1, 'kpl'),

    (3, 10, 1, 'kpl'),
    (3, 11, 1, 'kpl'),
    (3, 12, 1, 'kpl'),
    (3, 13, 1, 'kpl'),
    (3, 14, 1, 'kpl'),
    (3, 15, 1, 'kpl'),

    (4, 16, 1, 'kpl'),
    (4, 17, 1, 'kpl'),
    (4, 18, 1, 'kpl'),
    (4, 19, 1, 'kpl'),
    (4, 4, 1, 'kpl'),

    (5, 20, 1, 'kpl'),
    (5, 21, 1, 'kpl'),
    (5, 22, 1, 'kpl'),
    (5, 23, 1, 'kpl'),
    (5, 15, 1, 'kpl'),

    (6, 24, 1, 'kpl'),
    (6, 25, 1, 'kpl'),
    (6, 26, 1, 'kpl'),
    
    (7, 27, 1, 'kpl'),
    (7, 28, 1, 'kpl'),
    (7, 17, 1, 'kpl'),
    (7, 18, 1, 'kpl'),

    (8, 29, 1, 'kpl'),
    (8, 30, 1, 'kpl'),
    (8, 19, 1, 'kpl'),

    (9, 31, 1, 'kpl'),
    (9, 32, 1, 'kpl'),
    (9, 33, 1, 'kpl'),
    (9, 25, 1, 'kpl'),
    (9, 4, 1, 'kpl');