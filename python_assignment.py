import sqlite3
import pandas as pd


filename = r'C:\Users\Jerome Cura\Desktop\Assignment Python' # change depend the location of file
sqliteConnection = None
try:
    sqliteConnection = sqlite3.connect(f'{filename}\S30 ETL Assignment.db')
    cursor = sqliteConnection.cursor()

    orders = pd.read_sql("SELECT * FROM 'orders'", sqliteConnection)
    sales = pd.read_sql("SELECT * FROM 'sales'", sqliteConnection)
    items = pd.read_sql("SELECT * FROM 'items'", sqliteConnection)
    customers = pd.read_sql("SELECT * FROM 'customers'", sqliteConnection)


    orderSales = pd.merge(orders, sales, how="inner", on=["sales_id", "sales_id"])
    orderSalesItems = pd.merge(orderSales, items, how="inner", on=["item_id", "item_id"])
    orderSalesItemsCustomer = pd.merge(orderSalesItems, customers, how="inner", on=["customer_id", "customer_id"])
    orderSalesItemsCustomer1 = orderSalesItemsCustomer.groupby(['item_id', 'customer_id']).agg({
        "customer_id": "first",
        "age" : "first",
        "item_name": "first",
        "quantity":"sum"
        })
    orderSalesItemsCustomer1.reset_index(drop = True, inplace = True)

    orderSalesItemsCustomer1['quantity'] = orderSalesItemsCustomer1['quantity'].astype('int')
    orderSalesItemsCustomer1 = orderSalesItemsCustomer1[orderSalesItemsCustomer1['quantity'] > 0]
    orderSalesItemsCustomer2 = orderSalesItemsCustomer1[orderSalesItemsCustomer1['age'].between(18, 35)]
    SortValorderSalesItemsCustomer1 = orderSalesItemsCustomer2.sort_values(by='customer_id', ascending=True)
    colRenaming = {'customer_id':'Customer',
                   'age':'Age',
                   'item_name':'Item',
                   'quantity' : 'Quantity'
                    }
    SortValorderSalesItemsCustomer1.rename(columns = colRenaming, inplace=True)

    SortValorderSalesItemsCustomer1.to_csv('csvdata.csv', sep=';', header=True, index=False)

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")