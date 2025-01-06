from project import thread, spinner, exit
from rich.console import Console
console = Console()

def test_spinner():
    assert spinner("Loading...", 2) == "Done"
    assert spinner("Analyzing...", 10) =="Done"

def test_exit():
    assert exit() == console.print("Thank you very much for using [blue]SkySentiment[/blue]!🛫 Have a great day :>")

def test_thread():
    assert thread() == "Done"
