import typer
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

def print_cli_response(resp: Response) -> None:
    if 200 <= resp.status_code < 300:
        typer.secho(f"[✓] {resp.json()['msg']}", fg="green")
    else:
        typer.secho(f"[✗] {resp.json()['detail']}", fg="red")
