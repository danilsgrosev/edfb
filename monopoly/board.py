from monopoly.board_cells import generate_board_cells
from monopoly.properties import PROPERTIES

class Board:
    def __init__(self):
        self.cells = generate_board_cells()    # Координаты и названия клеток
        self.properties = {prop["id"]: prop for prop in PROPERTIES}  # Расширенные данные клеток

    def get_cell(self, cell_id):
        """Вернуть данные клетки: координаты, название"""
        return self.cells[cell_id]

    def get_property(self, cell_id):
        """Вернуть расширенные данные клетки (тип, цена, аренда и пр.)"""
        return self.properties.get(cell_id, None)

    def get_coords(self, cell_id):
        """Координаты для визуализации фишки/метки на поле"""
        cell = self.get_cell(cell_id)
        return cell["x"], cell["y"]

    def get_name(self, cell_id):
        """Имя клетки"""
        cell = self.get_cell(cell_id)
        return cell["name"]

    def get_type(self, cell_id):
        """Тип клетки (street, railroad, jail, chance и пр.)"""
        prop = self.get_property(cell_id)
        return prop["type"] if prop else None

    def all_cells(self):
        """Все клетки для обхода/визуализации"""
        return self.cells

    def all_properties(self):
        """Все расширенные свойства клеток"""
        return list(self.properties.values())

    def find_cells_by_type(self, cell_type):
        """Вернуть все id клеток заданного типа"""
        return [cell["id"] for cell in self.cells if self.get_type(cell["id"]) == cell_type]

    def find_cells_by_color(self, color):
        """Вернуть все id клеток определенной цветовой группы"""
        return [prop["id"] for prop in self.properties.values() if prop.get("color") == color]

    def is_property(self, cell_id):
        """Можно ли купить эту клетку (улица, ж/д, служба)"""
        t = self.get_type(cell_id)
        return t in ("street", "railroad", "utility")

    def is_special(self, cell_id):
        """Является ли клетка спец (шанс, казна, тюрьма, налог и пр.)"""
        t = self.get_type(cell_id)
        return t in ("chance", "community_chest", "tax", "jail", "free_parking", "go_to_jail", "go")

    def to_dict(self):
        return {
            "cells": self.cells,
            "properties": self.properties
        }

    @classmethod
    def from_dict(cls, data):
        board = cls()
        board.cells = data["cells"]
        board.properties = data["properties"]
        return board