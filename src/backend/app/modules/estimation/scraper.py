from pathlib import Path
import pandas as pd


class MaterialScraper:
    def get_latest_prices(self):
        csv_path = Path(__file__).resolve().parents[5] / "data" / "material_prices" / "market_rates_2025.csv"

        try:
            df = pd.read_csv(csv_path)
            return dict(zip(df["material"], df["price_inr"]))
        except Exception:
            return {
                "Cement (Bags)": 420,
                "Steel (Kg)": 78,
                "Sand (CFT)": 55,
                "Bricks (Nos)": 8,
                "Paint (Liters)": 320,
            }
