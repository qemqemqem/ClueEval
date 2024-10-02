import random
from dataclasses import dataclass

@dataclass
class Story:
    diversity_prompt: str
    random_crimes: list[str]
    random_places: list[str]
    random_people: list[str]

def get_random_details() -> Story:
    # This is for diversity prompting
    random_crime_elements = ["gun", "poison", "knife", "rope", "candlestick", "wrench", "lead pipe", "revolver", "dagger", "candle", "hammer", "hatchet", "screwdriver", "scissors", "bat", "trophy", "shovel", "poker", "axe", "machete", "ice pick", "crowbar", "syringe", "razor", "laser", "garrote", "blowgun", "crossbow", "bow", "sword", "machete", "chainsaw", "nunchucks", "brass knuckles", "boomerang", "flamethrower", "grenade", "landmine", "rocket launcher", "taser", "stun gun", "slingshot", "whip"]
    random_place_elements = ["drawing room", "kitchen", "library", "conservatory", "billiard room", "ballroom", "dining room", "lounge", "hall", "study", "cellar", "attic", "bathroom", "bedroom", "closet", "garage", "garden", "patio", "porch", "shed", "greenhouse", "pool", "sauna", "hot tub", "gazebo", "gym", "office", "studio", "workshop", "lab", "classroom", "auditorium", "theater", "studio", "gallery", "museum", "church", "temple", "synagogue", "mosque", "cathedral", "castle", "fortress", "palace", "mansion", "manor", "villa", "cabin", "cottage", "house", "apartment", "condo", "townhouse", "duplex", "triplex", "fourplex", "hotel", "motel", "inn", "hostel", "resort", "campground", "campsite", "tent", "yurt", "igloo", "cave", "treehouse", "hut", "shack", "barn", "stable"]
    random_person_elements = ["butler", "maid", "cook", "gardener", "chauffeur", "nanny", "nurse", "doctor", "nurse", "nun", "priest", "rabbi", "imam", "monk", "bishop", "cardinal", "pope", "king", "queen", "prince", "princess", "duke", "duchess", "earl", "countess", "baron", "baroness", "knight", "squire", "page", "jester", "fool", "bard", "minstrel", "troubadour", "juggler", "acrobat", "clown", "mime", "magician", "cheesemonger", "baker", "butcher", "candlemaker", "blacksmith", "farmer", "shepherd", "fisherman", "hunter", "trapper", "lumberjack", "miner", "sailor", "pirate", "soldier", "sailor", "pirate", "soldier", "guard", "watchman", "spy"]
    
    random_crimes = random.sample(random_crime_elements, 3)
    random_places = random.sample(random_place_elements, 3)
    random_people = random.sample(random_person_elements, 5)

    killer, victim = random_people[0], random_people[1]

    diversity_prompt = f"This is a mystery story in the style of a golden age classic, and it features the following elements:"
    for element in random_crimes + random_places + random_people:
        diversity_prompt += f"\n- {element}"

    diversity_prompt += f"\n\nThe central story is that a crime was committed with a {random.choice(random_crimes)} in the {random.choice(random_places)} by {killer}, killing {victim}. But there's shenanigans going on with the other stuff, too."

    return Story(diversity_prompt, random_crimes, random_places, random_people)

def main():
    story = get_random_details()
    print(story.diversity_prompt)

if __name__ == '__main__':
    main()
