#!/usr/bin/env python3
"""Command-line interface for the Todo App."""

import argparse
from .todo import TodoApp


def main():
    """Run the todo application CLI."""
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