from typing import Optional

from tinydb import TinyDB, where

from task import Task


class TasksInMemory(object):
    def __init__(self) -> None:
        super().__init__()
        self.data = dict()

    def push_task(self, description: str) -> str:
        task = Task(description=description)
        self.data[task.task_hash] = task
        return task.task_hash

    def pop_task(self, task_hash: str) -> Optional[Task]:
        return self.data.pop(task_hash, None)

    def list_tasks(self):
        return list(self.data.values())

    def keys(self):
        return self.data.keys()


class TaskStore(object):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path

    def push_task(self, description: str) -> str:
        task = Task(description=description)
        with TinyDB(self.file_path) as db:
            db.insert(task.as_dict())
        return task.task_hash

    def pop_task(self, task_hash: str) -> dict:
        with TinyDB(self.file_path) as db:
            task_to_delete = db.search(where('task_hash') == task_hash)
            if task_to_delete:
                task_to_delete = task_to_delete[0]
                db.remove(where('task_hash') == task_hash)
        return task_to_delete

    def list_tasks(self):
        with TinyDB(self.file_path) as db:
            return [Task.load(data) for data in db.all()]

    def keys(self):
        task_hashes = []
        with TinyDB(self.file_path) as db:
            for doc in iter(db):
                task_hashes.append(doc.get('task_hash'))
        return task_hashes
