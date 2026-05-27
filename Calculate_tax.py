import math

def calculate_new_regime_tax(gross_salary: float, new_regime_deductions: float = 0.0) -> dict:
    """
    Calculates tax under the New Tax Regime (Budget 2025/2026 rules).
    Allows an automatic ₹75,000 standard deduction for salaried individuals.
    Accepts allowed custom deductions (e.g., Section 80CCD(2) NPS, 80CCH).
    """
    # 1. Apply Automatic Standard Deduction for New Regime
    standard_deduction = 75000.0
    
    # 2. Compute Net Taxable Income with New Regime Deductions
    net_income = max(0.0, gross_salary - standard_deduction - new_regime_deductions)
    
    # 3. New Tax Regime Progressive Slabs (Budget 2025 rules)
    slabs = [
        (400000, 0.00),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
        (float('inf'), 0.30)
    ]
    
    base_tax = 0.0
    previous_limit = 0.0
    
    for limit, rate in slabs:
        if net_income > previous_limit:
            taxable_in_slab = min(net_income, limit) - previous_limit
            base_tax += taxable_in_slab * rate
            previous_limit = limit
        else:
            break
            
    # 4. Section 87A Rebate (Full tax rebate up to ₹12,00,000 net taxable income)
    rebate = 0.0
    if net_income <= 1200000.0:
        rebate = min(base_tax, 60000.0)
        
    tax_after_rebate = max(0.0, base_tax - rebate)
    
    # 5. Add 4% Health & Education Cess
    cess = tax_after_rebate * 0.04
    total_tax = tax_after_rebate + cess
    
    return {
        "regime": "New Tax Regime",
        "gross_salary": gross_salary,
        "standard_deduction": standard_deduction,
        "custom_deductions": new_regime_deductions,
        "net_taxable_income": net_income,
        "base_tax": base_tax,
        "rebate_87a": rebate,
        "cess": cess,
        "total_tax_payable": round(total_tax)
    }

def calculate_old_regime_tax(gross_salary: float, old_regime_deductions: float = 0.0) -> dict:
    """
    Calculates tax under the Old Tax Regime.
    Allows an automatic ₹50,000 standard deduction + itemized custom deductions.
    """
    # 1. Apply Automatic Standard Deduction for Old Regime
    standard_deduction = 50000.0
    
    # 2. Compute Net Taxable Income with Old Regime Deductions (80C, 80D, HRA, etc.)
    net_income = max(0.0, gross_salary - standard_deduction - old_regime_deductions)
    
    # 3. Old Tax Regime Progressive Slabs
    slabs = [
        (250000, 0.00),
        (500000, 0.05),
        (1000000, 0.20),
        (float('inf'), 0.30)
    ]
    
    base_tax = 0.0
    previous_limit = 0.0
    
    for limit, rate in slabs:
        if net_income > previous_limit:
            taxable_in_slab = min(net_income, limit) - previous_limit
            base_tax += taxable_in_slab * rate
            previous_limit = limit
        else:
            break
            
    # 4. Section 87A Rebate (Tax rebate up to ₹5,00,000 net taxable income)
    rebate = 0.0
    if net_income <= 500000.0:
        rebate = min(base_tax, 12500.0)
        
    tax_after_rebate = max(0.0, base_tax - rebate)
    
    # 5. Add 4% Health & Education Cess
    cess = tax_after_rebate * 0.04
    total_tax = tax_after_rebate + cess
    
    return {
        "regime": "Old Tax Regime",
        "gross_salary": gross_salary,
        "standard_deduction": standard_deduction,
        "custom_deductions": old_regime_deductions,
        "net_taxable_income": net_income,
        "base_tax": base_tax,
        "rebate_87a": rebate,
        "cess": cess,
        "total_tax_payable": round(total_tax)
    }

def print_tax_comparison(gross_income: float, deductions_old: float, deductions_new: float):
    """
    Helper function to execute calculations and output an easy-to-read comparison.
    """
    new_regime_res = calculate_new_regime_tax(gross_income, new_regime_deductions=deductions_new)
    old_regime_res = calculate_old_regime_tax(gross_income, old_regime_deductions=deductions_old)
    
    print("=" * 50)
    print(f" TAX COMPARISON FOR GROSS INCOME: ₹{gross_income:,.2f}")
    print("=" * 50)
    
    for res in [new_regime_res, old_regime_res]:
        print(f"\n📌 {res['regime']}:")
        print(f"  Gross Salary          : ₹{res['gross_salary']:,.2f}")
        print(f"  (-) Standard Deduction: ₹{res['standard_deduction']:,.2f}")
        print(f"  (-) Custom Deductions : ₹{res['custom_deductions']:,.2f}")
        print(f"  Net Taxable Income    : ₹{res['net_taxable_income']:,.2f}")
        print(f"  Base Slab Tax         : ₹{res['base_tax']:,.2f}")
        print(f"  (-) Sec 87A Rebate    : ₹{res['rebate_87a']:,.2f}")
        print(f"  (+) Education Cess    : ₹{res['cess']:,.2f}")
        print(f"  👉 FINAL PAYABLE TAX  : ₹{res['total_tax_payable']:,}")
    
    print("-" * 50)
    diff = old_regime_res['total_tax_payable'] - new_regime_res['total_tax_payable']
    if diff > 0:
        print(f"✅ New Regime saves you ₹{diff:,} compared to the Old Regime.")
    elif diff < 0:
        print(f"✅ Old Regime saves you ₹{abs(diff):,} compared to the New Regime.")
    else:
        print("🤝 Both regimes result in the exact same tax liability.")
    print("=" * 50)

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Test Data Setup
    my_gross_salary = 2138292
    
    # Custom deductions unique to each regime configuration
    my_old_regime_deductions = 0  # e.g., 1.5L (80C) + 50k (80D) + 50k (NPS)
    my_new_regime_deductions = 80112   # e.g., 50k Corporate NPS Contribution under Sec 80CCD(2)
    
    # Run comparative report
    print_tax_comparison(my_gross_salary, my_old_regime_deductions, my_new_regime_deductions)
