from contextlib import closing
import sqlite3
from typing import List, Type, Union

from objects.experiences import WorkExperience
from objects.jobcenter import Jobcenter
from objects.people import Coach, Employee, Participant
from objects.training import Training
from utils import custom_exceptions


class Database:
    """A class for establishing a connection to a data base"""

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.conn = None

    def connect_to_database(self) -> None:
        """Establish the connection to the data base"""

        self.conn = sqlite3.connect(self.database_path)
        self.conn.row_factory = sqlite3.Row

    def add_coach(self, coach: Coach) -> None:
        """Insert coach data into the data base"""

        sql = "INSERT INTO Coaches (Anrede, Vorname, Nachname) " \
              "VALUES (?, ?, ?)"

        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (coach.title, coach.first_name, coach.last_name))
            self.conn.commit()

        print(f"{coach} successfully added to the database.")

    def add_language_skill(self, participant_database_id: str, language: str, level: str) -> None:
        """Add a language including level of proficiency for a particular participant to the database"""

        sql = "INSERT INTO Sprachkenntnisse (Teilnehmer_ID, Sprache, Level) " \
              "VALUES (?, ?, ?)"

        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (participant_database_id, language, level))
            self.conn.commit()

    def add_jobcenter(self, jobcenter: Jobcenter) -> None:
        """Insert jobcenter data into the data base"""

        sql = "INSERT INTO Jobcenter (Name, 'E-Mail', Strasse, Nr, PLZ, Stadt) " \
              "VALUES (?, ?, ?, ?, ?, ?)"

        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (jobcenter.name, jobcenter.email, jobcenter.street, jobcenter.street_nr,
                                 jobcenter.zip_code, jobcenter.city))
            self.conn.commit()

        print(f"{jobcenter} successfully added to the database.")

    def add_work_experience(self, participant: Participant, work_experience: WorkExperience) -> None:
        """Insert workexperience data into the data base"""

        sql = "INSERT INTO Arbeitserfahrung ('Teilnehmer-ID', Branche, Dauer, Führungsverantwortung) " \
              "VALUES (?, ?, ?)"

        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (participant.data_base_id, work_experience.industry,
                                 work_experience.years_of_experience, work_experience.leadership_responsibility))
            self.conn.commit()

        print(f"{work_experience} successfully added to the database for participant {participant.full_name}.")

    def add_participant(self, participant: Participant) -> None:
        """Insert participant data into the data base"""
        sql = "INSERT INTO Teilnehmer (Anrede, Vorname, Nachname, Strasse_und_Nr, PLZ, Stadt, Herkunftsland," \
              "Führerschein, Kundennummer, 'E-Mail', Handynummer, Aufenthaltsstatus, Muttersprache, " \
              "'Schulabschluss in Deutschland') " \
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (participant.title, participant.first_name, participant.last_name,
                                 participant.street_and_nr, participant.zip_code, participant.city,
                                 participant.country_of_origin, participant.driving_license,
                                 participant.id_with_jc, participant.email, participant.cell_phone_nr,
                                 participant.residency_status, participant.mother_tongue,
                                 participant.school_degree_germany))
            self.conn.commit()

        print(f"{participant} successfully added to the database.")

    def check_for_coach_full_name(self, coach_first_name: str, coach_last_name: str) -> bool:
        """Check whether an entry for a coach with a given first and last name"""

        sql = "SELECT * FROM Coaches WHERE Vorname = ? AND Nachname = ?"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, [coach_first_name, coach_last_name])
            row = cursor.fetchone()

        if row is None:
            return False
        else:
            return True

    def check_for_jobcenter_name(self, jobcenter_name: str) -> bool:
        """Check whether a Jobcenter with a given name exists in database"""

        sql = "SELECT * FROM Jobcenter WHERE Name = ?"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, [jobcenter_name])
            row = cursor.fetchone()

        if row is None:
            return False
        else:
            return True

    def check_for_participant_jc_id(self, jobcenter_id: str) -> bool:
        """Check whether an entry for a participant with a given jobcenter ID (Kundennummer) exists"""

        sql = "SELECT * FROM Teilnehmer WHERE Kundennummer = ?"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, [jobcenter_id])
            row = cursor.fetchone()

        if row is None:
            return False
        else:
            return True

    def get_column_names(self, table_name: str) -> List[str]:
        """Get a list of all column names of a table in database"""

        # prevent sql injection
        if not table_name.isalnum():
            raise custom_exceptions.SQLInjectionWarning

        sql = f"SELECT * FROM {table_name}"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            column_names = [description[0] for description in cursor.description]

        return column_names

    def get_coaches(self) -> List[Coach]:
        """Return a list of all coaches found in the database"""

        sql = "SELECT * FROM Coaches"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        coaches = []
        for the_row in results:
            coaches.append(self.create_coach(sqlite3_row=the_row))

        return coaches

    def get_employees(self) -> List[Employee]:
        """Return a list of all employees found in the database"""

        sql = "SELECT * FROM Mitarbeiter"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        employees = []
        for row in results:
            employees.append(self.create_employee(sqlite3_row=row))

        return employees

    def get_jobcenters(self) -> List[Jobcenter]:
        """Return a list of all jobcenters found in the database"""

        sql = "SELECT * FROM Jobcenter"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        jobcenter = []
        for row in results:
            jobcenter.append(self.create_jobcenter(sqlite3_row=row))

        return jobcenter

    def get_participants(self) -> List[Participant]:
        """Return a list of all participants found in the database"""

        sql = "SELECT * FROM Teilnehmer"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        participants = []
        for row in results:
            participants.append(self.create_participant(sqlite3_row=row))

        return participants

    def get_trainings(self) -> List[Training]:
        """Return a list of all trainings found in the database"""

        sql = "SELECT * FROM Massnahmen"
        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        trainings = []
        for row in results:
            trainings.append(self.create_training(sqlite3_row=row))

        return trainings

    def select_multiple_query(self, query: str) -> List[sqlite3.Row]:
        """Executes a select statement and returns all result rows of the table."""

        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def select_single_query(self, query: str, arguments: Union[None, list] = None) -> sqlite3.Row:
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

    def update_password(self, user_id: str, password: str) -> bool:
        """Updates a password for an existing user"""

        # check if user exists
        sql = "SELECT * FROM Passwoerter WHERE ID = ?"
        row = self.select_single_query(sql, arguments=[user_id])
        if row is None:
            print(f"The database does not contain a user with the ID {user_id}.")
            print("Password cannot be updated.")
            return False

        # update password
        print("Ok, lets update the password.")

        self.connect_to_database()
        with closing(self.conn.cursor()) as cursor:
            sql = "UPDATE Passwoerter SET Passwort = ? WHERE ID = ?"
            cursor.execute(sql, (password, user_id))
            self.conn.commit()
        print(f"Password for user with the ID {user_id} successfully updated.")
        return True

    @staticmethod
    def create_coach(sqlite3_row: sqlite3.Row) -> Coach:
        """Create an Participant object from an sqlite3.Row"""

        return Coach(title=sqlite3_row["Anrede"],
                     first_name=sqlite3_row["Vorname"],
                     last_name=sqlite3_row["Nachname"],
                     data_base_id=sqlite3_row["ID"],
                     )

    @staticmethod
    def create_employee(sqlite3_row: sqlite3.Row) -> Employee:
        """Create an Employee object from an sqlite3.Row"""

        return Employee(title=sqlite3_row["Anrede"],
                        first_name=sqlite3_row["Vorname"],
                        last_name=sqlite3_row["Nachname"],
                        data_base_id=sqlite3_row["ID"]
                        )

    @staticmethod
    def create_jobcenter(sqlite3_row: sqlite3.Row) -> Jobcenter:
        """Create a Jobcenter object from an sqlite3.Row"""

        return Jobcenter(name=sqlite3_row["Name"],
                         street=sqlite3_row["Strasse"],
                         street_nr=sqlite3_row["Nr"],
                         zip_code=sqlite3_row["PLZ"],
                         city=sqlite3_row["Stadt"],
                         data_base_id=sqlite3_row["ID"]
                         )

    @staticmethod
    def create_participant(sqlite3_row: sqlite3.Row) -> Participant:
        """Create an Participant object from an sqlite3.Row"""

        return Participant(title=sqlite3_row["Anrede"],
                           first_name=sqlite3_row["Vorname"],
                           last_name=sqlite3_row["Nachname"],
                           street_and_nr=sqlite3_row["Strasse_und_Nr"],
                           zip_code=sqlite3_row["PLZ"],
                           city=sqlite3_row["Stadt"],
                           email=sqlite3_row["E-Mail"],
                           cell_phone_nr=sqlite3_row["Handynummer"],
                           residency_status=sqlite3_row["Aufenthaltsstatus"],
                           client_id_with_jc=sqlite3_row["Kundennummer"],
                           country_of_origin=sqlite3_row["Herkunftsland"],
                           driving_license=sqlite3_row["Führerschein"],
                           mother_tongue=sqlite3_row["Muttersprache"],
                           school_degree_germany=sqlite3_row["Schulabschluss in Deutschland"],
                           data_base_id=sqlite3_row["ID"]
                           )

    @staticmethod
    def create_training(sqlite3_row: sqlite3.Row) -> Training:
        """Create a Training object from an sqlite3.Row"""

        cost_per_training_lesson = sqlite3_row["Kosten_pro_UE"]

        # convert to float
        try:
            cost_per_training_lesson = float(cost_per_training_lesson)
        except ValueError:
            cost_per_training_lesson = float(cost_per_training_lesson.replace(",", "."))

        return Training(name=sqlite3_row["Bezeichnung"],
                        cost_per_training_lesson=cost_per_training_lesson,
                        data_base_id=sqlite3_row["ID"])

    @staticmethod
    def create_work_experience(sqlite3_row: sqlite3.Row) -> WorkExperience:
        """Create a work experience object from an sqlite3.Row"""

        return WorkExperience(
            industry=sqlite3_row["Branche"],
            years_of_experience=sqlite3_row["Dauer"],
            leadership_responsibility=sqlite3_row["Führungsverantwortung"]
        )

    @classmethod
    def test_database(cls) -> "Database":
        return cls(database_path="../../Database/test_database.db")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.database_path})"


if __name__ == '__main__':
    test_db = Database.test_database()
    # print(test_db.check_for_coach_full_name(coach_first_name="Erika", coach_last_name="Musterfrau"))
    print(test_db.select_single_query.__annotations__)
    row = test_db.select_single_query("SELECT * FROM Coaches WHERE ID = 2")
    print(row)
    print(type(row))
