DROP TABLE IF EXISTS sales;

CREATE EXTERNAL TABLE IF NOT EXISTS sales (
    sale_id INT,
    seller_name STRING,
    card_name STRING,
    card_rarity STRING,
    card_condition STRING,
    price DOUBLE,
    quantity INT,
    sale_date DATE,
    card_set STRING,
    buyer_name STRING,
    transaction_status STRING
)
USING csv
OPTIONS (
    path '{{pwd}}/tests/.data/sales.csv',
    header 'true',
    inferSchema 'true'
);