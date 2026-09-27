from black_scholes import black_scholes_price, greeks
from monte_carlo import monte_carlo_price
from visualize import plot_payoff, plot_simulated_paths, plot_convergence


def main():
    # Example option: stock at 100, strike at 100, 1 year to expiry,
    # 5% risk-free rate, 20% annualized volatility
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    option_type = "call"

    print("=" * 50)
    print("Black-Scholes vs. Monte Carlo")
    print("=" * 50)
    print(f"S={S}, K={K}, T={T}, r={r}, sigma={sigma}, type={option_type}")
    print()

    bs_price = black_scholes_price(S, K, T, r, sigma, option_type)
    print(f"Black-Scholes price:  {bs_price:.4f}")

    mc_result = monte_carlo_price(S, K, T, r, sigma, option_type, num_simulations=100_000, seed=42)
    print(f"Monte Carlo price:    {mc_result['price']:.4f}  (+/- {mc_result['standard_error']:.4f})")

    difference = abs(bs_price - mc_result["price"])
    print(f"Absolute difference:  {difference:.4f}")
    print()

    print("Greeks (Black-Scholes):")
    for name, value in greeks(S, K, T, r, sigma, option_type).items():
        print(f"  {name.capitalize():<6}: {value:.4f}")
    print()

    print("Generating charts...")
    plot_payoff(K, option_type=option_type, save_path="payoff.png")
    plot_simulated_paths(S, T, r, sigma, num_paths=30, seed=42, save_path="paths.png")
    plot_convergence(S, K, T, r, sigma, option_type=option_type, save_path="convergence.png")
    print("Charts saved: payoff.png, paths.png, convergence.png")


if __name__ == "__main__":
    main()