from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import DOUBLE
from rich.json import JSON
from rich import print_json

console = Console(width=100)

def display_story_element(text: str, title: str = None, style: str = "cyan") -> None:
    """
    Display a story element with an optional title.
    """
    content = Text(text.strip())
    panel = Panel(
        content,
        border_style=style,
        box=DOUBLE,
        expand=False,
        title=title,
        title_align="center"
    )
    console.print(panel)

def display_narrative(text: str, speaker: str = None, style: str = "green") -> None:
    """
    Display narrative text with an optional speaker.
    """
    content = Text(text.strip())
    panel = Panel(
        content,
        border_style=style,
        expand=False,
        title=speaker,
        title_align="left" if speaker else "right"
    )
    console.print(panel)

def display_bullet_points(points: list[str], title: str = "Bullet Points", style: str = "yellow") -> None:
    """
    Display a list of bullet points.
    """
    content = Text("\n".join(f"• {point}" for point in points))
    panel = Panel(
        content,
        border_style=style,
        box=DOUBLE,
        expand=False,
        title=title,
        title_align="center"
    )
    console.print(panel)

def display_error(error_message: str) -> None:
    """
    Display an error message.
    """
    panel = Panel(
        Text(error_message),
        border_style="red",
        title="Error",
        title_align="center",
        expand=False
    )
    console.print(panel)

def display_json(json_data: str, title: str = "JSON Data", style: str = "blue") -> None:
    """
    Display JSON data in a pretty format using Rich's built-in JSON formatting.
    """
    try:
        print_json(json_data)
    except Exception as e:
        display_error(f"Failed to display JSON data: {str(e)}")
    # json_content = JSON(json_data)
    # panel = Panel(
    #     json_content,
    #     border_style=style,
    #     box=DOUBLE,
    #     expand=False,
    #     title=title,
    #     title_align="center"
    # )
    # console.print(panel)
