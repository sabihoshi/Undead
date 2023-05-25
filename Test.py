import json
import math
from typing import Dict

from rich import print
from rich.panel import Panel
from rich.table import Table

from Undead import *


def print_fancy_box(content: Table) -> None:
    panel = Panel(content, expand=False)
    print(panel)


class Test:


    def test(self) -> None:
        self.mummy = Mummy("King Tut")
        self.ghost = Ghost("Casper")
        self.vampire = Vampire("Dracula")

        self.test_undead: Dict[str, Undead] = {}

        file = input("Enter the name of the test file: ")
        test = json.load(open(file if file else "test1.json", "r"))

        undead_mapping = {
            "Zombie": Zombie,
            "Vampire": Vampire,
            "Skeleton": Skeleton,
            "Ghost": Ghost,
            "Lich": Lich,
            "Mummy": Mummy
        }

        for undead in test["undead"]:
            undead_type = undead_mapping[undead["undead"]]
            undead_instance = undead_type(undead["name"])
            self.test_undead[undead_instance.get_name()] = undead_instance

        cases = test["cases"]

        for index, case in enumerate(cases):
            attacker = self.test_undead[case["attacker"]]
            target = self.test_undead[case["target"]]

            # Information
            print("Information")
            table = Table.grid(padding=(0, 5), expand=False)
            table.add_column(style="bold cyan", justify="right")
            table.add_column(style="magenta")
            table.add_row(f"Test Case #{index + 1}", case['description'])
            print_fancy_box(table)
            # sleep(3)

            # Actually attacking
            print("Simulation")
            ability = attacker.get_ability(name=(case["ability"]))
            ability.use_ability(target)
            # sleep(3)

            # Results
            print("Expected Result                 | Actual Result")
            table = Table.grid(padding=(0, 3), expand=False)
            table.add_column("Name", justify="right", style="cyan", no_wrap=True)
            table.add_column("HP", justify="right", style="magenta")
            table.add_column("Status", justify="right", style="magenta")
            table.add_column()
            table.add_column("HP", justify="left", style="blue")
            table.add_column("Status", justify="left", style="blue")
            table.add_row("Name", "HP", "Status", "", "HP", "Status", style="bold blue")

            passed = True
            for name, expected_undead in case["expected_result"].items():
                actual_undead = self.test_undead[name]

                if not math.isclose(expected_undead["hp"], actual_undead.get_hp(), rel_tol=1e-3):
                    passed = False

                if expected_undead["is_dead"] != actual_undead.is_dead():
                    passed = False

                table.add_row(
                    name, f"{expected_undead['hp']} HP", "Dead" if expected_undead["is_dead"] else "Alive", "|",
                    f"{actual_undead.get_hp()} HP", "Dead" if actual_undead.is_dead() else "Alive"
                )

            table.add_row("Result", "Passed" if passed else "Failed", style="bold green" if passed else "bold red")
            print_fancy_box(table)
            # sleep(5)

            print("=" * 100)
