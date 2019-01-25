from repl import TaskHandler
from task_store import TaskStore


def main():
    task_handler = TaskHandler(TaskStore('db.json'))
    task_handler.cmdloop()


if __name__ == '__main__':
    main()
