import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id:
            self.update()
        else:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        CONN.commit()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        all_rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in all_rows]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
