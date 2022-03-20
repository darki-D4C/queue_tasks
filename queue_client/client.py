#!/usr/bin/env python
import json
from msilib.schema import Error
import sys
import requests
import time

"""
    Send request to server to add task and print result
"""
def add_task(data, type):
    payload = {'data': data, 'type': type}
    r = requests.post("http://localhost:8080/add", data=json.dumps(payload))
    print("Your id is " + r.json()['id'])
    exit(0)

"""
    Send request to server and get status
"""
def get_task_status(id):
    payload = {'id': id}
    r = requests.get('http://localhost:8080/get_status', params=payload)
    if(r.status_code != 200):
        print("Invalid id")
        exit(2)
    data = r.json()
    print("This task status is " + data['status'])
    exit(0)
    
"""
    Send request to server and get result
"""
def get_task_result(id):
    payload = {'id': id}
    r = requests.get('http://localhost:8080/get_result', params=payload)
    if(r.status_code != 200):
        print("Invalid id")
        exit(2)
    data = r.json()['result']
    print("This task result is " + data)
    exit(0)

"""
    Interactive mode where user inputs data,type and awaits result from server
"""
def interactive_mode():
    try:
        print("""
                                    Welcome to Tasks™ client!
                This programm will acompany you along the processing of your chosen task.
                Please follow instructions which programm suggest to you.
                What type of task are you interested in?
                (Three types are available: Reverse, Pairwise permutation, Duplicate chars by their position)
                1. Reverse
                2. Pairwise permutation
                3. Duplicate chars by their position
                Please, enter a number between 1 and 3.
            """)
        type_id = input_type()
        task_type = match_type(type_id)
        task_data = input_data()
        try:
            task_id = add_task_interactive(task_data, task_type)
            payload = {'id': task_id }
            get_status_interactive(params = payload)
            get_result_interactive(params = payload)
            print("""
                    Thank you for using our programm!
                """)
            exit(0)
        except (requests.exceptions.RequestException):
            print("\nError accured while trying to access our servers.\nPlease try again later")
            exit(2)
    except KeyboardInterrupt:
        print('\nThank you for using our programm!')
        exit(0)
        


"""
    Get from user his type of task
"""
def input_type():
    while True:
        type_id = input("Please choose a number between 1 and 3: ")
        try:
            type_id = int(type_id)
            if(type_id > 0 and type_id < 4):
                break
        except ValueError:
            continue
    return type_id

"""
    Match task type with provided index
"""
def match_type(index):
    match index:
        case 1:
            return 'reverse'
        case 2:
            return 'pairwise_permutation'
        case 3:
            return 'dup_by_idx'


"""
    Get data from user
"""
def input_data():
    while True:
        try:
            task_data = input("Please enter a string: ")
            if(len(task_data)!=0):
                break
        except EOFError:
            continue
    return task_data

"""
    Add task to process queue and get id
"""
def add_task_interactive(task_data, task_type):
    payload = {'data': task_data, 'type': task_type}
    r = requests.post("http://localhost:8080/add", data=json.dumps(payload))
    task_id = r.json()['jui']
    print("Your task id is " + task_id)
    return task_id

"""
    Get status of task until it completes
"""
def get_status_interactive(params):
    print("Waiting for status...")
    status = ''
    while status != "done":
        r = requests.get("http://localhost:8080/get_status", params=params)
        new_status = r.json()['status']
        if(new_status!=status):
            print("Task is " + new_status.replace("_"," "))
            status = new_status
        if(status!="done"): time.sleep(5)

"""
    Get result of task and print it
"""
def get_result_interactive(params):
    r = requests.get('http://localhost:8080/get_result', params=params)
    result = r.json()['result']
    print("\nYour task result is " + result)
    

def main(argv):
    match argv[0]:
        case "add_task":
            if(len(argv)!=3):
                print(f"Wrong number of arguments \nProvided {len(argv)-1} - Required 2 ")
                exit(2)
            add_task(argv[1],argv[2])    
        case "get_status":
            if(len(argv)!=2):
                print(f"Wrong number of arguments \nProvided {len(argv)-1} - Required 1 ")
                exit(2)
            get_task_status(argv[1])    
        case "get_result":
            if(len(argv)!=2):
                print(f"Wrong number of arguments \nProvided {len(argv)-1} - Required 1 ")
                exit(2)
            get_task_result(argv[1]) 
        case "interactive":
            interactive_mode()
        case "--help":
            print("""                   Welcome to Tasks™ client!
        You can run client be specifying type of operation and data for that operation (in that order)
        To add task use 'task_type' 'data' after that you will be given an unique id for your task.
        (Three types of task are available: Reverse, Pairwise permutation, Duplicate chars by their position)
        1. reverse 
        2. pairwise_permutation
        3. dup_by_idx
        To get status or result of a task run client with either get_status or get_result and id (in that order)
        """)
            exit(0)
        case _:
            print("Invalid operation type")
            exit(2)
            

if __name__ == "__main__":
    if(len(sys.argv) == 1 ):
        print("""                   Welcome to Tasks™ client!
        You can run client be specifying type of operation and data for that operation (in that order)
        To add task use 'task_type' 'data' after that you will be given an unique id for your task.
        (Three types of task are available: Reverse, Pairwise permutation, Duplicate chars by their position)
        1. reverse 
        2. pairwise_permutation
        3. dup_by_idx
        To get status or result of a task run client with either get_status or get_result and id (in that order)
        """)
        exit(0)
    main(sys.argv[1:])