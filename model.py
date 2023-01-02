import sqlite3
from dataclasses import dataclass
from datetime import datetime
from datetime import date


class Repeat(dataclass):
    day: int  # bit mask
    week_interval: int
    due: datetime


class Todo(dataclass):
    id: int
    name: str
    done: bool
    progress: int
    date: date
    repeat: Repeat
    importance: int
    content: str


class CalenderEvent(dataclass):
    id: int
    name: str
    from_time: datetime
    to_time: datetime
    repeat: Repeat
    importance: int
    content: str
