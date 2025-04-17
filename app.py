from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

log_file = Path("query.txt")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search(query: str = Form(...), option: str = Form(...)):
    print(f"Received query: '{query}' with dropdown option: {option}")

    with log_file.open("w", encoding="utf-8") as f:
        f.write(f'["{query}", {option}]\n')

    file_path = Path("output.json")
    if not file_path.exists():
        return HTMLResponse(content="<p>No output file found.</p>", status_code=404)

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)  # this will now be a dict
    except Exception as e:
        return HTMLResponse(content=f"<p>Error reading output: {e}</p>", status_code=500)

    # Format as single vertical output
    html = "<h2>Query Result</h2>"
    html += "<div style='border:1px solid #ccc; padding:10px; margin-bottom:10px;'>"
    for key, value in data.items():
        html += f"<strong>{key}:</strong> {value}<br>"
    html += "</div>"

    return HTMLResponse(content=html)


@app.get("/logs", response_class=HTMLResponse)
async def read_logs():
    if not log_file.exists():
        return "<h2>No logs found.</h2>"

    with log_file.open("r", encoding="utf-8") as f:
        content = f.readlines()

    formatted = "<br>".join(line.strip() for line in content)
    return f"<h2>Logged Queries</h2><div>{formatted}</div>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
