import pyodbc

import mysql.connector

from IPython import embed

# MS SQL Server connection details

ms_sql_server = {

    'server': '172.26.1.14',

    'database': 'FalcaPOSQADB',

    'username': 'sa',

    'password': 'sql2014$', # Use Windows authentication

}


# MySQL Server connection details

mysql_server = {

    'host': 'localhost',

    'user': 'root',

    'password': 'Falca@1234',

    'database': 'suggi_prod_5thoct',

}


def copy_schema_and_data():

    try:

        # print("DRIVER={SQL Server};SERVER=172.26.1.14;DATABASE=FalcaPOSQADB;UID=sa;PWD=sql2014$;TrustServerCertificate=yes")

        # Connect to MS SQL Server using Windows authentication

        # ms_sql_conn = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server};SERVER=35.154.120.224,1433;DATABASE=FalcaPOSProdDB;UID=SHAKTI_USER;PWD=sHAKTI2023$!;TrustServerCertificate=yes")


        ms_sql_conn = pyodbc.connect(driver='{ODBC Driver 18 for SQL Server}',
                               server='35.154.120.224,1433',
                               database='FalcaPOSProdDB',
                               uid='SHAKTI_USER',
                               pwd='Viral@falca',
                               TrustServerCertificate='yes')
        # ms_sql_conn = pyodbc.connect(

        # f"DRIVER={{SQL Server}};SERVER={ms_sql_server['server']};DATABASE={ms_sql_server['database']};"

        # f"UID={ms_sql_server['username']};PWD={ms_sql_server['password']}")

        ms_sql_cursor = ms_sql_conn.cursor()


        print(ms_sql_conn)

        # Connect to MySQL Server

        mysql_conn = mysql.connector.connect(

            host=mysql_server['host'],

            user=mysql_server['user'],

            password=mysql_server['password'],

            database=mysql_server['database']

        )

        mysql_cursor = mysql_conn.cursor()


        # Get list of tables in MS SQL Server database

        ms_sql_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';")

        tables = ms_sql_cursor.fetchall()
        print(tables)
        for table in tables:

            table_name = table[0]
            # print(table_name)
            if table_name in ["'Supplier Codes$'","Seeds$","Fertlizers$","CPC$","Organics$","SpecilityNutrients$","ToolsImplements$","MissingCategory$","MissingCategory2$","'Falca POS Reports$'","Sheet1$","StateCodes$"]:
                continue


            # Fetch the schema structure from MS SQL Server
            ms_sql_cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table_name}';")

            columns = ms_sql_cursor.fetchall()
            print(columns)
            schema_columns = ', '.join([f"{col[3]} {col[7]}({col[8]})" if col[7] == 'VARCHAR' else f"{col[3]} {col[7]}" for col in columns])
            print(schema_columns)
            # schema_columns = schema_columns.replace("varchar", "text")
            schema_columns = schema_columns.replace("nvarchar", "text")
            schema_columns = schema_columns.replace("varchar", "text")
            schema_columns = schema_columns.replace("uniqueidentifier", "text")
            schema_columns = schema_columns.replace("bit", "text")
            print(table_name,schema_columns)



            # print(schema_columns)

            # Create the table in MySQL with the same schema
            print(f"CREATE TABLE {table_name} ({schema_columns});")
            print("===================")
            mysql_cursor.execute(f"CREATE TABLE {table_name} ({schema_columns});")

    


            # Fetch data from MS SQL Server and insert into MySQL

            ms_sql_cursor.execute(f"SELECT * FROM {table_name};")

            data_rows = ms_sql_cursor.fetchall()

            for row in data_rows:
                # if table_name in ["tblstockproduct"]:
                #     row[2] = ""
                #     values = ', '.join([f"'{value}'" if value is not None else "NULL" for value in row])
                #     values = values.replace("'True'",'1')
                #     values = values.replace("'False'",'0')
                    # print(values,table_name)
                    
                # elif table_name in ["tblattribute","tblcustomer","tblpurchaseorder","tbldistrict","tblmanufacture","tblskurequest","tblproduct","tblproducttype","tblsale_product_price_mapping","tblstate","tblstockproduct_invoice","tblstore","tblsupplier","tbluser","tblcreditnote","tblcategory","tblpincode","tblbank","tblsupplier_addresss_mapping","tblstore_deposit"] :
                #     values = ', '.join([f"'{value}'" if value is not None else "NULL" for value in row])
                #     values = values.replace("'True'",'1')
                #     values = values.replace("'False'",'0')
                

                # elif table_name in ["tblpurchaseorder_product_mapping","tblstore_assert","tblvillagename","VillageLists$"]:
                #     continue
                
                # else:
                values = ', '.join([f"'{value}'" if value is not None else "NULL" for value in row])
                
                try:
                    mysql_cursor.execute(f"INSERT INTO {table_name} VALUES ({values});")
                except Exception as e:
                    print(e)


            mysql_conn.commit()

        print("Schema and data copied successfully!")


    except Exception as e:

        print("An error occurred:", e)

    finally:

        ms_sql_cursor.close()

        ms_sql_conn.close()

        mysql_cursor.close()

        mysql_conn.close()


if __name__ == "__main__":

    copy_schema_and_data()