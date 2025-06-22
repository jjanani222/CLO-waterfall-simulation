# CLO-waterfall-simulation
This project simulates the interest waterfall and compliance mechanics of a simplified Collateralized Loan Obligation (CLO). The model illustrates how Overcollateralization (OC) test results impact cash flow distributions to Senior, Mezzanine, and Equity tranches.

## Features

- Tranche-level interest allocation based on payment priority
- Overcollateralization (OC) test logic with configurable threshold
- Two scenarios modeled:
  - Base Case: OC test passes
  - Stress Case: OC test fails due to reduced collateral
- Visualization of results using `matplotlib`
- Human-readable and well-documented Python implementation
- Includes structured project analysis in LaTeX (with optional compiled PDF)
