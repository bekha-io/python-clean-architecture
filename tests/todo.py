import datetime
import unittest
import random

from domain.usecases.todo import TodoUseCase, AbsTodoRepo
from domain.entities.todo import Todo
from repo.memory import MemoryTodoRepo
from utils.filters import TodoIsDoneFilter, TodoCreatedDateFilter


class ParentTestCase(unittest.TestCase):
    repo_class = MemoryTodoRepo

    def setUp(self) -> None:
        self.repo = self.repo_class()
        self.use_case = TodoUseCase(self.repo)
        self.test_todos = [
            Todo(text=i) for i in range(1, 100)
        ]

        for todo in self.test_todos:
            self.repo.save(todo)

    def tearDown(self) -> None:
        for todo in self.test_todos:
            self.use_case.delete_todo(todo.id)


class TestTodoUseCase(ParentTestCase):

    def test_created_todo_has_unique_uuid(self):
        todo = Todo(text='Testing todo #1')
        self.assertNotEqual(todo.id, self.use_case.create_todo(todo.text).id)

    def test_get_done_todos(self):
        done_todos = []
        for todo in self.repo.get_all():
            is_done = bool(random.getrandbits(1))
            if is_done:
                todo.is_done = True
                self.repo.save(todo)
                done_todos.append(todo)
        self.assertEqual(len(done_todos), len(self.use_case.get_done_todos()))

    def test_get_undone_todos(self):
        undone_todos = []
        for todo in self.repo.get_all():
            is_done = bool(random.getrandbits(1))
            if is_done:
                todo.is_done = True
                self.repo.save(todo)
            else:
                undone_todos.append(todo)
        self.assertEqual(undone_todos, self.use_case.get_undone_todos())


class TestMemoryTodoRepo(ParentTestCase):

    def test_delete_todo_bulk(self):
        for todo in self.test_todos:
            self.repo.delete(todo.id)
        self.assertEqual([], self.repo.get_all())

    def test_done_todos_filter(self):
        done_todos = []
        for todo in self.repo.get_all():
            is_done = bool(random.getrandbits(1))
            if is_done:
                todo.is_done = True
                self.repo.save(todo)
                done_todos.append(todo)

        done_todos_filter_res = self.repo.get_by_filter(TodoIsDoneFilter())
        self.assertEqual(done_todos, done_todos_filter_res)


class TestTodoFilters(ParentTestCase):

    def test_todo_done_filter(self):
        done, undone = [], []
        for todo in self.test_todos:
            if bool(random.getrandbits(1)):
                todo.is_done = True
                done.append(todo)
            else:
                undone.append(todo)

        done_filtered = list(filter(lambda x: TodoIsDoneFilter().check(x), self.test_todos))
        undone_filtered = list(filter(lambda x: TodoIsDoneFilter(is_done=False).check(x), self.test_todos))

        self.assertEqual(done_filtered, done)
        self.assertEqual(undone_filtered, undone)

    def test_todo_date_filter__both_dates(self):
        flt = TodoCreatedDateFilter(from_date=datetime.datetime(month=1, day=1, year=2000),
                                    to_date=datetime.datetime(month=1, day=10, year=2000))

        todos_all = []
        filter_match = []
        for x in range(1, 100):
            if bool(random.getrandbits(1)):
                todo = Todo(text=x, created_at=datetime.datetime(month=1, day=5, year=2000))
                todos_all.append(todo)
                filter_match.append(todo)
            else:
                todos_all.append(Todo(text=x))

        filter_res = list(filter(lambda obj: flt.check(obj), todos_all))
        self.assertEqual(filter_match, filter_res)
