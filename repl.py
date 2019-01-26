import cmd

from task_store import TaskStore


class TaskHandler(cmd.Cmd):
    def __init__(self, task_store: TaskStore, completekey='tab', stdin=None, stdout=None):
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
        print(f'added task id {self.push_task(data)}')

    def push_task(self, description: str):
        return self.task_store.push_task(description=description)

    def do_pop(self, task_hash: str):
        deleted_task = self.pop_task(task_hash=task_hash)
        if deleted_task is not None:
            print(f'removed task [{deleted_task}]')
        else:
            print(f'could not find key {task_hash}')

    def pop_task(self, task_hash: str):
        return self.task_store.pop_task(task_hash=task_hash)

    def complete_pop(self, text: str, _line: str, _start_index: int, _end_index: int):
        text = text.strip()
        return [key for key in self.task_store.keys() if key.startswith(text)]

    def do_ls(self, _data: str):
        for task in self.list_tasks():
            print(task)

    def do_list(self, _data: str):
        for task in self.list_tasks():
            print(task)

    def list_tasks(self):
        return self.task_store.list_tasks()

    def do_EOF(self, _data):
        print('Good bye!')
        return True
