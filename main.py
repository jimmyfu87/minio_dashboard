import os
from datetime import datetime

import pandas as pd
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
bucket_summary_file_path = 'buckets_summary.csv'

def get_bucket_data(path: str):
    bucket_data = pd.read_csv(path, index_col=0)
    return bucket_data


def get_bucket_last_update_time(path: str):
   bucket_last_update_time = datetime.fromtimestamp(os.path.getmtime(path))
   return bucket_last_update_time


def get_status_num(data: pd.DataFrame):
    cautious_num = len(data[data['status']=='Cautious'])
    aware_num = len(data[data['status']=='Aware'])
    healthy_num = len(data[data['status']=='Healthy'])
    return cautious_num, aware_num, healthy_num


@app.get("/", response_class=HTMLResponse)
def tables(request: Request):
    bucket_data = get_bucket_data(bucket_summary_file_path)
    bucket_last_update_time = get_bucket_last_update_time(bucket_summary_file_path)
    cautious_num, aware_num, healthy_num = get_status_num(bucket_data)
    return templates.TemplateResponse("index.html", {"request": request, "results": bucket_data, 
                                                      "cautious_num": cautious_num,
                                                      "aware_num": aware_num,
                                                      "healthy_num": healthy_num,
                                                      'last_update_time': bucket_last_update_time})


@app.get("/get_top_use_ratio_bucket")
def get_top_usage_bucket():
    bucket_data = get_bucket_data(bucket_summary_file_path)
    bucket_num = len(bucket_data)
    top_use_ratio = bucket_data.sort_values(by=['use_ratio'], ascending=False)
    if bucket_num>5:
        top_use_ratio = top_use_ratio[0:5]
    bucket_ls = top_use_ratio['bucket_name'].tolist()
    use_ratio_ls = top_use_ratio['use_ratio'].tolist()
    use_ratio_ls = [round(i, 2) for i in use_ratio_ls]
    return  {"bucket": bucket_ls, "use_ratio": use_ratio_ls}


@app.get("/get_top_management_unit")
def get_top_management_unit():
    bucket_data = get_bucket_data(bucket_summary_file_path)
    bucket_num = len(bucket_data)
    top_unit = bucket_data.value_counts('management_unit')
    if bucket_num>5:
        top_unit = top_unit[0:5]
    unit_ls = top_unit.index.tolist()
    unit_num_ls = top_unit.tolist()
    return  {"unit": unit_ls, "unit_num": unit_num_ls}


@app.get("/get_model_use_distribution")
def get_model_use_distribution():
    bucket_data = get_bucket_data(bucket_summary_file_path)
    bucket_num = len(bucket_data)
    purpose_percent = bucket_data.value_counts('purpose')/bucket_num
    if bucket_num<3:
        top_purpose = purpose_percent
    else:
        top_purpose = purpose_percent[0:3]
    purpose_ls = top_purpose.index.tolist()
    purpose_percent_ls =  top_purpose.tolist()
    if bucket_num>3:
        purpose_ls.append('others')
        purpose_percent_ls.append(1-sum(purpose_percent_ls))
    purpose_percent_ls = [round(i*100, 2) for i in purpose_percent_ls]
    return  {"purpose": purpose_ls, "purpose_percent": purpose_percent_ls}


if __name__ == '__main__':
    uvicorn.run(app = 'main:app', host = '0.0.0.0' , port=8080, reload= True, debug = True)
