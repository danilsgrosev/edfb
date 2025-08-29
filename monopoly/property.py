class Property:
    def __init__(self, cell_info):
        """
        cell_info: dict из PROPERTIES (monopoly/properties.py)
        """
        self.id = cell_info["id"]
        self.name = cell_info["name"]
        self.type = cell_info["type"]
        self.price = cell_info.get("price", None)
        self.color = cell_info.get("color", None)
        self.rent = cell_info.get("rent", None)  # список для улиц/жд, None для спец. клеток
        self.amount = cell_info.get("amount", None)  # для налогов
        self.owner_id = None   # user_id владельца
        self.house_count = 0   # для улиц (0-4)
        self.hotel = False     # True, если отель построен
        self.mortgaged = False # (опционально для будущего)
    
    def buy(self, player_id):
        """Передать право собственности игроку"""
        self.owner_id = player_id

    def build_house(self):
        """Построить дом (до 4)"""
        if self.type == "street" and self.house_count < 4 and not self.hotel:
            self.house_count += 1
            return True
        return False

    def build_hotel(self):
        """Построить отель (если уже 4 дома)"""
        if self.type == "street" and self.house_count == 4 and not self.hotel:
            self.hotel = True
            self.house_count = 4
            return True
        return False

    def calc_rent(self, dice_roll=None, rr_owned=1, util_owned=1):
        """
        Вернуть сумму аренды для данной клетки:
        - Для улиц: базовая + застройка
        - Для ж/д: зависит от числа RR у владельца
        - Для служб: зависит от dice_roll и числа служб
        """
        if self.type == "street" and self.rent:
            if self.hotel:
                return self.rent[5]
            return self.rent[self.house_count]
        elif self.type == "railroad" and self.rent:
            idx = min(rr_owned - 1, 3)
            return self.rent[idx]
        elif self.type == "utility":
            if dice_roll is None:
                return 0
            if util_owned == 2:
                return dice_roll * 10
            else:
                return dice_roll * 4
        elif self.type == "tax" and self.amount:
            return self.amount
        else:
            return 0

    def reset(self):
        """Сбросить собственность (при банкротстве или продаже)"""
        self.owner_id = None
        self.house_count = 0
        self.hotel = False
        self.mortgaged = False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "price": self.price,
            "color": self.color,
            "rent": self.rent,
            "amount": self.amount,
            "owner_id": self.owner_id,
            "house_count": self.house_count,
            "hotel": self.hotel,
            "mortgaged": self.mortgaged
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(data)
        obj.owner_id = data.get("owner_id", None)
        obj.house_count = data.get("house_count", 0)
        obj.hotel = data.get("hotel", False)
        obj.mortgaged = data.get("mortgaged", False)
        return obj