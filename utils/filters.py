import abc
import datetime


class Filter(abc.ABC):
    @abc.abstractmethod
    def check(self, obj) -> bool: ...


class TodoIsDoneFilter(Filter):
    def __init__(self, is_done: bool = True):
        self.is_done = is_done

    def check(self, obj) -> bool:
        if hasattr(obj, 'is_done'):
            return obj.is_done == self.is_done
        return False


class TodoCreatedDateFilter(Filter):
    from_date: datetime.datetime
    to_date: datetime.datetime

    def __init__(self, from_date: datetime.datetime = None, to_date: datetime.datetime = None):
        self.from_date = from_date
        self.to_date = to_date

    def check(self, obj) -> bool:
        if hasattr(obj, 'created_at'):
            if self.from_date and self.to_date:
                return self.from_date < obj.created_at < self.to_date
            elif self.from_date and not self.to_date:
                return self.from_date < obj.created_at
            elif self.to_date and not self.from_date:
                return obj.created_at < self.to_date
        return False