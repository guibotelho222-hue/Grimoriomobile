import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import flet as ft
import common_ui
from oraculo_tab import OracleTab
from tab_cofre import CofreTab


def main(page: ft.Page):
    """Grimório v2.0 – entry point."""

    # ── Page configuration ─────────────────────────────────────
    page.title = "Grimório v2.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = common_ui.COLORS["bg_primary"]
    page.padding = 0
    page.scroll = None

    page.theme = ft.Theme(
        color_scheme_seed="#7B2D8E",
    )

    # ── Header ─────────────────────────────────────────────────
    header = common_ui.build_header(page)

    # ── Tab controllers ────────────────────────────────────────
    cofre_tab = CofreTab(page)
    oracle_tab = OracleTab(page, on_reading_saved=cofre_tab.refresh)

    def on_tab_change(e):
        """Refresh vault contents when the user switches to the Cofre tab."""
        if e.control.selected_index == 1:
            cofre_tab.refresh()
            page.update()

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        on_change=on_tab_change,
        label_color=common_ui.COLORS["gold"],
        unselected_label_color=common_ui.COLORS["text_muted"],
        indicator_color=common_ui.COLORS["gold"],
        divider_color=common_ui.COLORS["divider"],
        tabs=[
            ft.Tab(
                text="Oráculo",
                icon=ft.icons.AUTO_AWESOME,
                content=oracle_tab.build(),
            ),
            ft.Tab(
                text="Cofre",
                icon=ft.icons.LOCK_OUTLINED,
                content=cofre_tab.build(),
            ),
        ],
        expand=True,
    )

    # ── Assemble ───────────────────────────────────────────────
    page.add(header, tabs)


ft.app(target=main)
