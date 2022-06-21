import typing
from uuid import UUID

from domain.usecases.todo import AbsTodoRepo
from domain.entities.todo import Todo
from utils.filters import Filter


class MemoryTodoRepo(AbsTodoRepo):
    _data = {}

    def get_by_filter(self, flt: Filter) -> typing.List[Todo]:
        all_todos = self.get_all()
        return list(filter(lambda x: flt.check(x), all_todos))

    def get_all(self) -> typing.List[Todo]:
        res = []
        for value in self._data.values():
            res.append(Todo.parse_obj(value))
        return res

    def get_by_uuid(self, uuid: UUID) -> Todo:
        if uuid in self._data.keys():
            return self._data[uuid]

    def delete(self, uuid: UUID) -> bool:
        try:
            self._data.pop(uuid)
            return True if uuid not in self._data.keys() else False
        except KeyError:
            return False

    def save(self, todo: Todo) -> bool:
        self._data[todo.id] = todo
        return True if todo in self._data[todo.id] else False
