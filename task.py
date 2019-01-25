import datetime
import hashlib
import time

import pytz
from marshmallow import schema, fields, post_load


def serialize_timestamp(timestamp: float, timezone: str = 'Asia/Kolkata') -> str:
    return datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone(timezone)).strftime('%d %B %Y %H:%M:%S %z')


class TaskSchema(schema.Schema):

    def __init__(self) -> None:
        super().__init__(strict=True)

    description = fields.Str()
    completed = fields.Bool()
    created_at = fields.Float(load_only=True)
    task_hash = fields.Str()
    created_at_display = fields.Method(method_name='timestamp_to_datetime', dump_only=True)

    def timestamp_to_datetime(self, obj):
        return serialize_timestamp(obj.created_at)

    @post_load
    def make_task(self, data):
        return Task(**data)


class Task(object):
    def __init__(self, description: str, completed: bool = False, task_hash: str = None,
                 created_at: float = None) -> None:
        super().__init__()
        self.description = description
        self.completed = completed
        self.created_at = created_at if created_at else self._now()
        self.task_hash = task_hash if task_hash else self.calculate_task_hash(self.description)

    @staticmethod
    def calculate_task_hash(description: str, hash_size: int = 6) -> str:
        return hashlib.md5(description.encode('utf-8')).hexdigest()[:hash_size]

    @staticmethod
    def _now() -> float:
        return time.time()

    @staticmethod
    def load(data: dict) -> 'Task':
        return TaskSchema().load(data).data

    def as_dict(self) -> dict:
        return TaskSchema().dump(self).data

    def __repr__(self) -> str:
        return TaskSchema().dumps(self).data
