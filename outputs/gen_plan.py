import json
import math
import base64
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

OUTPUT_DIR = Path('outputs')
WIDTH = 5.8
LENGTH = 47.0
GRID_STEP = 5.0

COLOR_MAP = {
    'F': '#2c7bb6',
    'M': '#fdae61',
    'E': '#d7191c',
}
LINE_WIDTHS = {
    'F': 1.4,
    'M': 2.0,
    'E': 2.8,
}

TRANSVERSE_PATTERN = (0, (1.4, 2.2))
UNCERTAIN_PATTERN = (0, (2.4, 2.4))


def load_data():
    fissures = json.loads(OUTPUT_DIR.joinpath('fissures.json').read_text(encoding='utf-8'))['fissures']
    zones = json.loads(OUTPUT_DIR.joinpath('zones.json').read_text(encoding='utf-8'))['zones']
    return fissures, zones


def draw_plan(fissures, zones):
    fig, ax = plt.subplots(figsize=(6.3, 13.5))
    ax.set_xlim(-0.6, WIDTH + 1.8)
    ax.set_ylim(-2.0, LENGTH + 11)
    ax.set_aspect('equal')
    ax.axis('off')

    # Roadway rectangle
    road = Rectangle((0, 0), WIDTH, LENGTH, facecolor='#f5f5f5', edgecolor='black', linewidth=1.4)
    ax.add_patch(road)

    # Grid lines
    for y in [y for y in [i * GRID_STEP for i in range(int(math.ceil(LENGTH / GRID_STEP)) + 1)] if y <= LENGTH]:
        ax.plot([0, WIDTH], [y, y], color='#d9d9d9', linewidth=0.5)
        ax.text(WIDTH + 0.2, y, f"{y:.0f} m", va='center', ha='left', fontsize=7, color='#555555')
    ax.plot([WIDTH / 2, WIDTH / 2], [0, LENGTH], color='#808080', linewidth=0.8, linestyle=(0, (2.96, 1.28)))

    # Zones (simplified rectangles)
    for zone in zones:
        start = zone['chainage_debut_m']
        end = zone['chainage_fin_m']
        length = end - start
        largeur = zone['largeur_m']
        cote = zone['cote']
        if cote == 'gauche':
            x0 = 0
        elif cote == 'droite':
            x0 = max(WIDTH - largeur, 0)
        else:  # centre
            x0 = (WIDTH - largeur) / 2
        rect = Rectangle((x0, start), largeur, length, linewidth=1.4,
                         edgecolor='#333333', facecolor='none')
        if zone['type_zone'] == 'craquelage':
            rect.set_hatch('///')
            rect.set_edgecolor('#555555')
        elif zone['type_zone'] == 'affaissement':
            rect.set_facecolor('#e6e6e6')
            rect.set_edgecolor('#d7191c')
            rect.set_linestyle((0, (2.4, 2.4)))
        else:
            rect.set_facecolor('#999999')
            rect.set_edgecolor('#000000')
        ax.add_patch(rect)
        label = f"{zone['id']} {zone['type_zone'].upper()}"
        if zone.get('severite'):
            label += f" {zone['severite']}"
        if zone['incertitude']:
            label += ' (?)'
        ax.text(x0 + largeur / 2, start + length / 2, label,
                ha='center', va='center', fontsize=7, color='#333333', rotation=90)

    # Fissures
    for fissure in fissures:
        severity = fissure['severite']
        color = COLOR_MAP.get(severity, '#000000')
        linewidth = LINE_WIDTHS.get(severity, 1.2)
        incertitude = fissure['incertitude']
        linestyle = UNCERTAIN_PATTERN if incertitude else 'solid'
        label = f"{fissure['id']} {severity}"
        if incertitude:
            label += ' (?)'
        if fissure['type'] == 'longitudinale':
            x = fissure['offset_m']
            y0 = fissure['chainage']['de']
            y1 = fissure['chainage']['a']
            ax.plot([x, x], [y0, y1], color=color, linewidth=linewidth, linestyle=linestyle)
            ax.text(x + 0.12, (y0 + y1) / 2, label, ha='left', va='center', fontsize=7, color=color, rotation=90)
        else:
            y = fissure['chainage']['de']
            dash_pattern = TRANSVERSE_PATTERN
            if incertitude:
                dash_pattern = UNCERTAIN_PATTERN
            ax.plot([0, WIDTH], [y, y], color=color, linewidth=linewidth,
                    linestyle=dash_pattern)
            ax.text(WIDTH + 0.25, y, label, ha='left', va='center', fontsize=7, color=color)

    # Legend
    legend_elements = [
        Line2D([0], [0], color=COLOR_MAP['F'], linewidth=LINE_WIDTHS['F'], label='F (faible)'),
        Line2D([0], [0], color=COLOR_MAP['M'], linewidth=LINE_WIDTHS['M'], label='M (moyenne)'),
        Line2D([0], [0], color=COLOR_MAP['E'], linewidth=LINE_WIDTHS['E'], label='E (majeure)'),
        Line2D([0], [0], color='black', linewidth=1.4, linestyle=TRANSVERSE_PATTERN, label='Fissure transversale (pointillé)'),
        Line2D([0], [0], color='black', linewidth=1.4, linestyle=UNCERTAIN_PATTERN, label='Incertitude'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.35, 1.0), frameon=False, fontsize=7)

    # Cartouche / title
    ax.text(0, LENGTH + 4.5, '10e Rue E – Tronçon Rue Hope à CP Éloiz', fontsize=11, fontweight='bold')
    ax.text(0, LENGTH + 3.4, 'Plan des fissures (chaînage 0 m à 47 m) – échelle 1:200', fontsize=8)
    ax.text(0, LENGTH + 2.4, 'Nord vers le haut | Grille tous les 5 m | Auteur : Équipe IA', fontsize=7)

    # North arrow
    ax.annotate('N', xy=(WIDTH + 1.0, LENGTH - 6.0), xytext=(WIDTH + 1.0, LENGTH - 1.5),
                arrowprops=dict(arrowstyle='-|>', linewidth=1.2), ha='center', fontsize=9)

    # Scale bar (10 m)
    scale_length = 10
    ax.plot([0.3, 0.3 + scale_length / (LENGTH / WIDTH)], [-1.4, -1.4], color='black', linewidth=2.0)
    ax.text(0.3 + scale_length / (LENGTH / WIDTH) / 2, -1.9, '10 m', ha='center', va='top', fontsize=7)

    fig.tight_layout()
    return fig, ax


def export_figures(fig):
    svg_path = OUTPUT_DIR / '10e_rue_plan.svg'
    png_path = OUTPUT_DIR / '10e_rue_plan.png'
    fig.savefig(svg_path, format='svg')
    fig.savefig(png_path, format='png', dpi=300)

    with png_path.open('rb') as f:
        encoded = base64.b64encode(f.read()).decode('ascii')
    (OUTPUT_DIR / '10e_rue_plan.png.b64').write_text(encoded, encoding='utf-8')


if __name__ == '__main__':
    fissures_data, zones_data = load_data()
    fig_obj, _ = draw_plan(fissures_data, zones_data)
    export_figures(fig_obj)