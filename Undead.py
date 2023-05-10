from abc import ABC, abstractmethod
from typing import Optional, Union, List


class Ability:
    def __init__(self, name: str, description: str, method: callable):
        self._name = name
        self._description = description
        self._method = method

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_method(self) -> callable:
        return self._method

    def use_ability(self, undead: "Undead", other_undead: "Undead") -> None:
        self._method(other_undead)
        print(f"{self._name} used on {other_undead.get_name()}")
        print(f"{self._name} description: {self._description}")
        print(f"{undead.get_name()} HP: {undead.get_hp()}")
        print(f"{other_undead.get_name()} HP: {other_undead.get_hp()}")


class Undead(ABC):
    def __init__(self, name: Optional[str] = None, hp: Optional[int] = None):
        self._hp: float = hp if hp else 100
        self._name: str = name if name else "Undead"
        self._is_dead: bool = False
        self._abilities: List[Ability] = []

    def is_dead(self, dead: Optional[bool] = None) -> Union[bool, None]:
        if dead is None:
            return self._is_dead
        else:
            self._is_dead = dead

    def get_name(self) -> str:
        return self._name

    def get_hp(self) -> float:
        return self._hp

    def set_name(self, name: str) -> None:
        self._name = name

    def set_hp(self, hp: Optional[float] = None, multiplier: Optional[float] = None) -> None:
        if multiplier is None:
            self._hp = hp
        else:
            self._hp = self._hp * multiplier

    def list_abilities(self) -> None:
        for ability in self._abilities:
            print(f"{ability.get_name()}: {ability.get_description()}")


class Zombie(Undead):
    """
    As an undead, it inherits all the common characteristics of the undead class. Zombie can eat another undead as a
    result it will increase its HP by the half of the HP of the undead being eaten. Zombie may attack other undead. Its
    attack damage is half of its HP. Zombie could only attack if its HP is greater than 50. If the zombie’s HP is
    reduced to 0, it will die. On creation, zombie has the default HP of the undead.
    """

    def __init__(self, name: str = "Zombie"):
        super().__init__(name)
        super()._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 50% of its HP.",
                "method": self.attack
            },
            {
                "name": "Eat",
                "description": "Eat another undead to gain 50% of its HP.",
                "method": self.eat
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.5 if self.get_hp() > 50 else 0
        other_undead.set_hp(other_undead.get_hp() - damage)
        return damage

    def eat(self, other_undead: 'Undead') -> None:
        self.set_hp(self.get_hp() + int(other_undead.get_hp() * 0.5))
        other_undead.set_hp(int(other_undead.get_hp() * 0.5))


class Vampire(Undead):
    """
    A vampire as an undead, inherits all the common characteristics of the undead class. Vampire can bite which
    increases their HP by 80% of the undead HP being bitten. Vampire could attack other undead. Its attack damage is
    same as its HP. If its HP is reduced to 0, vampire will not die, but it cannot attack anymore. When vampires are
    created, they possess a starting HP of 120.
    """

    def __init__(self, name: str = "Vampire"):
        super().__init__(name, hp=120)
        super()._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to its HP.",
                "method": self.attack
            },
            {
                "name": "Bite",
                "description": "Bite another undead to gain 80% of its HP.",
                "method": self.bite
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp()
        other_undead.set_hp(other_undead.get_hp() - damage)
        return damage

    def bite(self, other_undead: 'Undead') -> None:
        self.set_hp(self.get_hp() + int(other_undead.get_hp() * 0.8))
        other_undead.set_hp(int(other_undead.get_hp() * 0.8))


class Skeleton(Undead):
    """
    Skeleton as an undead, receives all the similar characteristics of an undead. Skeleton may attack other undead. Its
    attack damage is 70% of its HP. If skeleton HP is reducing to 0, same with the zombie, it will die. Skeleton has an
    80 HP.
    """

    def __init__(self, name: str = "Skeleton"):
        super().__init__(name, hp=80)
        super()._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 70% of its HP.",
                "method": self.attack
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.7
        other_undead.set_hp(other_undead.get_hp() - damage)
        return damage


class Ghost(Undead):
    """
    Ghost are like virtual version of an undead. It inherits all the characteristics that the undead has. Ghost may
    attack other undead. Its attack damage is only 20% of its HP. Ghost only receives 10% of the damage being done to
    it. If ghost HP is reduced to 0, it will be perished. Ghost initial HP would be the half of the initial HP of the
    undead. Ghost can haunt which increases its HP by the 10% of the undead being haunt.
    """

    def __init__(self, name: str = "Ghost"):
        super().__init__(name)
        self.set_hp(multiplier=0.5)
        super()._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 20% of its HP.",
                "method": self.attack
            },
            {
                "name": "Haunt",
                "description": "Haunt another undead to gain 10% of its HP.",
                "method": self.haunt
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.2
        other_undead.set_hp(other_undead.get_hp() - damage)
        return damage

    def haunt(self, other_undead: 'Undead') -> None:
        self.set_hp(self.get_hp() + int(other_undead.get_hp() * 0.1))
        other_undead.set_hp(int(other_undead.get_hp() * 0.9))


class Lich(Undead):
    """
    Lich is a kind of undead like skeleton, but it has reach immortality. Lich has another ability. It could cast a
    spell on undead which gets the 10% of their HP and add it to its HP. Lich attack damage is equal to 70 percent of
    its Hp. If Lich HP is reduced to 0, it cannot attack anymore but still alive.
    """

    def __init__(self, name: str = "Lich"):
        super().__init__(name)
        super()._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 70% of its HP.",
                "method": self.attack
            },
            {
                "name": "Cast Spell",
                "description": "Cast a spell on another undead to gain 10% of its HP.",
                "method": self.cast_spell
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.7
        other_undead.set_hp(other_undead.get_hp() - damage)
        return damage

    def cast_spell(self, other_undead: 'Undead') -> None:
        self.set_hp(self.get_hp() + int(other_undead.get_hp() * 0.1))
        other_undead.set_hp(int(other_undead.get_hp() * 0.9))

    def is_dead(self, dead: Optional[bool] = None) -> bool:
        return True


class Mummy(Undead):
    """
    Mummy is an undead like zombie, but it does not eat its own kind. Mummy can attack other undead; its attack
    damage is equal to the half of its HP plus 10% of the undead HP. If its HP reached 0, it will die and needs to be
    revived again. When revived it will have its initial HP again.
    """

    def __init__(self, name: str = "Mummy"):
        super().__init__(name)
        super()._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 50% of its HP plus 10% of the undead HP.",
                "method": self.attack
            },
            {
                "name": "Revive",
                "description": "Revive itself to its initial HP.",
                "method": self.revive
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.5 + other_undead.get_hp() * 0.1
        other_undead.set_hp(other_undead.get_hp() - damage)
        return damage

    def revive(self, other_undead: 'Undead') -> None:
        self.set_hp(100)
