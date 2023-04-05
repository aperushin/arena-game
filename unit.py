from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon: Weapon | None = None
        self.armor: Armor | None = None
        self._is_skill_used = False

    @property
    def health_points(self) -> str:
        return f'{round(self.hp)}'

    @property
    def stamina_points(self):
        return f'{round(self.stamina)}'

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """
        Calculates attack damage and applies hp and sp damage to both sides

        :returns: Resulting damage
        """
        raw_damage = self.weapon.damage * self.unit_class.attack

        # Target armor calculation
        if target.stamina > 0:
            target_armor = target.armor.defence * target.unit_class.armor
            target.take_stamina_damage(target.armor.stamina_per_turn)
        else:
            target_armor = 0

        resulting_damage = raw_damage - target_armor

        self.take_stamina_damage(self.weapon.stamina_per_hit)
        if resulting_damage > 0:
            target.take_damage(resulting_damage)
            return resulting_damage
        return 0

    def take_damage(self, damage: float) -> None:
        new_hp = self.hp - damage
        self.hp = new_hp if new_hp > 0 else 0

    def take_stamina_damage(self, damage: float) -> None:
        new_stamina = self.stamina - damage
        self.stamina = new_stamina if new_stamina > 0 else 0

    def regen_stamina(self, amount: int):
        if self.stamina + amount <= self.unit_class.max_stamina:
            self.stamina += amount
        else:
            self.stamina = self.unit_class.max_stamina

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        if self._is_skill_used:
            return 'The skill was already used'

        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        hit_damage = self._count_damage(target)

        if hit_damage:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {round(hit_damage)} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        if not self._is_skill_used:
            will_use_skill = randint(1, 10) == 10  # Can't be bothered with magic numbers rn
            if will_use_skill:
                return self.use_skill(target)

        hit_damage = self._count_damage(target)

        if hit_damage:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {round(hit_damage)} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, но ваш(а) {target.armor.name} его останавливает."
