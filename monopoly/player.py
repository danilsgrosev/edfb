class Player:
    def __init__(self, user_id, username, avatar_url):
        self.user_id = user_id           # Telegram user id
        self.username = username         # Telegram username
        self.avatar_url = avatar_url     # URL к аватарке (либо путь к локальному файлу)
        self.balance = 1500              # Начальный баланс
        self.position = 0                # Текущая позиция на поле (cell_id)
        self.properties = []             # id всех купленных клеток (улицы, ж/д, службы)
        self.in_jail = False             # В тюрьме ли игрок
        self.jail_turns = 0              # Количество ходов в тюрьме
        self.is_active = True            # Активен ли игрок (выбыл или нет)

    def move(self, steps):
        """Переместить игрока на поле (с учетом 40 клеток)"""
        if self.in_jail:
            return False
        self.position = (self.position + steps) % 40

    def pay(self, amount):
        """Списать деньги со счета"""
        self.balance -= amount
        if self.balance < 0:
            self.is_active = False

    def receive(self, amount):
        """Получить деньги"""
        self.balance += amount

    def add_property(self, property_id):
        """Добавить собственность"""
        if property_id not in self.properties:
            self.properties.append(property_id)

    def remove_property(self, property_id):
        """Удалить собственность (например, при банкротстве)"""
        if property_id in self.properties:
            self.properties.remove(property_id)

    def go_to_jail(self):
        self.in_jail = True
        self.jail_turns = 0
        self.position = 10  # клетка JAIL

    def free_from_jail(self):
        self.in_jail = False
        self.jail_turns = 0

    def to_dict(self):
        """Сохранить/восстановить состояние игрока"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'avatar_url': self.avatar_url,
            'balance': self.balance,
            'position': self.position,
            'properties': self.properties,
            'in_jail': self.in_jail,
            'jail_turns': self.jail_turns,
            'is_active': self.is_active
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data['user_id'], data['username'], data['avatar_url'])
        player.balance = data['balance']
        player.position = data['position']
        player.properties = data['properties']
        player.in_jail = data['in_jail']
        player.jail_turns = data['jail_turns']
        player.is_active = data['is_active']
        return player