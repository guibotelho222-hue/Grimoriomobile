import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import datetime
import math
import flet as ft


# ══════════════════════════════════════════════════════════════════════
#  THEME PALETTE – Grimório v2.0 · Rei Joaquim & Princesa Guerreira
# ══════════════════════════════════════════════════════════════════════

COLORS = {
    # Backgrounds
    "bg_deep":         "#0B0118",
    "bg_primary":      "#0D0221",
    "bg_secondary":    "#1A0A2E",
    "bg_card":         "#241540",
    "bg_card_hover":   "#2E1D50",
    # Golds
    "gold":            "#FFD700",
    "gold_dim":        "#B8860B",
    "gold_pale":       "#F0E68C",
    # Purples
    "purple_deep":     "#4A0E6F",
    "purple":          "#7B2D8E",
    "purple_light":    "#9B59B6",
    # Accents
    "crimson":         "#DC143C",
    "crimson_dark":    "#8B0000",
    "emerald":         "#2ECC71",
    "teal":            "#1ABC9C",
    # Text
    "cream":           "#FFF8DC",
    "white":           "#FFFFFF",
    "text_primary":    "#F5E6D3",
    "text_secondary":  "#A89070",
    "text_muted":      "#6B5B4F",
    # Structural
    "divider":         "#3D2B5E",
    "shadow":          "#000000",
}


# ══════════════════════════════════════════════════════════════════════
#  LOCALE HELPERS  (Portuguese – independent of system locale)
# ══════════════════════════════════════════════════════════════════════

MESES_PT = {
    1: "Janeiro",   2: "Fevereiro",  3: "Março",      4: "Abril",
    5: "Maio",      6: "Junho",      7: "Julho",      8: "Agosto",
    9: "Setembro",  10: "Outubro",   11: "Novembro",  12: "Dezembro",
}

DIAS_SEMANA_PT = {
    0: "Segunda-feira",  1: "Terça-feira",   2: "Quarta-feira",
    3: "Quinta-feira",   4: "Sexta-feira",   5: "Sábado",
    6: "Domingo",
}


def format_date_pt(dt=None):
    """Return a fully spelled-out date string in Brazilian Portuguese."""
    if dt is None:
        dt = datetime.date.today()
    dia_semana = DIAS_SEMANA_PT[dt.weekday()]
    return f"{dia_semana}, {dt.day} de {MESES_PT[dt.month]} de {dt.year}"


# ══════════════════════════════════════════════════════════════════════
#  DYNAMIC MOON PHASE ENGINE
#
#  Uses the mean synodic month (~29.53 days) starting from a known
#  astronomical New Moon (2000-01-06 18:14 UTC).  Accuracy ≈ ±1 day,
#  which is appropriate for a spiritual / oracle application.
# ══════════════════════════════════════════════════════════════════════

MOON_PHASES = [
    {"name": "Nova",              "emoji": "🌑"},
    {"name": "Crescente",         "emoji": "🌒"},
    {"name": "Quarto Crescente",  "emoji": "🌓"},
    {"name": "Gibosa Crescente",  "emoji": "🌔"},
    {"name": "Cheia",             "emoji": "🌕"},
    {"name": "Gibosa Minguante",  "emoji": "🌖"},
    {"name": "Quarto Minguante",  "emoji": "🌗"},
    {"name": "Minguante",         "emoji": "🌘"},
]

_REF_NEW_MOON = datetime.datetime(2000, 1, 6, 18, 14, 0)
SYNODIC_PERIOD = 29.53058867          # mean synodic month (days)
_PHASE_SEGMENT = SYNODIC_PERIOD / 8.0  # width of each phase slice


def get_moon_age(dt=None):
    """Days elapsed since the most recent New Moon (0 … ~29.53)."""
    if dt is None:
        dt = datetime.datetime.now()
    elif isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
        dt = datetime.datetime.combine(dt, datetime.time(12, 0, 0))
    diff_seconds = (dt - _REF_NEW_MOON).total_seconds()
    return (diff_seconds / 86400.0) % SYNODIC_PERIOD


def get_moon_phase(dt=None):
    """
    Return a dict describing today's moon phase:
        name   – Portuguese phase name
        emoji  – corresponding moon emoji
        index  – 0..7
        age    – moon age in days (float)
    """
    age = get_moon_age(dt)
    idx = int(age / _PHASE_SEGMENT) % 8
    phase = dict(MOON_PHASES[idx])
    phase["index"] = idx
    phase["age"] = round(age, 2)
    return phase


def get_moon_illumination(dt=None):
    """Approximate visible illumination percentage (0-100)."""
    age = get_moon_age(dt)
    illum = (1.0 - math.cos(2.0 * math.pi * age / SYNODIC_PERIOD)) / 2.0
    return round(illum * 100, 1)


# ══════════════════════════════════════════════════════════════════════
#  HEADER COMPONENT  –  dynamic moon-phase badge
# ══════════════════════════════════════════════════════════════════════

def build_header(page: ft.Page) -> ft.Container:
    """Build the app header bar with the live moon-phase badge."""
    phase = get_moon_phase()
    illum  = get_moon_illumination()

    moon_badge = ft.Container(
        content=ft.Row(
            [
                ft.Text(phase["emoji"], size=22),
                ft.Column(
                    [
                        ft.Text(
                            phase["name"],
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["gold"],
                        ),
                        ft.Text(
                            f"{illum}% iluminada",
                            size=9,
                            color=COLORS["text_secondary"],
                        ),
                    ],
                    spacing=0,
                ),
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=COLORS["bg_card"],
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border=ft.border.all(1, COLORS["gold_dim"]),
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "📖 Grimório v2.0",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLORS["gold"],
                                ),
                                ft.Text(
                                    "Rei Joaquim & Princesa Guerreira",
                                    size=12,
                                    italic=True,
                                    color=COLORS["text_secondary"],
                                ),
                            ],
                            spacing=2,
                        ),
                        moon_badge,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(
                    format_date_pt(),
                    size=10,
                    color=COLORS["text_muted"],
                    text_align=ft.TextAlign.RIGHT,
                ),
                ft.Divider(height=1, color=COLORS["divider"]),
            ],
            spacing=6,
        ),
        padding=ft.padding.only(left=16, right=16, top=12, bottom=4),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[COLORS["bg_secondary"], COLORS["bg_primary"]],
        ),
    )
    return header


# ══════════════════════════════════════════════════════════════════════
#  SHARED WIDGET HELPERS
# ══════════════════════════════════════════════════════════════════════

def styled_card(content, on_click=None, border_color=None):
    """Themed card container with optional tap handler."""
    return ft.Container(
        content=content,
        bgcolor=COLORS["bg_card"],
        border_radius=12,
        padding=16,
        border=ft.border.all(1, border_color or COLORS["divider"]),
        ink=True,
        on_click=on_click,
    )


def section_title(text, icon=None, color=None):
    """Section heading row with optional icon."""
    controls = []
    if icon:
        controls.append(ft.Icon(icon, color=color or COLORS["gold"], size=18))
    controls.append(
        ft.Text(
            text,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=color or COLORS["gold"],
        )
    )
    return ft.Row(controls, spacing=8)


def body_text(text, size=13, color=None):
    """Standard body text with theme defaults."""
    return ft.Text(text, size=size, color=color or COLORS["text_primary"])


def gold_divider():
    """Thin gold-tinted divider line."""
    return ft.Divider(height=1, color=COLORS["gold_dim"], thickness=0.5)
