-- Description: This script creates the database schema for the project.
-- SQL Server 2019 syntax

CREATE TABLE Food (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(50)
);

CREATE TABLE Food_Type (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(50)
);

CREATE TABLE Food_Type_Association (
    Type_ID INT,
    Food_ID INT,
    PRIMARY KEY (Type_ID, Food_ID)
);

CREATE TABLE Recommendation (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Main_Dish_ID INT,
    Beverage_ID INT,
    Dessert_ID INT
);

CREATE TABLE Associated_Reservations (
    Reservation_ID INT,
    Table_ID INT,
    PRIMARY KEY (Reservation_ID, Table_ID)
);

CREATE TABLE Reservations (
    Reservation_ID INT IDENTITY(1,1) PRIMARY KEY,
    User_ID NVARCHAR(50),
    Number_Of_People INT
);

CREATE TABLE Table_Availability (
    Table_ID INT,
    Date_Reserved DATE,
    Start_Time TIME,
    End_Time TIME, -- Should always be Start_Time + 2 hours
    PRIMARY KEY (Table_ID, Date_Reserved, Start_Time, End_Time)
);

CREATE TABLE Tables (
    Table_Number INT PRIMARY KEY,
    Chairs INT
);

CREATE TABLE User (
    Username NVARCHAR(50) PRIMARY KEY,
    Encrypted_Password NVARCHAR(50),
    First_Name NVARCHAR(50),
    Last_Name1 NVARCHAR(50),
    Last_Name2 NVARCHAR(50),
    Security_Question NVARCHAR(50),
    Security_Answer NVARCHAR(50)
);

CREATE TABLE User_Type (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Type_Name NVARCHAR(50)
);

CREATE TABLE User_Type_Association (
    Username NVARCHAR(50),
    Type_ID INT,
    PRIMARY KEY (Username, Type_ID)
);

CREATE TABLE Restaurant_Data (
    Local_ID INT IDENTITY(1,1) PRIMARY KEY,
    Opening_Time TIME,
    Closing_Time TIME,
    Local_Location NVARCHAR(50)
);

-- Adding foreign key constraints
ALTER TABLE Food_Type_Association
ADD CONSTRAINT FK_Food_Type_Association_Food_Type
FOREIGN KEY (Type_ID) 
REFERENCES Food_Type(ID);

ALTER TABLE Food_Type_Association
ADD CONSTRAINT FK_Food_Type_Association_Food
FOREIGN KEY (Food_ID) 
REFERENCES Food(ID);

ALTER TABLE Recommendation
ADD CONSTRAINT FK_Recommendation_Main_Dish
FOREIGN KEY (Main_Dish_ID) 
REFERENCES Food(ID);

ALTER TABLE Recommendation
ADD CONSTRAINT FK_Recommendation_Beverage
FOREIGN KEY (Beverage_ID) 
REFERENCES Food(ID);

ALTER TABLE Recommendation
ADD CONSTRAINT FK_Recommendation_Dessert
FOREIGN KEY (Dessert_ID) 
REFERENCES Food(ID);

ALTER TABLE Associated_Reservations
ADD CONSTRAINT FK_Associated_Reservations_Reservation
FOREIGN KEY (Reservation_ID) 
REFERENCES Reservations(Reservation_ID);

ALTER TABLE Associated_Reservations
ADD CONSTRAINT FK_Associated_Reservations_Table
FOREIGN KEY (Table_ID) 
REFERENCES Tables(Table_Number);

ALTER TABLE Reservations
ADD CONSTRAINT FK_Reservations_User
FOREIGN KEY (User_ID) 
REFERENCES [User](Username);

ALTER TABLE User_Type_Association
ADD CONSTRAINT FK_User_Type_Association_User
FOREIGN KEY (Username) 
REFERENCES [User](Username);

ALTER TABLE User_Type_Association
ADD CONSTRAINT FK_User_Type_Association_User_Type
FOREIGN KEY (Type_ID) 
REFERENCES User_Type(ID);
