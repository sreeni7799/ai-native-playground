#!/usr/bin/env python3

import argparse
import json
import os
from typing import List, Dict

class TodoApp:
    def __init__(self, filename: str = "todos.json"):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self) -> List[Dict]:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_todos(self):
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)

    def add_todo(self, task: str):
        todo_id = len(self.todos) + 1
        new_todo = {
            "id": todo_id,
            "task": task,
            "completed": False
        }
        self.todos.append(new_todo)
        self.save_todos()
        print(f"Added todo #{todo_id}: {task}")

    def list_todos(self):
        if not self.todos:
            print("No todos found.")
            return
        
        print("\nYour todos:")
        print("-" * 40)
        for todo in self.todos:
            status = "✓" if todo["completed"] else "○"
            print(f"{status} #{todo['id']}: {todo['task']}")
        print("-" * 40)

    def delete_todo(self, todo_id: int):
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                removed_todo = self.todos.pop(i)
                self.save_todos()
                print(f"Deleted todo #{todo_id}: {removed_todo['task']}")
                return
        print(f"Todo #{todo_id} not found.")

def main():
    parser = argparse.ArgumentParser(description="Simple command line todo application")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    add_parser = subparsers.add_parser('add', help='Add a new todo')
    add_parser.add_argument('task', help='The todo task to add')

    list_parser = subparsers.add_parser('list', help='List all todos')

    delete_parser = subparsers.add_parser('delete', help='Delete a todo')
    delete_parser.add_argument('id', type=int, help='ID of the todo to delete')

    args = parser.parse_args()

    todo_app = TodoApp()

    if args.command == 'add':
        todo_app.add_todo(args.task)
    elif args.command == 'list':
        todo_app.list_todos()
    elif args.command == 'delete':
        todo_app.delete_todo(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()