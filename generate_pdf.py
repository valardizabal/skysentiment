from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(100)
        self.cell(90, 10, "Sentiment Analysis Report", align="C")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


"""
After sentiment analysis, creates a pdf based on the airlines' sentiment analysis.

:param n: list of dictionaries of airlines
:type n: list
"""


def create_pdf(airline_dict):
    pdf = PDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Times", size=11)

    # Start of PDF
    for i in range(len(airline_dict)):
        airline = airline_dict[i]
        ratings = airline["ratings"]
        sentiments = airline["sentiment_scores"]

        pdf.cell(0, 10, f"{i+1})", new_x="LMARGIN", new_y="NEXT")
        pdf.image(f"img/{airline["filename"]}.png", 20, 25, 46)

        pdf.cell(0, 30, f"Airline: {airline["airline"]}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5, f"Country: {airline["country"]}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(
            0,
            10,
            f"Star Rating from SkyTrax: {airline["star"]} STARS",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.cell(0, 10, f"Services Ratings: ", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(10)
        for key in ratings.keys():
            pdf.cell(
                0,
                5,
                f"{key.replace('_', " ").title()}: {ratings[key]}/5",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.cell(10)

        pdf.cell(-10)
        pdf.cell(0, 10, f"Sentiment Scores: ", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(10)
        for key in sentiments.keys():
            pdf.cell(
                0,
                5,
                f"{key}: {sentiments[key]} reviews",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.cell(10)

        pdf.cell(-10)
        pdf.set_font("Times", size=14, style="B")
        pdf.cell(
            0,
            20,
            f"Overall Rating: {airline["overall_rating"]}",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        pdf.set_font("Times", size=11)

        pdf.image(f"charts/{airline["filename"]}-pie.png", 90, 60, 80)
        pdf.image(f"charts/{airline["filename"]}-bar.png", 180, 60, 100)

        # Adds page based on the length of the list of airlines
        if (i + 1) < len(airline_dict):
            pdf.add_page()

    # Change name of pdf file depending on the list
    if len(airline_dict) == 10:
        pdf.output("pdfs/sentiment-analysis.pdf")
    elif len(airline_dict) < 10 and len(airline_dict) != 1:
        pdf.output(f"pdfs/{airline["country"]}-sentiment-analysis.pdf")
    else:
        pdf.output(f"pdfs/{airline["airline"]}-sentiment-analysis.pdf")
