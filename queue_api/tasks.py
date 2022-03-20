import asyncio
from task import Task
from contextlib import suppress


class Tasks:
    """Class to represent tasks storage entity"""
        
    def __init__(self):
        self.all_tasks = {} # key: id, value: task
        self.is_started = False
        self.tasks_queue = asyncio.Queue(maxsize=-1)
    
    """
        Add task to queue and return this task id
    """
    async def add_task(self,data,type):
        new_task = Task(data,type)
        self.all_tasks[new_task.id] = new_task
        await self.tasks_queue.put(new_task)
        return new_task.id

    """
        Start processing queue
    """
    async def start(self):
        if not self.is_started:
            self.is_started = True
            self._queue_process = asyncio.ensure_future(self._run())

    """
        Stop processing queue
    """
    async def stop(self):
        if self.is_started:
            self.is_started = False
            self._queue_process.cancel()
            with suppress(asyncio.CancelledError):
                await self._queue_process

    """
        Run queue until all tasks are processed and then stop process
    """
    async def _run(self):
        while not self.tasks_queue.empty():
            task = await self.tasks_queue.get()
            task.do_func()
            task.status = "in_progress"
            await asyncio.sleep(task.interval)
            task.status = "done"
        await self.stop()
        
    
    """
        Get status of task by id from tasks data storage
    """    
    async def get_status_by_id(self,id):
        try:
            task = self.all_tasks[id]
        except KeyError:
            return "id_not_found"
        return task.status
    
    """
        Get result of task by id from tasks data storage
    """   
    async def get_result_by_id(self,id):
        try:
            task = self.all_tasks[id]
        except KeyError:
            return "id_not_found"
        if(task.status != 'done'):
            return "not_processed"
        return task.data