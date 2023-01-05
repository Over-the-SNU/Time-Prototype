import sqlite3
from abc import *
from typing import ClassVar, List, Optional
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
    def create(self, obj=None, **kwargs):
        pass

    @abstractmethod
    def update(self, id, obj=None, **kwargs):
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
            r = Repeat(day=item[7], week_interval=item[8], due=datetime.strptime(item[9], "%Y-%m-%d").date()) if item[7] is not None else None
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

        r = Repeat(day=result[7], week_interval=result[8], due=datetime.strptime(result[9], "%Y-%m-%d").date()) if result[7] is not None else None
        return Todo(id=result[0], name=result[1], done=result[2] != 0, progress=result[3],
                    date=datetime.strptime(result[4], "%Y-%m-%d").date(),
                    repeat=r, importance=result[5], content=result[6])

    def create(self, obj=None, **kwargs) -> None:
        if not obj:
            if "name" not in kwargs:
                raise ValueError("Missing essential field 'name'")
            if "date" not in kwargs:
                raise ValueError("Missing essential field 'date'")
            if not isinstance(kwargs["date"], date):
                raise ValueError(f"Invalid type for field 'date' (Expected='date', Got={type(kwargs['date'])}")

            val_name = kwargs["name"]
            val_date = kwargs["date"]
            val_importance = 0 if "importance" not in kwargs else kwargs["importance"]
            val_content = "" if "content" not in kwargs else kwargs["content"]
        else:
            val_name = obj.name
            val_date = obj.date
            val_importance = obj.importance
            val_content = obj.content

        self.cursor.execute(f"""
        INSERT INTO Todos(TodoName, TodoDate, Importance, Content)
        VALUES ( '{val_name}', '{val_date.strftime("%Y-%m-%d")}', {val_importance}, '{val_content}' );
        """)
        self.connection.commit()

        repeat = kwargs["repeat"] if "repeat" in kwargs else obj.repeat
        if repeat:
            id = self.cursor.execute("SELECT last_insert_rowid()").fetchone()
            self.cursor.execute(f"""
            INSERT INTO TodoRepeats
            VALUES ( {id[0]}, {repeat.day}, {repeat.week_interval}, '{repeat.due.strftime("%Y-%m-%d")}' );
            """)
            self.connection.commit()

    def update(self, id, obj=None, **kwargs) -> None:
        if not obj:
            obj = self.get(id)

        val_name = obj.name
        val_done = obj.done
        val_progress = obj.progress
        val_date = obj.date
        val_importance = obj.importance
        val_content = obj.content

        if "name" in kwargs:
            val_name = kwargs["name"]
        if "done" in kwargs:
            val_done = kwargs["done"]
        if "progress" in kwargs:
            val_progress = kwargs["progress"]
        if "date" in kwargs:
            val_date = kwargs["date"]
        if "importance" in kwargs:
            val_importance = kwargs["importance"]
        if "content" in kwargs:
            val_content = kwargs

        repeat = obj.repeat
        if "repeat" in kwargs:
            repeat = kwargs["repeat"]

        self.cursor.execute(f"""
        UPDATE Todos
        SET TodoName='{val_name}', Done={1 if val_done else 0},
        Progress={val_progress},
        TodoDate='{val_date.strftime("%Y-%m-%d")}',
        Importance={val_importance},
        Content='{val_content}'
        WHERE TodoID = {id};
        """)
        self.connection.commit()

        r = self.cursor.execute(f"""
        SELECT * FROM TodoRepeats
        WHERE TodoID={id};
        """).fetchone()

        if repeat:
            if r:
                self.cursor.execute(f"""
                UPDATE TodoRepeats
                SET Days={repeat.day},
                WeekInterval={repeat.week_interval},
                DueDate='{repeat.due.strftime("%Y-%m-%d")}'
                WHERE TodoID={id}
                """)
            else:
                self.cursor.execute(f"""
                INSERT INTO TodoRepeats
                VALUES ( {id}, {repeat.day}, {repeat.week_interval}, '{repeat.due.strftime("%Y-%m-%d")}' );
                """)

            self.connection.commit()
        elif r:
            self.cursor.execute(f"""
            DELETE FROM TodoRepeats WHERE TodoID={id}
            """)
            self.connection.commit()

    def delete(self, id) -> None:
        self.cursor.execute(f"""
        DELETE FROM TodoRepeats WHERE TodoID={id}
        """)
        self.cursor.execute(f"""
        DELETE FROM Todos WHERE TodoID={id}
        """)
        self.connection.commit()


class ScheduleManager(Manager):
    def __init__(self, db_name="TIME.db"):
        super().__init__(db_name)
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Schedules(
            ScheduleID INTEGER PRIMARY KEY,
            ScheduleName TEXT NOT NULL,
            FromTime DATETIME2 NOT NULL,
            ToTime DATETIME2 NOT NULL,
            Importance INTEGER DEFAULT 0,
            Content TEXT NOT NULL
            );
            """
        ).execute(
            """
            CREATE TABLE IF NOT EXISTS ScheduleRepeats(
            ScheduleID INTEGER,
            Days INTEGER,
            WeekInterval INTEGER,
            DueDate DATE,
            FOREIGN KEY (ScheduleID) REFERENCES Schedules(ScheduleID)
            );
            """
        ).fetchall()

    def all(self) -> List['Schedule']:
        result = self.cursor.execute("""
        SELECT Schedules.ScheduleID, Schedules.ScheduleName, Schedules.FromTime, Schedules.ToTime,
         Schedules.Importance, Schedules.Content, ScheduleRepeats.Days,
         ScheduleRepeats.WeekInterval, ScheduleRepeats.DueDate
         FROM Schedules
        LEFT JOIN ScheduleRepeats ON Schedules.ScheduleID = ScheduleRepeats.ScheduleID
        """).fetchall()

        ret = []
        for item in result:
            r = Repeat(day=item[6], week_interval=item[7], due=datetime.strptime(item[8], "%Y-%m-%d").date()) if item[6] is not None else None
            ret.append(
                Schedule(id=item[0], name=item[1], from_time=datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S"),
                         to_time=datetime.strptime(item[3], "%Y-%m-%d %H:%M:%S"), repeat=r, importance=item[4],
                         content=item[5]))
        return ret

    def get(self, id) -> 'Schedule':
        item = self.cursor.execute(f"""
                SELECT Schedules.ScheduleID, Schedules.ScheduleName, Schedules.FromTime, Schedules.ToTime,
                 Schedules.Importance, Schedules.Content, ScheduleRepeats.Days,
                 ScheduleRepeats.WeekInterval, ScheduleRepeats.DueDate
                 FROM Schedules
                LEFT JOIN ScheduleRepeats ON Schedules.ScheduleID = ScheduleRepeats.ScheduleID
                WHERE Schedules.ScheduleID = {id}
                """).fetchall()

        if not item:
            raise ValueError("ID NOT EXIST")

        item = item[0]

        r = Repeat(day=item[6], week_interval=item[7], due=datetime.strptime(item[8], "%Y-%m-%d").date()) if item[6] is not None else None

        return Schedule(id=item[0], name=item[1], from_time=datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S"),
                        to_time=datetime.strptime(item[3], "%Y-%m-%d %H:%M:%S"), repeat=r, importance=item[4],
                        content=item[5])

    def create(self, obj=None, **kwargs) -> None:

        if not obj:
            if "name" not in kwargs:
                raise ValueError("Missing essential field 'name'")
            if "from_time" not in kwargs:
                raise ValueError("Missing essential field 'from_time'")
            if not isinstance(kwargs["from_time"], datetime):
                raise ValueError(
                    f"Invalid type for field 'from_time' (Expected='datetime', Got={type(kwargs['from_time'])}")
            if "to_time" not in kwargs:
                raise ValueError("Missing essential field 'to_time'")
            if not isinstance(kwargs["to_time"], datetime):
                raise ValueError(
                    f"Invalid type for field 'to_time' (Expected='datetime', Got={type(kwargs['to_time'])}")

            val_name = kwargs["name"]
            val_from_time = kwargs["from_time"]
            val_to_time = kwargs["to_time"]
            val_importance = 0 if "importance" not in kwargs else kwargs["importance"]
            val_content = "" if "content" not in kwargs else kwargs["content"]
        else:
            val_name = obj.name
            val_from_time = obj.from_time
            val_to_time = obj.to_time
            val_importance = obj.importance
            val_content = obj.content

        repeat = kwargs["repeat"] if "repeat" in kwargs else obj.repeat

        self.cursor.execute(f"""
        INSERT INTO Schedules(ScheduleName, FromTime, ToTime, Importance, Content)
        VALUES ( '{val_name}', '{val_from_time.strftime("%Y-%m-%d %H:%M:%S")}',
         '{val_to_time.strftime("%Y-%m-%d %H:%M:%S")}', {val_importance}, '{val_content}' );
        """)
        self.connection.commit()

        if repeat:
            id = self.cursor.execute("SELECT last_insert_rowid()").fetchone()
            self.cursor.execute(f"""
            INSERT INTO ScheduleRepeats
            VALUES ( {id[0]}, {repeat.day}, {repeat.week_interval}, '{repeat.due.strftime("%Y-%m-%d")}' );
            """)
            self.connection.commit()

    def update(self, id, obj=None, **kwargs) -> None:
        if not obj:
            obj = self.get(id)

        val_name = obj.name
        val_from_time = obj.from_time
        val_to_time = obj.to_time
        val_importance = obj.importance
        val_content = obj.content

        if "name" in kwargs:
            val_name = kwargs["name"]
        if "from_time" in kwargs:
            val_from_time = kwargs["from_time"]
        if "to_time" in kwargs:
            val_to_time = kwargs["to_time"]
        if "importance" in kwargs:
            val_importance = kwargs["importance"]
        if "content" in kwargs:
            val_content = kwargs["content"]

        self.cursor.execute(f"""
                UPDATE Schedules
                SET ScheduleName='{val_name}',
                FromTime='{val_from_time.strftime("%Y-%m-%d %H:%M:%S")}',
                ToTime='{val_to_time.strftime("%Y-%m-%d %H:%M:%S")}',
                Importance={val_importance},
                Content='{val_content}'
                WHERE ScheduleID = {id};
                """)
        self.connection.commit()

        r = self.cursor.execute(f"""
                SELECT * FROM ScheduleRepeats
                WHERE ScheduleID={id};
                """).fetchone()

        repeat = kwargs["repeat"] if "repeat" in kwargs else obj.repeat

        if obj.repeat:
            if r:
                self.cursor.execute(f"""
                        UPDATE ScheduleRepeats
                        SET Days={repeat.day},
                        WeekInterval={repeat.week_interval},
                        DueDate='{repeat.due.strftime("%Y-%m-%d")}'
                        WHERE ScheduleID={id}
                        """)
            else:
                self.cursor.execute(f"""
                        INSERT INTO ScheduleRepeats
                        VALUES ( {id}, {repeat.day}, {repeat.week_interval}, '{repeat.due.strftime("%Y-%m-%d")}' );
                        """)

            self.connection.commit()
        elif r:
            self.cursor.execute(f"""
                    DELETE FROM ScheduleRepeats WHERE ScheduleID={id}
                    """)
            self.connection.commit()

    def delete(self, id) -> None:
        self.cursor.execute(f"""
        DELETE FROM Schedules WHERE ScheduleID={id}
        """)
        self.cursor.execute(f"""
        DELETE FROM ScheduleRepeats WHERE ScheduleID={id}
        """)
        self.connection.commit()


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
    date: date
    progress: Optional[int] = 0
    repeat: Optional[Repeat] = None
    importance: Optional[int] = 0
    content: Optional[str] = ''


@dataclass
class Schedule:
    objects: ClassVar[Manager] = ScheduleManager()
    id: int
    name: str
    from_time: datetime
    to_time: datetime
    repeat: Optional[Repeat] = None
    importance: Optional[int] = 0
    content: Optional[str] = ''
