"""
Devuelve las comidas por cada tipo
SELECT * FROM Food
INNER JOIN Food_Type_Association
ON Food.ID = Food_Type_Association.Food_ID
WHERE Food_Type_Association.Type_ID = 1;

Devuelve los tipos de comida
SELECT * FROM Food_Type;
"""