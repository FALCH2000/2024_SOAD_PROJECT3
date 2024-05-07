-- SCRIPT DE CONSULTAS COMUNES 

-- Consulta para saber cuales comidas hay en la base de datos
SELECT * FROM Food;

-- Consulta para saber los tipos existentes de comida
SELECT * FROM Food_Type;

-- Consulta para saber cuales son las comidas y sus tipos
SELECT f.Name AS Food_Name, ft.Name AS Food_Type
FROM Food f
INNER JOIN Food_Type_Association fta ON f.ID = fta.Food_ID
INNER JOIN Food_Type ft ON fta.Type_ID = ft.ID;

-- Consulta para saber los postres con ID y Nombre
SELECT ID, Name
FROM Food
WHERE ID IN (
    SELECT Food_ID
    FROM Food_Type_Association
    WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Dessert')
);

-- Consulta para saber las bebidas con ID y Nombre
SELECT ID, Name
FROM Food
WHERE ID IN (
    SELECT Food_ID
    FROM Food_Type_Association
    WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Drink')
);

-- Consulta para saber los platos principales con ID y Nombre
SELECT ID, Name
FROM Food
WHERE ID IN (
    SELECT Food_ID
    FROM Food_Type_Association
    WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'MainCourse')
);

-- Consulta para saber las recomendaciones de comida segun el nombre de solo 1 comida
-- Si pongo una comida que no existe en la BD, no devuelve NADA
DECLARE @FoodName NVARCHAR(50) = 'Pizza Margarita';

-- Subconsulta para obtener el ID del plato basándose en su nombre
DECLARE @FoodID INT;
SELECT @FoodID = ID
FROM Food
WHERE Name = @FoodName;

-- Subonsulta para obtener la recomendacion disponible para una comida especifica
SELECT 
    Main_Dish.Name AS Main_Dish,
    Drink.Name AS Drink,
    Dessert.Name AS Dessert
FROM 
    Recommendation R
INNER JOIN 
    Food Main_Dish ON R.Main_Dish_ID = Main_Dish.ID
INNER JOIN 
    Food Drink ON R.Drink_ID = Drink.ID
INNER JOIN 
    Food Dessert ON R.Dessert_ID = Dessert.ID
WHERE 
    R.Main_Dish_ID = @FoodID OR R.Drink_ID = @FoodID OR R.Dessert_ID = @FoodID;

-- Consulta para saber las recomendaciones de comida segun el nombre de 2 comidas
-- En la segunda comida si paso un nombre que no esta asociado pero si existe como comida, da un
-- resultado default (el de la tercera comida asociada)
DECLARE @Food1 NVARCHAR(50) = 'Pizza Margarita'; -- Nombre de la primera comida
DECLARE @Food2 NVARCHAR(50) = 'Mojito'; -- Nombre de la segunda comida

-- Subconsulta para obtener el ID de las dos comidas especificadas
DECLARE @Food1ID INT;
DECLARE @Food2ID INT;

SELECT @Food1ID = ID FROM Food WHERE Name = @Food1;
SELECT @Food2ID = ID FROM Food WHERE Name = @Food2;

-- Subconsulta para encontrar la tercera comida de la recomendación
SELECT TOP 1
    Food.Name AS Third_Food
FROM 
    Recommendation R
JOIN 
    Food ON R.Main_Dish_ID = Food.ID OR R.Drink_ID = Food.ID OR R.Dessert_ID = Food.ID
WHERE 
    Food.ID NOT IN (@Food1ID, @Food2ID) 
    AND (R.Main_Dish_ID = @Food1ID OR R.Main_Dish_ID = @Food2ID 
        OR R.Drink_ID = @Food1ID OR R.Drink_ID = @Food2ID 
        OR R.Dessert_ID = @Food1ID OR R.Dessert_ID = @Food2ID);

-- Consulta para saber las reservaciones existentes
SELECT * FROM Reservations;

-- Consulta para saber la disponibilidad de las mesas
SELECT * FROM Table_Availability;

-- Consulta para saber las mesas de una reserva en particular
SELECT * 
FROM Reservation_Tables_Association 
WHERE Reservation_ID = 1;

-- Consulta para saber las mesas ocupadas en una fecha y hora especifica de las reservaciones existentes
DECLARE @DateReserved DATE = '2021-12-01';
DECLARE @StartTime TIME = '19:00:00';
DECLARE @EndTime TIME = '21:00:00';

SELECT 
    Table_Availability.Table_ID
FROM
    Table_Availability
JOIN
    Reservation_Tables_Association RTA ON Table_Availability.Table_ID = RTA.Table_ID
WHERE
    Table_Availability.Date_Reserved = @DateReserved
    AND Table_Availability.Start_Time = @StartTime
    AND Table_Availability.End_Time = @EndTime;

-- Consulta para insertar una nueva reserva considerando la disponibilidad de mesas

