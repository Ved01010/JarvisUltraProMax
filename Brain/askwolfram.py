import wolframalpha
from APIs.wolfapi import mrwolfapi

# I have set my API in APIs folder with a python file with mrwolfapi as a variable which has the WolframAlpha API Key
# Add your own API by creating a variable here and replace the (mrwolfapi) to your own variable which has your API
wolf_asker = wolframalpha.Client(mrwolfapi) # you have to replace it here


def ask_mr_wolf(query):
    try:
        res = wolf_asker.query(query)
        answer = next(res.results).text
        return answer
    except Exception as e:
        return f"Sorry i couldn't find that answer {e}"
