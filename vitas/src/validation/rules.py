from datetime import datetime
from dateutil.relativedelta import relativedelta

class LivestockClassifier:
    """
    Implementează regulile de business pentru clasificarea animalelor (Capitolul 4.7).
    """

    @staticmethod
    def calculate_age_months(birth_date_str):
        """Calculează vârsta în luni față de data curentă (Cerința 6.6)."""
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            now = datetime.now()
            diff = relativedelta(now, birth_date)
            return diff.years * 12 + diff.months
        except:
            return None

    def classify_bovine(self, age_months, sex):
        """Reguli Bovine (Capitolul 4.7)"""
        if age_months < 12:
            return "Viței"
        if sex == "F" and 12 <= age_months <= 24:
            return "Juninci"
        if sex == "F" and age_months > 24:
            return "Bovine productive"
        if sex == "M" and age_months > 12:
            return "Masculi"
        return "Bovine (Alte categorii)"

    def classify_ovine(self, age_months, sex):
        """Reguli Ovine (Capitolul 4.7)"""
        if age_months < 6:
            return "Miei"
        if sex == "M" and 6 <= age_months <= 12:
            return "Tineret mascul"
        if sex == "F" and 6 <= age_months <= 18:
            return "Oi neintrate în producție"
        if sex == "F" and age_months > 18:
            return "Oi productive"
        if sex == "M" and age_months > 12:
            return "Berbeci"
        return "Ovine (Alte categorii)"

    def get_category(self, species, birth_date_str, sex):
        """Determină categoria finală bazată pe specie, sex și vârstă (Cerința 6.6)."""
        age_months = self.calculate_age_months(birth_date_str)
        if age_months is None:
            return "Dată invalidă"

        s = species.lower()
        if "bov" in s:
            return self.classify_bovine(age_months, sex)
        elif "ovin" in s:
            return self.classify_ovine(age_months, sex)
        # Se pot adăuga aici regulile pentru Caprine și Suine similar
        return f"{species} (Neclasificat)"