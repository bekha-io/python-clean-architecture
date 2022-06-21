from uuid import UUID
from abc import ABC, abstractmethod
import typing

from utils.filters import Filter, TodoIsDoneFilter
from domain.entities.todo import Todo


class AbsTodoRepo(ABC):
    @abstractmethod
    def get_all(self) -> typing.List[Todo]: ...

    @abstractmethod
    def get_by_uuid(self, uuid: UUID) -> Todo: ...

    @abstractmethod
    def delete(self, uuid: UUID) -> bool: ...

    @abstractmethod
    def save(self, todo: Todo) -> bool:  ...

    @abstractmethod
    def get_by_filter(self, flt: Filter) -> typing.List[Todo]: ...


class TodoUseCase:
    _repo: AbsTodoRepo

    def __init__(self, repo: AbsTodoRepo):
        self._repo = repo

    def create_todo(self, text: str) -> Todo:
        todo = Todo(text=text)
        self._repo.save(todo)
        return todo

    def get_all_todos(self) -> typing.List[Todo]:
        return self._repo.get_all()

    def get_todo_by_uuid(self, uuid: UUID) -> Todo:
        return self._repo.get_by_uuid(uuid)

    def delete_todo(self, uuid: UUID) -> bool:
        return self._repo.delete(uuid)

    def get_undone_todos(self) -> typing.List[Todo]:
        return list(filter(lambda obj: TodoIsDoneFilter(is_done=False).check(obj), self._repo.get_all()))

    def get_done_todos(self) -> typing.List[Todo]:
        return list(filter(lambda obj: TodoIsDoneFilter().check(obj), self._repo.get_all()))
