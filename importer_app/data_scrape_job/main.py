from dotenv import load_dotenv
import requests
import os
import json
load_dotenv()
if __name__=="__main__":
    try:
        qry_url = f'{os.environ.get("API_URL")}/getexchangedata'
        response = requests.request("GET", qry_url)
        print(response.text)
    except Exception as e:
        print(e)
        print('responding default value')

