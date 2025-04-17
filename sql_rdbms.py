
import pymysql
import openai
import sys

openai.api_key = "your-api-key"

# initial pymysql connection
def __init__(self, host, user, password, database):
    self.connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )
    self.database = database

# SQL query
def nl_to_sql(self, nl_query, table, key):
    try:
        # Confirm SQL key
        if key != 0:
            sys.exit(0)

        # Proceed with the normal flow if key is 0
        prompt = f"Database: {table}\nQuery: {nl_query}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate the following commands into SQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        sql_query = response['choices'][0]['message']['content'].strip()

        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
            if cursor.description:
                return cursor.fetchall()
            else:
                self.connection.commit()
                return f"{cursor.rowcount} row(s) affected."

    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    db = ChatDB_SQL(host="localhost", user="root")

    # Get table info for prompt context
    tables = db.list_tables()
    schema_info = ""
    for t in tables:
        schema = db.get_table_schema(t)
        schema_info += f"Table: {t}\nColumns: " + ", ".join(col["Field"] for col in schema) + "\n\n"

    # db.close()
