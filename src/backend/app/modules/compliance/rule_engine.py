from typing import Optional
from .city_db import CityDatabase


class RuleEngine:
    def __init__(self):
        self.db = CityDatabase()

    def check_feasibility(self, city: str, area_sqft: float, manual_fsi: Optional[float] = None):
        rules = self.db.get_city_rules(city)
        db_fsi = rules.get("fsi", 1.0)

        if manual_fsi is not None:
            fsi = manual_fsi
            fsi_source = "Manual Override"
        else:
            fsi = db_fsi
            fsi_source = "City Database"

        min_sqft = rules.get("min_sqft", 0)
        is_legal = area_sqft >= min_sqft
        max_buildable = area_sqft * fsi

        breakdown = []
        if is_legal:
            breakdown.append(f"✅ Plot Area ({area_sqft} sq.ft) > Min Requirement ({min_sqft} sq.ft)")
        else:
            breakdown.append(f"❌ Plot Area ({area_sqft} sq.ft) < Min Requirement ({min_sqft} sq.ft)")

        breakdown.append(f"ℹ️ FSI Applied: {round(fsi, 2)}x ({fsi_source})")
        breakdown.append(f"➡️ Max Buildable Area: {round(max_buildable, 2)} sq.ft")

        return {
            "city": city,
            "is_buildable": is_legal,
            "max_buildable_area": round(max_buildable, 2),
            "allowed_floors": rules.get("max_floors", 2),
            "compliance_breakdown": breakdown,
        }
