import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
import datetime
import flet as ft
import common_ui
import oracle


class CofreTab:
    """
    Cofre (Vault) tab – persisted history of saved oracle readings.

    Data is stored via ``page.client_storage`` (Android SharedPreferences)
    under the key ``grimorio_readings`` as a JSON array of dicts.
    """

    STORAGE_KEY = "grimorio_readings"

    def __init__(self, page: ft.Page):
        self.page = page
        self.list_view = ft.ListView(
            spacing=8,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
        )
        self._empty_state = self._build_empty_state()
        self.refresh()

    # ── empty-state placeholder ─────────────────────────────────

    @staticmethod
    def _build_empty_state():
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("🔮", size=48, text_align=ft.TextAlign.CENTER),
                    ft.Text(
                        "O Cofre está vazio",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=common_ui.COLORS["text_secondary"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Consulte o Oráculo e salve suas leituras aqui.",
                        size=13,
                        color=common_ui.COLORS["text_muted"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.padding.symmetric(vertical=60, horizontal=20),
            alignment=ft.alignment.center,
        )

    # ── storage helpers ─────────────────────────────────────────

    def _load_readings(self):
        try:
            raw = self.page.client_storage.get(self.STORAGE_KEY)
            return json.loads(raw) if raw else []
        except Exception:
            return []

    def _save_readings(self, readings):
        try:
            self.page.client_storage.set(
                self.STORAGE_KEY, json.dumps(readings, ensure_ascii=False)
            )
        except Exception:
            pass

    def _delete_reading(self, index):
        readings = self._load_readings()
        if 0 <= index < len(readings):
            readings.pop(index)
            self._save_readings(readings)
        self.refresh()
        self.page.update()

    # ── confirmation dialog ─────────────────────────────────────

    def _confirm_delete(self, index):
        def do_delete(e):
            dlg.open = False
            self.page.update()
            self._delete_reading(index)

        def cancel(e):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(
                "Excluir leitura?",
                color=common_ui.COLORS["crimson"],
            ),
            content=ft.Text(
                "Esta ação não pode ser desfeita.",
                color=common_ui.COLORS["text_primary"],
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel),
                ft.TextButton(
                    "Excluir",
                    on_click=do_delete,
                    style=ft.ButtonStyle(
                        color=common_ui.COLORS["crimson"],
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=common_ui.COLORS["bg_card"],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    # ── detail dialog ───────────────────────────────────────────

    def _show_detail(self, reading):
        elem = oracle.ELEMENTOS.get(reading.get("elemento", ""), {})

        try:
            dt = datetime.datetime.fromisoformat(reading["timestamp"])
            date_str = common_ui.format_date_pt(dt.date())
            time_str = dt.strftime("%H:%M")
        except Exception:
            date_str = "Data desconhecida"
            time_str = ""

        def close_dlg(e):
            dlg.open = False
            self.page.update()

        keyword_chips = [
            ft.Container(
                content=ft.Text(
                    kw, size=9, color=common_ui.COLORS["purple_light"]
                ),
                bgcolor=common_ui.COLORS["bg_secondary"],
                border_radius=10,
                padding=ft.padding.symmetric(horizontal=8, vertical=3),
            )
            for kw in reading.get("palavras", [])
        ]

        dlg = ft.AlertDialog(
            title=ft.Column(
                [
                    ft.Text(
                        reading.get("emoji_entidade", "📖"),
                        size=30,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        reading.get("card_nome", "Carta"),
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=common_ui.COLORS["gold"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        (
                            f'{reading.get("entidade", "")} · '
                            f'{elem.get("emoji", "")} {reading.get("elemento", "")}'
                        ),
                        size=11,
                        color=common_ui.COLORS["text_secondary"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"🗓️ {date_str} às {time_str}",
                            size=10,
                            color=common_ui.COLORS["text_muted"],
                        ),
                        ft.Text(
                            (
                                f'{reading.get("moon_emoji", "")} '
                                f'Lua {reading.get("moon_phase", "")} '
                                f'({reading.get("illumination", 0)}%)'
                            ),
                            size=10,
                            color=common_ui.COLORS["purple_light"],
                        ),
                        common_ui.gold_divider(),
                        common_ui.section_title("Mensagem", ft.icons.AUTO_AWESOME),
                        ft.Text(
                            reading.get("mensagem", ""),
                            size=13,
                            color=common_ui.COLORS["text_primary"],
                            italic=True,
                        ),
                        common_ui.gold_divider(),
                        common_ui.section_title(
                            "Conselho",
                            ft.icons.LIGHTBULB_OUTLINE,
                            common_ui.COLORS["emerald"],
                        ),
                        ft.Text(
                            reading.get("conselho", ""),
                            size=12,
                            color=common_ui.COLORS["text_primary"],
                        ),
                        ft.Row(keyword_chips, wrap=True, spacing=4, run_spacing=4),
                    ],
                    spacing=6,
                    scroll="auto",
                ),
                width=320,
                height=400,
            ),
            actions=[ft.TextButton("Fechar", on_click=close_dlg)],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=common_ui.COLORS["bg_card"],
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    # ── list-item builder ───────────────────────────────────────

    def _build_reading_item(self, reading, index):
        elem = oracle.ELEMENTOS.get(reading.get("elemento", ""), {})

        try:
            dt = datetime.datetime.fromisoformat(reading["timestamp"])
            date_str = f"{dt.day:02d}/{dt.month:02d}/{dt.year}  {dt.strftime('%H:%M')}"
        except Exception:
            date_str = "—"

        def on_tap(e, r=reading):
            self._show_detail(r)

        def on_delete(e, idx=index):
            self._confirm_delete(idx)

        return common_ui.styled_card(
            ft.Row(
                [
                    # Entity icon column
                    ft.Column(
                        [
                            ft.Text(
                                reading.get("emoji_entidade", "📖"), size=28
                            ),
                            ft.Text(elem.get("emoji", ""), size=14),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    # Text info
                    ft.Column(
                        [
                            ft.Text(
                                reading.get("card_nome", "Carta"),
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=common_ui.COLORS["gold"],
                            ),
                            ft.Text(
                                reading.get("entidade", ""),
                                size=11,
                                color=common_ui.COLORS["text_secondary"],
                                italic=True,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        f"🗓️ {date_str}",
                                        size=9,
                                        color=common_ui.COLORS["text_muted"],
                                    ),
                                    ft.Text(
                                        (
                                            f'{reading.get("moon_emoji", "")} '
                                            f'{reading.get("moon_phase", "")}'
                                        ),
                                        size=9,
                                        color=common_ui.COLORS["purple_light"],
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        expand=True,
                        spacing=2,
                    ),
                    # Delete button
                    ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_color=common_ui.COLORS["crimson"],
                        icon_size=20,
                        tooltip="Excluir",
                        on_click=on_delete,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            on_click=on_tap,
        )

    # ── refresh ─────────────────────────────────────────────────

    def refresh(self):
        """Reload readings from storage and rebuild the visible list."""
        readings = self._load_readings()
        self.list_view.controls.clear()

        if not readings:
            self.list_view.controls.append(self._empty_state)
        else:
            self.list_view.controls.append(
                ft.Container(
                    content=common_ui.section_title(
                        f"Leituras Salvas ({len(readings)})",
                        ft.icons.LOCK_OUTLINED,
                    ),
                    padding=ft.padding.only(bottom=4),
                )
            )
            for i, reading in enumerate(readings):
                self.list_view.controls.append(
                    self._build_reading_item(reading, i)
                )
            self.list_view.controls.append(ft.Container(height=20))

    # ── public build ────────────────────────────────────────────

    def build(self) -> ft.Container:
        """Return the complete tab content control."""
        return ft.Container(content=self.list_view, expand=True)
