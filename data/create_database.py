import mysql.connector as ddd


conn = ddd.connect(
    host="localhost",
    user="root",
    password="toor"
)

cursor = conn.cursor()





sf1 = """ DROP DATABASE IF EXISTS `sql_inventory`  """ 
sf2 = """ CREATE DATABASE `sql_inventory` """
sf3 = """ USE `sql_inventory` """
sf4 = """ 
    CREATE TABLE `products` (
        `product_id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(50) NOT NULL,
        `quantity_in_stock` int(11) NOT NULL,
        `unit_price` decimal(4,2) NOT NULL,
        PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
"""

sf5 = """ 
INSERT INTO `products` (name, quantity_in_stock, unit_price) VALUES 
			('Laptop', 70, 80.12),
			('PC', 49, 200.25),
			('Camios', 700, 4.24)
"""

formulas = [sf1, sf2, sf3, sf4, sf5]

[cursor.execute(s) for s in formulas]

conn.commit()


