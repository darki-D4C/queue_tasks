Hello!
(OS - Windows 10,
Python version - cpython
Python 3.10.0)

This set of steps will enable you to run both server and client of Tasks™.

Server will be openned on local host , port - 8080, (http://localhost:8080/)
Client can be run by using run_client to get into virtual env and exectuing client.py script
To get info about client run "./client.py --help" (without quotes)
Available endpoints are /add, /get_status, /get_result :

    /add:
        POST request with required body with format (json) "{"data":data,"type":type}" 
        which will add task to processing queue and will return (json) id of newly created task
        {"id":id}

    /get_status:
        GET request with required query params with id=id which will return (json) {"status":status}

    /get_result:
        GET request with required query params with id=id which will return (json) {"result":result}

    If any of endpoints required params/body are incorrect suitable error will be returned

Server will add,store,process tasks and provide status and result of each task.

Setup:
    1. python -m venv ./queue-env  # This will install virtual env for project
    2. pip install -r /tmp/requirements.txt # This will install requirements
    3. ./queue-env/Scripts/activate # To start enviroment

To start server:
    python ./queue_api/app.py

To start client:
    python ./queue/client/client.py (and add arguments, to see available execute with "--help")