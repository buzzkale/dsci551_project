from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from openai import OpenAI

# openai.api_key = "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"

client = MongoClient("mongodb://ec2-52-53-188-196.us-west-1.compute.amazonaws.com:27017/")
db = client.eurofootball
client_openai = OpenAI()


def nl2mongo(nl_query):
    # variables
    # print(f"Natural language query: {nl_query}")
    collections = ""
    context = ""
    prompt = ""

    # different context for different DBs
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
    
    return mongo_query

def mongo_query_results(mongo_query):
    # print(f"Generated MongoDB query: {mongo_query}")

    try:
        # turning string into Python code
        result = eval(mongo_query)
        
        # printing results
        # if isinstance(result, int) or isinstance(result, float):
        #     print(result)
        # else:
        #     for r in result:
        #         print(r)

        # result list
        result_list = []
        if isinstance(result, int) or isinstance(result, float):
            result_list.append(result)
        else:
            for r in result:
                result_list.append(r)
        
        return result_list, mongo_query

    except Exception as e:
        # print(f"Error executing MongoDB query: {e}")
        return e, mongo_query

# test code:
# selected_db, mongo_query = nl2mongo(2, "How many games did the league Premier League play in 2015?")
# mongo_query_results(selected_db, mongo_query)