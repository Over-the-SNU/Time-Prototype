import sqlite3
from typing import ClassVar
from dataclasses import dataclass
from datetime import datetime
from datetime import date


class Manager:
    __object_set = set()

    def __init__(self):
        # DB에서 불러오기
        pass

    def __del__(self):
        # DB에 저장
        pass

    def all(self):
        pass

    def get(self, id):
        pass

    def create(self, obj):
        pass

    def update(self, id, obj):
        pass

    def delete(self, id):
        pass


@dataclass
class Repeat:
    day: int  # bit mask
    week_interval: int
    due: date


@dataclass
class Todo:
    objects: ClassVar[Manager] = Manager()
    id: int
    name: str
    done: bool
    progress: int
    date: date
    repeat: Repeat
    importance: int
    content: str


@dataclass
class CalenderEvent:
    objects: ClassVar[Manager] = Manager()
    id: int
    name: str
    from_time: datetime
    to_time: datetime
    repeat: Repeat
    importance: int
    content: str
