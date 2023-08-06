
import numpy as np
from scipy import stats
from functools import lru_cache

# v6 estimator
def estimate_mean(z):
    return np.exp(estimate_tau(z))

def estimate_tau(z):
    n = z.size
    x = np.log(z)
    x_bar = np.mean(x)
    s2 = np.sum((x - x_bar) ** 2)
    n1 = n - 1
    n4 = n + 4

    return x_bar + n1 * s2 / (2 * n4 * n1 + 3 * s2)

# var(tau) approximation estimator
def estimate_tau_variance(z):
    n = z.size
    x = np.log(z)
    x_bar = np.mean(x)
    s2 = np.sum((x - x_bar) ** 2)
    n1 = n - 1
    n4 = n + 4

    return s2 / (n * n1) + 8 * n4 ** 2 * s2 ** 2 / (n1 * (3 * s2 / n1 + 2 * n4) ** 4)

def T_func(n, sigma, N, C):
    sigma2 = sigma ** 2
    n1 = n - 1
    n4 = n + 4

    a = 2 * n4 + 3 * sigma2 * C / n1

    return (
            (N + n ** 0.5 * sigma / 2 * (2 * C / a - 1))
            / (C / n1 + 8 * sigma2 * n * n1 * n4 ** 2 * (C / n1) ** 2 / a ** 4) ** 0.5
    )

@lru_cache(maxsize=128)
def generate_T_dist(n, sigma, count=10000):
    rs = np.random.RandomState(seed=1)
    N = rs.normal(size=count)
    C = rs.chisquare(n - 1, size=count)
    return T_func(n, sigma, N, C)

# public
def test_mean_1samp(z, expected, alternative='two-sided'):
    tau_var = estimate_tau_variance(z)
    tau = estimate_tau(z)

    n = z.size
    x = np.log(z)
    x_bar = np.mean(x)
    s2 = np.sum((x - x_bar) ** 2)
    sigma = (s2 / (n - 1)) ** 0.5

    T = generate_T_dist(n, sigma)
    q = 1 - stats.percentileofscore(T, (tau - np.log(expected)) / tau_var ** 0.5) / 100.0

    if alternative == 'less':
        return q
    elif alternative == 'greater':
        return 1 - q
    elif alternative == 'two-sided':
        return 1 - 2 * np.abs(q - 0.5)

def estimate_confidence_interval(z):
    tau_var = estimate_tau_variance(z)
    tau = estimate_tau(z)

    n = z.size
    x = np.log(z)
    x_bar = np.mean(x)
    s2 = np.sum((x - x_bar) ** 2)
    sigma = (s2 / (n - 1)) ** 0.5

    T = generate_T_dist(n, sigma)
    t1 = np.quantile(T, 0.99)
    t2 = np.quantile(T, 0.01)

    return np.exp(tau - t1 * tau_var ** 0.5), np.exp(tau - t2 * tau_var ** 0.5)
