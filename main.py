from __future__ import annotations

from typing import Any

from Test import Test
from Undead import *


def print_fancy_box(content: Table) -> None:
    panel = Panel(content, expand=False)
    print(panel)


def create_undead() -> Any | None:
    undead_types = {
        "a": Zombie,
        "b": Vampire,
        "c": Skeleton,
        "d": Ghost,
        "e": Lich,
        "f": Mummy
    }

    print("Create Undead:")

    table = Table.grid(padding=(0, 1), expand=False)

    table.add_column(justify="left", style="bold green")
    table.add_column(justify="left", style="bold yellow")

    table.add_row("a. Zombie", "b. Vampire")
    table.add_row("c. Skeleton", "d. Ghost")
    table.add_row("e. Lich", "f. Mummy")

    print_fancy_box(table)

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

    table = Table.grid(padding=(0, 1), expand=False)
    table.add_column(justify="left", style="bold green")
    table.add_column(justify="left", style="bold yellow")

    abilities = undead.list_abilities()
    for i in range(len(abilities)):
        ability = abilities[i]
        table.add_row(f"[{i + 1}] {ability.get_name()}", ability.get_description())

    print_fancy_box(table)

    ability = undead.prompt_ability()
    display_undead(undead_list)
    while True:
        try:
            index = int(input("Choose an undead: ")) - 1
            chosen_undead = undead_list[index]
            ability.use_ability(chosen_undead)
            break
        except (IndexError, TypeError):
            print("Invalid choice, try again.")


def display_undead(undead_list: List[Undead]) -> None:
    table = Table.grid(padding=(0, 1), expand=False)

    table.add_column(justify="left", style="bold magenta")
    table.add_column(justify="left", style="bold cyan")
    table.add_column(justify="left", style="bold red")

    for index, undead in enumerate(undead_list):
        table.add_row(f"[{index + 1}]. {undead.get_name()}",
                      f"{'Alive' if not undead.is_dead() else 'Dead'}",
                      f"{undead.get_hp()}")

    print_fancy_box(table)


def game_menu() -> None:
    undead_list = []
    while True:
        table = Table.grid(padding=(0, 1), expand=False)

        table.add_column(justify="left", style="bold magenta")
        table.add_column(justify="left", style="bold cyan")

        table.add_row("1. Create Undead", "2. Command Undead")
        table.add_row("3. Display Undead", "4. Auto Test")
        table.add_row("", "Q. Quit")

        print_fancy_box(table)
        choice = input("Enter your choice: ")

        if choice == '1':
            new_undead = create_undead()
            if new_undead is not None:
                undead_list.append(new_undead)
        elif choice == '2':
            if undead_list:
                display_undead(undead_list)
                while True:
                    try:
                        undead_index = int(input("Choose an undead by index to command: ")) - 1
                        chosen = undead_list[undead_index]
                        list_except_chosen = [c for c in undead_list if c is not chosen]

                        command_undead(chosen, list_except_chosen)
                        break
                    except (IndexError, TypeError):
                        print("Invalid choice, try again.")
            else:
                print("No undead have been created.")
        elif choice == '3':
            if undead_list:
                display_undead(undead_list)
            else:
                print("No undead have been created.")
        elif choice == '4':
            Test().test()
        elif choice == 'q':
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    game_menu()
