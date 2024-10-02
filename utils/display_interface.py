from typing import Optional

from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.box import DOUBLE

console = Console()


def show_narrative_text(text: str | Text, speaker: str = "", color: str = "green") -> None:
    """
    Display a block of narrative text in the console.
    """
    content = text if isinstance(text, Text) else Text(text.strip())
    if speaker:
        panel = Panel(content, border_style=color, expand=False, title=speaker, title_align="left")
    else:
        panel = Panel(content, border_style=color, expand=False)
    console.print(panel)


def get_user_text(prompt: str) -> str:
    """
    Get text input from the user.
    """
    return console.input(f"> {prompt}")


def show_rule_text(text: str, rule: str = "") -> None:
    """
    Display a block of text with a rule name in the console.
    """
    content = Text(text.strip())
    title = "Game Rules" if rule else None
    panel = Panel(content, border_style="yellow", box=DOUBLE, expand=False, title=title, title_align="center")
    console.print(panel)


def show_error(error_message: str, e: Optional[Exception] = None) -> None:
    """
    Display an error message in the console.
    """
    panel = Panel(Text(error_message), border_style="red", title="Error", title_align="center", expand=False)
    console.print(panel)

    if e:
        console.print(f"[red]Exception: {e}[/red]")


_previous_situation = ""


def show_situation(situation_text: str, title: str = None, only_new: bool = False) -> None:
    """
    Display the current situation details in the console.
    If only_new is True, only show lines that have changed since the last call.
    """
    global _previous_situation

    original_situation_text = situation_text

    if only_new:
        new_lines = []
        previous_lines = _previous_situation.split('\n')
        current_lines = situation_text.strip().split('\n')

        for line in current_lines:
            if line not in previous_lines:
                new_lines.append(line)

        if not new_lines:
            return  # Nothing new to display

        situation_text = '\n'.join(new_lines)

    panel = Panel(
        Text(situation_text.strip()),
        border_style="cyan",
        box=DOUBLE,
        expand=False,
        title="Current Situation",
        title_align="right"
    )
    console.print(panel)

    _previous_situation = original_situation_text.strip()
