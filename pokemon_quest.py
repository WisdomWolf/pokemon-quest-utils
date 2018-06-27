# coding: utf-8
from functools import reduce


class Pokemon:
    def __init__(self, name, level, hp, atk, health_slots, atk_slots, dual_slots=0):
        self.name = name
        self.level = level
        self._base_hp = hp
        self._base_atk = atk
        self.health_slots = health_slots
        self.atk_slots = atk_slots
        self.dual_slots = dual_slots
        self.health_stones = []
        self.atk_stones = []
        
    @property
    def hp(self):
        return reduce(lambda x, y: x + y, [stone.hp for stone in self.health_stones], self._base_hp)
    
    @property
    def atk(self):
        return reduce(lambda x, y: x + y, [stone.atk for stone in self.atk_stones], self._base_atk)
    
    @property
    def cp(self):
        return self.hp + self.atk
    
    @property
    def base_cp(self):
        return self._base_hp + self._base_atk
    
    def _add_stone(self, stone, stone_type):
        total_type_stones = len(getattr(self, '%s_stones' % stone_type))
        if total_type_stones < getattr(self, '%s_slots' % stone_type) + self.dual_slots and len(self.health_stones) + len(self.atk_stones) < self.health_slots + self.atk_slots + self.dual_slots:
            getattr(self, '%s_stones' % stone_type).append(stone)
        else:
            raise ValueError('No free slots to add new stone')
        
    def add_health_stone(self, stone):
        self._add_stone(stone, 'health')
        
    def add_atk_stone(self, stone):
        self._add_stone(stone, 'atk')
    
    def clear_stones(self):
        self.health_stones = []
        self.atk_stones = []
            
    def __repr__(self):
        return '{}(name={}, CP={})'.format(self.__class__.__name__, self.name, self.cp)
    
    def __str__(self):
        return self.__repr__
    
class PowerStone:
    def __init__(self, stone_type, value, extras=None):
        self.stone_type = stone_type
        if self.stone_type == 'health':
            self.hp = value
        elif self.stone_type == 'atk':
            self.atk = value
        else:
            raise TypeError('%s is not a valid stone type' % stone_type)
        self.extras = extras
        
