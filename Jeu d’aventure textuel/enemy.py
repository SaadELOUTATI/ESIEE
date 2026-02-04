"""Enemy model for combat resolution."""

import labels as L


class Enemy:
    """
    Represents a basic enemy with health and attack power.
    """

    def __init__(self, name: str, hp: int, attack: int) -> None:
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self) -> bool:
        """Return True if the enemy still has HP."""
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        """
        Apply damage to the enemy and return the effective damage.
        """
        amount = max(0, int(amount))
        self.hp = max(0, self.hp - amount)
        return amount

    def __str__(self) -> str:
        return L.ENEMY_STR_TEMPLATE.format(
            name=self.name,
            hp=self.hp,
            attack=self.attack,
        )
