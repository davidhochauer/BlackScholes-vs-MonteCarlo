from flask import Flask, render_template, request

from black_scholes import black_scholes_price, greeks
from monte_carlo import monte_carlo_price

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    form_values = {"S": 100, "K": 100, "T": 1, "r": 0.05, "sigma": 0.2, "option_type": "call"}

    if request.method == "POST":
        # Read and convert form inputs; fall back to an error message on bad input
        try:
            S = float(request.form.get("S"))
            K = float(request.form.get("K"))
            T = float(request.form.get("T"))
            r = float(request.form.get("r"))
            sigma = float(request.form.get("sigma"))
            option_type = request.form.get("option_type")

            form_values = {"S": S, "K": K, "T": T, "r": r, "sigma": sigma, "option_type": option_type}

            bs_price = black_scholes_price(S, K, T, r, sigma, option_type)
            mc = monte_carlo_price(S, K, T, r, sigma, option_type, num_simulations=50_000, seed=42)
            g = greeks(S, K, T, r, sigma, option_type)

            results = {
                "bs_price": bs_price,
                "mc_price": mc["price"],
                "mc_error": mc["standard_error"],
                "greeks": g,
            }
        except (ValueError, TypeError):
            results = {"error": "Please enter valid numbers for all fields."}

    return render_template("index.html", results=results, values=form_values)


if __name__ == "__main__":
    app.run(debug=True)