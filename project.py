from airline_reviews_analysis import sea_airlines, airline_files, data_analysis
from generate_pdf import create_pdf
from pyfiglet import Figlet
import time
from beaupy import confirm, select
from beaupy.spinners import *
from rich.console import Console
import threading

figlet = Figlet()
font_list = figlet.getFonts()
figlet.setFont(font="banner")
console = Console()

"""
Main Method

Calls thread method for sentiment analysis and then the menu method for the choices.
"""


def main():

    print(figlet.renderText("SkySentiment"))
    console.print(
        "Welcome to [blue]SkySentiment[/blue]: SEA Airline Review Insights!🛫\nGet insights on customer satisfaction (based on SkyTrax) with the top 10 SEA airlines through sentiment analysis and visual reports."
    )
    if confirm("Continue with sentiment analysis?"):
        thread()
        menu()

    else:
        exit()


"""
Users can select from which: all, by specific country or airline to generate pdf files of its sentiment analysis.

:param n: list of dictionaries of airlines
:type n: list
"""


def get_report(a_list):
    console.print(f"Choose from the following:")
    choices = [
        "1. All SEA airlines",
        "2. by specific country",
        "3. by specific airline",
    ]

    choice = select(choices, cursor="🢧", cursor_style="cyan")
    console.print(f"You chose: {choice}")

    if choice == "2. by specific country":
        console.print("Choose a country: ")
        countries = [
            "Indonesia",
            "Malaysia",
            "Philippines",
            "Singapore",
            "Thailand",
            "Vietnam",
        ]
        country = select(countries, cursor="🢧", cursor_style="cyan")

        new_list = list(filter(lambda s: s["country"] == country, a_list))
        sorted_list = sorted(new_list, key=lambda s: s["overall_rating"], reverse=True)
        create_pdf(sorted_list)

    elif choice == "3. by specific airline":
        console.print("Choose an airline: ")
        airlines = [
            "AirAsia",
            "Singapore Airlines",
            "Lion Air",
            "VietJet Air",
            "Vietnam Airlines",
            "Cebu Pacific",
            "Garuda Indonesia",
            "Philippine Airlines",
            "Malaysia Airlines",
            "Thai Airways",
        ]
        airline = select(airlines, cursor="🢧", cursor_style="cyan")

        new_list = list(filter(lambda s: s["airline"] == airline, a_list))
        create_pdf(new_list)
    else:
        sorted_list = sorted(a_list, key=lambda s: s["overall_rating"], reverse=True)
        create_pdf(sorted_list)

    spinner("Generating PDF file...", 2)
    console.print(
        "[green]Generated PDF File! ✅[/green] Please view pdf in 'pdfs' folder."
    )
    menu()


"""
Users can view the top 3 highest rated airlines in SEA.

:param n: list of dictionaries of airlines
:type n: list
"""


def view_highest(a_list):
    console.print(
        "[green bold underline]Top 3 Highest Rated Airlines in SEA:[/green bold underline]\n"
    )
    sorted_list = sorted(a_list, key=lambda s: s["overall_rating"], reverse=True)
    for i, airline in enumerate(sorted_list[:3]):
        stars = ""
        for _ in range(airline["star"]):
            stars += "⭐"

        ratings = airline["ratings"]
        sentiments = airline["sentiment_scores"]

        console.print(
            f"{i+1}. [cyan bold underline]{airline["airline"]}[/cyan bold underline]\nCountry: {airline["country"]}\nSkyTrax Rating: {stars}"
        )
        console.print(f"[underline]Services Ratings[/underline]")
        for key in ratings.keys():
            console.print(f"{key}: {ratings[key]}/5")
        console.print(f"[underline]Sentiment Ratings[/underline]")
        for key in sentiments.keys():
            console.print(f"{key}: {sentiments[key]} reviews")
        console.print(
            f"[green bold]OVERALL AIRLINE RATING: {airline["overall_rating"]}[/green bold]\n"
        )
    menu()


"""
Users can view the 3 lowest rated airlines in SEA.

:param n: list of dictionaries of airlines
:type n: list
"""


def view_lowest(a_list):
    console.print(
        "[red bold underline]3 Lowest Rated Airlines in SEA:[/red bold underline]\n"
    )
    sorted_list = sorted(a_list, key=lambda s: s["overall_rating"])
    for i, airline in enumerate(sorted_list[:3]):
        stars = ""
        for _ in range(airline["star"]):
            stars += "⭐"

        ratings = airline["ratings"]
        sentiments = airline["sentiment_scores"]

        console.print(
            f"{i+1}. [cyan bold underline]{airline["airline"]}[/cyan bold underline]\nCountry: {airline["country"]}\nSkyTrax Rating: {stars}"
        )
        console.print(f"[underline]Services Ratings[/underline]")
        for key in ratings.keys():
            console.print(f"{key}: {ratings[key]}/5")
        console.print(f"[underline]Sentiment Ratings[/underline]")
        for key in sentiments.keys():
            console.print(f"{key}: {sentiments[key]} reviews")
        console.print(
            f"[red bold]OVERALL AIRLINE RATING: {airline["overall_rating"]}[/red bold]\n"
        )
    menu()


"""
Users can view the highest rated airlines by a specific country in SEA.

:param n: list of dictionaries of airlines
:type n: list
"""


def view_per_country(a_list):
    console.print("Choose a country: ")
    countries = [
        "Indonesia",
        "Malaysia",
        "Philippines",
        "Singapore",
        "Thailand",
        "Vietnam",
    ]
    country = select(countries, cursor="🢧", cursor_style="cyan")
    new_list = list(filter(lambda s: s["country"] == country, a_list))
    sorted_list = sorted(new_list, key=lambda s: s["overall_rating"], reverse=True)

    console.print(f"[cyan bold underline]Top Airlines:[/cyan bold underline]\n")
    for i, airline in enumerate(sorted_list):
        stars = ""
        for _ in range(airline["star"]):
            stars += "⭐"
        ratings = airline["ratings"]
        sentiments = airline["sentiment_scores"]
        console.print(
            f"{i+1}. [cyan bold underline]{airline["airline"]}[/cyan bold underline]\nCountry: {airline["country"]}\nSkyTrax Rating: {stars}"
        )
        console.print(f"[underline]Services Ratings[/underline]")
        for key in ratings.keys():
            console.print(f"{key}: {ratings[key]}/5")
        console.print(f"[underline]Sentiment Ratings[/underline]")
        for key in sentiments.keys():
            console.print(f"{key}: {sentiments[key]} reviews")
        console.print(
            f"[green bold]OVERALL AIRLINE RATING: {airline["overall_rating"]}[/green bold]\n"
        )
    menu()


"""
Thank you message when exiting the program.
"""


def exit():
    return console.print(
        "Thank you very much for using [blue]SkySentiment[/blue]!🛫 Have a great day :>"
    )


"""
Choices after doing sentiment analysis.
"""


def menu():
    choices = [
        "1. Get Sentiment Analysis Report in .pdf format",
        "2. View the Top 3 Highest Rated SEA Airlines",
        "3. View the 3 Lowest Rated SEA Airlines",
        "4. View the Best Airline/s Per Country",
        "5. [red]Exit[/red]",
    ]

    console.print("What do you want to do next?")
    # Choose one item from a list
    choice = select(choices, cursor="🢧", cursor_style="cyan")
    console.print(f"You chose: {choice}")
    match choice:
        case "1. Get Sentiment Analysis Report in .pdf format":
            get_report(sea_airlines)
        case "2. View the Top 3 Highest Rated SEA Airlines":
            view_highest(sea_airlines)
        case "3. View the 3 Lowest Rated SEA Airlines":
            view_lowest(sea_airlines)
        case "4. View the Best Airline/s Per Country":
            view_per_country(sea_airlines)
        case "5. [red]Exit[/red]":
            exit()


"""
Spinner animation for processing data.

:param n: text to put in the animation as well as the seconds it will animate
:type n: str, int
:return: Done
:rtype: str
"""


def spinner(text, seconds):
    spinner = Spinner(DOTS, text)
    spinner.start()

    time.sleep(seconds)

    spinner.stop()
    return "Done"


"""
Using threads to run the animation and the data analysis method simultaneously.

:return: Done
:rtype: str
"""


def thread():
    # Spinner for Sentiment Analysis
    t1 = threading.Thread(
        target=spinner,
        args=(
            "Analyzing...",
            76,
        ),
    )
    t1.start()
    data_analysis(airline_files)
    t1.join()
    console.print("[green]Sentiment Analysis Done! ✅[/green]")
    return "Done"


if __name__ == "__main__":
    main()
