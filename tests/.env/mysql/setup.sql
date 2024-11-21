CREATE DATABASE IF NOT EXISTS ploosh;

USE ploosh;

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_name VARCHAR(100) NOT NULL,
    card_name VARCHAR(100) NOT NULL,
    card_rarity VARCHAR(50),
    card_condition VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    quantity INT,
    sale_date DATE,
    card_set VARCHAR(100),
    buyer_name VARCHAR(100),
    transaction_status VARCHAR(50)
);

INSERT INTO sales (seller_name, card_name, card_rarity, card_condition, price, quantity, sale_date, card_set, buyer_name, transaction_status)
VALUES
('John Doe', 'Charizard', 'Rare', 'Mint', 250.00, 1, '2024-11-01', 'Base Set', 'Jane Smith', 'Completed'),
('Jane Smith', 'Blastoise', 'Holo Rare', 'Excellent', 180.00, 1, '2024-11-02', 'Base Set', 'Alex Johnson', 'Completed'),
('Alex Johnson', 'Pikachu', 'Common', 'Near Mint', 15.00, 4, '2024-11-03', 'Jungle', 'Chris Brown', 'Completed'),
('Chris Brown', 'Dragonite', 'Ultra Rare', 'Good', 300.00, 1, '2024-11-04', 'Fossil', 'Emma Green', 'Pending'),
('Emma Green', 'Zapdos', 'Holo Rare', 'Mint', 150.00, 1, '2024-11-05', 'Fossil', 'Sarah White', 'Completed'),
('Sarah White', 'Venusaur', 'Rare', 'Good', 120.00, 2, '2024-11-06', 'Base Set', 'John Doe', 'Completed'),
('Liam Brown', 'Moltres', 'Rare', 'Near Mint', 140.00, 1, '2024-11-07', 'Fossil', 'Jane Smith', 'Completed'),
('Olivia Taylor', 'Articuno', 'Rare', 'Excellent', 100.00, 1, '2024-11-08', 'Fossil', 'Alex Johnson', 'Cancelled'),
('Sophia Wilson', 'Eevee', 'Common', 'Mint', 20.00, 3, '2024-11-09', 'Jungle', 'Chris Brown', 'Completed'),
('Mason Martinez', 'Jolteon', 'Rare', 'Near Mint', 80.00, 1, '2024-11-10', 'Jungle', 'Emma Green', 'Completed'),
('Ethan White', 'Flareon', 'Rare', 'Excellent', 85.00, 1, '2024-11-11', 'Jungle', 'Sarah White', 'Completed'),
('Lucas Harris', 'Vaporeon', 'Rare', 'Mint', 100.00, 1, '2024-11-12', 'Jungle', 'Liam Brown', 'Completed'),
('Amelia Clark', 'Machamp', 'Holo Rare', 'Mint', 75.00, 1, '2024-11-13', 'Base Set', 'Olivia Taylor', 'Completed'),
('Harper Lewis', 'Gengar', 'Rare', 'Mint', 80.00, 1, '2024-11-14', 'Fossil', 'Sophia Wilson', 'Completed'),
('Evelyn Walker', 'Snorlax', 'Rare', 'Mint', 90.00, 1, '2024-11-15', 'Jungle', 'Mason Martinez', 'Completed'),
('Henry King', 'Charizard', 'Rare', 'Excellent', 250.00, 1, '2024-11-16', 'Base Set', 'Ethan White', 'Completed'),
('Isabella Moore', 'Mewtwo', 'Holo Rare', 'Near Mint', 220.00, 1, '2024-11-17', 'Fossil', 'Lucas Harris', 'Completed'),
('Sophia Wilson', 'Articuno', 'Rare', 'Mint', 120.00, 1, '2024-11-18', 'Fossil', 'Amelia Clark', 'Completed'),
('Liam Brown', 'Pikachu', 'Common', 'Good', 10.00, 5, '2024-11-19', 'Jungle', 'Harper Lewis', 'Pending'),
('Emma Green', 'Moltres', 'Rare', 'Excellent', 140.00, 1, '2024-11-20', 'Fossil', 'Evelyn Walker', 'Completed'),
('Chris Brown', 'Blastoise', 'Holo Rare', 'Mint', 180.00, 1, '2024-11-21', 'Base Set', 'Henry King', 'Completed'),
('Alex Johnson', 'Eevee', 'Common', 'Mint', 25.00, 2, '2024-11-22', 'Jungle', 'Isabella Moore', 'Completed'),
('John Doe', 'Dragonite', 'Ultra Rare', 'Near Mint', 320.00, 1, '2024-11-23', 'Base Set', 'Jane Smith', 'Pending'),
('Jane Smith', 'Machamp', 'Holo Rare', 'Good', 70.00, 1, '2024-11-24', 'Base Set', 'Alex Johnson', 'Completed'),
('Sarah White', 'Vaporeon', 'Rare', 'Excellent', 100.00, 1, '2024-11-25', 'Jungle', 'Chris Brown', 'Cancelled'),
('Olivia Taylor', 'Jolteon', 'Rare', 'Mint', 85.00, 1, '2024-11-26', 'Jungle', 'Emma Green', 'Completed'),
('Henry King', 'Zapdos', 'Holo Rare', 'Good', 140.00, 1, '2024-11-27', 'Fossil', 'Sophia Wilson', 'Completed'),
('Ethan White', 'Gengar', 'Rare', 'Excellent', 75.00, 1, '2024-11-28', 'Fossil', 'Mason Martinez', 'Completed'),
('Amelia Clark', 'Mewtwo', 'Holo Rare', 'Mint', 230.00, 1, '2024-11-29', 'Fossil', 'Ethan White', 'Completed'),
('Lucas Harris', 'Charizard', 'Rare', 'Near Mint', 250.00, 1, '2024-11-30', 'Base Set', 'Lucas Harris', 'Completed'),
('Harper Lewis', 'Snorlax', 'Rare', 'Excellent', 90.00, 1, '2024-12-01', 'Jungle', 'Liam Brown', 'Completed'),
('Sophia Wilson', 'Flareon', 'Rare', 'Good', 85.00, 1, '2024-12-02', 'Jungle', 'Isabella Moore', 'Pending'),
('Mason Martinez', 'Articuno', 'Rare', 'Mint', 120.00, 1, '2024-12-03', 'Fossil', 'Harper Lewis', 'Completed'),
('Emma Green', 'Moltres', 'Holo Rare', 'Mint', 140.00, 1, '2024-12-04', 'Fossil', 'Henry King', 'Completed'),
('John Doe', 'Pikachu', 'Common', 'Mint', 15.00, 3, '2024-12-05', 'Jungle', 'Chris Brown', 'Completed'),
('Jane Smith', 'Dragonite', 'Ultra Rare', 'Excellent', 300.00, 1, '2024-12-06', 'Base Set', 'Sophia Wilson', 'Completed'),
('Alex Johnson', 'Machamp', 'Holo Rare', 'Mint', 75.00, 1, '2024-12-07', 'Base Set', 'Emma Green', 'Completed'),
('Chris Brown', 'Vaporeon', 'Rare', 'Good', 90.00, 1, '2024-12-08', 'Jungle', 'John Doe', 'Completed'),
('Olivia Taylor', 'Jolteon', 'Rare', 'Near Mint', 80.00, 1, '2024-12-09', 'Jungle', 'Jane Smith', 'Pending'),
('Ethan White', 'Gengar', 'Rare', 'Mint', 85.00, 1, '2024-12-10', 'Fossil', 'Liam Brown', 'Completed'),
('Amelia Clark', 'Eevee', 'Common', 'Excellent', 25.00, 3, '2024-12-11', 'Jungle', 'Olivia Taylor', 'Completed'),
('Sophia Wilson', 'Charizard', 'Rare', 'Good', 220.00, 1, '2024-12-12', 'Base Set', 'Alex Johnson', 'Cancelled'),
('Lucas Harris', 'Zapdos', 'Holo Rare', 'Mint', 150.00, 1, '2024-12-13', 'Fossil', 'Emma Green', 'Completed'),
('Harper Lewis', 'Mewtwo', 'Ultra Rare', 'Near Mint', 200.00, 1, '2024-12-14', 'Fossil', 'Sarah White', 'Completed'),
('Henry King', 'Lapras', 'Rare', 'Mint', 95.00, 1, '2024-12-16', 'Fossil', 'Sophia Wilson', 'Completed'),
('Ethan White', 'Ditto', 'Rare', 'Excellent', 85.00, 1, '2024-12-17', 'Fossil', 'Amelia Clark', 'Completed'),
('Sarah White', 'Bulbasaur', 'Common', 'Near Mint', 12.00, 5, '2024-12-18', 'Base Set', 'Lucas Harris', 'Completed'),
('Emma Green', 'Charmander', 'Common', 'Mint', 15.00, 4, '2024-12-19', 'Base Set', 'Chris Brown', 'Pending'),
('Jane Smith', 'Squirtle', 'Common', 'Good', 10.00, 6, '2024-12-20', 'Base Set', 'Mason Martinez', 'Completed'),
('John Doe', 'Jigglypuff', 'Common', 'Excellent', 8.00, 10, '2024-12-21', 'Jungle', 'Liam Brown', 'Completed'),
('Olivia Taylor', 'Clefairy', 'Rare', 'Mint', 50.00, 1, '2024-12-22', 'Base Set', 'Ethan White', 'Completed'),
('Lucas Harris', 'Nidoking', 'Holo Rare', 'Good', 125.00, 1, '2024-12-23', 'Base Set', 'John Doe', 'Cancelled'),
('Alex Johnson', 'Hitmonchan', 'Holo Rare', 'Near Mint', 100.00, 1, '2024-12-24', 'Base Set', 'Jane Smith', 'Completed'),
('Sophia Wilson', 'Kangaskhan', 'Rare', 'Excellent', 80.00, 1, '2024-12-25', 'Jungle', 'Henry King', 'Completed'),
('Chris Brown', 'Scyther', 'Rare', 'Mint', 85.00, 1, '2024-12-26', 'Jungle', 'Emma Green', 'Completed'),
('Harper Lewis', 'Pinsir', 'Rare', 'Near Mint', 70.00, 1, '2024-12-27', 'Jungle', 'Olivia Taylor', 'Completed'),
('Mason Martinez', 'Aerodactyl', 'Rare', 'Good', 100.00, 1, '2024-12-28', 'Fossil', 'Sarah White', 'Completed'),
('Liam Brown', 'Kabutops', 'Rare', 'Mint', 105.00, 1, '2024-12-29', 'Fossil', 'Alex Johnson', 'Completed'),
('Evelyn Walker', 'Magikarp', 'Common', 'Excellent', 5.00, 20, '2024-12-30', 'Base Set', 'Lucas Harris', 'Completed'),
('Amelia Clark', 'Gyarados', 'Holo Rare', 'Near Mint', 150.00, 1, '2024-12-31', 'Base Set', 'Sophia Wilson', 'Pending'),
('Sarah White', 'Ditto', 'Rare', 'Mint', 90.00, 1, '2025-01-01', 'Fossil', 'Henry King', 'Completed'),
('Emma Green', 'Pidgeot', 'Rare', 'Good', 70.00, 1, '2025-01-02', 'Jungle', 'Chris Brown', 'Completed'),
('John Doe', 'Electabuzz', 'Rare', 'Excellent', 60.00, 2, '2025-01-03', 'Base Set', 'Liam Brown', 'Completed'),
('Jane Smith', 'Magmar', 'Rare', 'Mint', 55.00, 1, '2025-01-04', 'Fossil', 'Mason Martinez', 'Completed'),
('Olivia Taylor', 'Jynx', 'Common', 'Excellent', 30.00, 3, '2025-01-05', 'Base Set', 'Ethan White', 'Completed'),
('Alex Johnson', 'Alakazam', 'Holo Rare', 'Mint', 175.00, 1, '2025-01-06', 'Base Set', 'Jane Smith', 'Completed'),
('Sophia Wilson', 'Chansey', 'Holo Rare', 'Good', 100.00, 1, '2025-01-07', 'Base Set', 'Olivia Taylor', 'Completed'),
('Chris Brown', 'Geodude', 'Common', 'Near Mint', 5.00, 12, '2025-01-08', 'Base Set', 'John Doe', 'Completed'),
('Henry King', 'Grimer', 'Common', 'Excellent', 7.00, 8, '2025-01-09', 'Fossil', 'Emma Green', 'Completed'),
('Ethan White', 'Muk', 'Rare', 'Mint', 85.00, 1, '2025-01-10', 'Fossil', 'Sophia Wilson', 'Completed'),
('Harper Lewis', 'Rhydon', 'Rare', 'Good', 75.00, 1, '2025-01-11', 'Jungle', 'Chris Brown', 'Cancelled'),
('Mason Martinez', 'Tauros', 'Common', 'Near Mint', 10.00, 10, '2025-01-12', 'Jungle', 'Alex Johnson', 'Completed'),
('Evelyn Walker', 'Exeggutor', 'Rare', 'Mint', 65.00, 1, '2025-01-13', 'Jungle', 'Sarah White', 'Completed'),
('Lucas Harris', 'Venonat', 'Common', 'Excellent', 5.00, 15, '2025-01-14', 'Jungle', 'Harper Lewis', 'Pending');


CREATE VIEW sales_by_seller AS 
    SELECT 
        seller_name,
        SUM(price) AS total_sales
    FROM sales 
        WHERE transaction_status = 'Completed' 
    GROUP BY seller_name 
    ORDER BY total_sales DESC;