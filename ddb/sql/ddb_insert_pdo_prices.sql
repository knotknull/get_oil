insert into pdo_prices (price, date, tmstmp) values (3.339, '2025-02-26', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.289, '2025-02-27', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.289, '2025-02-28', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.289, '2025-03-01', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.289, '2025-03-02', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.289, '2025-03-03', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.289, '2025-03-04', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.289, '2025-03-05', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.229, '2025-03-06', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.229, '2025-03-07', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.229, '2025-03-08', current_localtimestamp());





map@hexagon:/sql/> tail -2 ddb_insert_test_prices.sql
insert into test_prices (price, date, tmstmp) values (3.229, '2025-03-07', current_localtimestamp());
insert into test_prices (price, date, tmstmp) values (3.229, '2025-03-08', current_localtimestamp());
map@hexagon:/sql/> tail -2 ddb_insert_pdo_prices.sql
insert into pdo_prices (price, date, tmstmp) values (3.229, '2025-03-07', current_localtimestamp());
insert into pdo_prices (price, date, tmstmp) values (3.229, '2025-03-08', current_localtimestamp());

