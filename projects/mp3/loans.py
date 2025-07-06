race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "5": "White",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander"
}

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
    def __repr__(self):
        return f"Applicant({repr(self.age)}, {sorted(self.race)})"
    def lower_age(self):
        cleaned = self.age.replace('<', '').replace('>', '')
        parts = cleaned.split('-')
        return int(parts[0])
    def __lt__(self, other):
        return self.lower_age()<other.lower_age()
class Loan:
    def __init__(self, values):
        self.loan_amount = self.float_extract(values["loan_amount"])
        self.property_value = self.float_extract(values["property_value"])
        self.interest_rate = self.float_extract(values["interest_rate"])
        
        self.applicants = []
        applicant_age = values["applicant_age"]
        applicant_races = [values[f"applicant_race-{i}"] for i in range(1,6) if values[f"applicant_race-{i}"]]
        self.applicants.append(Applicant(applicant_age, applicant_races))
        
        if values["co-applicant_age"] != "9999":
            co_age = values["co-applicant_age"]
            co_races = [values[f"co-applicant_race-{i}"] for i in range(1,6) if values[f"co-applicant_race-{i}"]]
            self.applicants.append(Applicant(co_age, co_races))

    def float_extract(self, string):
        if string == "NA" or string == "Exempt":
            return -1
        else:
            return float(string)

    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.loan_amount} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return self.__str__()

    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate >= 0 and self.loan_amount >= 0
        amt = self.loan_amount
        rate = self.interest_rate / 100
        
        while amt > 0:
            yield amt
            amt = amt + amt * rate - yearly_payment
            
import json, zipfile, csv
from io import TextIOWrapper

# Load banks.json once
# at top of loans.py
with open("banks.json") as f:
    BANK_DATA = json.load(f)
NAME_TO_LEI = {entry["name"].lower(): entry["lei"] for entry in BANK_DATA}
class Bank:
    def __init__(self, name):
        lower_name = name.lower()
        if lower_name not in NAME_TO_LEI:
            raise ValueError(f"{name} not found in banks.json")
        
        self.name = name
        self.lei = NAME_TO_LEI[lower_name]
        self.loan_list = []

        with zipfile.ZipFile("wi.zip") as zf:
            with zf.open("wi.csv") as file:
                reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))
                for row in reader:
                    if row["lei"] == self.lei:
                        self.loan_list.append(Loan(row))
    
    def __len__(self):
        return len(self.loan_list)

    def __getitem__(self, index):
        return self.loan_list[index]
class BST:
    def __init__(self):
        self.root = None
     
    def __getitem__(self, key):
        if self.root is None:
            raise KeyError(f"{key} not found in empty BST")
        return self.root.lookup(key)