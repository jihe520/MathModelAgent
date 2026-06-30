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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle


@dataclass(frozen=True)
class CitySpec:
    name: str
    group: str


GROUP_ORDER = ["Megacity", "Large City", "Medium City I", "Medium City II", "Small City"]
GROUP_COLORS = {
    "Megacity": "#34485b",
    "Large City": "#557280",
    "Medium City I": "#759b9d",
    "Medium City II": "#95bdae",
    "Small City": "#c8ded4",
}


CITY_SPECS = [
    CitySpec("Shanghai", "Megacity"),
    CitySpec("Hangzhou", "Large City"),
    CitySpec("Nanjing", "Large City"),
    CitySpec("Suzhou", "Large City"),
    CitySpec("Hefei", "Medium City I"),
    CitySpec("Ningbo", "Large City"),
    CitySpec("Wuxi", "Large City"),
    CitySpec("Changzhou", "Medium City I"),
    CitySpec("Shaoxing", "Medium City I"),
    CitySpec("Nantong", "Medium City I"),
    CitySpec("Yangzhou", "Medium City II"),
    CitySpec("Yancheng", "Medium City II"),
    CitySpec("Taizhou", "Medium City I"),
    CitySpec("Wuhu", "Medium City II"),
    CitySpec("Jiaxing", "Medium City I"),
    CitySpec("Taizhou", "Medium City I"),
    CitySpec("Ma'anshan", "Medium City II"),
    CitySpec("Zhenjiang", "Medium City II"),
    CitySpec("Jinhua", "Medium City II"),
    CitySpec("Huzhou", "Medium City II"),
    CitySpec("Anqing", "Small City"),
    CitySpec("Zhoushan", "Small City"),
    CitySpec("Tongling", "Small City"),
    CitySpec("Chuzhou", "Medium City II"),
    CitySpec("Chizhou", "Small City"),
    CitySpec("Xuancheng", "Small City"),
]


BAR_COUNTS = [
    ("Shanghai", 314, 46),
    ("Hangzhou", 139, 39),
    ("Nanjing", 110, 37),
    ("Suzhou", 89, 29),
    ("Ningbo", 77, 34),
    ("Wuxi", 61, 22),
    ("Hefei", 67, 12),
    ("Yangzhou", 48, 27),
    ("Changzhou", 53, 8),
    ("Nantong", 39, 7),
    ("Shaoxing", 34, 11),
    ("Jiaxing", 32, 4),
    ("Taizhou", 19, 1),
    ("Huzhou", 19, 0),
    ("Taizhou", 23, 1),
    ("Zhenjiang", 22, 1),
    ("Ma'anshan", 21, 4),
    ("Jinhua", 14, 1),
    ("Yancheng", 17, 6),
    ("Wuhu", 16, 2),
    ("Chuzhou", 17, 1),
    ("Xuancheng", 13, 1),
    ("Tongling", 8, 1),
    ("Anqing", 8, 0),
    ("Zhoushan", 8, 0),
    ("Chizhou", 8, 0),
]


METRICS = {
    "PCM": {"ylim": (0, 9), "xlim": (0, 7), "ylabel": "PCM(°C)", "unit": "°C"},
    "PCD": {"ylim": (0, 350), "xlim": (0, 300), "ylabel": "PCD(m)", "unit": "m"},
    "PCI": {"ylim": (0, 0.06), "xlim": (0, 0.06), "ylabel": "PCI", "unit": ""},
    "PCG": {"ylim": (0, 2.5), "xlim": (0, 2.2), "ylabel": "PCG", "unit": ""},
}


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 9,
            "axes.linewidth": 0.75,
            "xtick.major.width": 0.65,
            "ytick.major.width": 0.65,
            "legend.frameon": False,
        }
    )


def kde_1d(values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    std = max(np.std(values, ddof=1), 1e-6)
    bandwidth = max(1.06 * std * values.size ** (-1 / 5), std * 0.16, 1e-5)
    z = (grid[:, None] - values[None, :]) / bandwidth
    density = np.exp(-0.5 * z**2).mean(axis=1) / (bandwidth * np.sqrt(2 * np.pi))
    return density / density.max() if density.max() > 0 else density


def simulate_city_metric_data(seed: int = 20260629) -> dict[str, list[np.ndarray]]:
    rng = np.random.default_rng(seed)
    group_offsets = {
        "Megacity": {"PCM": 3.0, "PCD": 150.0, "PCI": 0.019, "PCG": 0.95},
        "Large City": {"PCM": 2.8, "PCD": 155.0, "PCI": 0.020, "PCG": 0.95},
        "Medium City I": {"PCM": 3.1, "PCD": 150.0, "PCI": 0.019, "PCG": 0.98},
        "Medium City II": {"PCM": 3.2, "PCD": 145.0, "PCI": 0.018, "PCG": 0.96},
        "Small City": {"PCM": 3.6, "PCD": 160.0, "PCI": 0.020, "PCG": 1.05},
    }
    ranges = {
        "PCM": (0.0, 8.8, 0.85),
        "PCD": (10.0, 340.0, 36.0),
        "PCI": (0.001, 0.060, 0.0075),
        "PCG": (0.05, 2.45, 0.28),
    }

    data: dict[str, list[np.ndarray]] = {metric: [] for metric in METRICS}
    for city_idx, city in enumerate(CITY_SPECS):
        n = 42 + int(52 * (np.sin(city_idx * 0.57) + 1) / 2)
        phase = np.sin(city_idx / 3.1)
        secondary = np.cos(city_idx / 2.0)
        for metric in METRICS:
            low, high, spread = ranges[metric]
            base = group_offsets[city.group][metric]
            if metric == "PCM":
                mean = base + 0.45 * phase + 0.018 * city_idx
                values = rng.normal(mean, spread, n)
            elif metric == "PCD":
                mean = base + 20.0 * phase + 11.0 * secondary
                values = rng.normal(mean, spread, n)
            elif metric == "PCI":
                mean = base + 0.0035 * phase - 0.00008 * city_idx
                values = rng.normal(mean, spread, n)
            else:
                mean = base + 0.16 * phase + 0.05 * secondary
                values = rng.normal(mean, spread, n)
            data[metric].append(np.clip(values, low, high))
    return data


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(length=2.5, color="#333333", labelcolor="#111111")


def draw_panel_a(ax: plt.Axes) -> None:
    effect_color = "#315f5e"
    no_effect_color = "#9a9a9a"
    cities = [item[0] for item in BAR_COUNTS]
    effect = np.array([item[1] for item in BAR_COUNTS])
    no_effect = np.array([item[2] for item in BAR_COUNTS])
    y = np.arange(len(cities))

    ax.barh(y, effect, color=effect_color, edgecolor="white", linewidth=0.45, height=0.74)
    ax.barh(y, no_effect, left=effect, color=no_effect_color, edgecolor="white", linewidth=0.45, height=0.74)
    for yi, e, n in zip(y, effect, no_effect, strict=True):
        if e > 12:
            ax.text(e - 7, yi, f"{e}", ha="right", va="center", color="white", fontsize=8)
        else:
            ax.text(e + 1.5, yi, f"{e}", ha="left", va="center", color=effect_color, fontsize=7)
        if n >= 8:
            ax.text(e + n / 2, yi, f"{n}", ha="center", va="center", color="white", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels(cities, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 375)
    ax.set_xticks(np.arange(0, 376, 50))
    ax.tick_params(axis="y", length=0, pad=1)
    ax.grid(axis="x", color="#e1e1e1", lw=0.45)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_linewidth(0.65)

    header = Rectangle((0, -1.48), 375, 0.94, facecolor="#b9b9b9", edgecolor="#444444", linewidth=0.7, clip_on=False)
    ax.add_patch(header)
    ax.text(187.5, -1.02, "Number of Urban Parks", ha="center", va="center", fontsize=10)

    handles = [
        Patch(facecolor=effect_color, edgecolor="white", label="Show a cooling effect"),
        Patch(facecolor=no_effect_color, edgecolor="white", label="No significant cooling effect"),
    ]
    ax.legend(handles=handles, title="Legend", loc="lower right", bbox_to_anchor=(0.98, 0.01), fontsize=8, title_fontsize=9)
    ax.text(-0.052, 1.02, "a", transform=ax.transAxes, fontsize=11)


def draw_horizontal_box(ax: plt.Axes, values: np.ndarray, y: float, color: str) -> None:
    q1, med, q3 = np.percentile(values, [25, 50, 75])
    iqr = q3 - q1
    lo = np.min(values[values >= q1 - 1.5 * iqr])
    hi = np.max(values[values <= q3 + 1.5 * iqr])
    box_h = 0.18
    ax.plot([lo, hi], [y, y], color="#3f3f3f", lw=0.6, zorder=3)
    ax.plot([lo, lo], [y - box_h / 2, y + box_h / 2], color="#3f3f3f", lw=0.6, zorder=3)
    ax.plot([hi, hi], [y - box_h / 2, y + box_h / 2], color="#3f3f3f", lw=0.6, zorder=3)
    ax.add_patch(
        Rectangle((q1, y - box_h / 2), q3 - q1, box_h, facecolor=color, edgecolor="#3f3f3f", linewidth=0.55, zorder=4)
    )
    ax.plot([med, med], [y - box_h / 2, y + box_h / 2], color="white", lw=0.8, zorder=5)


def draw_raincloud(ax: plt.Axes, grouped_values: dict[str, np.ndarray], metric: str, show_ylabels: bool) -> None:
    cfg = METRICS[metric]
    x_min, x_max = cfg["xlim"]
    grid = np.linspace(x_min, x_max, 320)
    metric_seed = {"PCM": 101, "PCD": 202, "PCI": 303, "PCG": 404}[metric]
    rng = np.random.default_rng(metric_seed)

    for row, group in enumerate(GROUP_ORDER):
        y = len(GROUP_ORDER) - 1 - row
        values = grouped_values[group]
        color = GROUP_COLORS[group]
        density = kde_1d(values, grid) * 0.53
        ax.fill_between(grid, y, y + density, color=color, alpha=0.96, linewidth=0)
        ax.plot(grid, y + density, color="#53666a", lw=0.65)
        ax.hlines(y, x_min, x_max, color="#cfcfcf", lw=0.6)
        sample = values if values.size < 330 else rng.choice(values, 330, replace=False)
        jitter = rng.uniform(-0.24, -0.08, size=sample.size)
        ax.scatter(sample, y + jitter, s=2.0, color="#333333", alpha=0.46, linewidths=0, zorder=2)
        draw_horizontal_box(ax, values, y + 0.08, color)
        ax.axvline(np.mean(values), ymin=(y + 0.03) / 5, ymax=(y + 0.52) / 5, color="white", lw=0.6, ls=(0, (2, 2)))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.55, 4.78)
    ax.set_title(metric, fontsize=9, fontweight="bold", pad=5)
    ax.grid(axis="x", color="#ececec", lw=0.45)
    ax.set_axisbelow(True)
    ax.set_yticks(range(len(GROUP_ORDER)))
    ax.set_yticklabels(list(reversed(GROUP_ORDER)) if show_ylabels else [], fontsize=8)
    ax.tick_params(axis="y", length=0, pad=2)
    style_axis(ax)
    if metric == "PCM":
        ax.set_xticks(np.arange(0, 8, 1))
        ax.text(1.01, -0.05, "°C", transform=ax.transAxes, ha="left", va="top", fontsize=8)
    elif metric == "PCD":
        ax.set_xticks([0, 100, 200, 300])
        ax.text(1.01, -0.05, "m", transform=ax.transAxes, ha="left", va="top", fontsize=8)
    elif metric == "PCI":
        ax.set_xticks([0, 0.02, 0.04, 0.06])
    else:
        ax.set_xticks([0, 1, 2])


def draw_vertical_boxplot_panel(ax: plt.Axes, metric: str, metric_data: list[np.ndarray]) -> None:
    means = []
    for idx, (values, city) in enumerate(zip(metric_data, CITY_SPECS, strict=True), start=1):
        color = GROUP_COLORS[city.group]
        q1, med, q3 = np.percentile(values, [25, 50, 75])
        iqr = q3 - q1
        lo = np.min(values[values >= q1 - 1.5 * iqr])
        hi = np.max(values[values <= q3 + 1.5 * iqr])
        means.append(float(np.mean(values)))

        ax.plot([idx, idx], [lo, hi], color="#a0a0a0", lw=0.65, zorder=1)
        ax.plot([idx - 0.17, idx + 0.17], [lo, lo], color="#a0a0a0", lw=0.65, zorder=1)
        ax.plot([idx - 0.17, idx + 0.17], [hi, hi], color="#a0a0a0", lw=0.65, zorder=1)
        ax.add_patch(
            Rectangle(
                (idx - 0.32, q1),
                0.64,
                q3 - q1,
                facecolor=color,
                edgecolor="white",
                linewidth=0.5,
                alpha=0.78,
                zorder=2,
            )
        )
        ax.plot([idx - 0.30, idx + 0.30], [med, med], color="#315f5e", lw=1.0, zorder=3)
        ax.scatter(idx, means[-1], marker="^", s=14, color="#d44d5d", edgecolor="white", linewidth=0.25, zorder=4)

    ax.plot(np.arange(1, len(CITY_SPECS) + 1), means, color="#2f6791", lw=0.75, alpha=0.72, zorder=3)
    ax.set_xlim(0.3, len(CITY_SPECS) + 0.7)
    ax.set_ylim(*METRICS[metric]["ylim"])
    ax.set_ylabel(METRICS[metric]["ylabel"], fontsize=9)
    ax.set_xticks(np.arange(1, len(CITY_SPECS) + 1))
    ax.set_xticklabels([str(i) for i in range(1, len(CITY_SPECS) + 1)], fontsize=7)
    ax.tick_params(axis="x", length=0, pad=1)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="y", color="#efefef", lw=0.45)
    for spine in ax.spines.values():
        spine.set_linewidth(0.75)


def add_city_and_legend_panel(ax: plt.Axes) -> None:
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_autoscale_on(False)
    ax.text(-0.05, 1.03, "c", transform=ax.transAxes, fontsize=11)

    columns = [(1, CITY_SPECS[:9]), (10, CITY_SPECS[9:18]), (19, CITY_SPECS[18:])]
    x_positions = [0.00, 0.36, 0.70]
    for col, (start_idx, cities) in enumerate(columns):
        for row, city in enumerate(cities):
            original_idx = start_idx + row
            ax.text(x_positions[col], 0.96 - row * 0.050, f"{original_idx:02d}.{city.name}", ha="left", va="top", fontsize=8)

    y0 = 0.31
    ax.add_patch(Rectangle((0.00, y0), 0.09, 0.035, facecolor="white", edgecolor="#333333", linewidth=0.7))
    ax.text(0.12, y0 + 0.017, "25%-75%", va="center", fontsize=8)
    ax.plot([0.00, 0.09], [y0 - 0.050, y0 - 0.050], color="#315f5e", lw=2.0)
    ax.text(0.12, y0 - 0.050, "Median Line", va="center", fontsize=8)
    ax.scatter(0.045, y0 - 0.105, marker="^", s=16, color="#d44d5d", edgecolor="white", linewidth=0.3)
    ax.text(0.12, y0 - 0.105, "Mean", va="center", fontsize=8)
    ax.plot([0.00, 0.09], [y0 - 0.160, y0 - 0.160], color="#777777", lw=0.8)
    ax.plot([0.00, 0.00], [y0 - 0.177, y0 - 0.143], color="#777777", lw=0.8)
    ax.plot([0.09, 0.09], [y0 - 0.177, y0 - 0.143], color="#777777", lw=0.8)
    ax.text(0.12, y0 - 0.160, "Range with 1.5IQR", va="center", fontsize=8)
    ax.plot([0.00, 0.09], [y0 - 0.215, y0 - 0.215], color="#2f6791", lw=0.9)
    ax.text(0.12, y0 - 0.215, "Connecting line Mean", va="center", fontsize=8)

    for idx, group in enumerate(GROUP_ORDER):
        y = y0 - idx * 0.054
        ax.add_patch(Rectangle((0.57, y), 0.09, 0.035, facecolor=GROUP_COLORS[group], edgecolor="white", linewidth=0.5))
        ax.text(0.69, y + 0.017, group, va="center", fontsize=8)


def make_figure(output_stem: Path) -> None:
    configure_matplotlib()
    city_metric_data = simulate_city_metric_data()
    grouped_values = {
        metric: {
            group: np.concatenate([values for values, city in zip(metric_values, CITY_SPECS, strict=True) if city.group == group])
            for group in GROUP_ORDER
        }
        for metric, metric_values in city_metric_data.items()
    }

    fig = plt.figure(figsize=(13.0, 10.0), facecolor="white")
    ax_a = fig.add_axes([0.055, 0.455, 0.295, 0.500])
    draw_panel_a(ax_a)

    b_axes = {
        "PCM": fig.add_axes([0.405, 0.720, 0.315, 0.225]),
        "PCD": fig.add_axes([0.765, 0.720, 0.215, 0.225]),
        "PCI": fig.add_axes([0.405, 0.455, 0.315, 0.225]),
        "PCG": fig.add_axes([0.765, 0.455, 0.215, 0.225]),
    }
    for metric, ax in b_axes.items():
        draw_raincloud(ax, grouped_values[metric], metric, show_ylabels=metric in {"PCM", "PCI"})
    b_axes["PCM"].text(-0.10, 1.06, "b", transform=b_axes["PCM"].transAxes, fontsize=11)

    ax_c_legend = fig.add_axes([0.055, 0.070, 0.295, 0.335])
    add_city_and_legend_panel(ax_c_legend)

    c_axes = {
        "PCM": fig.add_axes([0.405, 0.265, 0.315, 0.170]),
        "PCD": fig.add_axes([0.765, 0.265, 0.215, 0.170]),
        "PCI": fig.add_axes([0.405, 0.070, 0.315, 0.170]),
        "PCG": fig.add_axes([0.765, 0.070, 0.215, 0.170]),
    }
    for metric, ax in c_axes.items():
        draw_vertical_boxplot_panel(ax, metric, city_metric_data[metric])

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    make_figure(ROOT / "outputs" / "urban_park_cooling_combo_replica")


if __name__ == "__main__":
    main()
