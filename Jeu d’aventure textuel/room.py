"""Room model with exits, items, and characters."""

import labels as L


class Room:
    """
    Représente une pièce du jeu d’aventure.

    Une Room correspond à un lieu dans lequel le joueur peut se trouver.
    Elle possède un nom, une description et un ensemble de sorties menant
    vers d’autres pièces.

    Attributs
    ----------
    name : str
        Nom de la pièce.
    description : str
        Description textuelle de la pièce.
    exits : dict
        Dictionnaire associant une direction (str) à une autre Room ou à None.

    Méthodes
    --------
    get_exit(direction)
        Retourne la pièce associée à la direction donnée.
    get_exit_string()
        Retourne une chaîne décrivant les sorties disponibles.
    get_long_description()
        Retourne une description complète de la pièce incluant les sorties.

    Exemples
    --------
    >>> room = Room("Cuisine", "dans une cuisine sombre")
    >>> room.exits["nord"] = None
    >>> room.get_exit("nord") is None
    True
    >>> "Sorties" in room.get_exit_string()
    True
    """


    def __init__(self, name, description, image=None):
        """Create a room with a name, description, and empty containers."""
        self.name = name
        self.description = description
        self.image = image
        self.perception_descriptions = {}
        self.exits = {}
        self.inventory = []
        self.characters = []
        self.enemies = []



    def look(self, stability_value=None):
        """Return the full room description with items, enemies, and characters."""
        res = self.get_long_description(stability_value)
        res += "\n" + self.format_items() + "\n"
        res += "\n" + self.get_enemies() + "\n"
        res += "\n" + self.format_characters() + "\n"
        return res


    def get_characters(self):
        """Return a copy of the characters list."""
        return list(self.characters)

    def get_items(self):
        """Return a copy of the room inventory."""
        return list(self.inventory)

    def format_characters(self):
        """Format the character list for display."""
        characters = self.get_characters()
        if not characters:
            return L.ROOM_NO_CHARACTERS

        res = f"{L.ROOM_CHARACTERS_HEADER}\n"
        for index, character in enumerate(characters, start=1):
            res += f"    {index}) {character}\n"
        return res.rstrip()

    def get_enemies(self):
        """Format the enemy list for display."""
        if not self.enemies:
            return L.ROOM_NO_ENEMIES

        res = f"{L.ROOM_ENEMIES_HEADER}\n"
        for enemy in self.enemies:
            res += f"    - {enemy}\n"
        return res


    def get_inventory(self):
        """Return the formatted inventory string."""
        return self.format_items()

    def format_items(self):
        """Format the room items for display."""
        items = self.get_items()
        if not items:
            return L.ROOM_NO_ITEMS

        res = f"{L.ROOM_ITEMS_HEADER}\n"
        for index, item in enumerate(items, start=1):
            res += f"    {index}) {item}\n"
        return res.rstrip()

    def get_exit(self, direction):
        """Return the room in the given direction, or None."""

        # Return the room in the given direction if it exists.
        if direction in self.exits:
            return self.exits[direction]
        return None

    # Return a string describing the room's exits.
    def get_exit_string(self):
        """Return a human-readable string of available exits."""
        exit_string = L.ROOM_EXITS_PREFIX
        parts = []
        for direction, room in self.exits.items():
            if room is not None:
                parts.append(f"{direction} : {room.name}")
        exit_string += ", ".join(parts)
        return exit_string

    def get_description(self, stability_value=None):
        """Return the base or perception-altered description."""
        if not self.perception_descriptions or stability_value is None:
            return self.description

        try:
            value = int(stability_value)
        except (TypeError, ValueError):
            return self.description

        if value <= 4 and "low" in self.perception_descriptions:
            return self.perception_descriptions["low"]
        if value >= 8 and "high" in self.perception_descriptions:
            return self.perception_descriptions["high"]
        return self.description

    # Return a long description of this room including exits.
    def get_long_description(self, stability_value=None):
        """Return the long description string including exits."""
        description_text = self.get_description(stability_value)
        body = L.ROOM_DESCRIPTION_PREFIX.format(description=description_text)
        return L.ROOM_LONG_DESCRIPTION_TEMPLATE.format(
            name=self.name,
            body=body,
            exits=self.get_exit_string(),
        )
