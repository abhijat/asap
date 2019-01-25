import unittest

from task import Task, TaskSchema


class SerializationTests(unittest.TestCase):
    def test_serialize_task_to_dict(self):
        task = Task(description='I need to test serialization', completed=False)
        serialized = task.as_dict()

        self.assertDictEqual({
            'description': task.description,
            'completed': task.completed,
            'task_hash': Task.calculate_task_hash(task.description),
            'created_at_display': TaskSchema().timestamp_to_datetime(task),
        }, serialized)
