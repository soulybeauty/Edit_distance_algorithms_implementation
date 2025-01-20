from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from damerau_levenshtein import spelling_correction as sp1
from levenshtein_distance import spelling_correction as sp2
from norwig import correction as sp3
from weighted_edit_distance import spelling_correction as sp4
from utils import cleaner
import time
import psutil

app = FastAPI()
templates = Jinja2Templates(directory=r"C:\Users\melik\ailab\spellcheck")

# Home page route
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request, "context": ""})

# Route for simple edit distance
@app.post("/simple_edit")
async def simple_edit(request: Request, q: str = None):
    process = psutil.Process()
    request = await request.json()
    start_time = time.time()
    start_cpu = process.cpu_percent()
    start_ram = process.memory_info().rss / (1024 * 1024) 
    result = sp2(cleaner(request['text']))
    end_time = time.time()
    end_cpu = process.cpu_percent()
    end_ram = process.memory_info().rss / (1024 * 1024)  # RAM usage in MB
    execution_time = (end_time - start_time).__round__(2)
    cpu_usage = end_cpu - start_cpu
    ram_usage = end_ram - start_ram
    
    print("Execution time:", execution_time, "seconds")
    print("CPU usage:", cpu_usage, "%")
    print("RAM usage:", ram_usage, "MB")

    print(q)
    print(result)
    result.append({"execution_time": f"{execution_time} sec", "cpu_usage": f"{cpu_usage}%", "ram_usage": f"{ram_usage}MB", "method": "simple_edit"})
    return {"response": result}

# Route for optimized edit distance
@app.post("/optimized_edit")
async def simple_edit(request: Request, q: str = None):
    process = psutil.Process()
    request = await request.json()
    start_time = time.time()
    start_cpu = process.cpu_percent()
    start_ram = process.memory_info().rss / (1024 * 1024) 
    result = sp1(cleaner(request['text']))
    end_time = time.time()
    end_cpu = process.cpu_percent()
    end_ram = process.memory_info().rss / (1024 * 1024)  # RAM usage in MB
    execution_time = (end_time - start_time).__round__(2)
    cpu_usage = end_cpu - start_cpu
    ram_usage = end_ram - start_ram
    
    print("Execution time:", execution_time, "seconds")
    print("CPU usage:", cpu_usage, "%")
    print("RAM usage:", ram_usage, "MB")
    result.append({"execution_time": f"{execution_time} sec", "cpu_usage": f"{cpu_usage}%", "ram_usage": f"{ram_usage}MB", "method": "optimized_edit"})
    return {"response": result}

# Route for Norwig edit distance
@app.post("/norwig_edit/")
async def simple_edit(request: Request, q: str = None):
    results = []
    process = psutil.Process()
    request = await request.json()
    start_time = time.time()
    start_cpu = process.cpu_percent()
    start_ram = process.memory_info().rss / (1024 * 1024) 
    results = sp3(cleaner(request['text']))
    end_time = time.time()
    end_cpu = process.cpu_percent()
    end_ram = process.memory_info().rss / (1024 * 1024)  # RAM usage in MB
    
    execution_time = (end_time - start_time).__round__(2)
    cpu_usage = end_cpu - start_cpu
    ram_usage = end_ram - start_ram
    
    print("Execution time:", execution_time, "seconds")
    print("CPU usage:", cpu_usage, "%")
    print("RAM usage:", ram_usage, "MB")
    results.append({"execution_time": f"{execution_time} sec", "cpu_usage": f"{cpu_usage}%", "ram_usage": f"{ram_usage}MB", "method": "norwig_edit"})
    print(results)
    return {"response": results}

# Route for weighted edit distance
@app.post("/weighted_edit")
async def simple_edit(request: Request):
    process = psutil.Process()
    request = await request.json()
    start_time = time.time()
    start_cpu = process.cpu_percent()
    start_ram = process.memory_info().rss / (1024 * 1024)
    result = sp4(cleaner(request['text']), t=float(request['transpose_cost']), d=float(request['delete_cost']), r=float(request['replace_cost']), s=float(request['insert_cost']))
    end_time = time.time()
    end_cpu = process.cpu_percent()
    end_ram = process.memory_info().rss / (1024 * 1024)  # RAM usage in MB
    
    execution_time = (end_time - start_time).__round__(2)
    cpu_usage = end_cpu - start_cpu
    ram_usage = end_ram - start_ram
    
    print("Execution time:", execution_time, "seconds")
    print("CPU usage:", cpu_usage, "%")
    print("RAM usage:", ram_usage, "MB")
    result.append({"execution_time": f"{execution_time} sec", "cpu_usage": f"{cpu_usage}%", "ram_usage": f"{ram_usage}MB", "method": "weighted_edit"})
    print(result)
    return {"response": result}
