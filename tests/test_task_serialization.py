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

    def test_deserialize_task_from_dict(self):
        data = {
            'description': 'foobar',
            'completed': False,
            'task_hash': Task.calculate_task_hash('foobar'),
            'created_at': Task._now(),
        }

        task = Task.load(data)
        self.assertEqual('foobar', task.description)
        self.assertFalse(task.completed)
        self.assertEqual(Task.calculate_task_hash('foobar'), task.task_hash)
        self.assertFalse(hasattr(task, 'created_at_display'))
