# Seat Categories
SEAT_CATEGORIES = [
    '', 'BALCONY', 'BOX', 'BOX A', 'BOX B',
    'BUDGET', 'COMFORT XL', 'DELUXE', 'DIAMOND', 'DIAMOND SOFA',
    'ECONOMY', 'ELITE', 'EXECUTIVE', 'FIRST CLASS',
    'GOLD', 'JACK', 'KING', 'KING CIRCLE',
    'LEGEND CLASS', 'LOUNGE+UPGRADE', 'LOUNGER',
    'NORMAL', 'PLATINUM', 'PLATINUM A',
    'PREMIUM', 'PREMIUMXL', 'QUEEN', 'QUEEN CIRCLE',
    'SECOND CLASS', 'SILVER', 'SPECIAL', 'XLSLIDER'
]

# User Slang to Category Mapping
SLANG_MAPPING = {
    "premium": ["PREMIUM", "PREMIUMXL"],
    "vip": ["PREMIUM", "PREMIUMXL", "PLATINUM", "DIAMOND"],
    "recliner": ["LOUNGER", "COMFORT XL", "DIAMOND SOFA"],
    "sofa": ["DIAMOND SOFA"],
    "box": ["BOX", "BOX A", "BOX B"],
    "balcony": ["BALCONY"],
    "gold": ["GOLD"],
    "platinum": ["PLATINUM", "PLATINUM A"],
    "diamond": ["DIAMOND", "DIAMOND SOFA"],
    "king": ["KING", "KING CIRCLE"],
    "queen": ["QUEEN", "QUEEN CIRCLE"],
    "lounge": ["LOUNGE+UPGRADE", "LOUNGER"],
    "executive": ["EXECUTIVE"],
    "first class": ["FIRST CLASS"],
    "elite": ["ELITE"],
    "legend": ["LEGEND CLASS"],
    "budget": ["BUDGET", "ECONOMY"],
    "cheap": ["BUDGET", "ECONOMY", "SPECIAL"],
    "economy": ["ECONOMY"],
    "normal": ["NORMAL"],
    "regular": ["NORMAL"],
    "silver": ["SILVER"],
    "special": ["SPECIAL"],
}

# Budget Keywords
BUDGET_KEYWORDS = {
    "budget": 60, "cheap": 60, "cheapest": 60, "low cost": 60,
    "low price": 60, "affordable": 60, "economical": 60,
    "inexpensive": 60, "pocket friendly": 60, "special": 60,
    "economy": 60, "basic": 60, "lowest price": 60,
    "minimum price": 60, "under 100": 100, "below 100": 100
}