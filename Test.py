import math
from typing import Dict

from rich import print
from rich.panel import Panel
from rich.table import Table

from Undead import Undead, Mummy, Ghost, Vampire


def print_fancy_box(content: Table) -> None:
    panel = Panel(content, expand=False)
    print(panel)


class Test:
    test_undead: Dict[str, Undead] = []

    def test(self) -> None:
        self.mummy = Mummy("King Tut")
        self.ghost = Ghost("Casper")
        self.vampire = Vampire("Dracula")

        self.test_undead = {
            self.mummy.get_name(): self.mummy,
            self.ghost.get_name(): self.ghost,
            self.vampire.get_name(): self.vampire
        }

        cases = [
            {
                "description": "Casper haunts King Tut",
                "attacker": self.ghost,
                "target": self.mummy,
                "ability": "Haunt",
                "expected_result": {
                    "Casper": {
                        "hp": 60,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 100,
                        "is_dead": False
                    },
                    "Dracula": {
                        "hp": 120,
                        "is_dead": False
                    }
                }
            },
            {
                "description": "King Tut attacks Casper",
                "attacker": self.mummy,
                "target": self.ghost,
                "ability": "Attack",
                "expected_result": {
                    "Casper": {
                        "hp": 54.4,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 100,
                        "is_dead": False
                    },
                    "Dracula": {
                        "hp": 120,
                        "is_dead": False
                    }
                }
            },
            {
                "description": "Casper haunts Dracula",
                "attacker": self.ghost,
                "target": self.vampire,
                "ability": "Haunt",
                "expected_result": {
                    "Casper": {
                        "hp": 66.4,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 100,
                        "is_dead": False
                    },
                    "Dracula": {
                        "hp": 120,
                        "is_dead": False
                    }
                }
            },
            {
                "description": "Dracula attacks Casper",
                "attacker": self.vampire,
                "target": self.ghost,
                "ability": "Attack",
                "expected_result": {
                    "Casper": {
                        "hp": 54.4,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 100,
                        "is_dead": False
                    },
                    "Dracula": {
                        "hp": 120,
                        "is_dead": False
                    }
                }
            },
            {
                "description": "King Tut attacks Dracula",
                "attacker": self.mummy,
                "target": self.vampire,
                "ability": "Attack",
                "expected_result": {
                    "Casper": {
                        "hp": 54.4,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 100,
                        "is_dead": False
                    },
                    "Dracula": {
                        "hp": 58,
                        "is_dead": False
                    }
                }
            },
            {
                "description": "Dracula bites King Tut",
                "attacker": self.vampire,
                "target": self.mummy,
                "ability": "Bite",
                "expected_result": {
                    "Casper": {
                        "hp": 54.4,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 100,
                        "is_dead": False
                    },
                    "Dracula": {
                        "hp": 138,
                        "is_dead": False
                    }
                }
            },
            {
                "description": "Casper haunts Dracula",
                "attacker": self.ghost,
                "target": self.vampire,
                "ability": "Haunt",
                "expected_result": {
                    "Casper": {
                        "hp": 68.2,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 100,
                        "is_dead": False
                    },
                    "Dracula": {
                        "hp": 138,
                        "is_dead": False
                    }
                }
            },
            {
                "description": "Dracula attacks King Tut",
                "attacker": self.vampire,
                "target": self.mummy,
                "ability": "Attack",
                "expected_result": {
                    "Casper": {
                        "hp": 68.2,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 0,
                        "is_dead": True
                    },
                    "Dracula": {
                        "hp": 138,
                        "is_dead": False
                    }
                }
            },
            {
                "description": "King Tut revives",
                "attacker": self.mummy,
                "target": self.mummy,
                "ability": "Revive",
                "expected_result": {
                    "Casper": {
                        "hp": 68.2,
                        "is_dead": False
                    },
                    "King Tut": {
                        "hp": 100,
                        "is_dead": False
                    },
                    "Dracula": {
                        "hp": 138,
                        "is_dead": False
                    }
                }
            }
        ]

        for index, case in enumerate(cases):
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
            attacker = case["attacker"]
            ability = attacker.get_ability(name=(case["ability"]))
            ability.use_ability(case["target"])
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

                if not math.isclose(expected_undead["hp"], actual_undead.get_hp()):
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
