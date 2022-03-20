from aiohttp import web
import json
from tasks import Tasks

tasks = Tasks()

"""
    Decorator for validating /add body fields
"""
def add_task_validation(func):
    async def wrapper(*args, **kwargs):
        try:
            body = await args[0].json()
        except json.JSONDecodeError:
            return web.Response(text=json.dumps({"error":"no_fields"}), status=404)
        if('data' not in body and 'type' not in body):
            return web.Response(text=json.dumps({"error":"invalid_fields"}), status=404)
        if(body['type'] not in ['reverse','pairwise_permutation','dup_by_idx']):
            return web.Response(text=json.dumps({"error":"invalid_type"}), status=404)
        return await func(*args, **kwargs)
    return wrapper
"""
    Decorator for validating /get_... query parameters
"""
def get_task_validation(func):
    async def wrapper(*args, **kwargs):
        try:
            body = args[0].query
        except json.JSONDecodeError:
            return web.Response(text=json.dumps({"error":"no_fields"}), status=404)
        if('id' not in body):
           return web.Response(text=json.dumps({"error":"invalid_fields"}), status=404)
        return await func(*args, **kwargs)
    return wrapper

"""
    Add task view
"""
@add_task_validation
async def add_task(request):
    body = await request.json()
    data = body['data']
    task_type = body["type"]
    new_id = await tasks.add_task(data,task_type)
    response_obj = { 'id' : new_id }
    return web.Response(text=json.dumps(response_obj))

"""
    Get task status view
"""
@get_task_validation
async def get_task_status(request):
    params = request.query
    req_id = params['id']
    result = await tasks.get_status_by_id(req_id)
    if(result == "id_not_found"):
        return web.Response(text=json.dumps({"error":result}), status=404)
    response_obj = { 'status' : result }
    return web.Response(text=json.dumps(response_obj))

"""
    Get task result view
"""
@get_task_validation
async def get_task_result(request):
    params = request.query
    req_id = params['id']
    result = await tasks.get_result_by_id(req_id)
    
    if(result == "id_not_found"):
        return web.Response(text=json.dumps({"error":result}), status=404)
    
    response_obj = { 'result' : result }

    return web.Response(text=json.dumps(response_obj))

"""
    Start processing queue middleware
"""
@web.middleware
async def start_queue(request, handler):
    response = await handler(request)
    await tasks.start()
    return response

app = web.Application(middlewares=[start_queue])
app.router.add_post('/add', add_task)
app.router.add_get('/get_status', get_task_status)
app.router.add_get('/get_result', get_task_result)

if __name__ == '__main__':
    web.run_app(app)