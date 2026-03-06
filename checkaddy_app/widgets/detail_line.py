from __future__ import annotations

from textual.widgets import Static


class DetailLine(Static):
    def __init__(self, label: str, value: str = "-", element_id: str = "") -> None:
        super().__init__(id=element_id, classes="detail-row")
        self.label = label
        self.value = value

    def on_mount(self) -> None:
        self.set_value(self.value)

    def set_value(self, value: str) -> None:
        self.value = value
        self.update(f"[dim]{self.label}:[/] {value}")
