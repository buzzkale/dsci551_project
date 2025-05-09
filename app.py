from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# import mongodb
import sql_rdbms

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search(query: str = Form(...), option: str = Form(...)):
    print(f"Received query: '{query}' with DB option: {option}")
    
    try:
        if (int(option)== 1):
            # TODO: implement sql
            sql_query = sql_rdbms.nl_2_sql(query)
            result, raw_query = sql_rdbms.sql_query_results(sql_query)

            html = "<h2>Query Result</h2>"
            html += f"<p><strong>SQL Query:</strong> <code>{raw_query}</code></p>"
            html += "<div style='border:1px solid #ccc; padding:10px; margin-top:10px;'>"

            if isinstance(result, Exception):
                html += f"<p style='color:red;'>Error: {result}</p>"
            elif isinstance(result, (int, float, str)):
                html += f"<p>{result}</p>"
            elif isinstance(result, list):
                if not result:
                    html += "<p>No results found.</p>"
                else:
                    for i, item in enumerate(result):
                        html += f"<pre><strong>Result {i+1}</strong>: {item}</pre>"
            else:
                html += f"<pre>{result}</pre>"

            html += "</div>"
            return HTMLResponse(content=html)
        elif (int(option)==2):
            mongo_query = mongodb.nl2mongo(query)
            result, raw_query = mongodb.mongo_query_results(mongo_query)

            html = "<h2>Query Result</h2>"
            html += f"<p><strong>MongoDB Query:</strong> <code>{raw_query}</code></p>"
            html += "<div style='border:1px solid #ccc; padding:10px; margin-top:10px;'>"

            if isinstance(result, Exception):
                html += f"<p style='color:red;'>Error: {result}</p>"
            elif isinstance(result, (int, float, str)):
                html += f"<p>{result}</p>"
            elif isinstance(result, list):
                if not result:
                    html += "<p>No results found.</p>"
                else:
                    for i, item in enumerate(result):
                        html += f"<pre><strong>Result {i+1}</strong>: {item}</pre>"
            else:
                html += f"<pre>{result}</pre>"

            html += "</div>"
            return HTMLResponse(content=html)
        

    except Exception as e:
        return HTMLResponse(content=f"<p style='color:red;'>Server Error: {e}</p>", status_code=500)
