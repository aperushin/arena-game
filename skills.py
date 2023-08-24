from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
    Base skill class
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina_required(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    def _is_enough_stamina(self) -> bool:
        return self.user.stamina >= self.stamina_required

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        self.user = user
        self.target = target
        if self._is_enough_stamina:
            return self.skill_effect()
        return f"{self.user.name} tried to use {self.name}, but didn't have enough stamina"

    def skill_effect(self) -> str:
        self.user.take_stamina_damage(self.stamina_required)
        self.target.take_damage(self.damage)
        return f'{self.user.name} uses {self.name} and deals {round(self.damage)} damage to the opponent.'


class FuryPunch(Skill):
    name = 'Fury Punch'
    stamina_required = 6
    damage = 12


class HardShot(Skill):
    name = 'Hard Shot'
    stamina_required = 5
    damage = 15
