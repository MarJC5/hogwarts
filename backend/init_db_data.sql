-- Initial data for Hogwarts House Points System

-- Add Wizards (Students)
INSERT INTO wizards (name, house, wand, patronus) VALUES
-- Gryffindor students
('Harry Potter', 'Gryffindor', 'Holly and Phoenix feather, 11 inches', 'Stag'),
('Hermione Granger', 'Gryffindor', 'Vine wood and Dragon heartstring, 10¾ inches', 'Otter'),
('Ron Weasley', 'Gryffindor', 'Willow and Unicorn hair, 14 inches', 'Jack Russell Terrier'),
('Neville Longbottom', 'Gryffindor', 'Cherry and Unicorn hair, 13 inches', 'Non-corporeal'),
('Ginny Weasley', 'Gryffindor', 'Yew, unknown core', 'Horse'),

-- Slytherin students
('Draco Malfoy', 'Slytherin', 'Hawthorn and Unicorn hair, 10 inches', NULL),
('Pansy Parkinson', 'Slytherin', 'Unknown', NULL),
('Blaise Zabini', 'Slytherin', 'Unknown', NULL),
('Gregory Goyle', 'Slytherin', 'Unknown', NULL),
('Vincent Crabbe', 'Slytherin', 'Unknown', NULL),

-- Ravenclaw students
('Luna Lovegood', 'Ravenclaw', 'Unknown', 'Hare'),
('Cho Chang', 'Ravenclaw', 'Unknown', 'Swan'),
('Padma Patil', 'Ravenclaw', 'Unknown', NULL),
('Terry Boot', 'Ravenclaw', 'Unknown', NULL),
('Michael Corner', 'Ravenclaw', 'Unknown', NULL),

-- Hufflepuff students
('Cedric Diggory', 'Hufflepuff', 'Ash, 12¼ inches, unicorn hair', NULL),
('Hannah Abbott', 'Hufflepuff', 'Unknown', NULL),
('Susan Bones', 'Hufflepuff', 'Unknown', NULL),
('Justin Finch-Fletchley', 'Hufflepuff', 'Unknown', NULL),
('Ernie Macmillan', 'Hufflepuff', 'Unknown', NULL);

-- Add Teachers
INSERT INTO teachers (name, subject, house) VALUES
('Albus Dumbledore', 'Headmaster', NULL),
('Minerva McGonagall', 'Transfiguration', 'Gryffindor'),
('Severus Snape', 'Potions', 'Slytherin'),
('Filius Flitwick', 'Charms', 'Ravenclaw'),
('Pomona Sprout', 'Herbology', 'Hufflepuff'),
('Rubeus Hagrid', 'Care of Magical Creatures', NULL),
('Horace Slughorn', 'Potions', 'Slytherin'),
('Remus Lupin', 'Defense Against the Dark Arts', NULL),
('Sybill Trelawney', 'Divination', NULL),
('Gilderoy Lockhart', 'Defense Against the Dark Arts', NULL);

-- Add House Points
-- Note: You'll need to adjust the teacher_id and wizard_id values based on the actual IDs assigned by your database
-- The examples below assume specific IDs which may be different in your actual database

-- Gryffindor points
INSERT INTO house_points (house, points, reason, teacher_id, wizard_id) VALUES
('Gryffindor', 50, 'Saving the Philosophers Stone', 1, 1),  -- Dumbledore awards Harry
('Gryffindor', 10, 'Answering correctly in Transfiguration class', 2, 2),  -- McGonagall awards Hermione
('Gryffindor', 5, 'Bravery in Herbology class', 5, 4),  -- Sprout awards Neville
('Gryffindor', -10, 'Out after curfew', 3, 3),  -- Snape deducts from Ron
('Gryffindor', 20, 'Excellence in Charms', 4, 2),  -- Flitwick awards Hermione

-- Slytherin points
INSERT INTO house_points (house, points, reason, teacher_id, wizard_id) VALUES
('Slytherin', 15, 'Perfect potion brewing', 3, 6),  -- Snape awards Draco
('Slytherin', 10, 'Helping in classroom setup', 3, 7),  -- Snape awards Pansy
('Slytherin', 5, 'Correct answer in Potions', 7, 8),  -- Slughorn awards Blaise
('Slytherin', -5, 'Disruptive behavior', 2, 9),  -- McGonagall deducts from Goyle
('Slytherin', 20, 'Prefect duties', 3, 6),  -- Snape awards Draco

-- Ravenclaw points
INSERT INTO house_points (house, points, reason, teacher_id, wizard_id) VALUES
('Ravenclaw', 25, 'Outstanding Charms essay', 4, 11),  -- Flitwick awards Luna
('Ravenclaw', 15, 'Creative spell application', 4, 12),  -- Flitwick awards Cho
('Ravenclaw', 10, 'Excellence in Transfiguration', 2, 13),  -- McGonagall awards Padma
('Ravenclaw', -5, 'Late to class', 3, 14),  -- Snape deducts from Terry
('Ravenclaw', 20, 'Helping younger students', 4, 15),  -- Flitwick awards Michael

-- Hufflepuff points
INSERT INTO house_points (house, points, reason, teacher_id, wizard_id) VALUES
('Hufflepuff', 30, 'Exceptional teamwork', 5, 16),  -- Sprout awards Cedric
('Hufflepuff', 15, 'Helping in the greenhouses', 5, 17),  -- Sprout awards Hannah
('Hufflepuff', 10, 'Kindness to first years', 1, 18),  -- Dumbledore awards Susan
('Hufflepuff', 5, 'Good participation in class', 6, 19),  -- Hagrid awards Justin
('Hufflepuff', -5, 'Forgotten homework', 3, 20);  -- Snape deducts from Ernie

-- House-wide points (with no specific student)
INSERT INTO house_points (house, points, reason, teacher_id, wizard_id) VALUES
('Gryffindor', 100, 'Winning the Quidditch match', 2, NULL),
('Slytherin', 50, 'Best decorated common room', 3, NULL),
('Ravenclaw', 75, 'Highest average in examinations', 4, NULL),
('Hufflepuff', 60, 'Community service project', 5, NULL); 