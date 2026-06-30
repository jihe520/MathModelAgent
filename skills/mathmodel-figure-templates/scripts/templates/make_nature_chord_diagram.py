from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch, Wedge


@dataclass(frozen=True)
class NodeSpec:
    label: str
    color: str
    weight: float


NODES = [
    NodeSpec("Zn β-ribbon", "#edeaf5", 1.05),
    NodeSpec("KH", "#c6c0dc", 1.05),
    NodeSpec("SHS", "#8176b0", 1.2),
    NodeSpec("TPR", "#6b248b", 1.0),
    NodeSpec("GT-B", "#6a4209", 2.0),
    NodeSpec("GT-A", "#9d5c08", 1.45),
    NodeSpec("ATP-grasp", "#d3ba73", 1.3),
    NodeSpec("AB\nhydrolase", "#ead99f", 2.7),
    NodeSpec("TIM\nbarrel", "#efe7cf", 5.2),
    NodeSpec("Hybrid", "#f4f5f4", 2.7),
    NodeSpec("Acetyltrans", "#bce7df", 1.2),
    NodeSpec("ATPase", "#7dd2c4", 0.7),
    NodeSpec("Actin", "#4fb9ac", 0.82),
    NodeSpec("NADP", "#2a948c", 0.82),
    NodeSpec("Rossmann", "#006d64", 1.0),
    NodeSpec("P-loop\nNTPase", "#007160", 4.4),
    NodeSpec("AAA lid", "#063f38", 1.1),
    NodeSpec("E-set", "#7f1d8d", 0.8),
    NodeSpec("Calycin", "#a65dad", 0.8),
    NodeSpec("Ubiquitin", "#b58ac0", 0.8),
    NodeSpec("RNase H", "#d6c5df", 0.8),
    NodeSpec("PDDEXK", "#eadcf0", 1.0),
    NodeSpec("Cupin", "#f2f2f2", 2.4),
    NodeSpec("Phage barrel", "#e5f0dd", 1.4),
    NodeSpec("Dim A-B barrel", "#a4cf95", 1.8),
    NodeSpec("RING", "#49a65a", 1.5),
    NodeSpec("Peptidase CA", "#18823a", 0.9),
    NodeSpec("Peptidase MA", "#006f38", 1.0),
    NodeSpec("β-Propeller", "#a85a02", 2.0),
    NodeSpec("HTH", "#ca7005", 2.1),
    NodeSpec("Thioredoxin", "#f19926", 1.0),
    NodeSpec("GHD", "#f6c56a", 1.0),
    NodeSpec("OB", "#f2d8a2", 1.2),
    NodeSpec("Pkinase", "#f8edd8", 1.0),
]


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif", "serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 11,
            "axes.linewidth": 0.8,
        }
    )


def polar_to_xy(theta_deg: float, radius: float) -> np.ndarray:
    theta = np.deg2rad(theta_deg)
    return np.array([radius * np.cos(theta), radius * np.sin(theta)])


def lighten(color: str, amount: float = 0.35) -> tuple[float, float, float]:
    rgb = np.array(mpl.colors.to_rgb(color))
    return tuple(rgb + (1.0 - rgb) * amount)


def text_rotation(theta_deg: float) -> tuple[float, str]:
    angle = theta_deg % 360
    if 90 < angle < 270:
        return theta_deg + 90, "right"
    return theta_deg - 90, "left"


def compute_layout(
    nodes: list[NodeSpec],
    start_angle: float = 124.0,
    gap: float = 0.92,
) -> dict[str, dict[str, float]]:
    total_gap = gap * len(nodes)
    total_weight = sum(node.weight for node in nodes)
    current = start_angle
    layout: dict[str, dict[str, float]] = {}
    for node in nodes:
        arc = (360.0 - total_gap) * node.weight / total_weight
        start = current
        end = current - arc
        layout[node.label] = {
            "start": start,
            "end": end,
            "mid": (start + end) / 2.0,
            "arc": arc,
        }
        current = end - gap
    return layout


def build_flows(nodes: list[NodeSpec]) -> list[tuple[str, str, float]]:
    # A deterministic, data-like connectivity pattern: a few strong domain
    # families plus many faint background links, as in dense Circos summaries.
    rng = np.random.default_rng(20260629)
    labels = [node.label for node in nodes]
    flows: list[tuple[str, str, float]] = [
        ("TIM\nbarrel", "Hybrid", 13.5),
        ("TIM\nbarrel", "AB\nhydrolase", 9.0),
        ("P-loop\nNTPase", "HTH", 11.0),
        ("P-loop\nNTPase", "GT-B", 8.7),
        ("P-loop\nNTPase", "Acetyltrans", 7.8),
        ("β-Propeller", "HTH", 8.2),
        ("β-Propeller", "Pkinase", 5.4),
        ("RING", "Peptidase CA", 5.8),
        ("RING", "Peptidase MA", 5.0),
        ("GT-B", "GT-A", 5.0),
        ("GT-B", "ATP-grasp", 4.6),
        ("AAA lid", "KH", 4.2),
        ("AAA lid", "SHS", 3.8),
        ("Cupin", "PDDEXK", 3.7),
        ("Cupin", "β-Propeller", 4.0),
        ("OB", "Zn β-ribbon", 3.2),
        ("Thioredoxin", "GHD", 3.1),
        ("AB\nhydrolase", "Rossmann", 4.6),
        ("Actin", "ATPase", 3.4),
        ("NADP", "Rossmann", 3.2),
        ("Dim A-B barrel", "Phage barrel", 3.9),
        ("Dim A-B barrel", "RING", 3.0),
        ("RNase H", "PDDEXK", 3.3),
        ("E-set", "Calycin", 3.2),
        ("Ubiquitin", "P-loop\nNTPase", 3.8),
    ]

    high_weight_labels = np.array([node.label for node in nodes if node.weight > 1.0])
    for _ in range(92):
        source = str(rng.choice(labels))
        if rng.random() < 0.55:
            target = str(rng.choice(high_weight_labels))
        else:
            target = str(rng.choice(labels))
        if source == target:
            continue
        weight = float(rng.gamma(shape=1.35, scale=0.75) + 0.25)
        flows.append((source, target, min(weight, 3.4)))
    return flows


def ribbon_patch(
    start_angle: float,
    end_angle: float,
    width: float,
    color: str,
    radius: float = 0.805,
    alpha: float = 0.26,
    zorder: int = 2,
) -> PathPatch:
    width = min(max(width, 0.20), 8.0)
    s1, s2 = start_angle - width / 2, start_angle + width / 2
    e1, e2 = end_angle + width / 2, end_angle - width / 2

    p0 = polar_to_xy(s1, radius)
    p1 = polar_to_xy(e1, radius)
    p2 = polar_to_xy(e2, radius)
    p3 = polar_to_xy(s2, radius)
    c0 = polar_to_xy(s1, radius * 0.20)
    c1 = polar_to_xy(e1, radius * 0.20)
    c2 = polar_to_xy(e2, radius * 0.20)
    c3 = polar_to_xy(s2, radius * 0.20)

    vertices = [
        p0,
        c0,
        c1,
        p1,
        p2,
        c2,
        c3,
        p3,
        p0,
    ]
    codes = [
        MplPath.MOVETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.LINETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CLOSEPOLY,
    ]
    return PathPatch(MplPath(vertices, codes), facecolor=color, edgecolor="none", alpha=alpha, zorder=zorder)


def draw_sector_ring(ax: plt.Axes, layout: dict[str, dict[str, float]], nodes: list[NodeSpec]) -> None:
    ax.add_patch(Wedge((0, 0), 1.075, 0, 360, width=0.105, facecolor="#eeeeee", edgecolor="none", alpha=0.85, zorder=0))
    for node in nodes:
        item = layout[node.label]
        ax.add_patch(
            Wedge(
                (0, 0),
                1.000,
                theta1=item["end"],
                theta2=item["start"],
                width=0.115,
                facecolor=node.color,
                edgecolor="#3a3a3a",
                linewidth=0.38,
                zorder=5,
            )
        )
        ax.add_patch(
            Wedge(
                (0, 0),
                0.885,
                theta1=item["end"],
                theta2=item["start"],
                width=0.006,
                facecolor="#e8e8e8",
                edgecolor="none",
                zorder=5,
            )
        )


def draw_labels(ax: plt.Axes, layout: dict[str, dict[str, float]], nodes: list[NodeSpec]) -> None:
    for idx, node in enumerate(nodes):
        mid = layout[node.label]["mid"]
        rotation, ha = text_rotation(mid)
        arc = layout[node.label]["arc"]
        radius = 1.145
        if arc < 7.0:
            radius += (idx % 3) * 0.045
        if node.label in {"Acetyltrans", "ATPase", "Actin", "NADP", "Rossmann"}:
            radius += 0.030
        size = 11.8 if arc > 7.0 else 9.6
        if len(node.label.replace("\n", "")) > 11:
            size -= 0.7
        ax.text(
            *polar_to_xy(mid, radius),
            node.label,
            rotation=rotation,
            rotation_mode="anchor",
            ha=ha,
            va="center",
            fontsize=size,
            color="#090909",
            zorder=8,
        )


def make_figure(output_stem: Path) -> None:
    configure_matplotlib()
    layout = compute_layout(NODES)
    flows = build_flows(NODES)
    color_lookup = {node.label: node.color for node in NODES}

    fig, ax = plt.subplots(figsize=(10.6, 10.6), facecolor="white")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.38, 1.38)
    ax.set_ylim(-1.34, 1.39)
    ax.text(0.0, 1.315, "Circos Graph", ha="center", va="bottom", fontsize=22, fontfamily="serif")

    # First draw faint hairline links to create the dense Nature-style chord texture.
    sorted_flows = sorted(flows, key=lambda item: item[2])
    angle_rng = np.random.default_rng(9817)
    for source, target, weight in sorted_flows:
        s_arc = layout[source]["arc"]
        t_arc = layout[target]["arc"]
        s_mid = layout[source]["mid"] + angle_rng.uniform(-0.34 * s_arc, 0.34 * s_arc)
        t_mid = layout[target]["mid"] + angle_rng.uniform(-0.34 * t_arc, 0.34 * t_arc)
        source_color = color_lookup[source]
        alpha = 0.07 if weight < 1.1 else 0.12
        ribbon_width = 0.22 + 0.32 * weight
        if weight >= 3.5:
            alpha = 0.25
            ribbon_width = 0.48 + 0.70 * weight
        patch = ribbon_patch(
            s_mid,
            t_mid,
            ribbon_width,
            lighten(source_color, amount=0.18),
            alpha=alpha,
            zorder=1 if weight < 3.5 else 3,
        )
        ax.add_patch(patch)

    draw_sector_ring(ax, layout, NODES)
    draw_labels(ax, layout, NODES)

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=300, bbox_inches="tight", pad_inches=0.03)
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.03)
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def main() -> None:
    make_figure(ROOT / "outputs" / "nature_chord_diagram_replica")


if __name__ == "__main__":
    main()
