# Структура клеток для классической Монополии

PROPERTY_TYPES = [
    "go", "street", "railroad", "utility", "tax", "chance",
    "community_chest", "jail", "free_parking", "go_to_jail"
]

PROPERTY_COLORS = {
    "brown": "#8B4513",
    "light_blue": "#ADD8E6",
    "pink": "#FF69B4",
    "orange": "#FFA500",
    "red": "#FF0000",
    "yellow": "#FFFF00",
    "green": "#008000",
    "dark_blue": "#00008B",
    "railroad": "#222222",
    "utility": "#AAAAAA"
}

# Список всех 40 клеток с типом, ценой, цветом, арендой и прочими параметрами
PROPERTIES = [
    # id, name, type, price, color, rent, ...
    {"id": 0, "name": "GO", "type": "go"},
    {"id": 1, "name": "Mediterranean Avenue", "type": "street", "price": 60, "color": "brown", "rent": [2, 10, 30, 90, 160, 250]},
    {"id": 2, "name": "Community Chest", "type": "community_chest"},
    {"id": 3, "name": "Baltic Avenue", "type": "street", "price": 60, "color": "brown", "rent": [4, 20, 60, 180, 320, 450]},
    {"id": 4, "name": "Income Tax", "type": "tax", "amount": 200},
    {"id": 5, "name": "Reading Railroad", "type": "railroad", "price": 200, "color": "railroad", "rent": [25, 50, 100, 200]},
    {"id": 6, "name": "Oriental Avenue", "type": "street", "price": 100, "color": "light_blue", "rent": [6, 30, 90, 270, 400, 550]},
    {"id": 7, "name": "Chance", "type": "chance"},
    {"id": 8, "name": "Vermont Avenue", "type": "street", "price": 100, "color": "light_blue", "rent": [6, 30, 90, 270, 400, 550]},
    {"id": 9, "name": "Connecticut Avenue", "type": "street", "price": 120, "color": "light_blue", "rent": [8, 40, 100, 300, 450, 600]},
    {"id": 10, "name": "Jail", "type": "jail"},
    {"id": 11, "name": "St. Charles Place", "type": "street", "price": 140, "color": "pink", "rent": [10, 50, 150, 450, 625, 750]},
    {"id": 12, "name": "Electric Company", "type": "utility", "price": 150, "color": "utility"},
    {"id": 13, "name": "States Avenue", "type": "street", "price": 140, "color": "pink", "rent": [10, 50, 150, 450, 625, 750]},
    {"id": 14, "name": "Virginia Avenue", "type": "street", "price": 160, "color": "pink", "rent": [12, 60, 180, 500, 700, 900]},
    {"id": 15, "name": "Pennsylvania Railroad", "type": "railroad", "price": 200, "color": "railroad", "rent": [25, 50, 100, 200]},
    {"id": 16, "name": "St. James Place", "type": "street", "price": 180, "color": "orange", "rent": [14, 70, 200, 550, 750, 950]},
    {"id": 17, "name": "Community Chest", "type": "community_chest"},
    {"id": 18, "name": "Tennessee Avenue", "type": "street", "price": 180, "color": "orange", "rent": [14, 70, 200, 550, 750, 950]},
    {"id": 19, "name": "New York Avenue", "type": "street", "price": 200, "color": "orange", "rent": [16, 80, 220, 600, 800, 1000]},
    {"id": 20, "name": "Free Parking", "type": "free_parking"},
    {"id": 21, "name": "Kentucky Avenue", "type": "street", "price": 220, "color": "red", "rent": [18, 90, 250, 700, 875, 1050]},
    {"id": 22, "name": "Chance", "type": "chance"},
    {"id": 23, "name": "Indiana Avenue", "type": "street", "price": 220, "color": "red", "rent": [18, 90, 250, 700, 875, 1050]},
    {"id": 24, "name": "Illinois Avenue", "type": "street", "price": 240, "color": "red", "rent": [20, 100, 300, 750, 925, 1100]},
    {"id": 25, "name": "B&O Railroad", "type": "railroad", "price": 200, "color": "railroad", "rent": [25, 50, 100, 200]},
    {"id": 26, "name": "Atlantic Avenue", "type": "street", "price": 260, "color": "yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    {"id": 27, "name": "Ventnor Avenue", "type": "street", "price": 260, "color": "yellow", "rent": [22, 110, 330, 800, 975, 1150]},
    {"id": 28, "name": "Water Works", "type": "utility", "price": 150, "color": "utility"},
    {"id": 29, "name": "Marvin Gardens", "type": "street", "price": 280, "color": "yellow", "rent": [24, 120, 360, 850, 1025, 1200]},
    {"id": 30, "name": "Go To Jail", "type": "go_to_jail"},
    {"id": 31, "name": "Pacific Avenue", "type": "street", "price": 300, "color": "green", "rent": [26, 130, 390, 900, 1100, 1275]},
    {"id": 32, "name": "North Carolina Avenue", "type": "street", "price": 300, "color": "green", "rent": [26, 130, 390, 900, 1100, 1275]},
    {"id": 33, "name": "Community Chest", "type": "community_chest"},
    {"id": 34, "name": "Pennsylvania Avenue", "type": "street", "price": 320, "color": "green", "rent": [28, 150, 450, 1000, 1200, 1400]},
    {"id": 35, "name": "Short Line", "type": "railroad", "price": 200, "color": "railroad", "rent": [25, 50, 100, 200]},
    {"id": 36, "name": "Chance", "type": "chance"},
    {"id": 37, "name": "Park Place", "type": "street", "price": 350, "color": "dark_blue", "rent": [35, 175, 500, 1100, 1300, 1500]},
    {"id": 38, "name": "Luxury Tax", "type": "tax", "amount": 100},
    {"id": 39, "name": "Boardwalk", "type": "street", "price": 400, "color": "dark_blue", "rent": [50, 200, 600, 1400, 1700, 2000]},
]