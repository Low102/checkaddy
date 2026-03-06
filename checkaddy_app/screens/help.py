from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class HelpScreen(ModalScreen[None]):
    def compose(self) -> ComposeResult:
        with Container(id="help-dialog"):
            yield Static("Keyboard shortcuts", id="help-title")
            yield Static(
                "Enter runs validation and lookup\n"
                "Tab / Shift+Tab moves focus through controls\n"
                "Ctrl+L clears the form\n"
                "Ctrl+J toggles the JSON panel\n"
                "Ctrl+O opens explorer for current result\n"
                "Ctrl+G opens repository actions\n"
                "Ctrl+1/2/3 focuses network/address/lookup\n"
                "Alt+B / Alt+T selects previous / next network\n"
                "Ctrl+Left / Ctrl+Right also cycles network\n"
                "Ctrl+P opens command palette\n"
                "F1 opens help\n"
                "Q or Ctrl+C exits\n\n"
                "Only public addresses are supported. Never paste private keys or seed phrases.",
                id="help-body",
            )
            yield Button("Close", id="help-close", variant="primary")

    def on_mount(self) -> None:
        self.query_one("#help-close", Button).focus()

    @on(Button.Pressed, "#help-close")
    def handle_close(self) -> None:
        self.dismiss(None)
