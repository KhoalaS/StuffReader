from dataclasses import dataclass
import sqlite3
from flask import g


@dataclass
class GalleryState:
    handle: str
    id: str
    completed: bool
    bookmarked: bool
    last_page: int


class DbService:
    @staticmethod
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect("data.db")
            db.row_factory = sqlite3.Row
        return db

    def createState(self, handle: str, id: str, cur: sqlite3.Cursor):
        cur.execute(
            "INSERT INTO gallery_state VALUES (?,?,?,?,?)", (handle, id, False, False, 1))
        self.get_db().commit()

    def hasState(self, handle: str, id: str, cur: sqlite3.Cursor):

        cur.execute(
            "SELECT * FROM gallery_state WHERE handle = ? AND id = ?", (handle, id))
        state = cur.fetchone()
        return state is not None

    def getState(self, handle: str, id: str) -> GalleryState:
        cur = self.get_db().cursor()
        if not self.hasState(handle, id, cur):
            self.createState(handle, id, cur)

        cur.execute(
            "SELECT * FROM gallery_state WHERE handle = ? AND id = ?", (handle, id))
        state: GalleryState = cur.fetchone()
        return state

    def setBookmark(self, handle: str, id: str, value: bool):
        cur = self.get_db().cursor()

        if not self.hasState(handle, id, cur):
            self.createState(handle, id, cur)

        cur.execute(
            "UPDATE gallery_state SET bookmarked = ? WHERE handle = ? AND id = ?", (value, handle, id))
        self.get_db().commit()

    def setCompleted(self, handle: str, id: str, value: bool):
        cur = self.get_db().cursor()

        if not self.hasState(handle, id, cur):
            self.createState(handle, id, cur)

        cur.execute(
            "UPDATE gallery_state SET completed = ? WHERE handle = ? AND id = ?", (value, handle, id))
        self.get_db().commit()

    def setLastPage(self, handle: str, id: str, value: int):
        cur = self.get_db().cursor()

        if not self.hasState(handle, id, cur):
            self.createState(handle, id, cur)

        cur.execute(
            "UPDATE gallery_state SET last_page = ? WHERE handle = ? AND id = ?", (value, handle, id))
        self.get_db().commit()
