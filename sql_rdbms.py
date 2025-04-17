
import pymysql
import openai

openai.api_key = "your-api-key"



class ChatDB_SQL:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.database = database

    def close(self):
        self.connection.close()

    def list_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            return [row[f'Tables_in_{self.database}'] for row in cursor.fetchall()]

    def get_table_schema(self, table_name):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table_name};")
            return cursor.fetchall()

    def get_sample_rows(self, table_name, limit=5):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
            return cursor.fetchall()

    def nl_to_sql(self, nl_query, table_info=""):
        prompt = f"""
Database Info:
{table_info}
Query:
\"{nl_query}\"
"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate the following commands into SQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        sql_query = response['choices'][0]['message']['content'].strip()
        return sql_query

    def execute_sql(self, sql_query):
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
            if cursor.description:
                return cursor.fetchall()
            else:
                self.connection.commit()
                return f"{cursor.rowcount} row(s) affected."


if __name__ == "__main__":
    db = ChatDB_SQL(host="localhost", user="root")

    # Get table info for prompt context
    tables = db.list_tables()
    schema_info = ""
    for t in tables:
        schema = db.get_table_schema(t)
        schema_info += f"Table: {t}\nColumns: " + ", ".join(col["Field"] for col in schema) + "\n\n"

    # db.close()
