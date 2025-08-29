import random
from monopoly.player import Player
from monopoly.property import Property
from monopoly.properties import PROPERTIES
from monopoly.board_cells import generate_board_cells
from monopoly.cards import get_chance_card, get_community_chest_card

class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.players = []         # Список объектов Player
        self.player_order = []    # Порядок ходов (user_id)
        self.current_idx = 0      # Индекс текущего игрока
        self.started = False
        self.finished = False
        self.properties = [Property(cell) for cell in PROPERTIES]
        self.board_cells = generate_board_cells()
        self.turn_count = 0
        self.last_roll = None
        self.state = {}           # Для хранения любых временных данных (например, кто строит/платит)

    # ========== Игроки ==========
    def add_player(self, user_id, username, avatar_url):
        if self.started:
            return False
        if user_id in [p.user_id for p in self.players]:
            return False
        player = Player(user_id, username, avatar_url)
        self.players.append(player)
        self.player_order.append(user_id)
        return True

    def remove_player(self, user_id):
        self.players = [p for p in self.players if p.user_id != user_id]
        self.player_order = [uid for uid in self.player_order if uid != user_id]
        if self.current_idx >= len(self.player_order):
            self.current_idx = 0

    def get_player(self, user_id):
        for p in self.players:
            if p.user_id == user_id:
                return p
        return None

    def get_active_players(self):
        return [p for p in self.players if p.is_active]

    # ========== Старт и ход ==========
    def start(self):
        if len(self.players) < 2:
            return False
        self.started = True
        self.current_idx = 0
        self.turn_count = 1
        self.finished = False
        random.shuffle(self.player_order)
        return True

    def next_turn(self):
        """Переход к следующему игроку"""
        if not self.started or self.finished:
            return None
        self.current_idx = (self.current_idx + 1) % len(self.player_order)
        # Пропуск неактивных игроков
        start_idx = self.current_idx
        while not self.get_player(self.player_order[self.current_idx]).is_active:
            self.current_idx = (self.current_idx + 1) % len(self.player_order)
            if self.current_idx == start_idx:
                self.finished = True
                return None
        self.turn_count += 1
        return self.get_player(self.player_order[self.current_idx])

    def get_current_player(self):
        if not self.started or self.finished:
            return None
        return self.get_player(self.player_order[self.current_idx])

    # ========== Кости ==========
    def roll_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.last_roll = (dice1, dice2)
        return dice1, dice2

    # ========== Основная логика хода ==========
    def process_turn(self, user_id, dice=None):
        player = self.get_player(user_id)
        if not player or not player.is_active:
            return False, "Игрок не найден или выбыл!"
        if player.in_jail:
            return self.process_jail(player, dice)
        if dice is None:
            dice = self.roll_dice()
        steps = sum(dice)
        player.move(steps)
        cell = self.board_cells[player.position]
        prop = self.properties[player.position]
        # Логика по типу клетки:
        if prop.type == "street" or prop.type == "railroad" or prop.type == "utility":
            if prop.owner_id is None:
                return True, f"Вы попали на {prop.name}. Можно купить за {prop.price}."
            elif prop.owner_id != player.user_id:
                # Аренда
                owner = self.get_player(prop.owner_id)
                rent = prop.calc_rent(
                    dice_roll=steps,
                    rr_owned=self.count_rr(owner.user_id),
                    util_owned=self.count_util(owner.user_id)
                )
                player.pay(rent)
                owner.receive(rent)
                if player.balance < 0:
                    player.is_active = False
                    # Сбросить собственность
                    for pid in player.properties:
                        self.properties[pid].reset()
                    return True, f"{player.username} не может заплатить аренду и выбывает!"
                return True, f"Вы заплатили аренду {rent} игроку @{owner.username}."
            else:
                return True, "Вы попали на свою собственность."
        elif prop.type == "tax":
            player.pay(prop.amount)
            if player.balance < 0:
                player.is_active = False
                for pid in player.properties:
                    self.properties[pid].reset()
                return True, f"{player.username} не может оплатить налог и выбывает!"
            return True, f"Вы оплатили налог {prop.amount}."
        elif prop.type == "chance":
            card_text = get_chance_card()
            return True, f"Вы взяли карточку 'Шанс': {card_text}"
        elif prop.type == "community_chest":
            card_text = get_community_chest_card()
            return True, f"Вы взяли карточку 'Общественная казна': {card_text}"
        elif prop.type == "jail":
            return True, "Вы просто в гостях у тюрьмы."
        elif prop.type == "free_parking":
            return True, "Бесплатная парковка! Ничего не происходит."
        elif prop.type == "go_to_jail":
            player.go_to_jail()
            return True, "Вы отправляетесь в тюрьму!"
        elif prop.type == "go":
            player.receive(200)
            return True, "Вы прошли GO и получили 200."
        else:
            return True, f"Вы на клетке {prop.name}."

    def process_jail(self, player, dice=None):
        """Логика хода в тюрьме"""
        player.jail_turns += 1
        msg = ""
        if dice is None:
            dice = self.roll_dice()
        if dice[0] == dice[1]:
            player.free_from_jail()
            player.move(sum(dice))
            msg = f"Вам выпал дубль! Вы выходите из тюрьмы и идете на {sum(dice)} клеток."
        elif player.jail_turns >= 3:
            player.pay(50)
            player.free_from_jail()
            player.move(sum(dice))
            msg = f"Вы заплатили 50 и вышли из тюрьмы, перемещаясь на {sum(dice)} клеток."
        else:
            msg = f"Вы остаетесь в тюрьме (ход {player.jail_turns}/3)."
        return True, msg

    # ========== Покупка ==========
    def buy_property(self, user_id):
        player = self.get_player(user_id)
        if not player or not player.is_active:
            return False, "Игрок не найден или выбыл!"
        prop = self.properties[player.position]
        if prop.type not in ["street", "railroad", "utility"]:
            return False, "Эту клетку нельзя купить!"
        if prop.owner_id is not None:
            return False, "Собственность уже куплена!"
        if player.balance < prop.price:
            return False, "Недостаточно средств!"
        player.pay(prop.price)
        player.add_property(prop.id)
        prop.buy(player.user_id)
        return True, f"Вы купили {prop.name} за {prop.price}."

    # ========== Строительство ==========
    def build_house(self, user_id):
        player = self.get_player(user_id)
        prop = self.properties[player.position]
        if prop.type != "street" or prop.owner_id != user_id:
            return False, "Здесь нельзя строить дом!"
        # Логика проверки монополии (опционально)
        cost = self.get_house_cost(prop.color)
        if player.balance < cost:
            return False, "Недостаточно средств для строительства!"
        if prop.build_house():
            player.pay(cost)
            return True, f"Вы построили дом на {prop.name} за {cost}."
        else:
            return False, "Максимум домов уже построено!"

    def build_hotel(self, user_id):
        player = self.get_player(user_id)
        prop = self.properties[player.position]
        if prop.type != "street" or prop.owner_id != user_id:
            return False, "Здесь нельзя строить отель!"
        cost = self.get_hotel_cost(prop.color)
        if player.balance < cost:
            return False, "Недостаточно средств для строительства!"
        if prop.build_hotel():
            player.pay(cost)
            return True, f"Вы построили отель на {prop.name} за {cost}."
        else:
            return False, "Отель уже построен или недостаточно домов!"

    def get_house_cost(self, color):
        costs = {
            "brown": 50, "light_blue": 50, "pink": 100,
            "orange": 100, "red": 150, "yellow": 150,
            "green": 200, "dark_blue": 200
        }
        return costs.get(color, 100)

    def get_hotel_cost(self, color):
        return self.get_house_cost(color)

    # ========== Вспомогательные ==========
    def count_rr(self, user_id):
        count = 0
        for prop in self.properties:
            if prop.type == "railroad" and prop.owner_id == user_id:
                count += 1
        return count

    def count_util(self, user_id):
        count = 0
        for prop in self.properties:
            if prop.type == "utility" and prop.owner_id == user_id:
                count += 1
        return count

    def get_status(self):
        info = []
        for p in self.players:
            props = [self.properties[pid].name for pid in p.properties]
            info.append(f"@{p.username}: {p.balance}₽ | {'в тюрьме' if p.in_jail else ''} | {', '.join(props)}")
        return "\n".join(info)

    # ========== Сохранение ==========
    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "players": [p.to_dict() for p in self.players],
            "player_order": self.player_order,
            "current_idx": self.current_idx,
            "started": self.started,
            "finished": self.finished,
            "properties": [prop.to_dict() for prop in self.properties],
            "turn_count": self.turn_count,
            "last_roll": self.last_roll,
            "state": self.state
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(data["chat_id"])
        obj.players = [Player.from_dict(p) for p in data["players"]]
        obj.player_order = data["player_order"]
        obj.current_idx = data["current_idx"]
        obj.started = data["started"]
        obj.finished = data["finished"]
        obj.properties = [Property.from_dict(prop) for prop in data["properties"]]
        obj.turn_count = data["turn_count"]
        obj.last_roll = data["last_roll"]
        obj.state = data["state"]
        obj.board_cells = generate_board_cells()
        return obj