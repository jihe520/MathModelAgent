
= Model Design and Methodology

== Prediction Model

$ hat(y) = f(bold(x); theta) = sum_(i=1)^n theta_i phi_i(bold(x)) $

== Optimization Objective

$ cal(L)(theta) = frac(1, N) sum_(i=1)^N (y_i - hat(y)_i)^2 + lambda R(theta) $

== Ensemble Strategy

Random Forest with $n = 100$ estimators and `max_depth=10` for robust prediction.
