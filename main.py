"""
Solar Power Calculator
Author: Roshan Padit
GitHub: github.com/roshanpadit

This script estimates solar energy generation, savings
and payback period for a small rooftop solar system.
"""

from config import AVERAGE_SOLAR_IRRADIANCE_KWH_M2_DAY, DEFAULT_ELECTRICITY_RATE


def get_float_input(prompt, default=None):
    """Safely get a float input from user."""
    while True:
        user_input = input(prompt).strip()
        if user_input == "" and default is not None:
            return default
        try:
            value = float(user_input)
            if value < 0:
                print("Please enter a non-negative value.")
                continue
            return value
        except ValueError:
            print("Invalid number, try again.")


def calculate_solar_output(panel_wattage, number_of_panels,
                           system_efficiency, irradiance_kwh_m2_day):
    """
    Returns a dict with daily & monthly energy output (kWh).
    """
    total_system_kw = (panel_wattage * number_of_panels) / 1000.0
    efficiency_factor = system_efficiency / 100.0

    daily_energy_kwh = total_system_kw * irradiance_kwh_m2_day * efficiency_factor
    monthly_energy_kwh = daily_energy_kwh * 30  # approx

    return {
        "system_kw": total_system_kw,
        "daily_kwh": daily_energy_kwh,
        "monthly_kwh": monthly_energy_kwh,
    }


def estimate_savings(monthly_kwh, electricity_rate):
    return monthly_kwh * electricity_rate


def estimate_payback(total_system_cost, monthly_savings):
    if monthly_savings <= 0:
        return None
    return total_system_cost / (monthly_savings * 12)


def pretty_print_results(results):
    print("\n========== Solar System Summary ==========")
    print("Total system size        : {:.2f} kW".format(results["system_kw"]))
    print("Estimated daily energy   : {:.2f} kWh/day".format(results["daily_kwh"]))
    print("Estimated monthly energy : {:.2f} kWh/month".format(results["monthly_kwh"]))
    print("Electricity rate         : ₹{:.2f} per kWh".format(results["electricity_rate"]))
    print("Estimated monthly saving : ₹{:.2f} / month".format(results["monthly_savings"]))

    if results["payback_years"] is not None:
        print("Simple payback period    : {:.1f} years".format(results["payback_years"]))
    else:
        print("Simple payback period    : Not applicable (zero savings).")
    print("==========================================\n")


def main():
    print("==========================================")
    print("        SOLAR POWER CALCULATOR 🌞        ")
    print("==========================================\n")

    print("Enter basic system details:\n")

    panel_wattage = get_float_input("Panel wattage (W) [e.g. 330]: ")
    number_of_panels = int(get_float_input("Number of panels [e.g. 6]: "))
    system_efficiency = get_float_input(
        "System efficiency (%) [typical 75–85, default 80]: ", default=80.0
    )

    print("\nSite & tariff details:\n")

    irradiance = get_float_input(
        "Average solar irradiance (kWh/m²/day) "
        "[default for many Indian cities ≈ {}]: ".format(
            AVERAGE_SOLAR_IRRADIANCE_KWH_M2_DAY
        ),
        default=AVERAGE_SOLAR_IRRADIANCE_KWH_M2_DAY,
    )

    electricity_rate = get_float_input(
        "Electricity rate (₹/kWh) [default {}]: ".format(DEFAULT_ELECTRICITY_RATE),
        default=DEFAULT_ELECTRICITY_RATE,
    )

    total_system_cost = get_float_input(
        "Total system cost (₹) [include panels + inverter + installation]: "
    )

    energy = calculate_solar_output(
        panel_wattage=panel_wattage,
        number_of_panels=number_of_panels,
        system_efficiency=system_efficiency,
        irradiance_kwh_m2_day=irradiance,
    )

    monthly_savings = estimate_savings(energy["monthly_kwh"], electricity_rate)
    payback_years = estimate_payback(total_system_cost, monthly_savings)

    results = {
        "system_kw": energy["system_kw"],
        "daily_kwh": energy["daily_kwh"],
        "monthly_kwh": energy["monthly_kwh"],
        "electricity_rate": electricity_rate,
        "monthly_savings": monthly_savings,
        "payback_years": payback_years,
    }

    pretty_print_results(results)

    print("Note:")
    print("- This is a simplified estimation.")
    print("- Actual values depend on shading, orientation, temperature, etc.")
    print("\nThank you for using the Solar Power Calculator ☀️")


if __name__ == "__main__":
    main()
