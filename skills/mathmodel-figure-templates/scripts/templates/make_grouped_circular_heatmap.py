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
from matplotlib.patches import Patch, Rectangle


@dataclass(frozen=True)
class TraitSpec:
    name: str
    color: str
    pale: str


@dataclass(frozen=True)
class PairGroup:
    label: str
    color: str
    count: int


TRAITS_OUTER_TO_INNER = [
    TraitSpec("Insomnia", "#51448a", "#e7e4f2"),
    TraitSpec("Sleep duration", "#606766", "#ededeb"),
    TraitSpec("Long sleep", "#4e9568", "#e2f0e4"),
    TraitSpec("Short sleep", "#bd454c", "#f5dddd"),
    TraitSpec("Chronotype", "#7b54b9", "#ece3f6"),
    TraitSpec("Morningness", "#3d719b", "#e3edf5"),
    TraitSpec("Napping frequency", "#e58a50", "#f9e4d5"),
    TraitSpec("Sleepiness", "#5d6a67", "#e3e9e8"),
]


PAIR_GROUPS = [
    PairGroup("Sleep traits to cortical surface area", "#a9d9e8", 10),
    PairGroup("Sleep traits to cortical thickness", "#1f79b5", 10),
    PairGroup("Sleep traits to subcortical volume", "#9ee48e", 10),
    PairGroup("Sleep traits to longitudinal change", "#22a33a", 10),
    PairGroup("Cortical surface area to sleep traits", "#f28a9e", 12),
    PairGroup("Cortical thickness to sleep traits", "#f7ba67", 12),
    PairGroup("Subcortical volume to sleep traits", "#c8b3d8", 14),
    PairGroup("Longitudinal change to sleep traits", "#7b3db6", 14),
]


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif", "serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 10,
            "axes.linewidth": 0.8,
        }
    )


def make_trait_cmap(spec: TraitSpec) -> mpl.colors.LinearSegmentedColormap:
    return mpl.colors.LinearSegmentedColormap.from_list(
        f"{spec.name.replace(' ', '_')}_magnitude",
        [
            (0.00, spec.color),
            (0.35, spec.pale),
            (0.50, "#ffffff"),
            (0.65, spec.pale),
            (1.00, spec.color),
        ],
    )


def simulate_heatmap_values(seed: int = 20260629, n_traits: int = 8, n_items: int = 92) -> np.ndarray:
    rng = np.random.default_rng(seed)
    theta = np.linspace(0, 2 * np.pi, n_items, endpoint=False)
    values = np.zeros((n_traits, n_items), dtype=float)

    group_offsets = np.repeat(np.linspace(-0.85, 0.95, len(PAIR_GROUPS)), [g.count for g in PAIR_GROUPS])
    for trait_idx in range(n_traits):
        phase = trait_idx * 0.72
        wave = 1.35 * np.sin(theta * (1.0 + trait_idx % 3) + phase)
        wave += 0.95 * np.cos(theta * (2.3 + trait_idx / 6.0) - phase * 0.6)
        structured = wave + group_offsets * (0.65 - trait_idx * 0.035)
        noise = rng.normal(0, 1.25, n_items)
        values[trait_idx] = structured + noise

    strong_cells = [
        (0, 4, 4.7),
        (1, 15, -4.5),
        (2, 21, 4.3),
        (3, 31, -4.7),
        (4, 39, 4.5),
        (5, 53, -4.4),
        (6, 66, 4.2),
        (7, 74, -4.6),
        (2, 84, 4.7),
        (3, 88, -4.3),
    ]
    for trait_idx, item_idx, value in strong_cells:
        values[trait_idx, item_idx] = value

    return np.clip(values * 1.16, -5, 5)


def draw_ring_cells(
    ax: plt.Axes,
    theta: np.ndarray,
    width: float,
    radius: float,
    height: float,
    values: np.ndarray,
    cmap: mpl.colors.Colormap,
    norm: mpl.colors.Normalize,
) -> None:
    colors = cmap(norm(values))
    ax.bar(
        theta,
        np.full_like(theta, height),
        width=width,
        bottom=radius,
        color=colors,
        edgecolor="white",
        linewidth=0.55,
        align="center",
    )


def draw_group_ring(
    ax: plt.Axes,
    theta: np.ndarray,
    width: float,
    radius: float,
    height: float,
) -> list[str]:
    group_ids: list[str] = []
    for group_idx, group in enumerate(PAIR_GROUPS):
        group_ids.extend([group.color] * group.count)
    for angle, color in zip(theta, group_ids, strict=True):
        ax.bar(
            angle,
            height,
            width=width,
            bottom=radius,
            color=color,
            edgecolor="white",
            linewidth=0.55,
            align="center",
        )
    return group_ids


def text_rotation(angle_deg: float) -> tuple[float, str]:
    normalized = angle_deg % 360
    if 90 < normalized < 270:
        return angle_deg + 90, "right"
    return angle_deg - 90, "left"


def draw_outer_labels(
    ax: plt.Axes,
    theta: np.ndarray,
    radius: float,
    start_angle: float,
    step_angle: float,
) -> None:
    for idx, angle in enumerate(theta):
        angle_deg = start_angle + (idx + 0.5) * step_angle
        rotation, ha = text_rotation(angle_deg)
        ax.text(
            angle,
            radius,
            f"Brain Phenotype {idx + 1}",
            rotation=rotation,
            rotation_mode="anchor",
            ha=ha,
            va="center",
            fontsize=6.5,
            color="#111111",
        )


def draw_stars(
    ax: plt.Axes,
    theta: np.ndarray,
    values: np.ndarray,
    ring_radii_inner_to_outer: list[float],
    ring_height: float,
) -> None:
    outer_to_inner_index = list(reversed(range(values.shape[0])))
    candidates = np.argwhere(np.abs(values) > 4.1)
    for trait_outer_idx, item_idx in candidates:
        inner_order_idx = outer_to_inner_index[trait_outer_idx]
        radius = ring_radii_inner_to_outer[inner_order_idx] + ring_height * 0.50
        ax.text(theta[item_idx], radius, "*", ha="center", va="center", color="#f8f8f8", fontsize=11, fontweight="bold")


def add_trait_colorbar_stack(fig: plt.Figure, cmaps: list[mpl.colors.Colormap], norm: mpl.colors.Normalize) -> None:
    left = 0.735
    bottom_top = 0.764
    width = 0.095
    height = 0.014
    gap = 0.035
    gradient = np.linspace(-5, 5, 300).reshape(1, -1)

    fig.patches.append(
        Rectangle(
            (left - 0.010, bottom_top - 7 * gap - 0.010),
            0.245,
            7 * gap + height + 0.030,
            transform=fig.transFigure,
            facecolor="white",
            edgecolor="none",
            zorder=2,
        )
    )

    for idx, (spec, cmap) in enumerate(zip(TRAITS_OUTER_TO_INNER, cmaps, strict=True)):
        bottom = bottom_top - idx * gap
        cax = fig.add_axes([left, bottom, width, height])
        cax.set_zorder(3)
        cax.imshow(gradient, aspect="auto", cmap=cmap, norm=norm, extent=(-5, 5, 0, 1))
        cax.axvline(0, color="#333333", lw=0.8, ls=(0, (3, 2)))
        cax.set_yticks([])
        cax.set_xticks([-5, 0, 5])
        cax.set_xticklabels(["-5", "0", "5"], fontsize=8)
        cax.tick_params(axis="x", length=0, pad=1)
        for spine in cax.spines.values():
            spine.set_color("#111111")
            spine.set_linewidth(0.8)
        fig.text(left + width + 0.014, bottom + height / 2, spec.name, va="center", ha="left", fontsize=11, zorder=3)


def add_center_legend(fig: plt.Figure) -> None:
    left, bottom, width, height = 0.372, 0.410, 0.295, 0.205
    ax = fig.add_axes([left, bottom, width, height])
    ax.set_zorder(4)
    ax.axis("off")
    ax.text(0.00, 1.02, "Exposure and outcome pairs", fontsize=10, fontweight="bold", ha="left", va="bottom")

    handles = [Patch(facecolor=group.color, edgecolor="white", label=group.label) for group in PAIR_GROUPS]
    ax.legend(
        handles=handles,
        loc="upper left",
        bbox_to_anchor=(0.00, 0.98),
        frameon=False,
        fontsize=8.3,
        handlelength=1.2,
        handleheight=1.2,
        borderaxespad=0,
        labelspacing=0.55,
    )


def make_figure(output_stem: Path) -> None:
    configure_matplotlib()
    n_items = sum(group.count for group in PAIR_GROUPS)
    values = simulate_heatmap_values(n_items=n_items)

    start_angle = 82.0
    span_angle = 322.0
    step_angle = span_angle / n_items
    theta = np.deg2rad(start_angle + (np.arange(n_items) + 0.5) * step_angle)
    width = np.deg2rad(step_angle * 0.96)

    fig = plt.figure(figsize=(13.6, 12.6), facecolor="white")
    ax = fig.add_axes([0.005, 0.025, 0.805, 0.950], projection="polar")
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_axis_off()
    ax.set_facecolor("white")

    group_radius = 1.25
    group_height = 0.110
    ring_gap = 0.012
    heatmap_radius = 1.50
    ring_height = 0.115
    ring_radii = [heatmap_radius + i * (ring_height + ring_gap) for i in range(len(TRAITS_OUTER_TO_INNER))]
    outer_radius = ring_radii[-1] + ring_height
    ax.set_ylim(0, outer_radius + 0.70)

    draw_group_ring(ax, theta, width, group_radius, group_height)

    norm = mpl.colors.Normalize(vmin=-5, vmax=5)
    cmaps = [make_trait_cmap(spec) for spec in TRAITS_OUTER_TO_INNER]
    for trait_outer_idx, (spec, cmap) in enumerate(zip(TRAITS_OUTER_TO_INNER, cmaps, strict=True)):
        radius = ring_radii[len(TRAITS_OUTER_TO_INNER) - 1 - trait_outer_idx]
        draw_ring_cells(ax, theta, width, radius, ring_height, values[trait_outer_idx], cmap, norm)

    for radius in [group_radius, group_radius + group_height, heatmap_radius - 0.075, outer_radius]:
        angles = np.linspace(np.deg2rad(start_angle), np.deg2rad(start_angle + span_angle), 700)
        ax.plot(angles, np.full_like(angles, radius), color="white", lw=1.0, zorder=5)

    draw_stars(ax, theta, values, ring_radii, ring_height)
    draw_outer_labels(ax, theta, outer_radius + 0.265, start_angle, step_angle)

    add_center_legend(fig)
    add_trait_colorbar_stack(fig, cmaps, norm)

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=300, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.02)
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def main() -> None:
    make_figure(ROOT / "outputs" / "grouped_circular_heatmap_replica")


if __name__ == "__main__":
    main()
