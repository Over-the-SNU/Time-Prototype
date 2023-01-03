import sqlite3
from abc import *
from typing import ClassVar, List
from dataclasses import dataclass
from datetime import datetime
from datetime import date


class Manager(metaclass=ABCMeta):
    __object_set = set()

    def __init__(self, db_name="TIME.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        pass

    def __del__(self):
        # DB에 저장
        self.connection.close()
        print("DB SAVED")
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def create(self, obj):
        pass

    @abstractmethod
    def update(self, id, obj):
        pass

    @abstractmethod
    def delete(self, id):
        pass


class TodoManager(Manager):
    def __init__(self, db_name="TIME.db"):
        super().__init__(db_name)
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Todos(
            TodoID INTEGER PRIMARY KEY,
            TodoName TEXT NOT NULL,
            Done BOOLEAN DEFAULT 0,
            Progress INTEGER DEFAULT 0,
            TodoDate DATE NOT NULL,
            Importance INTEGER DEFAULT 0,
            Content TEXT NOT NULL
            );
            """
        ).execute(
            """
            CREATE TABLE IF NOT EXISTS TodoRepeats(
            TodoID INTEGER,
            Days INTEGER,
            WeekInterval INTEGER,
            DueDate DATE,
            FOREIGN KEY (TodoID) REFERENCES Todos(TodoID)
            );
            """
        ).fetchall()

    def all(self) -> List['Todo']:
        result = self.cursor.execute("""
        SELECT Todos.TodoID, Todos.TodoName, Todos.Done, Todos.Progress,
         Todos.TodoDate, Todos.Importance, Todos.Content, TodoRepeats.Days,
         TodoRepeats.WeekInterval, TodoRepeats.DueDate
         FROM Todos
        LEFT JOIN TodoRepeats ON Todos.TodoID = TodoRepeats.TodoID
        """).fetchall()

        ret = []
        for item in result:
            r = Repeat(day=item[7], week_interval=item[8], due=item[9]) if item[7] is not None else None
            ret.append(Todo(id=item[0], name=item[1], done=item[2] != 0, progress=item[3],
                            date=datetime.strptime(item[4], "%Y-%m-%d").date(),
                            repeat=r, importance=item[5], content=item[6]))
        return ret

    def get(self, id) -> 'Todo':
        result = self.cursor.execute(f"""
        SELECT Todos.TodoID, Todos.TodoName, Todos.Done, Todos.Progress,
         Todos.TodoDate, Todos.Importance, Todos.Content, TodoRepeats.Days,
         TodoRepeats.WeekInterval, TodoRepeats.DueDate
         FROM Todos
        LEFT JOIN TodoRepeats ON Todos.TodoID = TodoRepeats.TodoID
        WHERE Todos.TodoID = {id}
        """).fetchone()

        if not result:
            raise ValueError("ID NOT EXIST")

        r = Repeat(day=result[7], week_interval=result[8], due=result[9]) if result[7] is not None else None
        return Todo(id=result[0], name=result[1], done=result[2] != 0, progress=result[3],
                        date=datetime.strptime(result[4], "%Y-%m-%d").date(),
                        repeat=r, importance=result[5], content=result[6])

    def create(self, obj) -> None:
        self.cursor.execute(f"""
        INSERT INTO Todos(TodoName, TodoDate, Importance, Content)
        VALUES ( '{obj.name}', '{obj.date.strftime("%Y-%m-%d")}', {obj.importance}, '{obj.content}' );
        """)
        self.connection.commit()

        if obj.repeat:
            id = self.cursor.execute("SELECT last_insert_rowid()").fetchone()
            self.cursor.execute(f"""
            INSERT INTO TodoRepeats
            VALUES ( {id[0]}, {obj.repeat.day}, {obj.repeat.week_interval}, '{obj.repeat.due.strftime("%Y-%m-%d")}' );
            """)
            self.connection.commit()

    def update(self, id, obj):
        self.cursor.execute(f"""
        UPDATE Todos
        SET TodoName='{obj.name}', Done={1 if obj.done else 0},
        Progress={obj.progress},
        TodoDate='{obj.date.strftime("%Y-%m-%d")}',
        Importance={obj.importance},
        Content='{obj.content}'
        WHERE TodoID = {id};
        """)
        self.connection.commit()

        r = self.cursor.execute(f"""
        SELECT * FROM TodoRepeats
        WHERE TodoID={id};
        """).fetchone()

        if obj.repeat:
            if r:
                self.cursor.execute(f"""
                UPDATE TodoRepeats
                SET Days={obj.repeat.day},
                WeekInterval={obj.repeat.week_interval},
                DueDate='{obj.repeat.due.strftime("%Y-%m-%d")}'
                WHERE TodoID={id}
                """)
            else:
                self.cursor.execute(f"""
                INSERT INTO TodoRepeats
                VALUES ( {id}, {obj.repeat.day}, {obj.repeat.week_interval}, '{obj.repeat.due.strftime("%Y-%m-%d")}' );
                """)

            self.connection.commit()
        elif r:
            self.cursor.execute(f"""
            DELETE FROM TodoRepeats WHERE TodoID={id}
            """)
            self.connection.commit()

    def delete(self, id):
        self.cursor.execute(f"""
        DELETE FROM TodoRepeats WHERE TodoID={id}
        """)
        self.cursor.execute(f"""
        DELETE FROM Todos WHERE TodoID={id}
        """)


@dataclass
class Repeat:
    day: int  # bit mask
    week_interval: int
    due: date


@dataclass
class Todo:
    objects: ClassVar[Manager] = TodoManager()
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
    # objects: ClassVar[Manager] = Manager()
    id: int
    name: str
    from_time: datetime
    to_time: datetime
    repeat: Repeat
    importance: int
    content: str

