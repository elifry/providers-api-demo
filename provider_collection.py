import json
import heapq
from datetime import date

# Calculate the age from a birth date
def calculate_age_in_years(birth_date):
    birth_date = date.fromisoformat(birth_date)
    today = date.today()
    # Calculate the age by subtracting the year, month and day
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

class Provider:
    """A class to represent a provider of some service.

    Attributes:
        id (int): The unique identifier of the provider.
        first_name (str): The first name of the provider.
        last_name (str): The last name of the provider.
        sex (str): The sex of the provider.
        birth_date (str): The birth date of the provider in ISO format (YYYY-MM-DD).
        rating (float): The rating of the provider from 0 to 5.
        primary_skills (list): The list of primary skills of the provider.
        secondary_skill (list): The list of secondary skills of the provider.
        company (str): The company name of the provider.
        active (bool): The active status of the provider (True or False).
        country (str): The country name of the provider.
        language (str): The language name of the provider.
        age (int): Internal attribute to store the calculated age from the birth date attribute.

    Methods:
        check_types(data)
            Class method to check the types of each key and value in a data dictionary and return it.
            Extra type safety - we already init with individual parameters so it will be typesafe,
            but explicitly showing which type is expected is a better approach. Like we discussed
            in the interview, python needs more lines to be typesafe, but it's worth it.

        __init__(data)
            Instance method to initialize a provider object with a data dictionary.
            Initialize as individual parameters - more rigid but typesafe

        __lt__(other)
            Defines a comparison method for sorting providers by rating and popularity.
            Higher rating and lower popularity are more preferred.

        __dict__
            Property method to return a dictionary representation of the provider without the age attribute.
    """

    @classmethod
    def check_types(cls, data):
        expected_types = {
            "id": int,
            "first_name": str,
            "last_name": str,
            "sex": str,
            "birth_date": str,
            "rating": float,
            "primary_skills": list,
            "secondary_skill": list,
            "company": str,
            "active": bool,
            "country": str,
            "language": str
        }

        # Loop through the keys and values in the data dictionary and compare them with the expected types
        for key, value in data.items():
            # If the key is not in the expected types, raise an error
            if key not in expected_types:
                raise TypeError(f"Unexpected key: {key}")
            
            # If the value is not of the expected type, raise an error
            if not isinstance(value, expected_types[key]):
                raise TypeError(f"Expected type {expected_types[key]} for key {key}, got {type(value)} instead")
        
        # If no errors are raised, return the data dictionary
        return data

    def __init__(self, data):
        # Check the types
        data = self.check_types(data)

        # Initialize as individual parameters - more rigid but typesafe
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.sex = data["sex"]
        self.birth_date = data["birth_date"]
        self.rating = data["rating"]
        self.primary_skills = data["primary_skills"]
        self.secondary_skill = data["secondary_skill"]
        self.company = data["company"]
        self.active = data["active"]
        self.country = data["country"]
        self.language = data["language"]

        # Calculate the age from the birth date and assign it as an internal attribute
        self.age = calculate_age_in_years(self.birth_date)

    def __lt__(self, other):
        return (self.rating, -self.popularity) > (other.rating, -other.popularity)

    @property
    def __dict__(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "sex": self.sex,
            "birth_date": self.birth_date,
            "rating": self.rating,
            "primary_skills": self.primary_skills,
            "secondary_skill": self.secondary_skill,
            "company": self.company,
            "active": self.active,
            "country": self.country,
            "language": self.language
        }

def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class ProviderCollection:
    """A class to represent a collection of providers.

    Attributes:
        providers (list): The list of providers in the collection.

    Methods:
        __init__(filename)
            Instance method to initialize a provider collection object with a json filename.
            Loads all providers from json file into memory.

        filter_by_active(active)
            Instance method to filter the providers by their active attribute and return a list.

        filter_by_traits(traits)
            Instance method to filter the providers by their traits and return a list.

        sort_by_rating_and_popularity(providers)
            Instance method to sort a list of providers by their rating and popularity attributes and return a list.
            Higher rating = more preferred
            Lower popularity = more preferred
    """

    def __init__(self, filename):
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
        self.providers = [Provider(d) for d in data]

        # Create a dictionary to store the popularity of each provider
        self.popularity = {}

    def filter_by_active(self, active):
        return [p for p in self.providers if p.active == active]

    def filter_by_traits(self, traits, providers):
        filtered_providers = []

        # Loop through the providers in the collection
        for provider in providers:
            # Initialize a flag to indicate if the provider matches the traits
            match = True

            # Loop through the keys and values in the traits dictionary
            for key, value_list in traits.items():
                # Lowercase the key and the value
                key = key.lower()
                value_list = [value.lower() for value in value_list]

                # Get the corresponding attribute of the provider and lowercase it if it is a string or a list of strings
                attr = getattr(provider, key)
                if isinstance(attr, str):
                    attr = attr.lower()
                elif isinstance(attr, list) and all(isinstance(x, str) for x in attr):
                    attr = [x.lower() for x in attr]

                # If the key is "age", calculate the age from the birth date attribute and compare it with the value range or single value
                if key == "age":
                    age = calculate_age_in_years(provider.birth_date)
                    # Check if there is a "-" in the value list
                    if "-" in value_list[0]:
                        # If yes, split by "-" and convert to integers
                        min_age, max_age = map(int, value_list[0].split("-"))
                        # Check if the age is within the range
                        if not (min_age <= age <= max_age):
                            match = False
                            break
                    else:
                        # If no, assume there is only one value and convert to integer
                        target_age = int(value_list[0])
                        # Check if the age is equal to the target age
                        if age != target_age:
                            match = False
                            break
                        
                # If the attribute is a list of strings, check if it contains any of the values
                elif isinstance(attr, list):
                    # Use a list comprehension to filter by value_list
                    filtered_attr = [x for x in attr if x in value_list]
                    # Check if filtered_attr is empty or not
                    if not filtered_attr:
                        match = False
                        break
                
                # If the value list and the attribute are numeric, convert them to numbers
                elif all(is_numeric(x) for x in value_list) and is_numeric(attr):
                    value_list = [float(x) for x in value_list]
                    attr = float(attr)

                # If the attribute is not in the value list, set the flag to False and break the loop
                elif attr not in value_list:
                    match = False
                    break
            
            # If the flag is True, append the provider to the filtered list
            if match:
                filtered_providers.append(provider)
        
        # Return the filtered list
        return filtered_providers

    def sort_by_rating_and_popularity(self, providers):
        # Uses a priority queue
        queue = []
        for provider in providers:
            # Update the popularity of each provider and push them to the queue
            self.popularity[provider.id] = self.popularity.get(provider.id, 0) + 1
            provider.popularity = self.popularity[provider.id]
            heapq.heappush(queue, provider)

        # Pop the providers from the queue in sorted order and convert them to dictionaries
        result = []
        while queue:
            provider = heapq.heappop(queue)
            result.append(provider.__dict__)
        
        return result
