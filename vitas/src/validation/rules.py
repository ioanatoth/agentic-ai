import pandas as pd
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


class LivestockClassifier:
    """
    Implementează regulile de business și validarea conform Specie_Rasa.csv.
    """

    def __init__(self, reference_csv_path='Specie_Rasa.csv'):
        # Încărcăm nomenclatorul de specii și rase
        try:
            self.ref_data = pd.read_csv(reference_csv_path)
            self.valid_species = self.ref_data['Specia'].unique().tolist()
        except Exception as e:
            print(f"Eroare la încărcarea nomenclatorului: {e}")
            self.ref_data = pd.DataFrame()
            self.valid_species = []

    def validate_species_race(self, extracted_species, extracted_race):
        """
        Verifică dacă combinația Specie-Rasă este validă (Cerința 6.7)[cite: 1].
        """
        if self.ref_data.empty:
            return True, extracted_species  # Skip dacă nu avem date

        # Normalizare pentru comparare
        s_norm = str(extracted_species).strip()
        r_norm = str(extracted_race).strip()

        # Verificăm dacă specia există
        match = self.ref_data[self.ref_data['Specia'].str.contains(s_norm, case=False, na=False)]

        if match.empty:
            return False, f"Specie Necunoscută: {extracted_species}"

        # Verificăm dacă rasa aparține speciei respective
        race_match = match[match['Rasa'].str.contains(r_norm, case=False, na=False)]
        if race_match.empty:
            return False, f"Rasă neconformă pentru {extracted_species}: {extracted_race}"

        return True, "Valid"

    def calculate_age_months(self, birth_date_str):
        """Calculează vârsta în luni (Cerința 6.6)[cite: 1]."""
        try:
            # Curățare format dată
            clean_date = str(birth_date_str).replace('.', '-').replace('/', '-')
            birth_date = datetime.strptime(clean_date, "%Y-%m-%d")
            diff = relativedelta(datetime.now(), birth_date)
            return diff.years * 12 + diff.months
        except:
            return None

    def get_category(self, species, birth_date_str, sex):
        """Categorisire bazată pe regulile de business (Capitolul 4.7)[cite: 1]."""
        age = self.calculate_age_months(birth_date_str)
        if age is None: return "Dată Invalidă"

        s = str(species).lower()
        if "bov" in s:
            if age < 12: return "Viței"
            if sex == "F": return "Juninci" if age <= 24 else "Bovine productive"
            return "Masculi"
        elif "ovin" in s:
            if age < 6: return "Miei"
            if sex == "F": return "Oi productive" if age > 18 else "Oi neintrate în producție"
            return "Berbeci"

        return "Alte categorii"
