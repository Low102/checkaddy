from __future__ import annotations

from textual.widgets import Static


class MetricCard(Static):
    def __init__(self, title: str, value: str = "-", element_id: str = "") -> None:
        super().__init__(id=element_id, classes="metric-card")
        self.title = title
        self.value = value

    def on_mount(self) -> None:
        self.set_value(self.value)

    def set_value(self, value: str) -> None:
        self.value = value
        self.update("[dim]" + self.title + "[/]" + chr(10) + "[b]" + value + "[/]")
