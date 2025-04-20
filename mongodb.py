from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from openai import OpenAI
import json
from bson.json_util import dumps
import ast

# openai.api_key = "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"

client = MongoClient("mongodb://localhost:27017/")
client_openai = OpenAI()

def nl2mongo(db_selection, nl_query):
    # variables
    print(f"Natural language query: {nl_query}")
    db = None
    collections = ""
    context = ""
    prompt = ""

    # different context for different DBs
    if db_selection == 1:
        db = client.linkinpark
        collections = "linkin_park_youtube; linkin_park_youtube_comments"
        c1_fields = "ID (int),Video ID (string),Title (string),Thumbnail URL (string),Published At (datetime),Channel ID (string),Channel Title (string),View Count (int),Like Count (int),Dislike Count (int)"
        c2_fields = "ID (int),Video ID (string),Comment (string),Commenter (string),Comment Datetime (datetime),Sentiment (string)"
        context = f"""
        The MongoDB database I'm working with is about Linkin Park YouTube videos.
        It contains two collections: {collections}.
        The linkin_park_youtube collection contains the following fields: {c1_fields}.
        The linkin_park_youtube_comments collection contains the following fields: {c2_fields}
        """
    elif db_selection == 2:
        db = client.eurofootball
        collections = "teams; leagues; games"
        c1_fields = "teamID (int), name (string)"
        c2_fields = "leagueID (int),name (string),understatNotation (string)"
        c3_fields = "gameID (int),leagueID (int),season (int),date (datetime),homeTeamID (int),awayTeamID (int),homeGoals (int),awayGoals (int),homeProbability (float),drawProbability (float),awayProbability (float)"
        context = f"""
        The MongoDB database I'm working with is about professional European football.
        It contains three collections: {collections}.
        The teams collection contains the following fields: {c1_fields}.
        The leagues collection contains the following fields: {c2_fields}.
        The games collection contains the following fields: {c3_fields}.
        """
    elif db_selection == 3:
        db = client.bikestore
        collections = "brands; categories; products"
        c1_fields = "brand_id (int),brand_name (string)"
        c2_fields = "category_id (int),category_name (string)"
        c3_fields = "product_id (int),product_name (string),brand_id (int),category_id (int),model_year (int),list_price (float)"
        context = f"""
        The MongoDB database I'm working with is about bikes.
        It contains three collections: {collections}.
        The brands collection contains the following fields: {c1_fields}.
        The categories collection contains the following fields: {c2_fields}.
        The products collection contains the following fields: {c3_fields}.
        """

    # prompt to gpt
    prompt = f"""
        {context}.
        Convert the following natural language query into a MongoDB query. Return only the mongodb query. Do not include any explanations or markdown. I will be evaluating the query through PyMongo, so make sure the keys are in quotes. The result be a single line:
        {nl_query}
    """

    # print(f"PROMPT: {prompt}")
    
    # gpt response
    response = client_openai.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": "You are a MongoDB expert."
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
    mongo_query = response.output_text.strip()
    
    return db, mongo_query

def mongo_query_results(db, mongo_query):
    print(f"Generated MongoDB query: {mongo_query}")

    try:
        # turning string into Python code
        result = eval(mongo_query)
        
        # printing results
        if isinstance(result, int) or isinstance(result, float):
            print(result)
        else:
            for r in result:
                print(r)


    except Exception as e:
        print(f"Error executing MongoDB query: {e}")

# test code:
selected_db, mongo_query = nl2mongo(2, "How many games did the league Premier League play in 2015?")
mongo_query_results(selected_db, mongo_query)