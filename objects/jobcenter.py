class Jobcenter():

    def __init__(self, name, street_and_nr, zip_code, city, email=None, data_base_id=None):
        self.name = name
        self.street_and_nr = street_and_nr
        self.zip_code = zip_code
        self.city = city
        self.email = email
        self.data_base_id = data_base_id

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.street_and_nr!r}, {self.zip_code!r}, {self.city!r}, " \
               f"{self.email}, {self.data_base_id})"

    @classmethod
    def jobcenter_berlin_mitte(cls):
        return cls(name="Jobcenter Berlin Mitte", street_and_nr="Seydelstr. 2-5", zip_code="10117", city="Berlin")


if __name__ == '__main__':
    jc = Jobcenter.jobcenter_berlin_mitte()
    print(jc)