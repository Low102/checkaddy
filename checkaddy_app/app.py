from __future__ import annotations

import json
from typing import Iterable, Optional

from textual import on, work
from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.containers import Container, Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Button, Footer, Header, Input, Label, RadioButton, RadioSet, Static

from .api import ApiClient
from .constants import BTC, COIN_FROM_RADIO_ID, COIN_OPTIONS, COIN_RADIO_IDS, REPOSITORY_URL
from .css import APP_CSS
from .formatters import format_amount_display, format_validation_badge
from .lookup import build_lookup_result
from .models import LookupResult
from .screens import GithubRepositoryScreen, HelpScreen
from .validators import validate_address
from .widgets import DetailLine, MetricCard


class CheckAddyApp(App):
    CSS = APP_CSS
    TITLE = "checkaddy"
    SUB_TITLE = "Public multi-chain address validation"

    BINDINGS = [
        Binding("enter", "lookup", "Lookup"),
        Binding("ctrl+l", "clear_form", "Clear"),
        Binding("ctrl+j", "toggle_json", "JSON"),
        Binding("ctrl+o", "open_explorer", "Explorer"),
        Binding("ctrl+g", "open_github_repository", "Repo"),
        Binding("ctrl+1", "focus_coin_set", show=False),
        Binding("ctrl+2", "focus_address", show=False),
        Binding("ctrl+3", "focus_lookup_button", show=False),
        Binding("alt+b", "select_previous_coin", show=False),
        Binding("alt+t", "select_next_coin", show=False),
        Binding("ctrl+left", "select_previous_coin", show=False),
        Binding("ctrl+right", "select_next_coin", show=False),
        Binding("f1", "show_help", "Help"),
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    show_json = reactive(False)
    live_validation_timer: Optional[Timer] = None

    def __init__(self) -> None:
        super().__init__()
        self.client = ApiClient()
        self.last_result: Optional[LookupResult] = None
        self.selected_coin: str = COIN_OPTIONS[0][0]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="app"):
            yield from self._compose_hero()
            with Horizontal(id="layout"):
                yield from self._compose_sidebar()
                yield from self._compose_main()
        yield Footer()

    def _compose_hero(self) -> ComposeResult:
        with Container(id="hero"):
            yield Static("checkaddy", id="hero-title")
            yield Static(
                "Local address validation with live explorer data for UTXO and EVM public addresses.",
                id="hero-subtitle",
            )
            yield Static("Copyright (c) 2026 zv", id="hero-credit")

    def _compose_sidebar(self) -> ComposeResult:
        with VerticalScroll(id="sidebar"):
            with Container(classes="panel"):
                yield Static("Input", classes="panel-title")
                yield Label("Network")
                with RadioSet(id="coin-set"):
                    for index, (coin, label) in enumerate(COIN_OPTIONS):
                        yield RadioButton(label, id=COIN_RADIO_IDS[coin], value=index == 0)
                yield Label("Address", classes="subtle")
                yield Input(placeholder="Paste public wallet address", id="address")
                yield Static("Waiting for input", id="quick-validation")

            with Container(classes="panel", id="controls"):
                yield Static("Actions", classes="panel-title")
                yield Button("Validate and fetch", id="lookup", variant="primary")
                yield Button("Clear", id="clear")
                yield Button("Toggle JSON", id="toggle-json")

            with Container(classes="panel"):
                yield Static("Notes", classes="panel-title")
                yield Static(
                    "Supported: BTC, LTC, DOGE, DASH, BCH, ETH, BSC, Polygon.\n"
                    "EVM chains use 0x addresses; UTXO chains use Base58/Bech32/CashAddr.\n"
                    "Some fields can be unavailable depending on free endpoint limitations.",
                    classes="subtle",
                )

    def _compose_main(self) -> ComposeResult:
        with VerticalScroll(id="main"):
            with Container(classes="panel"):
                yield Static("Status", classes="panel-title")
                yield Static("Ready", id="status-body", classes="info")

            with Container(classes="panel"):
                yield Static("Overview", classes="panel-title")
                with Container(id="metrics"):
                    yield MetricCard("Confirmed balance", "-", "metric-confirmed")
                    yield MetricCard("Unconfirmed balance", "-", "metric-unconfirmed")
                    yield MetricCard("Total received", "-", "metric-received")
                    yield MetricCard("Total sent", "-", "metric-sent")
                    yield MetricCard("Transaction count", "-", "metric-tx-count")
                    yield MetricCard("Data source", "-", "metric-source")

            with Container(classes="panel"):
                yield Static("Details", classes="panel-title")
                with Container(id="details-grid"):
                    yield DetailLine("Coin", "-", "detail-coin")
                    yield DetailLine("Address", "-", "detail-address")
                    yield DetailLine("Validation", "-", "detail-validation")
                    yield DetailLine("Explorer", "-", "detail-explorer")
                    yield DetailLine("Fetched at UTC", "-", "detail-fetched")

            with Container(classes="panel hidden", id="json-panel"):
                yield Static("Normalized JSON", classes="panel-title")
                yield Static("{}", id="json-box", expand=True)

    def on_mount(self) -> None:
        self.query_one("#address", Input).focus()

    def on_unmount(self) -> None:
        self.client.close()

    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())

    def action_focus_coin_set(self) -> None:
        self.query_one("#coin-set", RadioSet).focus()

    def action_focus_address(self) -> None:
        self.query_one("#address", Input).focus()

    def action_focus_lookup_button(self) -> None:
        self.query_one("#lookup", Button).focus()

    def select_coin(self, coin: str, *, announce: bool = False) -> None:
        self.selected_coin = coin
        for coin_code, radio_id in COIN_RADIO_IDS.items():
            self.query_one(f"#{radio_id}", RadioButton).value = coin_code == coin
        self.refresh_live_validation()
        if announce:
            self.set_status(f"Selected {coin}", "info")

    def cycle_coin(self, step: int) -> None:
        ordered_coins = [coin for coin, _ in COIN_OPTIONS]
        current = self.current_coin()
        try:
            current_index = ordered_coins.index(current)
        except ValueError:
            current_index = 0
        next_coin = ordered_coins[(current_index + step) % len(ordered_coins)]
        self.select_coin(next_coin, announce=True)

    def action_select_previous_coin(self) -> None:
        self.cycle_coin(-1)

    def action_select_next_coin(self) -> None:
        self.cycle_coin(1)

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        yield SystemCommand(
            "Open Github repository",
            "Open or copy the project's GitHub URL",
            self.open_github_repository_options,
        )

    def action_open_github_repository(self) -> None:
        self.open_github_repository_options()

    def open_github_repository_options(self) -> None:
        self.push_screen(GithubRepositoryScreen(REPOSITORY_URL), self.handle_github_repository_choice)

    def handle_github_repository_choice(self, choice: Optional[str]) -> None:
        if choice == "open":
            self.open_url(REPOSITORY_URL)
            self.set_status("Opened repository in browser", "info")
        elif choice == "copy":
            self.copy_to_clipboard(REPOSITORY_URL)
            self.set_status("Repository URL copied to clipboard", "ok")

    def action_open_explorer(self) -> None:
        if self.last_result is None:
            self.set_status("No lookup result yet", "warn")
            return
        self.open_url(self.last_result.explorer_url)
        self.set_status("Opened address explorer", "info")

    def action_toggle_json(self) -> None:
        panel = self.query_one("#json-panel", Container)
        self.show_json = not self.show_json
        if self.show_json:
            panel.remove_class("hidden")
        else:
            panel.add_class("hidden")

    def action_clear_form(self) -> None:
        self.query_one("#address", Input).value = ""
        self.select_coin(BTC)
        self.query_one("#quick-validation", Static).update("Waiting for input")
        self.set_status("Ready", "info")
        self.reset_results()
        self.query_one("#address", Input).focus()

    def action_lookup(self) -> None:
        self.start_lookup()

    @on(Button.Pressed, "#lookup")
    def handle_lookup_button(self) -> None:
        self.start_lookup()

    @on(Button.Pressed, "#clear")
    def handle_clear_button(self) -> None:
        self.action_clear_form()

    @on(Button.Pressed, "#toggle-json")
    def handle_toggle_json_button(self) -> None:
        self.action_toggle_json()

    @on(Input.Changed, "#address")
    def handle_address_change(self) -> None:
        if self.live_validation_timer is not None:
            self.live_validation_timer.stop()
        self.live_validation_timer = self.set_timer(0.2, self.refresh_live_validation)

    @on(RadioSet.Changed, "#coin-set")
    def handle_coin_change(self) -> None:
        pressed_button = self.query_one("#coin-set", RadioSet).pressed_button
        if pressed_button is not None and pressed_button.id is not None:
            self.selected_coin = COIN_FROM_RADIO_ID.get(pressed_button.id, self.selected_coin)
        self.refresh_live_validation()

    def current_coin(self) -> str:
        return self.selected_coin

    def set_status(self, message: str, tone: str) -> None:
        widget = self.query_one("#status-body", Static)
        widget.update(message)
        widget.set_classes(tone)

    def refresh_live_validation(self) -> None:
        address = self.query_one("#address", Input).value.strip()
        coin = self.current_coin()
        widget = self.query_one("#quick-validation", Static)
        if not address:
            widget.update("Waiting for input")
            return
        valid, reason = validate_address(coin, address)
        prefix = "Format valid" if valid else "Format invalid"
        widget.update(f"{prefix}: {reason}")

    def reset_results(self) -> None:
        self.last_result = None
        self.metric("#metric-confirmed", "-")
        self.metric("#metric-unconfirmed", "-")
        self.metric("#metric-received", "-")
        self.metric("#metric-sent", "-")
        self.metric("#metric-tx-count", "-")
        self.metric("#metric-source", "-")
        self.detail("#detail-coin", "-")
        self.detail("#detail-address", "-")
        self.detail("#detail-validation", "-")
        self.detail("#detail-explorer", "-")
        self.detail("#detail-fetched", "-")
        self.query_one("#json-box", Static).update("{}")

    def metric(self, selector: str, value: str) -> None:
        self.query_one(selector, MetricCard).set_value(value)

    def detail(self, selector: str, value: str) -> None:
        self.query_one(selector, DetailLine).set_value(value)

    def start_lookup(self) -> None:
        address = self.query_one("#address", Input).value.strip()
        coin = self.current_coin()
        if not address:
            self.set_status("Address is required", "error")
            self.query_one("#address", Input).focus()
            return
        self.set_status(f"Looking up {coin} address", "warn")
        self.run_lookup(coin, address)

    @work(thread=True)
    def run_lookup(self, coin: str, address: str) -> None:
        result = build_lookup_result(self.client, coin, address)
        self.call_from_thread(self.apply_result, result)

    def apply_result(self, result: LookupResult) -> None:
        self.last_result = result
        self.metric("#metric-confirmed", format_amount_display(result.coin, result.confirmed_balance))
        self.metric("#metric-unconfirmed", format_amount_display(result.coin, result.unconfirmed_balance))
        self.metric("#metric-received", format_amount_display(result.coin, result.total_received))
        self.metric("#metric-sent", format_amount_display(result.coin, result.total_sent))
        tx_display = str(result.tx_count) if result.tx_count is not None else "Not available via free endpoint"
        self.metric("#metric-tx-count", tx_display)
        self.metric("#metric-source", result.data_source)

        self.detail("#detail-coin", result.coin)
        self.detail("#detail-address", result.address)
        self.detail(
            "#detail-validation",
            format_validation_badge(result.is_valid_format, result.validation_reason),
        )
        self.detail("#detail-explorer", result.explorer_url)
        self.detail("#detail-fetched", result.fetched_at_utc)
        self.query_one("#json-box", Static).update(json.dumps(result.as_dict(), indent=2, ensure_ascii=False))
        self.query_one("#json-panel", Container).refresh(layout=True)

        if result.api_error:
            self.set_status(f"Format valid, API request failed: {result.api_error}", "warn")
        elif result.api_skipped:
            self.set_status("Format invalid, remote lookup skipped", "error")
        else:
            self.set_status("Lookup completed", "ok")
