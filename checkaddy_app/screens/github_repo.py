from __future__ import annotations

from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class GithubRepositoryScreen(ModalScreen[Optional[str]]):
    def __init__(self, repository_url: str) -> None:
        super().__init__()
        self.repository_url = repository_url

    def compose(self) -> ComposeResult:
        with Container(id="github-dialog"):
            yield Static("Open Github repository", id="github-title")
            yield Static("Choose what to do with the repository URL:", id="github-body")
            yield Static(self.repository_url, id="github-url")
            with Horizontal(id="github-buttons"):
                yield Button("Open in browser", id="github-open", variant="primary")
                yield Button("Copy to clipboard", id="github-copy")
                yield Button("Cancel", id="github-cancel")

    def on_mount(self) -> None:
        self.query_one("#github-open", Button).focus()

    @on(Button.Pressed, "#github-open")
    def handle_open(self) -> None:
        self.dismiss("open")

    @on(Button.Pressed, "#github-copy")
    def handle_copy(self) -> None:
        self.dismiss("copy")

    @on(Button.Pressed, "#github-cancel")
    def handle_cancel(self) -> None:
        self.dismiss(None)
