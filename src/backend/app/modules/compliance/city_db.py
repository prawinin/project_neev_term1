class CityDatabase:
    def __init__(self):
        self.rules = {
            "Bangalore": {"min_sqft": 600, "fsi": 1.75, "max_floors": 3},
            "Delhi": {"min_sqft": 500, "fsi": 2.0, "max_floors": 4},
            "Pune": {"min_sqft": 550, "fsi": 1.5, "max_floors": 3},
            "Bokaro": {"min_sqft": 450, "fsi": 1.2, "max_floors": 2},
        }

    def get_city_rules(self, city: str):
        return self.rules.get(city, {"min_sqft": 500, "fsi": 1.5, "max_floors": 2})
