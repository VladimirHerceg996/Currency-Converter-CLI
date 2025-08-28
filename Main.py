import requests
import argparse

# === CONFIG ===
API_KEY = "69DbkeIuRoxCL3YYi0r6lm8AHpYhuwW8"  
API_URL = "https://api.apilayer.com/exchangerates_data/convert"

HEADERS = {"apikey": API_KEY}

# Popularne konverzije za brzi meni
POPULAR = [
    ("EUR", "USD"),
    ("USD", "RSD"),
    ("EUR", "GBP"),
    ("CHF", "EUR"),
    ("BTC", "USD"),
]

# === ARGPARSE (za --debug flag) ===
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()
DEBUG = args.debug


def convert_currency(base: str, target: str, amount: float) -> float:
    """Convert amount from base to target currency."""
    params = {"from": base, "to": target, "amount": amount}
    response = requests.get(API_URL, headers=HEADERS, params=params)

    if DEBUG:
        print("DEBUG status:", response.status_code)
        print("DEBUG response:", response.text)

    if response.status_code != 200:
        raise Exception("API request failed!")

    data = response.json()
    if not data.get("success"):
        raise Exception(f"API error: {data.get('error', {}).get('info', 'Unknown error')}")

    return data["result"]


def show_menu():
    """Prikazuje popularne konverzije."""
    print("\n📊 Popular conversions:")
    for i, (b, t) in enumerate(POPULAR, 1):
        print(f" {i}. {b} -> {t}")
    print(" 0. Custom conversion")


def main():
    print("=== Currency Converter CLI ===")
    print("💡 Example currencies: EUR, USD, RSD, GBP, CHF, JPY, AUD, CAD, CNY, BTC")

    show_menu()
    choice = input("\nChoose option: ").strip()

    try:
        if choice.isdigit() and int(choice) in range(1, len(POPULAR) + 1):
            base, target = POPULAR[int(choice) - 1]
            amount = float(input(f"Enter amount in {base}: "))
        else:
            base = input("Enter base currency: ").strip().upper()
            target = input("Enter target currency: ").strip().upper()
            amount = float(input("Enter amount: "))

        result = convert_currency(base, target, amount)
        print(f"\n✅ Result: {amount:.2f} {base} = {result:.2f} {target}")

    except ValueError:
        print("❌ Invalid amount! Please enter a number.")
    except Exception as e:
        print("❌ Error:", e)


if __name__ == "__main__":
    main()
