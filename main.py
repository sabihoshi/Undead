from __future__ import annotations

from typing import List, Any

from Undead import *
from rich import print
from rich.panel import Panel
from rich.table import Table


def print_fancy_box(content: Table) -> None:
    panel = Panel(content, expand=False)
    print(panel)


def print_menu_options() -> None:
    table = Table.grid(padding=(0, 1), expand=False)
    table.add_column(justify="left", style="bold magenta")
    table.add_column(justify="left", style="bold cyan")

    table.add_row("1. Create Undead", "2. Command Undead")
    table.add_row("3. Display Undead", "4. Quit")

    print_fancy_box(table)


def print_sub_menu_options(submenu: str) -> None:
    table = Table.grid(padding=(0, 1), expand=False)
    table.add_column(justify="left", style="bold green")
    table.add_column(justify="left", style="bold yellow")

    if submenu == "create_undead":
        table.add_row("a. Zombie", "b. Vampire")
        table.add_row("c. Skeleton", "d. Ghost")
    elif submenu == "command_undead":
        table.add_row("1. Ability 1", "2. Ability 2")

    print_fancy_box(table)


def battle(attacker: Undead, target: Undead) -> None:
    damage = attacker.attack()
    target.set_hp(target.get_hp() - int(damage))
    if isinstance(target, Ghost):
        target.receive_damage(damage)
    if target.get_hp() <= 0:
        target.set_hp(0)
        target.is_dead(True)

    print(f"{attacker.get_name()} attacked {target.get_name()} for {damage} damage.")
    print(f"{target.get_name()} now has {target.get_hp()} HP.")
    if target.is_dead():
        print(f"{target.get_name()} is dead.")
    print()


def create_undead() -> Any | None:
    undead_types = {
        "a": Zombie,
        "b": Vampire,
        "c": Skeleton,
        "d": Ghost
    }

    print("Create Undead:")
    print_sub_menu_options("create_undead")
    choice = input("Enter your choice: ").lower()

    if choice in undead_types:
        name = input("Enter a custom name or press Enter to use the default name: ")
        if name:
            return undead_types[choice](name)
        else:
            return undead_types[choice]()
    else:
        print("Invalid choice.")
        return None


def command_undead(undead: Undead, undead_list: List[Undead]) -> None:
    print(f"Command {undead.get_name()}:")
    print_sub_menu_options("command_undead")



def display_undead(undead_list: List[Undead]) -> None:
    for undead in undead_list:
        print(f"{undead.get_name()} - HP: {undead.get_hp()} - State: {'Alive' if not undead.is_dead() else 'Dead'}")


def game_menu() -> None:
    undead_list = []
    while True:
        print_menu_options()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_undead = create_undead()
            if new_undead is not None:
                undead_list.append(new_undead)
        elif choice == 2:
            if undead_list:
                for index, undead in enumerate(undead_list):
                    print(f"{index}. {undead.get_name()} - {'Alive' if not undead.is_dead() else 'Dead'}")
                undead_index = int(input("Choose an undead by index to command: "))
                print_sub_menu_options("command_undead")
                choice = int(input("Enter your choice: "))
                command_undead(undead_list[undead_index], undead_list, choice)
            else:
                print("No undead have been created.")
        elif choice == 3:
            if undead_list:
                display_undead(undead_list)
            else:
                print("No undead have been created.")
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    game_menu()
