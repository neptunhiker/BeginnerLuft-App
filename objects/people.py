import random
from typing import Tuple, Union


class Human:

    def __init__(self, title: str, first_name: str, last_name: str) -> None:
        self.title = title
        self._first_name = first_name
        self._last_name = last_name
        self._full_name = f"{first_name} {last_name}"

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        self._first_name = value
        self._full_name = f"{self._first_name} {self._last_name}"

    @last_name.setter
    def last_name(self, value: str) -> None:
        self._last_name = value
        self._full_name = f"{self._first_name} {self._last_name}"

    @full_name.setter
    def full_name(self, value: str) -> None:
        raise AttributeError


class Employee(Human):

    def __init__(self, title: str, first_name: str, last_name: str, data_base_id: str = None) -> None:
        super(Employee, self).__init__(title=title, first_name=first_name, last_name=last_name)
        self.data_base_id = data_base_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title}, {self.first_name}, {self.last_name}, {self.data_base_id})"


class Participant(Human):

    def __init__(self, title: str, first_name: str, last_name: str, street_and_nr: str = None,
                 zip_code: Union[None, str] = None, city: Union[None, str] = None,
                 client_id_with_jc: Union[None, str] = None, country_of_origin: str = None,
                 driving_license: Union[None, bool] = None, data_base_id: Union[None, str] = None) -> None:
        super().__init__(title=title, first_name=first_name, last_name=last_name)
        self.street_and_nr = street_and_nr
        self.zip_code = zip_code
        self.city = city
        self.avgs_coupons = {}
        self.id_with_jc = client_id_with_jc
        self.country_of_origin = country_of_origin
        self.driving_license = driving_license
        self.data_base_id = data_base_id

    @classmethod
    def test_participant(cls, male_or_female="female") -> "Participant":
        title, first_name, last_name = NameCreator.create_name(male_or_female)

        streets = ["Berlinerstr.", "Bergerstr.", "Kudamm", "Müllerstr.", "Seestr.", "Alt Moabit",
                   "Waidmannsluster Damm"]
        street_and_nr = f"{random.choice(streets)} {str(random.randint(1, 123))}"
        zip_code = "12345"
        city = "Berlin"
        id_with_jc = str(random.randint(1000000000, 9999999999)) + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        return cls(title=title, first_name=first_name, last_name=last_name, street_and_nr=street_and_nr,
                   zip_code=zip_code, city=city, client_id_with_jc=id_with_jc)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name} {self.street_and_nr} {self.zip_code} {self.city} " \
               f"Kundennummer: {self.id_with_jc}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title}, {self.first_name}, {self.last_name}, {self.street_and_nr}, " \
               f"{self.zip_code}, {self.city}, {self.id_with_jc}, {self.data_base_id})"


class Coach(Human):

    def __init__(self, title: str, first_name: str, last_name: str, data_base_id: Union[None, str] = None) -> None:
        super().__init__(title=title, first_name=first_name, last_name=last_name)
        self.data_base_id = data_base_id

    @classmethod
    def test_coach(cls) -> "Coach":
        """Factory method for creating a test coach"""
        title, first_name, last_name = NameCreator.create_name()
        return cls(title, first_name, last_name)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title}, {self.first_name}, {self.last_name}, {self.data_base_id})"


class NameCreator:

    @classmethod
    def create_name(cls, male_or_female: Union[None, str]) -> Tuple[str, str, str]:
        """Creates a random name including title in German"""

        if male_or_female is None:
            male_or_female = random.choice(("male", "female"))

        female_first_names = ["Aliya", "Amira", "Halima", "Joelle", "Lara", "Nehal", "Rimas", "Tanisha"]
        male_first_names = ["Fahed", "Fathi", "Hamdi", "Inaam", "Jasem", "Karim", "Rabih", "Samir"]
        last_names = ["Habib", "Ali", "Ayad", "Bakir", "Noor", "Qadir", "Khoury", "Al Rashid", "Syed"]

        if male_or_female == "female":
            title = "Frau"
            first_name = random.choice(female_first_names)
        else:
            title = "Herr"
            first_name = random.choice(male_first_names)
        last_name = random.choice(last_names)

        return title, first_name, last_name


def main():
    aishe = Participant.test_participant()
    print(repr(aishe))
    print(aishe)


if __name__ == '__main__':
    main()
