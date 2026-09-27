# Black-Scholes vs. Monte Carlo: An Options Pricing Toolkit
#### Video Demo: <URL HERE>
#### Description:

This project implements and compares two fundamental approaches to pricing
European options: the closed-form Black-Scholes formula and a
Monte Carlo simulation. The goal was not just to produce a working
tool, but to be able to demonstrate why two
completely different mathematical approaches to the same problem converge
on the same answer, and where each one's strengths and weaknesses lie.

An option gives its holder the right, but not the obligation, to buy
(a call) or sell (a put) an underlying stock at a fixed price (the strike)
by a certain date. Pricing that right correctly is one of the foundational
problems in quantitative finance, and it's directly relevant to my planned
studies in Volkswirtschaftslehre and, later, Quantitative Economics and
Finance, as of September 27, 2026.

## What the project does
 
Given five inputs — the current stock price, the strike price, the time
to expiration, the risk-free interest rate, and the volatility of the
underlying stock — the toolkit:
 
1. Computes the exact option price using the Black-Scholes formula, along
   with the associated "Greeks" (Delta, Gamma, Vega, Theta, Rho), which
   measure how sensitive the price is to changes in each input.
2. Estimates the same price by simulating tens of thousands of random
   future stock price paths (under the assumption of geometric Brownian
   motion), computing the option's payoff along each simulated path, and
   averaging the discounted results.
3. Visualizes the results: a payoff diagram, a handful of simulated price
   paths, and — most importantly — a convergence chart that shows how the
   Monte Carlo estimate tightens around the exact Black-Scholes price as
   the number of simulations grows.
4. Exposes all of the above through a small Flask web app, so the same
   calculations can be run interactively in a browser instead of only
   from the command line.
## Files
 
- **`black_scholes.py`** — Implements the closed-form Black-Scholes
  pricing formula for European calls and puts, plus the five main Greeks.
  This is the analytical "ground truth" the rest of the project is
  checked against.
- **`monte_carlo.py`** — Implements `simulate_paths()`, which generates
  many random stock price trajectories under geometric Brownian motion,
  and `monte_carlo_price()`, which uses those simulated paths to estimate
  an option's price and reports the estimate's standard error (a measure
  of how much the estimate would vary if the simulation were rerun).
- **`visualize.py`** — Three plotting functions built on top of the two
  modules above: a payoff diagram, a chart of simulated price paths over
  time, and the convergence plot comparing Monte Carlo estimates (at
  increasing simulation counts) against the Black-Scholes price.
- **`main.py`** — Ties everything together: prices an example option both
  ways, prints a side-by-side comparison and the Greeks, and generates all
  three charts as PNG files.
- **`webapp.py`** and **`templates/index.html`** — A small Flask
  application that wraps the same `black_scholes.py` and `monte_carlo.py`
  functions in a browser-based form: enter the five inputs, get the
  Black-Scholes price, the Monte Carlo estimate, and the Greeks back
  instantly. No pricing logic is duplicated here — the web app only
  handles the form and the display.
- **`requirements.txt`** — Lists the dependencies (`numpy`, `scipy`,
  `matplotlib`, `flask`) needed to run the project.

## Running the project
 
```
pip install -r requirements.txt
python main.py
```
 
This prints the Black-Scholes price, the Monte Carlo estimate, and the
Greeks for an example call option, and saves `payoff.png`, `paths.png`,
and `convergence.png` in the project folder.
 
To use the interactive web version instead:
 
```
python webapp.py
```
 
Then open the URL printed in the terminal (typically
`http://127.0.0.1:5000`) in a browser.