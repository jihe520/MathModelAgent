# Plot Recipes

Use bundled scripts first. These notes are only for customization after a template has been copied into the workspace.

- SHAP composite: stacked horizontal mean-absolute importance bars plus class/model beeswarm strips and a feature-value colorbar.
- Paired raincloud: half-violins, jittered observations, box geometry, mean diamonds, and connected mean trends.
- ROC with CI: fold curves interpolated to a shared FPR grid, mean curve, standard-deviation band, AUC mean ± sd legend, and diagonal baseline.
- Taylor diagram: polar coordinates with angle `arccos(correlation)` and radius as model standard deviation.
- Correlation grid: lower scatter/fitted CI, diagonal histograms, upper coefficient cells with diverging colors and stars.
- Prediction marginal grid: predicted-vs-actual scatter plus top/right histograms and KDE-like curves.
- 3D tuning surface: `mpl_toolkits.mplot3d`, smooth response surface, colorbar, and checked camera angle.
- Split violin + correlation matrix: signed lower-triangle marker matrix plus left/right half-violin distribution comparison.
- Circular heatmap: polar bars, flipped outer labels, central legend, and ring-specific color scales.
- Chord diagram: outer `Wedge` sectors and translucent Bezier `PathPatch` ribbons.
- Urban cooling composite: stacked city bars, raincloud metric panels, city legend, and boxplots with connected means.
