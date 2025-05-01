import pyodbc
import pandas as panda


server = 'OE-5CD2266N-PLA'
database = 'tpcxbb_1gb'
username = 'sa'
password = 'P@ssword1'

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};TrustServerCertificate=yes;UID={username};PWD={password}'


conn = pyodbc.connect(connectionString)

input_query = '''
  SELECT
    ss_customer_sk AS customer,
    ROUND(COALESCE(returns_count / NULLIF(1.0*orders_count, 0), 0), 7) AS orderRatio,
    ROUND(COALESCE(returns_items / NULLIF(1.0*orders_items, 0), 0), 7) AS itemsRatio,
    ROUND(COALESCE(returns_money / NULLIF(1.0*orders_money, 0), 0), 7) AS monetaryRatio,
    COALESCE(returns_count, 0) AS frequency
    FROM
        (
          SELECT
            ss_customer_sk,
            -- return order ratio
            COUNT(distinct(ss_ticket_number)) AS orders_count,
            -- return ss_item_sk ratio
            COUNT(ss_item_sk) AS orders_items,
            -- return monetary amount ratio
            SUM( ss_net_paid ) AS orders_money
          FROM store_sales s
          GROUP BY ss_customer_sk
        ) orders

    LEFT OUTER JOIN
        (
          SELECT
            sr_customer_sk,
            -- return order ratio
            count(distinct(sr_ticket_number)) as returns_count,
            -- return ss_item_sk ratio
            COUNT(sr_item_sk) as returns_items,
            -- return monetary amount ratio
            SUM( sr_return_amt ) AS returns_money
          FROM store_returns
          GROUP BY sr_customer_sk 
          ) returned ON ss_customer_sk=sr_customer_sk'''




customer_data = panda.read_sql(input_query, conn)



print("Data frame:", customer_data.head(n=5))







