class Jobcenter:

    def __init__(self, name: str, street: str, street_nr: str, zip_code: str, city: str, email: str = None,
                 data_base_id: str = None) -> None:
        self.name = name
        self.street = street
        self.street_nr = street_nr
        self.zip_code = zip_code
        self.city = city
        self.email = email
        self.data_base_id = data_base_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.street!r}, {self.street_nr!r}, {self.zip_code!r}, " \
               f"{self.city!r}, {self.email}, {self.data_base_id})"

    @classmethod
    def jobcenter_berlin_mitte(cls) -> "Jobcenter":
        """Factory method for creating Jobcenter Berlin Mitte"""
        return cls(name="Jobcenter Berlin Mitte", street="Seydelstr.", street_nr="2-5",
                   zip_code="10117", city="Berlin")


if __name__ == '__main__':
    jc = Jobcenter.jobcenter_berlin_mitte()
    print(jc)