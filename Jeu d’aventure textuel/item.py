"""Item model and helpers."""

import labels as L


class Item:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """
    Représente un item manipulable par le joueur.
    Attributes:
        name (str): Le nom de l'item.
        description (str): La description de l'item.
        weight (float): Le poids de l'item en kilogrammes.
        effect_type (str | None): Le type d'effet (ex: "heal", "atk", "def").
        effect_value (int): La valeur de l'effet.
        usable (bool): True si l'item peut être utilisé.
    """

    def __init__(
        self,
        name,
        description,
        weight,
        effect_type=None,
        effect_value=0,
        usable=False,
        on_pickup=None,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.name = name
        self.description = description
        self.weight = weight
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.usable = usable
        self.on_pickup = on_pickup
        self.pickup_seen = False

    def __str__(self):
        return L.ITEM_STR_TEMPLATE.format(
            name=self.name,
            description=self.description,
            weight=self.weight,
        )


def create_stability_note():
    """
    Create the narrative note that hints at mental collapse without numbers.
    The message is returned only once, on first pickup.
    """
    text = L.STABILITY_NOTE_TEXT
    note = Item(
        L.STABILITY_NOTE_NAME,
        L.STABILITY_NOTE_DESC,
        0,
        usable=False,
    )
    note.pickup_seen = False

    def on_pickup(player, _game):
        if note.pickup_seen:
            return None
        note.pickup_seen = True
        player.read_stability_note = True
        return "\n" + text + "\n"

    note.on_pickup = on_pickup
    return note
