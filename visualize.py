import numpy as np
import matplotlib.pyplot as plt

from black_scholes import black_scholes_price
from monte_carlo import simulate_paths, monte_carlo_price


def plot_payoff(K, option_type="call", price_range=None, save_path=None):
    if price_range is None:
        price_range = np.linspace(0.5 * K, 1.5 * K, 200)

    if option_type == "call":
        payoffs = np.maximum(price_range - K, 0)
    else:
        payoffs = np.maximum(K - price_range, 0)

    plt.figure(figsize=(8, 5))
    plt.plot(price_range, payoffs, label=f"{option_type.capitalize()} payoff")
    plt.axvline(K, color="gray", linestyle="--", label=f"Strike (K={K})")
    plt.xlabel("Stock price at expiration")
    plt.ylabel("Payoff")
    plt.title(f"{option_type.capitalize()} Option Payoff at Expiration")
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_simulated_paths(S, T, r, sigma, num_paths=30, num_steps=252, seed=None, save_path=None):
    paths = simulate_paths(S, T, r, sigma, num_simulations=num_paths, num_steps=num_steps, seed=seed)
    time_grid = np.linspace(0, T, num_steps + 1)

    plt.figure(figsize=(8, 5))
    for i in range(num_paths):
        plt.plot(time_grid, paths[i], alpha=0.6, linewidth=0.8)
    plt.xlabel("Time (years)")
    plt.ylabel("Simulated stock price")
    plt.title(f"{num_paths} Simulated Price Paths (Geometric Brownian Motion)")
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_convergence(S, K, T, r, sigma, option_type="call", save_path=None):
    bs_price = black_scholes_price(S, K, T, r, sigma, option_type)

    simulation_counts = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000]
    mc_prices = []
    errors = []

    for n in simulation_counts:
        result = monte_carlo_price(S, K, T, r, sigma, option_type, num_simulations=n, seed=42)
        mc_prices.append(result["price"])
        errors.append(result["standard_error"])

    plt.figure(figsize=(8, 5))
    plt.errorbar(simulation_counts, mc_prices, yerr=errors, fmt="o-", capsize=4, label="Monte Carlo estimate")
    plt.axhline(bs_price, color="red", linestyle="--", label=f"Black-Scholes price ({bs_price:.4f})")
    plt.xscale("log")
    plt.xlabel("Number of simulations (log scale)")
    plt.ylabel("Option price")
    plt.title("Monte Carlo Convergence to Black-Scholes Price")
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

    plot_payoff(K, option_type="call")
    plot_simulated_paths(S, T, r, sigma, num_paths=30, seed=42)
    plot_convergence(S, K, T, r, sigma, option_type="call")