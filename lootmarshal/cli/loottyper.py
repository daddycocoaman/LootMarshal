import typer

from .utils import CustomHelpColorsCommand, CustomHelpColorsGroup


class LootMarshalTyper(typer.Typer):
    def __init__(
        self,
        *args,
        cls=CustomHelpColorsGroup,
        context_settings=dict(help_option_names=["-h"]),
        **kwargs
    ) -> None:
        super().__init__(
            *args,
            cls=cls,
            context_settings=context_settings,
            add_completion=False,
            **kwargs
        )

    def command(
        self,
        *args,
        cls=CustomHelpColorsCommand,
        context_settings=dict(help_option_names=["-h"]),
        **kwargs
    ) -> typer.Typer.command:
        return super().command(
            *args, cls=cls, context_settings=context_settings, **kwargs
        )
