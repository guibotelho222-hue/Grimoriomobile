import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
import flet as ft
import common_ui
import oracle


class OracleTab:
    """
    Oráculo tab – the main divination interface.

    Flow:  moon-influence banner  →  draw button  →  card reveal  →  save / reset.
    """

    def __init__(self, page: ft.Page, on_reading_saved=None):
        self.page = page
        self.on_reading_saved = on_reading_saved
        self.current_reading = None
        self._build_controls()

    # ── control factory ─────────────────────────────────────────

    def _build_controls(self):
        # Moon influence banner
        moon_info = oracle.get_moon_influence()
        self.moon_banner = common_ui.styled_card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(moon_info["phase"]["emoji"], size=20),
                            ft.Text(
                                f'Lua {moon_info["phase"]["name"]}',
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=common_ui.COLORS["gold"],
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Text(
                        moon_info["influence"]["energia"],
                        size=12,
                        color=common_ui.COLORS["purple_light"],
                        italic=True,
                    ),
                    ft.Text(
                        moon_info["influence"]["conselho"],
                        size=11,
                        color=common_ui.COLORS["text_secondary"],
                    ),
                ],
                spacing=4,
            ),
            border_color=common_ui.COLORS["purple_deep"],
        )

        # Central draw button
        self.draw_btn = ft.Container(
            content=ft.Column(
                [
                    ft.Text("✨", size=40, text_align=ft.TextAlign.CENTER),
                    ft.Text(
                        "Consultar o Oráculo",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=common_ui.COLORS["gold"],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Toque para receber a mensagem dos guias",
                        size=11,
                        color=common_ui.COLORS["text_secondary"],
                        text_align=ft.TextAlign.CENTER,
                        italic=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            bgcolor=common_ui.COLORS["bg_card"],
            border=ft.border.all(2, common_ui.COLORS["gold_dim"]),
            border_radius=16,
            padding=ft.padding.symmetric(vertical=30, horizontal=20),
            ink=True,
            on_click=self._on_draw,
            alignment=ft.alignment.center,
        )

        # Card result area (initially hidden)
        self.card_area = ft.Container(visible=False)

        # Action buttons (initially hidden)
        self.action_row = ft.Row(
            [
                ft.ElevatedButton(
                    "Nova Consulta",
                    icon=ft.icons.REFRESH,
                    on_click=self._on_reset,
                    bgcolor=common_ui.COLORS["bg_card"],
                    color=common_ui.COLORS["text_primary"],
                ),
                ft.ElevatedButton(
                    "Salvar no Cofre",
                    icon=ft.icons.SAVE,
                    on_click=self._on_save,
                    bgcolor=common_ui.COLORS["gold_dim"],
                    color=common_ui.COLORS["bg_primary"],
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            visible=False,
        )

    # ── draw card ───────────────────────────────────────────────

    def _on_draw(self, e):
        self.current_reading = oracle.build_full_reading()
        card = self.current_reading["card"]
        elem = oracle.ELEMENTOS.get(card["elemento"], {})

        # Build the revealed card view
        keyword_chips = [
            ft.Container(
                content=ft.Text(
                    kw,
                    size=10,
                    color=common_ui.COLORS["purple_light"],
                ),
                bgcolor=common_ui.COLORS["bg_secondary"],
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                border=ft.border.all(1, common_ui.COLORS["purple_deep"]),
            )
            for kw in card["palavras"]
        ]

        self.card_area.content = ft.Column(
            [
                # Entity & card title header
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                card["emoji_entidade"],
                                size=36,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                card["entidade"],
                                size=12,
                                color=common_ui.COLORS["text_secondary"],
                                text_align=ft.TextAlign.CENTER,
                                italic=True,
                            ),
                            ft.Text(
                                card["nome"],
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=common_ui.COLORS["gold"],
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f'{elem.get("emoji", "")} {card["elemento"]}',
                                    size=11,
                                    color=elem.get(
                                        "cor", common_ui.COLORS["text_secondary"]
                                    ),
                                ),
                                bgcolor=common_ui.COLORS["bg_primary"],
                                border_radius=10,
                                padding=ft.padding.symmetric(
                                    horizontal=10, vertical=3
                                ),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=ft.padding.symmetric(vertical=16),
                    alignment=ft.alignment.center,
                ),
                common_ui.gold_divider(),
                # Message
                ft.Container(
                    content=ft.Column(
                        [
                            common_ui.section_title(
                                "Mensagem", ft.icons.AUTO_AWESOME
                            ),
                            ft.Text(
                                card["mensagem"],
                                size=14,
                                color=common_ui.COLORS["text_primary"],
                                italic=True,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(vertical=8),
                ),
                common_ui.gold_divider(),
                # Advice
                ft.Container(
                    content=ft.Column(
                        [
                            common_ui.section_title(
                                "Conselho",
                                ft.icons.LIGHTBULB_OUTLINE,
                                common_ui.COLORS["emerald"],
                            ),
                            ft.Text(
                                card["conselho"],
                                size=13,
                                color=common_ui.COLORS["text_primary"],
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(vertical=8),
                ),
                # Keywords
                ft.Row(keyword_chips, wrap=True, spacing=6, run_spacing=6),
            ],
            spacing=4,
        )

        self.card_area.bgcolor = common_ui.COLORS["bg_card"]
        self.card_area.border_radius = 16
        self.card_area.border = ft.border.all(1, common_ui.COLORS["gold_dim"])
        self.card_area.padding = 16
        self.card_area.visible = True

        self.draw_btn.visible = False
        self.action_row.visible = True
        self.page.update()

    # ── save reading ────────────────────────────────────────────

    def _on_save(self, e):
        if self.current_reading is None:
            return

        try:
            raw = self.page.client_storage.get("grimorio_readings")
            readings = json.loads(raw) if raw else []
        except Exception:
            readings = []

        save_data = {
            "card_id":         self.current_reading["card"]["id"],
            "card_nome":       self.current_reading["card"]["nome"],
            "entidade":        self.current_reading["card"]["entidade"],
            "emoji_entidade":  self.current_reading["card"]["emoji_entidade"],
            "elemento":        self.current_reading["card"]["elemento"],
            "mensagem":        self.current_reading["card"]["mensagem"],
            "conselho":        self.current_reading["card"]["conselho"],
            "palavras":        self.current_reading["card"]["palavras"],
            "moon_phase":      self.current_reading["moon"]["phase"]["name"],
            "moon_emoji":      self.current_reading["moon"]["phase"]["emoji"],
            "illumination":    self.current_reading["illumination"],
            "timestamp":       self.current_reading["timestamp"],
        }
        readings.insert(0, save_data)
        readings = readings[:50]  # cap history

        try:
            self.page.client_storage.set(
                "grimorio_readings", json.dumps(readings, ensure_ascii=False)
            )
        except Exception:
            pass

        # Visual feedback
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(
                "✨ Leitura salva no Cofre!",
                color=common_ui.COLORS["gold"],
            ),
            bgcolor=common_ui.COLORS["bg_card"],
        )
        self.page.snack_bar.open = True

        if self.on_reading_saved:
            self.on_reading_saved()

        self.page.update()

    # ── reset ───────────────────────────────────────────────────

    def _on_reset(self, e):
        self.current_reading = None
        self.card_area.visible = False
        self.action_row.visible = False
        self.draw_btn.visible = True
        self.page.update()

    # ── public build ────────────────────────────────────────────

    def build(self) -> ft.Container:
        """Return the complete tab content control."""
        return ft.Container(
            content=ft.ListView(
                controls=[
                    self.moon_banner,
                    ft.Container(height=12),
                    self.draw_btn,
                    ft.Container(height=12),
                    self.card_area,
                    ft.Container(height=8),
                    self.action_row,
                    ft.Container(height=20),
                ],
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                spacing=0,
            ),
            expand=True,
        )
