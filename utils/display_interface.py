from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import DOUBLE
from rich.json import JSON
from rich import print_json
from story.evidence import StoryElement, TypeOfEvidence
from story.story_elements import get_elements

console = Console(width=100)
_recording = []
_is_recording = False

def start_recording():
    global _recording, _is_recording
    _recording = []
    _is_recording = True

def end_recording():
    global _is_recording
    _is_recording = False

def get_recording():
    return "\n\n".join(_recording)

def _record(content: str, title: str = None):
    if _is_recording:
        if "\n#" in content:
            content = content.replace("\n#", "\n####")
        if title:
            _recording.append(f"### {title}\n\n{content}")
        else:
            _recording.append(f"### Note\n\n{content}")

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
    _record(text, f"Story Element: {title if title else 'Untitled'}")

def display_story_elements(elements: list[StoryElement], title: str = "Story Elements", style: str = "cyan") -> None:
    """
    Display a list of StoryElements.
    """
    content = "\n".join([f"• [{element.when.name}]\t {element.text} ({element.type_of_evidence.value} of {element.target})" for element in elements])
    panel = Panel(
        Text(content),
        border_style=style,
        box=DOUBLE,
        expand=False,
        title=title,
        title_align="center"
    )
    console.print(panel)
    _record(content.replace("•", "*"), f"Story Elements: {title}")

def display_text(text: str, speaker: str = None, style: str = "green") -> None:
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
    _record(text, f"{speaker if speaker else 'Text'}")

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
    _record(content.plain.replace("•", "*"), f"Bullet Points: {title}")

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
    _record(error_message, "Error")

def display_json(json_data: str, title: str = "JSON Data", style: str = "blue") -> None:
    """
    Display JSON data in a pretty format using Rich's built-in JSON formatting.
    """
    try:
        print_json(json_data)
        _record(json_data, f"JSON Data: {title}")
    except Exception as e:
        error_message = f"Failed to display JSON data: {str(e)}"
        display_error(error_message)
        _record(error_message, "Error")
