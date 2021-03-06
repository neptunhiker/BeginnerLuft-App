import datetime
import random

from objects.jobcenter import Jobcenter
from objects.people import Participant
from objects.training import Training


class Invoice:

    def __init__(self, invoice_nr: str, total_amount: float, creation_date: datetime.date,
                 target_date: datetime.date, jobcenter: Jobcenter,
                 nr_training_lessons: int, participant: Participant, training: Training,
                 signer: str = "BeginnerLuft gGmbH", money_inflow=None) -> None:

        self.invoice_nr = invoice_nr
        self.total_amount = total_amount
        self.creation_date = creation_date
        self.target_date = target_date
        self.jobcenter = jobcenter
        self.nr_training_lessons = nr_training_lessons
        self.cost_per_training_lesson = training.cost_per_training_lesson
        self.participant = participant
        self.money_inflow = money_inflow
        self.signer = signer
        self.training = training

    @classmethod
    def test_invoice(cls, participant: Participant, jobcenter: Jobcenter) -> "Invoice":
        """Factory method for creating a test invoice"""

        invoice_nr = str(random.randint(201906, 202112)) + "-" + str(random.randint(10, 99))
        nr_training_lessons = random.randint(20, 50)
        cost_per_training_lesson = random.randint(10, 100)
        total_amount = nr_training_lessons * cost_per_training_lesson
        creation_date = datetime.date(year=random.randint(2019, 2021), month=random.randint(1, 12),
                                      day=random.randint(1,28))
        target_date = creation_date + datetime.timedelta(days=14)
        training = Training.test_training()

        return cls(invoice_nr=invoice_nr, total_amount=total_amount, creation_date=creation_date,
                   target_date=target_date, jobcenter=jobcenter, nr_training_lessons=nr_training_lessons,
                   training=training, participant=participant)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.invoice_nr}, {self.total_amount}, {self.creation_date}, " \
               f"{self.target_date}, {self.jobcenter}, {self.nr_training_lessons}, {self.participant}, " \
               f"{self.training}, {self.signer}, {self.money_inflow})"


if __name__ == '__main__':

    jc = Jobcenter.jobcenter_berlin_mitte()
    participant = Participant.test_participant()
    invoice = Invoice.test_invoice(participant=participant, jobcenter=jc)
    print(invoice)

