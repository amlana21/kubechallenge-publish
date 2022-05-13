from fastapi import FastAPI,Response
from fastapi.responses import PlainTextResponse,JSONResponse
import uvicorn
from dotenv import load_dotenv
import os
# from processdata import scrape_data
from data_scrape_api.apicode.processdata import scrape_data

from prometheus_client import start_http_server, Gauge,generate_latest,CONTENT_TYPE_LATEST
METRICS_PORT=5001

global metrics_init
metrics_init=False

import redis
app = FastAPI()
load_dotenv()
from datetime import date

# if os.getenv('API_ENV') == 'DEV':
#     load_dotenv()


@app.get("/",response_class=JSONResponse)
async def root():
    print('hello')
    return {"message": "Hello World"}





@app.get("/exchangemetrics", response_class=PlainTextResponse)
async def root():
    r = redis.Redis(host=os.environ.get('REDIS_URL'), port=os.environ.get('REDIS_PORT'),password=os.environ.get('REDIS_PASSWORD'), db=0)
    scraped_data=0.0
    try:
        todays_date=str(date.today())        
        redis_key=f'exchange_rate-{todays_date}'
        tmpdata=r.get(redis_key)
        scraped_data=tmpdata.decode("utf-8")
    except Exception as e:
        print(e)
        print('responding default value')
    return f'exchange_rate_btc_usd {scraped_data}'


@app.get("/getexchangedata", response_class=PlainTextResponse)
async def root():
    r = redis.Redis(host=os.environ.get('REDIS_URL'), port=os.environ.get('REDIS_PORT'),
                    password=os.environ.get('REDIS_PASSWORD'), db=0)
    scraped_data = 0.0
    respdata="error"
    try:
        scraped_data = scrape_data()
        todays_date = str(date.today())
        r.set(f'exchange_rate-{todays_date}', scraped_data)
        respdata = "done"
    except Exception as e:
        print(e)
        print('responding default value')
        todays_date = str(date.today())
        r.set(f'exchange_rate-{todays_date}', scraped_data)
    return respdata




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)