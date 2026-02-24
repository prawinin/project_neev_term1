from typing import Optional
from .scraper import MaterialScraper


class CostEstimator:
    def __init__(self):
        self.scraper = MaterialScraper()
        self.city_indices = {
            "Bangalore": 1.0,
            "Delhi": 1.12,
            "Pune": 0.96,
            "Bokaro": 0.82,
        }

    def calculate(self, area_sqft: float, city: str, manual_floors: Optional[int] = None):
        rates = self.scraper.get_latest_prices()
        city_factor = self.city_indices.get(city, 1.0)

        if manual_floors is not None:
            floors = manual_floors
        else:
            floors = 2 if area_sqft < 1200 else 3

        quantities = {
            "Cement (Bags)": int(area_sqft * floors * 0.45),
            "Steel (Kg)": int(area_sqft * floors * 4.0),
            "Sand (CFT)": int(area_sqft * floors * 1.8),
            "Bricks (Nos)": int(area_sqft * floors * 22),
            "Paint (Liters)": int(area_sqft * floors * 0.15),
        }

        material_cost = 0.0
        for item, qty in quantities.items():
            local_price = rates.get(item, 0) * city_factor
            material_cost += local_price * qty

        local_labor_rate = 400 * city_factor
        labor_cost = (area_sqft * floors) * local_labor_rate
        total_cost = material_cost + labor_cost

        return {
            "total_cost": round(total_cost, 2),
            "material_cost": round(material_cost, 2),
            "labor_cost": round(labor_cost, 2),
            "bill_of_materials": quantities,
            "unit_rates": rates,
            "city_factor_applied": city_factor,
            "floors_calculated": floors,
        }
