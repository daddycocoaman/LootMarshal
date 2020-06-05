import typer
import json
from click_help_colors import HelpColorsCommand, HelpColorsGroup
from requests import Response


class CustomHelpColorsGroup(HelpColorsGroup):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = "blue"
        self.help_options_color = "yellow"


class CustomHelpColorsCommand(HelpColorsCommand):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = "blue"
        self.help_options_color = "yellow"

def print_cli_response(resp: Response, value: str = None, status: bool = False) -> None:
    if 200 <= resp.status_code < 300:
        mark = "[✓] " if status else ""
        msg = resp.json()['msg']
        if status:
            typer.secho(f"{mark}{msg}", fg="green")
        else:
            output = msg.get(value, msg)
            typer.secho(f"{mark}{output}", fg="green")
    else:
        typer.secho(f"[✗] {resp.json()['detail']}", fg="red")
