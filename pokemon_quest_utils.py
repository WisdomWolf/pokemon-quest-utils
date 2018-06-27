# coding: utf-8
from functools import reduce
import yaml
import json
from json import JSONDecodeError

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

    def increase_level(self, levels):
        self.level += levels
        self._base_hp += levels
        self._base_atk += levels

    def __repr__(self):
        return '{}(name={}, level={}, CP={}, health_slots={}, atk_slots={}, dual_slots={})'.format(self.__class__.__name__, self.name, self.level, self.cp, self.health_slots, self.atk_slots, self.dual_slots)

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

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, ', '.join(['%s=%s' % (k, v) for k, v in self.__dict__.items()]))

def add_stones(stone_list=[]):
    answer = 'default'
    while answer != '' and answer.lower() != 'x':
        answer = input('add new stone: ')
        try:
            s_type, s_val, *s_ex = answer.split(' ', maxsplit=2)
        except ValueError:
            if answer != '' and answer.lower() != 'x':
                print('Unable to parse stone from %s' % answer)
                continue
            else:
                print('Returning stones...')
                break

        try:
            s_val = int(s_val)
            s_ex = json.loads(s_ex[0])
        except ValueError:
            print('Unable to parse int from %s' % s_val)
            continue
        except JSONDecodeError:
            print('Unable to load dict from %s' % s_ex)
            continue
        except (TypeError, IndexError):
            s_ex = None

        if s_type[0].lower() == 'a':
            stone = PowerStone('atk', s_val, s_ex)
        elif s_type[0].lower() == 'h':
            stone = PowerStone('health', s_val, s_ex)
        else:
            print('%s is not a valid stone type')
            continue
        stone_list.append(stone)
    return stone_list


def show_top_pokemon(pokemon_list, top=10):
    return sorted(pokemon_list, key=lambda x: x.cp, reverse=True)[:top]


def save_pokemon(pokemon_list, filename=None):
    filename = filename or 'pokemon_quest_pokemon.yml'
    with open(filename, 'w') as f:
        yaml.dump(pokemon_list, f, default_flow_style=False)
    print('Pokemon saved to %s successfully!' % filename)


def load_pokemon(filename=None):
    filename = filename or 'pokemon_quest_pokemon.yml'
    with open(filename, 'r') as f:
        return yaml.load(f)


def create_pokemon_dict(pokemon_list):
    return {pokemon.name: pokemon for pokemon in pokemon_list}

