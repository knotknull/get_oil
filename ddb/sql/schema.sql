CREATE TABLE pdo_prices (
	date  DATE PRIMARY KEY, 
	price DECIMAL(10,3), 
	tmstmp TIMESTAMP
);

CREATE TABLE test_prices (
	date  DATE PRIMARY KEY, 
	price DECIMAL(10,3), 
	tmstmp TIMESTAMP
);
