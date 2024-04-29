-- Script de consultas comunes para la base de datos

-- Si necesita borrar todas las instancias de una tabla, sin borrar la tabla en si, puede usar el siguiente comando:
-- DELETE FROM Food_Type_Association;

-- Consulta para saber cuales son las comidas y sus tipos
SELECT f.Name AS Food_Name, ft.Name AS Food_Type
FROM Food f
INNER JOIN Food_Type_Association fta ON f.ID = fta.Food_ID
INNER JOIN Food_Type ft ON fta.Type_ID = ft.ID;

-- Consulta para saber los ID de las comidas junto con el ID de su tipo de comida
SELECT * FROM Food_Type_Association

-- Consulta para saber los tipos de comida
SELECT * FROM Food_Type;

-- Consulta para saber cuales comidas hay en la base de datos
SELECT * FROM Food;
