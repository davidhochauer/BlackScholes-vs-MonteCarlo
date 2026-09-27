import numpy as np


def simulate_paths(S, T, r, sigma, num_simulations=100_000, num_steps=1, seed=None):
    rng = np.random.default_rng(seed)
    dt = T / num_steps

    # Start every path at the current price S
    paths = np.zeros((num_simulations, num_steps + 1))
    paths[:, 0] = S

    for t in range(1, num_steps + 1):
        # Random shocks, one per simulated path, drawn from a standard normal
        z = rng.standard_normal(num_simulations)

        # Geometric Brownian motion step: how the price moves from one step to the next
        paths[:, t] = paths[:, t - 1] * np.exp(
            (r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z
        )

    return paths


def monte_carlo_price(S, K, T, r, sigma, option_type="call", num_simulations=100_000, seed=None):
    paths = simulate_paths(S, T, r, sigma, num_simulations=num_simulations, num_steps=1, seed=seed)
    ending_prices = paths[:, -1]

    if option_type == "call":
        payoffs = np.maximum(ending_prices - K, 0)
    elif option_type == "put":
        payoffs = np.maximum(K - ending_prices, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Discount the average payoff back to today's value
    discounted_payoffs = np.exp(-r * T) * payoffs
    price = np.mean(discounted_payoffs)

    # Standard error: how much the estimate would wobble if we reran the simulation
    standard_error = np.std(discounted_payoffs) / np.sqrt(num_simulations)

    return {"price": price, "standard_error": standard_error}


if __name__ == "__main__":
    result = monte_carlo_price(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call", seed=42)
    print(f"Monte Carlo call price: {result['price']:.4f} (+/- {result['standard_error']:.4f})")