import unittest
from typing import Optional

from repl import TaskHandler
from task import Task
from task_store import TasksInMemory


class TaskHandlerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.task_store = TasksInMemory()
        self.task_handler = TaskHandler(task_store=self.task_store)

        self.description = 'We are not descended from fearful men'
        self.task_hash = Task.calculate_task_hash(self.description)

    def test_can_add_tasks_from_repl(self):
        self.task_handler.do_push(data=self.description)

        self.assertEqual(1, len(self.task_store.data))

        task: Optional[Task] = self.task_store.data.get(self.task_hash)
        self.assertEqual(self.description, task.description)

    def test_can_remove_added_task_from_repl(self):
        self.task_handler.do_push(data=self.description)

        self.assertEqual(1, len(self.task_store.data))

        self.task_handler.do_pop(self.task_hash)
        self.assertEqual(0, len(self.task_store.data))

    def test_can_list_added_tasks_from_repl(self):
        self.task_handler.do_push(data=self.description)
        tasks = self.task_handler.list_tasks()
        print(tasks)
