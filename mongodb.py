from pymongo import MongoClient
import openai
# from bson.json_util import dumps

openai.api_key = "your-api-key"

# connect to mongodb
client = MongoClient()
dsci551 = client.dsci551

def nl2mongo(db, nl_query):
    # variables
    collection = ""
    context = ""

    #
    if db == 1:
        collection = "drake"
        fields = "album, lyrics_title (title of song), lyrics_url, lyrics, track_views"
        context = f"The MongoDB collection I'm working with is about Drake lyrics. It contains the following fields: {fields}. The fields are not nested."
    elif db == 2:
        collection = "parliament"
        fields = "PersonID, PhotoURL (can be empty), Notes (can be empty), BirthDate, BirthDateIsProtected, ParliamentaryName, PreferredName, GenderTypeID, IsCurrent"
        context = f"The MongoDB collection I'm working with is about Scottish Parliament members. It contains the following fields: {fields}. The fields are not nested"
    elif db == 3:
        collection = "wine"
        fields = "points, title, description, taster_name, taster_twitter_handle, price, variety, region_1, region_2, province, country, winery"
        context = f"The MongoDB collection I'm working with is about wine reviews. It contains the following fields: {fields}. The fields are not nested."

    prompt = f"{context}\
                The name of the collection is \"{collection}\"\
                Convert the following natural language query into a MongoDB query in Python using PyMongo:\n\
                {nl_query}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a Python MongoDB expert."},
                  {"role": "user", "content": prompt}]
    )

    mongo_query = response["choices"][0]["message"]["content"].strip()
    
    return collection, mongo_query

def mongo_query_results(collection_name, mongo_query):
    print(f"Generated MongoDB query: {mongo_query}")

    collection = dsci551[collection_name]
    
    try:
        mongo_filter_dict = eval(mongo_query, {"__builtins__": None}, {})
    except Exception as e:
        print(f"Error evaluating filter: {e}")
        return

    result = collection.find(mongo_filter_dict)

    # TODO
    # convert result to json

    # for obj in result:
    # print(obj)

    return loads(dumps(result))