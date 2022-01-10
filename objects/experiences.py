from dataclasses import dataclass


@dataclass
class Workexperience:
    industry: str
    years_of_experience: str
    leadership_responsibility: bool

    def __str__(self) -> str:

        if self.leadership_responsibility:
            return f"{self.years_of_experience} experience in the '{self.industry}' " \
                   f"industry with leadership responsibility"
        else:
            return f"{self.years_of_experience} experience in the '{self.industry}' " \
                   f"industry without leadership responsibility"



if __name__ == '__main__':
    exp01 = Workexperience(
        industry="Bankenwesen",
        years_of_experience="< 2,5 Jahre",
        leadership_responsibility=True
    )

    exp02 = Workexperience(
        industry="Bankenwesen",
        years_of_experience="< 5 Jahre",
        leadership_responsibility=False
    )

    print(exp01)
    print(exp02)

