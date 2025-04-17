from pymongo import MongoClient
import openai
import json
from bson.json_util import dumps

openai.api_key = "your-api-key"

client = MongoClient()
# dsci551 = client.dsci551

def nl2mongo(db_selection, nl_query):
    # variables
    db = None
    collections = ""
    context = ""

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
        Convert the following natural language query into a MongoDB query. Return only the mongodb query. Do not include any explanations or markdown. The result be a single line:\n
        {nl_query}
    """
    
    # gpt response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a MongoDB expert."},
                  {"role": "user", "content": prompt}]
    )

    mongo_query = response["choices"][0]["message"]["content"].strip()
    
    return db, mongo_query

def mongo_query_results(db, mongo_query):
    print(f"Generated MongoDB query: {mongo_query}")
    
    try:
        # get collection and filtering
        collection_name = mongo_query.split(".find(")[0].split(".")[-1]
        raw_filter = mongo_query.split(".find(")[1].rstrip(")")
        # turn string into dictionary
        mongo_filter = eval(raw_filter) if raw_filter.strip() else {}

        # execute query
        collection = db[collection_name]
        result = collection.find(mongo_filter)

        print(f"\nResults from collection '{collection_name}':\n")
        for doc in result:
            print(json.loads(dumps(doc)))

    except Exception as e:
        print(f"Error executing MongoDB query: {e}")