import os
import unittest
from typing import Optional

from repl import TaskHandler
from task import Task
from task_store import TaskStore


class TaskHandlerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db_path = 'test_db.json'
        self.task_store = TaskStore(self.db_path)
        self.task_handler = TaskHandler(task_store=self.task_store)

        self.description = 'We are not descended from fearful men'
        self.task_hash = Task.calculate_task_hash(self.description)

    def tearDown(self):
        os.remove(self.db_path)

    def test_can_add_tasks_from_repl(self):
        self.task_handler.push_task(description=self.description)

        self.assertEqual(1, len(self.task_store))

        task: Optional[Task] = self.task_store.get_task(self.task_hash)
        self.assertEqual(self.description, task.description)
        self.assertEqual(self.task_hash, task.task_hash)
        self.assertFalse(task.completed)

    def test_can_remove_added_task_from_repl(self):
        self.task_handler.push_task(description=self.description)

        self.assertEqual(1, len(self.task_store))

        self.task_handler.pop_task(task_hash=self.task_hash)
        self.assertEqual(0, len(self.task_store))

    def test_can_list_added_tasks_from_repl(self):
        self.task_handler.push_task(description=self.description)

        task = self.task_handler.list_tasks()[0]
        self.assertEqual(self.description, task.description)
