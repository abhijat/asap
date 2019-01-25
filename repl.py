import cmd
from typing import Union

from task_store import TaskStore, TasksInMemory


class TaskHandler(cmd.Cmd):
    def __init__(self, task_store: Union[TasksInMemory, TaskStore], completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)
        self.task_store = task_store
        self.prompt = '[[asap]] '

    def do_prompt(self, new_prompt: str):
        new_prompt = new_prompt.strip()
        if not new_prompt:
            print('prompt <new_prompt>')
        else:
            self.prompt = f'{new_prompt} '

    def do_push(self, data: str):
        task_id = self.task_store.push_task(data)
        print(f'added task id {task_id}')

    def do_pop(self, key: str):
        task = self.task_store.pop_task(task_hash=key)
        if task is not None:
            print(f'removed task [{task}]')
        else:
            print(f'could not find key {key}')

    def complete_pop(self, text: str, _line: str, _start_index: int, _end_index: int):
        text = text.strip()
        return [key for key in self.task_store.keys() if key.startswith(text)]

    def do_ls(self, _data: str):
        self.list_tasks()

    def do_list(self, _data: str):
        self.list_tasks()

    def list_tasks(self):
        for task in self.task_store.list_tasks():
            print(task)

    def do_EOF(self, _data):
        print('Good bye!')
        return True
