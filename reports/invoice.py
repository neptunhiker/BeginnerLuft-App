from abc import ABC, abstractmethod
import datetime

import reportlab.platypus
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image, Paragraph, Table
from typing import List

from objects.invoice import Invoice
from objects.jobcenter import Jobcenter
from objects.people import Participant
from objects.training import Training
from utils import helpers, custom_exceptions


class PDFReport(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_header(cls):
        pass

    @abstractmethod
    def create_body(cls):
        pass

    @abstractmethod
    def create_footer(cls):
        pass

    @abstractmethod
    def save_report(self):
        pass


class PDFInvoice(PDFReport):
    """An invoice in pdf format"""

    def __init__(self, invoice_name: str, invoice: Invoice, time_period_start: datetime.date,
                 time_period_end: datetime.date, nr_of_training_lessons: int,
                 image_gallery_path: str = "../Assets",
                 path: str = "../../Output/PDF Rechnungen", save_file: bool = True,
                 show_success_message: bool = True) -> None:

        self.image_gallery_path = image_gallery_path
        self.invoice = invoice
        self.participant = invoice.participant
        self.training = invoice.training
        self.jobcenter = invoice.jobcenter
        self.creation_date = invoice.creation_date
        self.date_for_title = invoice.creation_date.strftime('%Y-%m-%d')
        self.date_for_invoice = helpers.format_to_german_date(self.creation_date)
        self.payment_horizon = (invoice.target_date - self.creation_date).days
        self.latest_payment_date = helpers.format_to_german_date(invoice.target_date)
        super().__init__()
        self.participant_name = self.participant.full_name
        self.participant_title = self.participant.title
        self.participant_id = self.participant.id_with_jc
        self.invoice_nr = self.invoice.invoice_nr
        self.time_period_start = time_period_start
        self.time_period_end = time_period_end
        self.training_name = self.training.name
        self.nr_of_training_lessons = nr_of_training_lessons
        self.cost_per_training_lesson = self.invoice.training.cost_per_training_lesson
        self.total_cost = round(self.nr_of_training_lessons * self.cost_per_training_lesson, 2)
        self.signer = invoice.signer
        self.iban = "DE28 4306 0967 1014 6919"
        self.bic = "GENODEM1GLS"
        self.bl_name = "BeginnerLuft gGmbH"
        self.bl_street = "Bandelstr. 1"
        self.bl_zip_city = "10559 Berlin"
        self.path = path
        self.full_path = f"{path}/{invoice_name}.pdf"

        self.width = A4[0]
        self.height = A4[1]

        # Create the pdf
        self.pdf = canvas.Canvas(self.full_path, pagesize=A4)
        self.pdf.setTitle(invoice_name)

        # Defining the size-structure of the report
        self.col_widths = [0.1 * self.width, 0.8 * self.width, 0.1 * self.width]
        self.row_heights = [0.17 * self.height, 0.73 * self.height, 0.1 * self.height]

        # Creating the main table of the report
        main_table = Table([
            ["", self.create_header(), ""],
            ["", self.create_body(), ""],
            ["", self.create_footer(), ""]
        ],
            colWidths=self.col_widths,
            rowHeights=self.row_heights
        )

        # Style of main table
        main_table.setStyle([
            # ('GRID', (0, 0), (-1, -1), 1, "red"),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ("LINEBELOW", (1, 0), (1, 0), 1, "grey"),
            ("LINEBELOW", (1, 1), (1, 1), 1, "grey"),
        ])

        main_table.wrapOn(self.pdf, 0, 0)
        main_table.drawOn(self.pdf, 0, 0)

        if save_file:
            self.save_report()
            if show_success_message:
                self.show_success_message()

    def create_header(self) -> reportlab.platypus.Table:
        """Create a header for the report"""

        img_path = f"{self.image_gallery_path}/logos/beginnerluft.png"
        img_width = self.col_widths[1] * 0.3
        img_height = self.row_heights[0] * 0.5
        img = Image(filename=img_path, width=img_width, height=img_height, kind="proportional")

        res = Table([
            [img],
            [f"{self.bl_name} - {self.bl_street} - {self.bl_zip_city}"]
        ],
            colWidths=self.col_widths[1],
            rowHeights=self.row_heights[0] / 2
        )

        res.setStyle([
            # ("VALIGN", (0, -1), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (0, 0), -40),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("TEXTCOLOR", (0, 0), (-1, -1), "grey"),
        ])

        return res

    def create_body(self) -> reportlab.platypus.Table:

        height_list = [0.15, 0.1, 0.05, 0.05, 0.45, 0.2]
        height_list = [height * self.row_heights[1] for height in height_list]

        res = Table([
            [self._body_create_address_for_recipient()],
            [self._body_create_address_bl()],
            [self._body_create_date_and_invoice_nr()],
            ["RECHNUNG"],
            [self._body_create_intro_text()],
            [self._body_create_greetings()],
        ],
            rowHeights=height_list
        )

        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("FONTSIZE", (0, 3), (-1, 3), 12),
            ("BOTTOMPADDING", (0, 3), (-1, 3), 12),
        ])

        return res

    def _body_create_address_for_recipient(self) -> List[reportlab.platypus.Paragraph]:
        """Create the adress field for the job center"""

        street_and_nr = f"{self.jobcenter.street} {self.jobcenter.street_nr}"
        para_list = []
        para_01 = Paragraph(f"""
                An das <br/>
                <b>{self.jobcenter.name}</b><br/>
                <b>{street_and_nr}</b><br/>
                <b>{self.jobcenter.zip_code} {self.jobcenter.city}</b>
                """)
        para_list.append(para_01)
        return para_list

    def _body_create_address_bl(self) -> List[reportlab.platypus.Paragraph]:
        """Create the address field for BeginnerLuft"""

        para_list = []
        para_01_style = ParagraphStyle("para_01_style")
        para_01_style.alignment = 0  # 2 = alignment RIGHT
        para_01 = Paragraph(f"""
                {self.bl_name}<br/>
                {self.bl_street}<br/>
                {self.bl_zip_city}
                """, para_01_style)
        para_list.append(para_01)
        return para_list

    def _body_create_date_and_invoice_nr(self) -> List[reportlab.platypus.Paragraph]:
        """Create date and invoice nr"""

        para_list = []
        para_01_style = ParagraphStyle("para_01_style")
        para_01_style.alignment = 2  # 2 = alignment RIGHT
        para_01 = Paragraph(f"""
                {self.date_for_invoice}<br/>
                """, para_01_style)
        para_list.append(para_01)
        return para_list

    def _body_create_intro_text(self) -> List[reportlab.platypus.Paragraph]:
        """Create the introductory text for the invoice"""
        if self.participant_title == "Herr":
            title = "Herrn"
        elif self.participant_title == "Frau":
            title = "Frau"
        else:
            title = ""

        para_list = []

        para_01 = Paragraph(f"""
        Sehr geehrte Damen und Herren,<br/><br/>

        hiermit stellen wir Ihnen unsere Leistungen im Rahmen der Ma??name "{self.training_name}"
        f??r {title} {self.participant_name} (Kundennummer {self.participant_id}) in Rechnung:<br/><br/><br/>
        """)

        if self.time_period_start.year == self.time_period_end.year:
            start_date = self.time_period_start.strftime("%d.%m.")
        else:
            start_date = self.time_period_start.strftime("%d.%m.%Y")
        end_date = self.time_period_end.strftime("%d.%m.%Y")

        # Format into German number formatting
        total_costs_formatted = str('{:0,.2f}'.format(self.total_cost)). \
            replace(".", "X").replace(",", ".").replace("X", ",")
        costs_per_training_formatted = str('{:0,.2f}'.format(self.cost_per_training_lesson).replace(".", ","))

        para_02 = Paragraph(f"""
            Rechnungsnummer: {self.invoice_nr}<br/>
            Zeitraum: {start_date} bis {end_date}<br/>
            {self.nr_of_training_lessons} Unterrichtseinheiten ?? 45 Minuten<br/>
            Kosten pro Unterrichtseinheit: {costs_per_training_formatted} ???<br/>
            <b>Rechnungsbetrag: {total_costs_formatted} ???</b><br/><br/><br/>
            """)

        para_03 = Paragraph(f"""
            Bitte ??berweisen Sie den Rechnungsbetrag innerhalb der n??chsten {self.payment_horizon} Tage, sp??testens bis 
            zum {self.latest_payment_date} auf folgendes Konto:<br/><br/>

            BeginnerLuft gGmbH<br/>
            IBAN: {self.iban}<br/>
            BIC: {self.bic}<br/>
            Verwendungszweck: {self.invoice_nr}
            """)

        para_list.append(para_01)
        para_list.append(para_02)
        para_list.append(para_03)

        return para_list

    def _body_create_invoice_details(self) -> reportlab.platypus.Table:
        """Create the details for the invoice"""

        if self.time_period_start.year == self.time_period_end.year:
            start_date = self.time_period_start.strftime("%d.%m.")
        else:
            start_date = self.time_period_start.strftime("%d.%m.%Y")
        end_date = self.time_period_end.strftime("%d.%m.%Y")

        # Format into German number formatting
        total_costs_formatted = str('{:0,.2f}'.format(self.total_cost)). \
            replace(".", "X").replace(",", ".").replace("X", ",")
        costs_per_training_formatted = str('{:0,.2f}'.format(self.cost_per_training_lesson).replace(".", ","))

        res_table = Table([
            [f"Rechnungsnummer: {self.invoice_nr}"],
            [f"Zeitraum: {start_date} bis {end_date}"],
            [f"{self.nr_of_training_lessons} Unterrichtseinheiten ?? 45 Minuten"],
            [f"Kosten pro Unterrichtseinheit: {costs_per_training_formatted} ???"],
            [f"Rechnungsbetrag: {total_costs_formatted} ???"],
        ],
        )

        res_table.setStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0)
        ])

        return res_table

    def _body_create_wire_instructions(self) -> List[reportlab.platypus.Paragraph]:
        """Create the wire instructions for transferring the money to BeginnerLuft"""

        para_list = []

        para_01 = Paragraph(f"""
            Bitte ??berweisen Sie den Rechnungsbetrag innerhalb der n??chsten {self.payment_horizon} Tage, sp??testens bis 
            zum {self.latest_payment_date} auf folgendes Konto:<br/><br/>

            BeginnerLuft gGmbH<br/>
            IBAN: {self.iban}<br/>
            BIC: {self.bic}<br/>
            Verwendungszweck: {self.invoice_nr}
                """)

        para_list.append(para_01)
        return para_list

    def _body_create_greetings(self) -> List[reportlab.platypus.Paragraph]:
        """Create the greetings at the end of the invoice document"""

        para_list = []
        para_01 = Paragraph(f"""
                    Mit freundlichen Gr????en<br/><br/><br/><br/><br/><br/>

                    {self.signer}
                        """)
        para_list.append(para_01)
        return para_list

    def create_footer(self) -> reportlab.platypus.Table:
        """Create a footer for the report"""

        width_list = [
            0.24 * self.col_widths[1],
            0.24 * self.col_widths[1],
            0.24 * self.col_widths[1],
            0.28 * self.col_widths[1],
        ]

        res = Table([
            ["BeginnerLuft gGmbH", "030 / 398 768 02", "Amtsgericht", "Bankinstitut: GLS Bank"],
            ["Bandelstr. 1", "www.beginnerluft.de", "Berlin Charlottenburg", f"IBAN: {self.iban}"],
            ["10559 Berlin", "info@beginnerluft.de", "HR209894 B", f"BIC: {self.bic}"]
        ],
            rowHeights=self.row_heights[2] / 7,  # use more rows to get lines closer together (hack)
            colWidths=width_list
        )

        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 40),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            # ("BACKGROUND", (0, 0), (-1, -1), color),
            ("TEXTCOLOR", (0, 0), (-1, -1), "grey"),
            # ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # horizontal
            # ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])
        return res

    def save_report(self) -> None:
        """Save the current page of the canvas, store the file and close the canvas"""

        self.pdf.showPage()
        self.pdf.save()

    def show_success_message(self) -> None:
        msg = f"Rechnung f??r {self.participant_name} erstellt und gespeichert unter\n\n{self.full_path}"
        helpers.MessageWindow(message_header="Rechnung erstellt!", message=msg)

    @classmethod
    def from_data(cls, participant_title: str, participant_first_name: str, participant_last_name: str,
                  participant_id: str, invoice_name: str, invoice_total_amount: float, invoice_nr: str,
                  invoice_creation_date: datetime.date, invoice_target_date: datetime.date,
                  training_name: str, training_cost_per_lesson: float,
                  coaching_start: datetime.date, coaching_end: datetime.date, coaching_nr_lessons: int,
                  jc_name: str, jc_street: str, jc_street_nr: str, jc_zip: str, jc_city: str,
                  path: str) -> "PDFInvoice":
        """Create instance of class only based on necessary data"""

        jc = Jobcenter(name=jc_name, street=jc_street, street_nr=jc_street_nr, zip_code=jc_zip, city=jc_city)
        participant = Participant(title=participant_title, first_name=participant_first_name,
                                  last_name=participant_last_name, client_id_with_jc=participant_id)
        training = Training(name=training_name, cost_per_training_lesson=training_cost_per_lesson)
        invoice = Invoice(invoice_nr=invoice_nr, total_amount=invoice_total_amount, creation_date=invoice_creation_date,
                          target_date=invoice_target_date, jobcenter=jc, nr_training_lessons=coaching_nr_lessons,
                          participant=participant, training=training)
        return cls(invoice_name=invoice_name, invoice=invoice, time_period_start=coaching_start,
                   time_period_end=coaching_end,
                   nr_of_training_lessons=coaching_nr_lessons, path=path, show_success_message=False)


if __name__ == '__main__':
    # jc = Jobcenter(name="Jobcenter Berlin Mitte", street_and_nr="Seydelstr. 2-5", zip_code="10117", city="Berlin")
    # participant = Participant.test_participant()
    # invoice = Invoice.test_invoice(participant=participant, jobcenter=jc)
    # pdf = PDFInvoice(time_period_start=datetime.date(year=2021, month=8, day=9),
    #                  time_period_end=datetime.date(year=2021, month=10, day=31),
    #                  nr_of_training_lessons=40, invoice=invoice
    #                  )

    pdf2 = PDFInvoice.from_data(
        participant_title="Herr",
        participant_first_name="John",
        participant_last_name="Doe",
        participant_id="12345-ASdf",
        invoice_total_amount=2000,
        invoice_nr="2021-10-asdf",
        invoice_creation_date=datetime.date(2021,11,22),
        invoice_target_date=datetime.date(2021,12, 5),
        training_name="Individuelles Berufscoaching",
        training_cost_per_lesson=20,
        coaching_start=datetime.date(2021,6,12),
        coaching_end=datetime.date(2021, 9, 17),
        coaching_nr_lessons=100,
        jc_name="Testjobcenter",
        jc_street="Berlinerstr.",
        jc_street_nr="123",
        jc_zip="12345",
        jc_city="Berlin"
    )
