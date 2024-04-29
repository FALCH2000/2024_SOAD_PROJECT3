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


-- Insertar tipos de usuarios
INSERT INTO User_Type (Type_Name)
VALUES ('Admin'), ('Client');

-- Insertar usuarios clientes

-- Insertar usuarios administradores

-- Insertar recomendaciones de comidas
