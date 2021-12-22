import sqlite3
from contextlib import closing
import datetime

from objects.jobcenter import Jobcenter
from objects.people import Employee, Participant
from objects.training import Training


class Database:
    """A class for establishing a connection to a data base"""

    def __init__(self, database_path):
        self.database_path = database_path
        self.conn = None

    def connect_to_database(self):
        """Establish the connection to the data base"""

        self.conn = sqlite3.connect(self.database_path)
        self.conn.row_factory = sqlite3.Row

    def get_employees(self):
        """Return a list of all employees found in the database"""
        sql = "SELECT * FROM Mitarbeiter"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        employees = []
        for row in results:
            employees.append(self.create_employee(row=row))

        return employees

    def get_jobcenters(self):
        """Return a list of all jobcenters found in the database"""

        sql = "SELECT * FROM Jobcenter"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        jobcenter = []
        for row in results:
            jobcenter.append(self.create_jobcenter(row=row))

        return jobcenter

    def get_participants(self):
        """Return a list of all participants found in the database"""

        sql = "SELECT * FROM Teilnehmer"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        participants = []
        for row in results:
            participants.append(self.create_participant(row=row))

        return participants

    def get_trainings(self):
        """Return a list of all trainings found in the database"""

        sql = "SELECT * FROM Massnahmen"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        trainings = []
        for row in results:
            trainings.append(self.create_training(row=row))

        return trainings

    def select_single_query(self, query, arguments=None):
        """Executes a select statement and returns the first result of the table row"""

        self.connect_to_database()

        with closing(self.conn.cursor()) as cursor:
            if arguments:
                if len(arguments) == 1:
                    cursor.execute(query, (arguments[0],))
                else:
                    cursor.execute(query, (arguments))
            else:
                cursor.execute(query)
            return cursor.fetchone()

    @staticmethod
    def create_employee(row):
        return Employee(title=row["Anrede"],
                           first_name=row["Vorname"],
                           last_name=row["Nachname"],
                           data_base_id=row["ID"]
                           )

    @staticmethod
    def create_jobcenter(row):
        return Jobcenter(name=row["Name"],
                         street_and_nr=row["Strasse"] + " " + row["Nr"],
                         zip_code=row["PLZ"],
                         city=row["Stadt"],
                         data_base_id=row["ID"]
                         )

    @staticmethod
    def create_participant(row):
        return Participant(title=row["Anrede"],
                           first_name=row["Vorname"],
                           last_name=row["Nachname"],
                           street_and_nr=row["Strasse_und_Nr"],
                           zip_code=row["PLZ"],
                           city=row["Stadt"],
                           client_id_with_jc=row["Kundennummer"],
                           data_base_id=row["ID"]
                           )

    @staticmethod
    def create_training(row):

        cost_per_training_lesson = row["Kosten_pro_UE"]

        # convert to float
        try:
            cost_per_training_lesson = float(cost_per_training_lesson)
        except ValueError:
            cost_per_training_lesson = float(cost_per_training_lesson.replace(",", "."))

        return Training(name=row["Bezeichnung"],
                        cost_per_training_lesson=cost_per_training_lesson,
                        data_base_id=row["ID"])

    @classmethod
    def test_database(cls):
        return cls(database_path="../../Database/test_database.db")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.database_path})"


if __name__ == '__main__':
    test_db = Database.test_database()
    print(test_db)

    employees = test_db.get_employees()

    for employee in employees:
        print(employee)
