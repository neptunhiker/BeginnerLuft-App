import datetime
import os.path
import platform
from tkinter import filedialog

import pandas as pd

import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, Image
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# gui.file_ze_coach = file_coach
# gui.file_ze_beginnerluft = file_bl
# gui.training_name = training_name
# gui.training_nr = training_nr
# gui.participant_name = participant_name
# gui.avgs_nr = avgs_nr
# gui.time_period = ?

class TimeReport():

    def __init__(self, file_coach, file_bl, training_name, training_nr, participant_first_name, participant_last_name,
                 participant_title, participant_jc_id, confirmation_period_start, confirmation_period_end):
        self.file_coach = file_coach
        self.file_bl = file_bl
        self.training_name = training_name
        self.training_nr = training_nr
        self.participant_title = participant_title
        self.participant_first_name = participant_first_name
        self.participant_last_name = participant_last_name
        self.participant_full_name = f"{self.participant_first_name} {self.participant_last_name}"
        self.participant_jc_id = participant_jc_id
        self.confirmation_period_start = confirmation_period_start
        self.confirmation_period_end = confirmation_period_end
        self.time_period = f"{self.confirmation_period_start.strftime('%d.%m.%Y')} bis " \
                           f"{self.confirmation_period_end.strftime('%d.%m.%Y')}"

        self.df_coach = pd.DataFrame()
        self.df_beginnerluft = pd.DataFrame()
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.date_ranges = None
        self.output_matrix = []
        self.month_selection = []
        self.error = False

        self._get_data()

        if not self.error:
            self._filter_df()
            self._determine_date_range()

    def _get_data(self):

        # get times of coachings conducted by coach
        try:
            if platform.system() == "Darwin":  # MAC
                self.df_coach = pd.read_excel(self.file_coach, sheet_name="Zeiterfassung")
            else:
                if int(pd.__version__[2:4]) < 21:
                    self.df_coach = pd.read_excel(self.file_coach, sheetname="Zeiterfassung")
                else:
                    self.df_coach = pd.read_excel(self.file_coach, sheet_name="Zeiterfassung")
            self.df_coach.dropna(how="all", inplace=True)
            self.df_coach = self.df_coach[["Datum", "Von", "Bis", "UE", "Kommentar bei Terminabsage"]]
        except FileNotFoundError as err:
            print(err)
        except Exception as err:
            print(err)
            raise Exception

        # get times of coachings conducted by BeginnerLuft
        try:
            if platform.system() == "Darwin":  # MAC
                self.df_beginnerluft = pd.read_excel(self.file_bl, sheet_name="Zeiterfassung")
            else:
                if int(pd.__version__[2:4]) < 21:
                    self.df_beginnerluft = pd.read_excel(self.file_bl, sheetname="Zeiterfassung")
                else:
                    self.df_beginnerluft = pd.read_excel(self.file_bl, sheet_name="Zeiterfassung")
            self.df_beginnerluft.dropna(how="all", inplace=True)
            self.df_beginnerluft = self.df_beginnerluft[["Datum", "Von", "Bis", "UE", "Kommentar bei Terminabsage"]]
        except FileNotFoundError as err:
            print(err)
        except Exception as err:
            print(err)
            raise Exception

        # rename columns
        for df in [self.df_coach, self.df_beginnerluft]:
            df.rename(columns={"Kommentar bei Terminabsage": "Kommentar"}, inplace=True)

        try:
            # concatenate the two data frames
            self.df = pd.concat([self.df_beginnerluft, self.df_coach], ignore_index=True)

            # sort dataframe by date
            self.df.sort_values(by=["Datum"], inplace=True)

            self.df["UE"] = self.df["UE"].fillna(0)  # fill UE with zero if cell is empty
            self.df = self.df.fillna("")
            self.filtered_df = self.df.copy()

        except Exception as err:
            print(err)
            self.error = True

    def filter_df(self, months):

        # filter dataframe for specific date range and update output matrix
        self._filter_df(month_selection=months)
        self._determine_date_range()
        # self._create_df_matrix()

    def _filter_df(self, month_selection="all"):

        # filter dataframe for specific date range
        # self.df["Datum"] = pd.to_datetime(self.df["Datum"])
        if month_selection != "all":
            self.filtered_df = self.df[self.df["Datum"].dt.month.isin(month_selection)]

    def _determine_date_range(self):

        if not self.filtered_df.empty:
            # locale.setlocale(locale.LC_TIME, locale.normalize("de"))  # does not work
            first_date = datetime.datetime.strftime(min(self.filtered_df["Datum"]), "%m/%Y")
            last_date = datetime.datetime.strftime(max(self.filtered_df["Datum"]), "%m/%Y")
            date_range = [first_date, last_date]
            self.date_ranges = date_range

    def _create_df_matrix(self):
        sum_ues = "{:.0f}".format(self.filtered_df["UE"].sum())
        self.filtered_df.loc[:, 'Datum'] = self.filtered_df['Datum'].apply(lambda x: x.strftime("%d.%m.%y"))
        self.filtered_df.loc[:, 'Von'] = self.filtered_df['Von'].apply(lambda x: x.strftime("%H:%M") if isinstance(x, datetime.datetime) else x)
        self.filtered_df.loc[:, 'Bis'] = self.filtered_df['Bis'].apply(lambda x: x.strftime("%H:%M") if isinstance(x, datetime.datetime) else x)
        self.filtered_df.loc[:, 'UE'] = self.filtered_df['UE'].apply(lambda x: "{:.0f}".format(x))


        matrix = self.filtered_df.values.tolist()
        matrix.insert(0, self.filtered_df.columns)  # header of dataframe
        matrix.append(["", "", "", sum_ues, ""])

        # ensure that matrix always has the same length and is printed from top to bottom (workaround)
        for i in range(28 - len(matrix)):
            matrix.append(["", "", "", "", ""])

        self.output_matrix = matrix

    def create_report(self, path):

        try:
            # filename = f"BeginnerLuft Zeiterfassung {self.gui.participant_name}.pdf"
            # path = os.path.join(output_directory, filename)
            pdf = canvas.Canvas(path, pagesize=A4)
            pdf.setTitle("BeginnerLuft Zeiterfassung")

            width, height = A4  # A$ is a tuple with two values (width, height)
            height_list = [
                0.15 * height,  # header
                0.80 * height,  # body
                0.05 * height  # footer
                ]

            # create output matrix
            self._create_df_matrix()

            main_table = Table([
                [self.gen_header_table(width=width, height=height_list[0])],
                [self.gen_body_table(width=width, height=height_list[1], data=self.output_matrix,
                                     training_name=self.training_name, training_nr=self.training_nr,
                                     participant_name=self.participant_full_name,
                                     participant_jc_id=self.participant_jc_id, time_period=self.time_period,
                                     date_ranges=self.date_ranges)],
                [self.gen_footer_table(width=width, height=height_list[2])]
            ],
                colWidths=width,
                rowHeights=height_list,
            )

            main_table.setStyle([
                # ("GRID", (0,0), (-1, -1), 1, "red"),  # a border
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, -2), (-1, -2), 20),
                ("LINEBELOW", (0,1), (-1,1), 1, "grey"),
            ])


            main_table.wrapOn(pdf, 0, 0)
            main_table.drawOn(pdf, 0, 0)

            pdf.showPage()
            pdf.save()

            return True

        except Exception as err:
            print(err)
            return False

    def gen_header_table(self, width, height):

        width_list = [
            0.1 * width,
            0.55 * width,
            0.45 * width,
        ]

        img_path = "assets/beginnerluft.png"
        img_width = width_list[1] * 0.3
        img_height = height * 0.5
        img = Image(filename=img_path, width=img_width, height=img_height, kind="proportional")

        res = Table([
            ["", img, ""],
        ],
            colWidths=width_list,
            rowHeights=height
        )

        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            # ("LEFTPADDING", (0, 0), (-1, -1), 0),
            # ("BACKGROUND", (0, 0), (-1, -1), color),
            # ("TEXTCOLOR", (0, 0), (-1, -1), "white"),
            ("ALIGN", (0, 0), (1, 1), "LEFT"),  # horizontal
            ("VALIGN", (0, 0), (1, 1), "MIDDLE"),
            ("LEFTPADDING", (-1, 0), (-1, 0), -width_list[1] + 98),  # unit is points
            ("FONTSIZE", (2,0), (2,0), 16),
            ("BOTTOMPADDING", (2, 0), (2, -1), 50),
            # ("LINEBELOW", (0,0), (-1,0), 1, "grey"),
        ])

        return res

    def gen_body_table(self, width, height, data, training_name, training_nr, participant_name, participant_jc_id,
                       time_period, date_ranges):

        participant_name = participant_name
        width_list = [
            0.1 * width,
            0.8 * width,
            0.1 * width,
        ]

        height_list = [
            0.15 * height,
            0.67 * height,
            0.08 * height,
            0.10 * height,
        ]
        res = Table([
            ["", self._gen_meta_data(width=width_list[1], height=height_list[3],
                                     participant_name=participant_name, training_name=training_name, training_nr=training_nr,
                                     participants_jc_id=participant_jc_id, time_period=time_period, date_ranges=date_ranges), ""],
            ["", self._gen_times_table(width=width_list[1], height=height_list[1], data=data), ""],
            ["", self._gen_confirmation_text(training_name=training_name, participant_name=participant_name,
                                        date_ranges=date_ranges), ""],
            ["", self._gen_signature_table(width=width_list[1], height=height_list[3], participant_name=participant_name),
             ""],
        ],
            colWidths=width_list,
            rowHeights=height_list
        )

        color = "#FFFF00"
        left_padding = 0

        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            # ("LINEABOVE", (1, 0), (1, 0), 1, color),
            # ("LINEBELOW", (1, 0), (1,-1), 1, "purple"),
            ("LEFTPADDING", (1, 0), (1, 3), left_padding),
            # ("BACKGROUND", (0, 0), (-1, -1), color),
            # ("TEXTCOLOR", (0, 0), (-1, -1), "white"),
            # ("ALIGN", (0, 0), (1, 1), "CENTER"),  # horizontal
            # ("VALIGN", (0, 0), (1, 1), "MIDDLE"),
            # ("LEFTPADDING", (-1, 0), (-1, 0), -width_list[1] + 35),  # unit is points
            # ("FONTSIZE", (2,0), (2,0), 20),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, -2), (-1, -2), 20),
            ("TOPPADDING", (0, 1), (-1, 1), 200),
        ])

        return res

    def _gen_meta_data(self, width, height, participant_name, training_name, training_nr, participants_jc_id,
                       time_period, date_ranges):

        # month_names = {}
        # month_names[1] = "Januar"
        # month_names[2] = "Februar"
        # month_names[3] = "März"
        # month_names[4] = "April"
        # month_names[5] = "Mai"
        # month_names[6] = "Juni"
        # month_names[7] = "Juli"
        # month_names[8] = "August"
        # month_names[9] = "September"
        # month_names[10] = "Oktober"
        # month_names[11] = "November"
        # month_names[12] = "Dezember"

        header = "Anwesenheitsliste"
        # min_month = date_ranges[0][0:2]
        # min_year = date_ranges[0][-4:]
        # max_month = date_ranges[1][0:2]
        # max_year = date_ranges[1][-4:]
        # min_month_german = month_names[int(min_month)][0:3]
        # max_month_german = month_names[int(max_month)][0:3]
        #
        # if min_year == max_year:
        #     header = f"{header} {min_month_german} bis {max_month_german} {max_year}"
        # else:
        #     header = f"{header} {min_month_german} {min_year} bis {max_month_german} {max_year}"

        # res = Table([
        #     [header],
        #     [f"Maßnahme: {training_name}"],
        #     [f"Maßnahmennummer: {training_nr}"],
        #     [f"Teilnehmer:in {participant_name}"]
        # ])

        width_list = [
            0.5 * width,
            0.4 * width,
            0.1 * width
        ]

        res = Table([
            [header, ""],
            [f"Teilnehmer:in {participant_name}", f"Maßnahme: {training_name}", ""],
            [f"Kundennummer: {participants_jc_id}", f"Maßnahmennummer: {training_nr}", ""],
            [f"Bewilligungszeitraum: {time_period}", "", ""]
        ],
            rowHeights=height / 3,
            colWidths=width_list
        )

        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            ("FONTSIZE", (0, 0), (0, 0), 16),
            ("BOTTOMPADDING", (0, 0), (0, 0), 14)
        ])

        return res

    def _gen_times_table(self, width, height, data):

        width_list = [
            0.15 * width,
            0.15 * width,
            0.15 * width,
            0.15 * width,
            0.4 * width,
        ]

        row_height = height / len(data) * 0.9

        res = Table(
            data,
            colWidths=width_list,
            rowHeights=row_height
        )

        res.setStyle([
            # ("GRID", (0,0), (-1,-1), 1, "red"),
            # ("TEXTCOLOR", (0,0), (-1,0), "red"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
            ("LINEBELOW", (0, 0), (-1, 0), 1, "black"),
            # ("LINEBELOW", (0, -2), (-1, -2), 1, "black"),
            ("ALIGN", (0, 0), (3, -1), "CENTER"),
        ])
        return res

    def _gen_confirmation_text(self, training_name, participant_name, date_ranges):

        # format time period
        if date_ranges[0] == date_ranges[1]:
            time_period = f"{date_ranges[0]}"
        else:
            time_period = f"{date_ranges[0]} bis {date_ranges[1]}"

        para_list = []
        para01_style = ParagraphStyle(name="para01")
        para01_style.spaceAfter = 15
        para01_style.textColor = "green"
        para01 = Paragraph("""
        <b>
        This page tests out a number of attributes of the paraStyle tag. This paragraph is in a
        style we have called "style1". It should be a normal paragraph, set in Courier 12 pt. It
        should be a normal paragraph, set in Courier (not bold).
        </b>
        """, para01_style)

        para02_style = ParagraphStyle(name="para02")
        para02 = Paragraph(f"""
        <i>
        Hiermit bestätige ich, {participant_name}, dass ich im Rahmen der Maßnahme '{training_name}' 
        der <b>BeginnerLuft gGmbH</b> an den oben genannten Terminen teilgenommen habe.
        </i>
        """, para02_style)

        # para_list.append(para01)
        para_list.append(para02)

        return para_list

    def _gen_signature_table(self, width, height, participant_name):

        width_list = [
            0.4 * width,
            0.2 * width,
            0.4 * width
        ]

        # img_path = "resources/Vanguard.png"
        # img_width = width_list[0] * 0.6
        # img_height = height * 0.5
        # img = Image(filename=img_path, width=img_width, height=img_height, kind="proportional")

        res = Table([
            ["_" * 30, "", "_" * 30],
            ["BeginnerLuft", "", participant_name],
        ],
            rowHeights=height / 5,
            colWidths=width_list,
        )

        res.setStyle([
            # ("GRID", (0,0), (-1,-1), 1, "blue"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ])

        return res

    def gen_footer_table(self, width, height):
        text = "BeginnerLuft gGmbH - Bandelstr. 1 - 10559 Berlin - www.beginnerluft.de"

        width_list = [
            0.1 * width,
            0.8 * width,
            0.1 * width,
        ]

        res = Table([
            ["", text, ""]
        ],
            rowHeights=height,
            colWidths=width_list
        )

        color = "#FFFF00"
        # color = colors.darkgrey
        res.setStyle([
            # ("GRID", (0, 0), (-1, -1), 1, "red"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            # ("BACKGROUND", (0, 0), (-1, -1), color),
            ("TEXTCOLOR", (0, 0), (-1, -1), "black"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # horizontal
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])
        return res


if __name__ == '__main__':
    pass
