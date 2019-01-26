from typing import Optional

from tinydb import TinyDB, where

from task import Task


class TaskStore(object):
    def __init__(self, file_path: Optional[str] = None) -> None:
        super().__init__()
        self.file_path = file_path

    def _get_db_handle(self):
        return TinyDB(self.file_path)

    def push_task(self, description: str) -> str:
        task = Task(description=description)
        with self._get_db_handle() as db:
            db.insert(task.as_dict())
        return task.task_hash

    def pop_task(self, task_hash: str) -> Optional[Task]:
        with self._get_db_handle() as db:
            tasks = db.search(where('task_hash') == task_hash)
            if tasks:
                task_to_delete = Task.load(tasks[0])
                db.remove(where('task_hash') == task_hash)
            else:
                task_to_delete = None
        return task_to_delete

    def get_task(self, task_hash: str) -> Optional[Task]:
        with self._get_db_handle() as db:
            tasks = db.search(where('task_hash') == task_hash)
            if tasks:
                return Task.load(tasks[0])
        return None

    def list_tasks(self):
        with self._get_db_handle() as db:
            return [Task.load(data) for data in db.all()]

    def keys(self):
        with self._get_db_handle() as db:
            return [doc.get('task_hash') for doc in iter(db)]

    def __len__(self):
        with self._get_db_handle() as db:
            return len(db)
