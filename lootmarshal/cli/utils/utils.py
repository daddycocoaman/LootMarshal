import json
import re
from pprint import pformat
from typing import List

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


def print_cli_response(
    resp: Response, value: str = None, status: bool = False, format: str = None
) -> None:
    if 200 <= resp.status_code < 300:
        mark = "[✓] " if status else ""
        msg = resp.json()["msg"]
        if status:
            typer.secho(f"{mark}{msg}\n", fg="green")
        else:
            output = msg.get(value, msg) if value else msg

            if format == "pretty":
                output = pformat(output, indent=4)
            elif format == "list":
                output = "\n\n".join([item for item in output])
            elif format == "json":
                output = json.dumps(output, indent=4)
            typer.secho(f"{mark}{output}\n", fg="green")
    else:
        typer.secho(f"[✗] {resp.json()['detail']}\n", fg="red")


def print_bad(msg: str) -> None:
    typer.secho(f"[✗] {msg}\n", fg="red")


def verify_tags(tags: List):
    tag_dict = {}
    try:
        for tag in tags:
            key, value = tag.split(",")
            if re.match(r"^\w+$", key) and re.match(r"^\w+$", value):
                tag_dict[key] = value
            else:
                raise typer.BadParameter(f"{key},{value}")
        return tag_dict
    except Exception as e:
        raise typer.BadParameter(e)
