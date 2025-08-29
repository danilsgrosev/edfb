from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Новые координаты: (x1, y1, x2, y2)
# Расчёт центра каждой клетки
RAW_COORDS = [
    (1110, 1109, 1275, 1270),  # GO
    (1003, 1112, 1108, 1271),  # Mediterranean Avenue
    (902, 1108, 1005, 1274),   # Community Chest 1
    (795, 1108, 898, 1272),    # Baltic Avenue
    (693, 1110, 795, 1274),    # Income Tax
    (585, 1106, 691, 1271),    # Reading Railroad
    (478, 1108, 585, 1269),    # Oriental Avenue
    (380, 1115, 476, 1272),    # Chance 1
    (269, 1108, 374, 1274),    # Vermont Avenue
    (167, 1106, 269, 1267),    # Connecticut Avenue
    (1, 1110, 167, 1263),      # Jail
    (0, 1004, 160, 1106),      # St. Charles Place
    (0, 901, 164, 995),        # Electric Company
    (1, 799, 164, 897),        # States Avenue
    (1, 686, 164, 792),        # Virginia Avenue
    (6, 584, 164, 688),        # Pennsylvania Railroad
    (4, 477, 160, 579),        # St. James Place
    (0, 370, 160, 473),        # Community Chest 2
    (1, 259, 164, 368),        # Tennessee Avenue
    (0, 170, 162, 268),        # New York Avenue
    (6, 2, 156, 161),          # Free Parking
    (171, 5, 267, 155),        # Kentucky Avenue
    (271, 0, 371, 152),        # Chance 2
    (373, 3, 471, 152),        # Indiana Avenue
    (482, 12, 582, 155),       # Illinois Avenue
    (587, 2, 687, 157),        # B&O Railroad
    (696, 3, 796, 159),        # Atlantic Avenue
    (796, 5, 898, 153),        # Ventnor Avenue
    (904, 9, 1002, 159),       # Water Works
    (1000, 7, 1111, 153),      # Marvin Gardens
    (1104, 9, 1261, 157),      # Go to Jail
    (1107, 161, 1266, 270),    # Pacific Avenue
    (1109, 275, 1270, 382),    # North Carolina Avenue
    (1111, 373, 1275, 470),    # Community Chest 3
    (1109, 484, 1270, 575),    # Pennsylvania Avenue
    (1109, 590, 1265, 690),    # Short Line
    (1113, 704, 1270, 790),    # Chance 3
    (1107, 786, 1274, 895),    # Park Place
    (1111, 899, 1266, 1001),   # Luxury Tax
    (1107, 997, 1268, 1103),   # Boardwalk
]

# Вычисление центров
CELL_COORDS = [((x1 + x2) // 2, (y1 + y2) // 2) for (x1, y1, x2, y2) in RAW_COORDS]

BOARD_SIZE = 1280
PLAYER_COLORS = [
    "#FF4500", "#1E90FF", "#228B22", "#FFD700", "#9400D3", "#00CED1", "#8B0000", "#FF69B4"
]

def get_avatar_image(avatar_url, size=56):
    try:
        response = requests.get(avatar_url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        img = img.resize((size, size), Image.ANTIALIAS)
        return img
    except Exception:
        return Image.new("RGBA", (size, size), "#CCCCCC")

def draw_board(game, font_path="arial.ttf"):
    img = Image.open("field.png").convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 1. Собственность: владельцы, дома, отели
    for prop in game.properties:
        if prop.owner_id is not None and 0 <= prop.id < len(CELL_COORDS):
            owner_idx = [p.user_id for p in game.players].index(prop.owner_id)
            cx, cy = CELL_COORDS[prop.id]
            # Метка владельца
            draw.ellipse([cx + 38, cy - 30, cx + 58, cy - 10],
                         fill=PLAYER_COLORS[owner_idx % len(PLAYER_COLORS)], outline="#222222")
            # Дома/отель
            if prop.type == "street":
                if prop.hotel:
                    draw.rectangle([cx - 50, cy + 38, cx - 10, cy + 58],
                                   fill="#D2691E", outline="#222222")
                else:
                    for h_idx in range(prop.house_count):
                        draw.rectangle([cx - 30 + h_idx * 22, cy + 38,
                                        cx - 10 + h_idx * 22, cy + 58],
                                       fill="#006600", outline="#222222")

    # 2. Фишки игроков
    for idx, player in enumerate(game.players):
        if 0 <= player.position < len(CELL_COORDS):
            cx, cy = CELL_COORDS[player.position]
            avatar_img = get_avatar_image(player.avatar_url, size=56)
            img.paste(avatar_img, (cx - 28, cy - 28), avatar_img)
            draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30],
                         outline=PLAYER_COLORS[idx % len(PLAYER_COLORS)], width=4)

    # 3. Баланс игроков
    try:
        font = ImageFont.truetype(font_path, 24)
    except Exception:
        font = ImageFont.load_default()

    y_panel = BOARD_SIZE - 60
    for idx, player in enumerate(game.players):
        text = f"@{player.username}: {player.balance}₽"
        draw.text((20 + idx * 220, y_panel), text,
                  fill=PLAYER_COLORS[idx % len(PLAYER_COLORS)], font=font)

    # 4. Текущий игрок
    cp = game.get_current_player()
    if cp:
        draw.text((BOARD_SIZE // 2 - 160, BOARD_SIZE - 30),
                  f"Ход игрока: @{cp.username}", fill="#222222", font=font)

    return img

def get_board_image_bytes(img):
    """Вернуть картинку в байтах для отправки через Telegram API"""
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio
