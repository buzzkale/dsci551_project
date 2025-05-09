
import pymysql
from openai import OpenAI

# initial pymysql connection
connection = pymysql.connect(
    host="ec2-52-53-188-196.us-west-1.compute.amazonaws.com",
    port=3306,
    user="root",
    password="Dsci-351",
    database="bikestore"
)
db = connection
client_openai = OpenAI()

# SQL query
def nl_2_sql(nl_query):
    tables = "brands; categories; products"
    t1_fields = "brand_id (INT), brand_name (VARCHAR)"
    t2_fields = "category_id (INT), category_name (VARCHAR)"
    t3_fields = "product_id (INT), product_name (VARCHAR), brand_id (INT), category_id (INT), model_year (YEAR), list_price (FLOAT)"

    context = f"""
    The MySQL database I'm working with is about bike stores.
    It contains three tables: {tables}.
    The brands table contains the following fields: {t1_fields}.
    The categories table contains the following fields: {t2_fields}.
    The products table contains the following fields: {t3_fields}.
    """

    # prompt to gpt
    prompt = f"""
        {context}
        Convert the following natural language query into a SQL query compatible with MySQL. Return only the SQL query. Do not include any explanations or markdown. The result should be a single line:
        {nl_query}
    """

    # gpt response
    response = client_openai.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": "Please return SQL commands as a SQL expert"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        text={"format": {"type": "text"}},
        temperature=0
    )

    # cleaning response
    sql_query = response.output_text.strip()

    return sql_query


# Execute SQL query and return results
def sql_query_results(sql_query):
    try:
        with db.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            result_list = []
            if len(rows) == 1 and len(rows[0]) == 1 and isinstance(rows[0][0], (int, float)):
                # Single numeric result
                # print(rows[0][0])
                result_list.append(rows[0][0])
            else:
                # Multiple rows/columns
                for row in rows:
                    cleaned_row = tuple(
                        col.strip('\r') if isinstance(col, str) else col for col in row
                    )
                    # print(row)
                    result_list.append(row)

            return result_list, sql_query

    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return e, sql_query


# Test example (uncomment to run)
# nl_query = "What brands have the letter R?"
# sql = nl_2_sql(nl_query)
# results, executed_sql = sql_query_results(sql)
# print("SQL:", executed_sql)
# print("Results:", results)
