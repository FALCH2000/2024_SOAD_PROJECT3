-- Insert tipos de alimentos
INSERT INTO Food_Type (Name)
VALUES ('MainCourse'), ('Drink'), ('Dessert');

-- Insert MainCourses
INSERT INTO Food (Name)
VALUES ('Pizza Margarita'), ('Spaghetti Carbonara'), ('Lasagna'), ('Chicken Alfredo'),
       ('Beef Wellington'), ('Sushi'), ('Burger'), ('Risotto'), ('Pad Thai'),
       ('Tacos'), ('Paella'), ('Fish and Chips'), ('Pho'), ('Curry'), ('Fajitas'),
       ('Pasta Carbonara'), ('Steak'), ('Roast Chicken'), ('Sushi'), ('Hamburger');

-- Insert Desserts
INSERT INTO Food (Name)
VALUES ('Tiramisu'), ('Cheesecake'), ('Chocolate Fondant'), ('Apple Pie'), ('Creme Brulee'),
       ('Banoffee Pie'), ('Panna Cotta'), ('Key Lime Pie'), ('Red Velvet Cake'), ('Cannoli'),
       ('Baklava'), ('Pavlova'), ('Cupcakes'), ('Chocolate Mousse'), ('Gelato'),
       ('Creme Brulee'), ('Tiramisu'), ('Chocolate Cake'), ('Apple Crisp'), ('Peach Cobbler');

-- Insert Drinks
INSERT INTO Food (Name)
VALUES ('Mojito'), ('Margarita'), ('Martini'), ('Cosmopolitan'), ('Gin and Tonic'),
       ('Pina Colada'), ('Daiquiri'), ('Tequila Sunrise'), ('Bloody Mary'), ('Mai Tai'),
       ('Old Fashioned'), ('White Russian'), ('Long Island Iced Tea'), ('Singapore Sling'),
       ('Moscow Mule'), ('Margarita'), ('Gin and Tonic'), ('Martini'), ('Sangria'),
       ('Negroni');

-- Insertar las asociaciones entre los tipos de comida y las comidas

-- Obtener los IDs de los tipos de comida
DECLARE @MainCourseID INT;
DECLARE @DessertID INT;
DECLARE @DrinkID INT;

SELECT @MainCourseID = ID FROM Food_Type WHERE Name = 'MainCourse';
SELECT @DessertID = ID FROM Food_Type WHERE Name = 'Dessert';
SELECT @DrinkID = ID FROM Food_Type WHERE Name = 'Drink';

-- Asociar MainCourses
INSERT INTO Food_Type_Association (Type_ID, Food_ID)
SELECT @MainCourseID, ID FROM Food WHERE Name IN (
    'Pizza Margarita', 'Spaghetti Carbonara', 'Lasagna', 'Chicken Alfredo',
    'Beef Wellington', 'Sushi', 'Burger', 'Risotto', 'Pad Thai',
    'Tacos', 'Paella', 'Fish and Chips', 'Pho', 'Curry', 'Fajitas',
    'Pasta Carbonara', 'Steak', 'Roast Chicken'
);

-- Asociar Desserts
INSERT INTO Food_Type_Association (Type_ID, Food_ID)
SELECT @DessertID, ID FROM Food WHERE Name IN (
    'Tiramisu', 'Cheesecake', 'Chocolate Fondant', 'Apple Pie', 'Creme Brulee',
    'Banoffee Pie', 'Panna Cotta', 'Key Lime Pie', 'Red Velvet Cake', 'Cannoli',
    'Baklava', 'Pavlova', 'Cupcakes', 'Chocolate Mousse', 'Gelato',
    'Creme Brulee', 'Tiramisu', 'Chocolate Cake', 'Apple Crisp', 'Peach Cobbler'
);

-- Asociar Drinks
INSERT INTO Food_Type_Association (Type_ID, Food_ID)
SELECT @DrinkID, ID FROM Food WHERE Name IN (
    'Mojito', 'Margarita', 'Martini', 'Cosmopolitan', 'Gin and Tonic',
    'Pina Colada', 'Daiquiri', 'Tequila Sunrise', 'Bloody Mary', 'Mai Tai',
    'Old Fashioned', 'White Russian', 'Long Island Iced Tea', 'Singapore Sling',
    'Moscow Mule', 'Margarita', 'Gin and Tonic', 'Martini', 'Sangria',
    'Negroni'
);

-- Insertar asociaciones faltantes
INSERT INTO Food_Type_Association (Type_ID, Food_ID)
VALUES (1, 20);


-- Insertar tipos de usuarios
INSERT INTO User_Type (Type_Name)
VALUES ('Admin'), ('Client');

-- Insertar usuarios
-- password = "admin1"
-- security answer = "Blue"
INSERT INTO User_ (Username, Encrypted_Password, First_Name, Last_Name1, Last_Name2, Security_Question, Security_Answer)
VALUES ('admin1', '25f43b1486ad95a1398e3eeb3d83bc4010015fcc9bedb35b43', 'Jimena', 'Leon', 'Huertas', 'What is your favorite color?', 'ec7d56a01607001e6401366417c5e2eb00ffa0df17ca1a9a8');
-- password = "admin1"
-- security answer = "Blue"
INSERT INTO User_ (Username, Encrypted_Password, First_Name, Last_Name1, Last_Name2, Security_Question, Security_Answer)
VALUES ('client1', '25f43b1486ad95a1398e3eeb3d83bc4010015fcc9bedb35b43', 'Fulana', 'Perez', 'Gonzalez', 'What is your favorite color?', 'ec7d56a016');

-- Asocia usuarios con el tipo de usuario Admin
INSERT INTO User_Type_Association (Username, Type_ID)
VALUES ('admin1', 1);
-- Asocia usuarios con el tipo de usuario Client
INSERT INTO User_Type_Association (Username, Type_ID)
VALUES ('client1', 2);

-- Insertar mesas
INSERT INTO Tables (Table_Number, Chairs)
VALUES (1, 4), (2, 6), (3, 2), (4, 8), (5, 4), (6, 6), (7, 2), (8, 8), (9, 4), (10, 6);

-- Insertar reservaciones
INSERT INTO Reservations (User_ID, Number_Of_People, Date_Reserved, Start_Time, End_Time)
VALUES ('client1', 4, '2021-12-01', '18:00:00', '20:00:00'),
       ('client1', 6, '2021-12-01', '16:00:00', '18:00:00'),
       ('client1', 2, '2021-12-01', '15:00:00', '17:00:00'),
       ('client1', 8, '2021-12-01', '20:00:00', '22:00:00'),
       ('client1', 13, '2021-12-01', '19:00:00', '21:00:00');

-- Insertar disponibilidad de mesas
INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time)
VALUES (1, '2021-12-01', '18:00:00', '20:00:00'),
       (2, '2021-12-01', '16:00:00', '18:00:00'),
       (3, '2021-12-01', '15:00:00', '17:00:00'),
       (4, '2021-12-01', '20:00:00', '22:00:00'),
       (5, '2021-12-01', '19:00:00', '21:00:00'), -- Table for 4 
       (8, '2021-12-01', '19:00:00', '21:00:00'); -- Table for 8

-- Insertar asociaciones entre reservaciones y mesas
INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID)
VALUES (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (5, 8); -- Reservation 5 uses tables 5 and 8

-- Insert Restaurant Information
INSERT INTO Restaurant_Data (Opening_Time, Closing_Time, Local_Location)
VALUES ('12:00:00', '20:00:00', 'Barrio Escalante');

-- Insert data into Recommendation table
-- Obtener los IDs de los platos principales, bebidas y postres
DECLARE @MainCourseID INT;
DECLARE @DrinkID INT;
DECLARE @DessertID INT;

SELECT @MainCourseID = MIN(Food_ID) FROM Food_Type_Association WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'MainCourse');
SELECT @DrinkID = MIN(Food_ID) FROM Food_Type_Association WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Drink');
SELECT @DessertID = MIN(Food_ID) FROM Food_Type_Association WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Dessert');

-- Insertar recomendaciones emparejando platos principales con bebidas y postres
DECLARE @Counter INT = 1;

WHILE @MainCourseID IS NOT NULL
BEGIN
    INSERT INTO Recommendation (Main_Dish_ID, Drink_ID, Dessert_ID)
    VALUES (@MainCourseID, @DrinkID, @DessertID);

    -- Obtener los IDs de los siguientes platos principales, bebidas y postres
    SELECT @MainCourseID = MIN(Food_ID) FROM Food_Type_Association WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'MainCourse') AND Food_ID > @MainCourseID;
    SELECT @DrinkID = MIN(Food_ID) FROM Food_Type_Association WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Drink') AND Food_ID > @DrinkID;
    SELECT @DessertID = MIN(Food_ID) FROM Food_Type_Association WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Dessert') AND Food_ID > @DessertID;

    SET @Counter = @Counter + 1;
END;

INSERT INTO Recommendation (Main_Dish_ID, Drink_ID, Dessert_ID)
VALUES (20, 60, 40);