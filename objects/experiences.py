from dataclasses import dataclass, field
import datetime


@dataclass(order=True)
class Workexperience:
    sort_index: datetime.date = field(init=False, repr=False)
    start_date: datetime.date
    end_date: datetime.date
    description: str

    def __post_init__(self) -> None:
        self.sort_index = self.start_date

    def __str__(self) -> str:
        format = "%Y-%m-%d"
        return f"Workexperience from {self.start_date.strftime(format)} until {self.end_date.strftime(format)}" \
               f" - description: {self.description}"


if __name__ == '__main__':
    exp01 = Workexperience(
        start_date=datetime.date(2019, 12, 13),
        end_date=datetime.date(2021, 1, 31),
        description="Mein Job"
    )

    exp02 = Workexperience(
        start_date=datetime.date(2020, 12, 13),
        end_date=datetime.date(2021, 1, 31),
        description="Mein Job"
    )

    print(exp02>exp01)
    print(exp02)

