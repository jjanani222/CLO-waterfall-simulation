import pandas as pd
import matplotlib.pyplot as plt


def run_clo_simulation(collateral_amount, label):
    # Define CLO structure
    df = pd.DataFrame({
        "Tranche": ["Senior", "Mezzanine", "Equity"],
        "Balance (£)": [50_000_000, 30_000_000, 20_000_000],
        "Rate": [0.05, 0.07, 0.00],
        "Priority": [1, 2, 3]
    })

    total_interest_income = 8_000_000
    senior_balance = df.loc[df["Tranche"] == "Senior", "Balance (£)"].values[0]
    oc_ratio = collateral_amount / senior_balance
    oc_pass = oc_ratio >= 1.25

    # Interest due
    df["Interest Due (£)"] = df["Balance (£)"] * df["Rate"]
    df = df.sort_values("Priority").reset_index(drop=True)

    # Waterfall allocation
    remaining_cash = total_interest_income
    paid = []

    for _, row in df.iterrows():
        if not oc_pass and row["Tranche"] != "Senior":
            payment = 0
        else:
            payment = min(row["Interest Due (£)"], remaining_cash)
        paid.append(payment)
        remaining_cash -= payment

    df["Paid (£)"] = paid
    df["Shortfall (£)"] = df["Interest Due (£)"] - df["Paid (£)"]
    df["Remaining Cash (£)"] = total_interest_income - df["Paid (£)"].cumsum()
    df["Scenario"] = label

    print(f"\n{label} ")
    print(f"OC Ratio: {oc_ratio:.2f}x → {'PASS' if oc_pass else 'FAIL'}")
    print(df[["Tranche", "Interest Due (£)", "Paid (£)", "Shortfall (£)", "Remaining Cash (£)"]])
    return df


df_base = run_clo_simulation(collateral_amount=100_000_000, label="Base Case (OC PASS)")
df_stress = run_clo_simulation(collateral_amount=55_000_000, label="Stress Case (OC FAIL)")

df_combined = pd.concat([df_base, df_stress], ignore_index=True)

fig, ax = plt.subplots(figsize=(9, 5))
for scenario in df_combined["Scenario"].unique():
    subset = df_combined[df_combined["Scenario"] == scenario]
    ax.bar(subset["Tranche"] + f" ({scenario.split()[0]})",
           subset["Paid (£)"], label=f"{scenario} - Paid")

plt.title("CLO Waterfall – Base vs Stress Case")
plt.ylabel("Amount Paid (£)")
plt.xticks(rotation=30)
plt.legend()
plt.tight_layout()
plt.show()
