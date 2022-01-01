import random
import sqlite3
import unittest

from databases.database import Database
from objects import jobcenter, training
from objects import people as people
import utils.helpers as helpers
from utils import custom_exceptions

class CheckForExistingEntries(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database("../../Database/unittest_test_database.db")

    def test_check_for_coach_full_name(self) -> None:
        coach_first_name = "Erika"
        coach_last_name = "Mustermann"
        output = self.db.check_for_coach_full_name(coach_first_name=coach_first_name, coach_last_name=coach_last_name)
        # self.assertEqual(target_output, output)
        self.assertTrue(output)

        coach_first_name = "Jimmy"
        coach_last_name = "Johnson"
        output = self.db.check_for_coach_full_name(coach_first_name=coach_first_name, coach_last_name=coach_last_name)
        self.assertFalse(output)

    def test_check_for_jobcenter_name(self) -> None:
        jc_name = "Testjobcenter"
        output = self.db.check_for_jobcenter_name(jobcenter_name=jc_name)
        self.assertTrue(output)

        jc_name = "Ein anderes Jobcenter"
        output = self.db.check_for_jobcenter_name(jobcenter_name=jc_name)
        self.assertFalse(output)

    def test_check_for_participant_jc_id(self) -> None:
        participant_jc_id = "123asd"
        output = self.db.check_for_participant_jc_id(jobcenter_id=participant_jc_id)
        self.assertTrue(output)

        participant_jc_id = "someotherid1234jasd"
        output = self.db.check_for_participant_jc_id(jobcenter_id=participant_jc_id)
        self.assertFalse(output)


class GetFunctions(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database("../../Database/unittest_test_database.db")

    def test_get_column_names(self) -> None:
        output = self.db._get_column_names(table_name="Teilnehmer")
        target_output = ["ID", "Anrede", "Vorname", "Nachname", "Strasse_und_Nr", "PLZ", "Stadt", "Kundennummer"]
        self.assertEqual(target_output, output)

        self.assertRaises(custom_exceptions.SQLInjectionWarning, self.db._get_column_names,
                          table_name="Teilnehmer; drop Teilnehmer")


    def test_get_employees(self) -> None:
        employees = self.db.get_employees()
        for employee in employees:
            self.assertIsInstance(employee, people.Employee)

    def test_get_jobcenters(self) -> None:
        jcs = self.db.get_jobcenters()
        for employee in jcs:
            self.assertIsInstance(employee, jobcenter.Jobcenter)

    def test_get_participants(self) -> None:
        participants = self.db.get_participants()
        for participant in participants:
            self.assertIsInstance(participant, people.Participant)

    def test_get_trainings(self) -> None:
        trainings = self.db.get_trainings()
        for train in trainings:
            self.assertIsInstance(train, training.Training)


class UpdatePassword(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database("../../Database/unittest_test_database.db")
        self.sql = "SELECT * FROM Passwoerter WHERE ID = 1"
        self.old_password = self.db.select_single_query(self.sql)["Passwort"]

    def test_update_password(self) -> None:
        universe = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        new_password = "".join(random.sample(universe, 10))
        new_hashed_password = helpers.hash_password(new_password)
        target_output = self.db.update_password(user_id="1", password=new_hashed_password)
        new_pwd_in_db = self.db.select_single_query(self.sql)["ID"]
        self.assertNotEqual(self.old_password, new_pwd_in_db)
        self.assertTrue(target_output)

    def test_bad_user_id(self) -> None:
        target_output = self.db.update_password(user_id="some non existent user id", password="new password")
        self.assertFalse(target_output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
