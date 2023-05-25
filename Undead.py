from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import Optional, List, Callable

from rich import print
from rich.panel import Panel
from rich.table import Table


class Ability:
    def __init__(self, undead: "Undead", name: str, description: str,
                 method: Callable[["Undead"], float], ability_type: AbilityType):
        self._undead: "Undead" = undead
        self._name: str = name
        self._description: str = description
        self._method: Callable[["Undead"], float] = method
        self._type: Ability.AbilityType = ability_type

    class AbilityType(Enum):
        ATTACK = "Attack"
        HEAL = "Heal"

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_method(self) -> Callable[["Undead"], float]:
        return self._method

    def use_ability(self, target: "Undead") -> None:
        amount = self._method(target)

        table = Table.grid(padding=(0, 1), expand=False)

        table.add_column(style="bold cyan", justify="right")
        table.add_column(style="magenta")

        table.add_row("Ability",
                      f"{self._undead.get_name()} used {self._name} on {target.get_name() if target is not self._undead else 'itself'}")
        table.add_row("Description", self._description)
        table.add_row(self._type.value, f"{amount} HP")

        table.add_row()

        # HP Values
        table.add_row(f"{self._undead.get_name()} HP", f"{self._undead.get_hp()}")
        if target is not self._undead:
            table.add_row(f"{target.get_name()} HP", f"{target.get_hp()}")

        # Death Values
        if self._undead.is_dead():
            table.add_row("", f"{self._undead.get_name()} is now dead.")
        if target.is_dead() and target is not self._undead:
            table.add_row("", f"{target.get_name()} is now dead.")

        panel = Panel(table, expand=False)
        print(panel)


class Undead(ABC):
    def __init__(self, name: Optional[str] = None, hp: Optional[int] = None):
        self._hp: float = hp if hp else 100
        self._name: str = name if name else "Undead"
        self._is_dead: bool = False
        self._abilities: List[dict] = []

    def is_dead(self, dead: Optional[bool] = None) -> bool | None:
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

    def take_damage(self, damage: float) -> float:
        self._hp -= damage
        self._hp = round(self._hp, 2)
        self._hp = 0 if self._hp < 0 else self._hp
        self.is_dead(self._hp <= 0)
        return damage

    def heal(self, heal: float) -> float:
        self._hp += heal
        self._hp = round(self._hp, 2)
        self._hp = 0 if self._hp < 0 else self._hp
        self.is_dead(self._hp <= 0)
        return heal

    def list_abilities(self) -> list[Ability]:
        return [Ability(self, a["name"], a["description"], a["method"], a["type"]) for a in self._abilities]

    def prompt_ability(self) -> Ability:
        while True:
            try:
                index = int(input("Choose an ability: ")) - 1
                return self.list_abilities()[index]
            except (IndexError, TypeError):
                print("Invalid choice, try again.")

    def get_ability(self, index: int = None, name: str = None):
        if index:
            return self.list_abilities()[index]
        elif name:
            return [a for a in self.list_abilities() if a.get_name().casefold() == name.casefold()][0]
        else:
            return self.prompt_ability()

    def print_details(self):
        table = Table.grid(padding=(0, 1), expand=False)

        table.add_column(style="cyan")
        table.add_column(style="magenta")
        table.add_column(style="green")

        table.add_row("Name", self._name)
        table.add_row("HP", f"{self._hp}")
        table.add_row("Dead", f"{self._is_dead}")

        panel = Panel(table, expand=False)
        print(panel)


class Zombie(Undead):
    """
    As an undead, it inherits all the common characteristics of the undead class. Zombie can eat another undead as a
    result it will increase its HP by the half of the HP of the undead being eaten. Zombie may attack other undead. Its
    attack damage is half of its HP. Zombie could only attack if its HP is greater than 50. If the zombie’s HP is
    reduced to 0, it will die. On creation, zombie has the default HP of the undead.
    """

    def __init__(self, name: str = "Zombie"):
        super().__init__(name)
        self._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 50% of its HP.",
                "method": self.attack,
                "type": Ability.AbilityType.ATTACK
            },
            {
                "name": "Eat",
                "description": "Eat another undead to gain 50% of its HP.",
                "method": self.eat,
                "type": Ability.AbilityType.HEAL
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.5 if self.get_hp() > 50 else 0
        return other_undead.take_damage(damage)

    def eat(self, other_undead: 'Undead') -> float:
        heal = other_undead.get_hp() * 0.5
        return self.heal(heal)


class Vampire(Undead):
    """
    A vampire as an undead, inherits all the common characteristics of the undead class. Vampire can bite which
    increases their HP by 80% of the undead HP being bitten. Vampire could attack other undead. Its attack damage is
    same as its HP. If its HP is reduced to 0, vampire will not die, but it cannot attack anymore. When vampires are
    created, they possess a starting HP of 120.
    """

    def __init__(self, name: str = "Vampire"):
        super().__init__(name, hp=120)
        self._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to its HP.",
                "method": self.attack,
                "type": Ability.AbilityType.ATTACK
            },
            {
                "name": "Bite",
                "description": "Bite another undead to gain 80% of its HP.",
                "method": self.bite,
                "type": Ability.AbilityType.HEAL
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() if self.get_hp() > 0 else 0
        return other_undead.take_damage(damage)

    def bite(self, other_undead: 'Undead') -> float:
        heal = other_undead.get_hp() * 0.8
        return self.heal(heal)


class Skeleton(Undead):
    """
    Skeleton as an undead, receives all the similar characteristics of an undead. Skeleton may attack other undead. Its
    attack damage is 70% of its HP. If skeleton HP is reducing to 0, same with the zombie, it will die. Skeleton has an
    80 HP.
    """

    def __init__(self, name: str = "Skeleton"):
        super().__init__(name, hp=80)
        self._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 70% of its HP.",
                "method": self.attack,
                "type": Ability.AbilityType.ATTACK
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.7
        return other_undead.take_damage(damage)


class Ghost(Undead):
    """
    Ghost are like virtual version of an undead. It inherits all the characteristics that the undead has. Ghost may
    attack other undead. Its attack damage is only 20% of its HP. Ghost only receives 10% of the damage being done to
    it. If ghost HP is reduced to 0, it will be perished. Ghost initial HP would be the half of the initial HP of the
    undead. Ghost can haunt which increases its HP by the 10% of the undead being haunted.
    """

    def __init__(self, name: str = "Ghost"):
        super().__init__(name)
        self.set_hp(multiplier=0.5)
        self._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 20% of its HP.",
                "method": self.attack,
                "type": Ability.AbilityType.ATTACK
            },
            {
                "name": "Haunt",
                "description": "Haunt another undead to gain 10% of its HP.",
                "method": self.haunt,
                "type": Ability.AbilityType.HEAL
            }
        ]

    def take_damage(self, damage: float) -> float:
        return super().take_damage(damage * 0.1)

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.2
        return other_undead.take_damage(damage)

    def haunt(self, other_undead: 'Undead') -> float:
        return self.heal(other_undead.get_hp() * 0.1)


class Lich(Skeleton):
    """
    Lich is a kind of undead like skeleton, but it has reach immortality. Lich has another ability. It could cast a
    spell on undead which gets the 10% of their HP and add it to its HP. Lich attack damage is equal to 70 percent of
    its HP. If Lich HP is reduced to 0, it cannot attack anymore but still alive.
    """

    def __init__(self, name: str = "Lich"):
        super().__init__(name)
        self._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 70% of its HP.",
                "method": self.attack,
                "type": Ability.AbilityType.ATTACK
            },
            {
                "name": "Cast Spell",
                "description": "Cast a spell on another undead to gain 10% of its HP.",
                "method": self.cast_spell,
                "type": Ability.AbilityType.HEAL
            }
        ]

    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.7 if self.get_hp() > 0 else 0
        return other_undead.take_damage(damage)

    def cast_spell(self, other_undead: 'Undead') -> float:
        heal = other_undead.get_hp() * 0.1
        return self.heal(heal)

    def is_dead(self, dead: Optional[bool] = None) -> bool:
        return True


class Mummy(Zombie):
    """
    Mummy is an undead like zombie, but it does not eat its own kind. Mummy can attack other undead; its attack
    damage is equal to the half of its HP plus 10% of the undead HP. If its HP reached 0, it will die and needs to be
    revived again. When revived it will have its initial HP again.
    """

    def __init__(self, name: str = "Mummy"):
        super().__init__(name)
        self._abilities = [
            {
                "name": "Attack",
                "description": "Attack another undead with damage equal to 50% of its HP plus 10% of the undead HP.",
                "method": self.attack,
                "type": Ability.AbilityType.ATTACK
            },
            {
                "name": "Revive",
                "description": "Revive itself to its initial HP.",
                "method": self.revive,
                "type": Ability.AbilityType.HEAL
            },
            {
                "name": "Eat",
                "description": "Eat another undead to gain 50% of its HP.",
                "method": self.eat,
                "type": Ability.AbilityType.HEAL
            }
        ]


    def attack(self, other_undead: 'Undead') -> float:
        damage = self.get_hp() * 0.5 + other_undead.get_hp() * 0.1
        return other_undead.take_damage(damage)

    def revive(self, other_undead: 'Undead') -> float:
        return self.heal(100)

    def eat(self, other_undead: 'Undead') -> float:
        return 0 if isinstance(other_undead, Mummy) else super().eat(other_undead)
