"""Character model and reactive dialogue helpers."""

import random
import labels as L


def merchant_dialogue(game, _character):
    """
    Scène narrative du Marchand avec choix moral et impact sur la stabilité.
    """
    player = game.player

    if player.merchant_sacrifice or player.merchant_refused:
        return L.MERCHANT_REPEAT_TEXT

    lines = L.MERCHANT_DIALOGUE_LINES

    print("\n" + "\n".join(lines) + "\n")

    choice = ""
    prompt_input = getattr(game, "input_func", input)
    while choice not in ("accepter", "refuser", "a", "r", "1", "2"):
        choice = prompt_input("> ").strip().lower()

    if choice in ("accepter", "a", "1"):
        result = L.MERCHANT_ACCEPT_TEXT
        print(result)
        player.has_crystal = True
        player.merchant_sacrifice = True
        game.adjust_stability(-3)
    else:
        result = L.MERCHANT_REFUSE_TEXT
        print(result)
        player.merchant_refused = True
        player.met_yara = True
        game.adjust_stability(1)
        if not player.has_crystal:
            print(L.MERCHANT_NO_CRYSTAL_TEXT)
            game.finished = True

    return None


def _format_reply(character, line):
    """Format a NPC reply with the configured template."""
    return L.NPC_REPLY_TEMPLATE.format(name=character.name, line=line)


def ralen_reactive(game, character):
    """Return Ralen's reply adjusted by the player's stability."""
    player = game.player
    state = player.get_stability_state()
    if state in ("au bord de l'effondrement", "effondrement"):
        line = L.RALEN_REACTIVE_LINES["collapse"]
    elif state == "vacillant":
        line = L.RALEN_REACTIVE_LINES["vacillant"]
    elif player.read_stability_note and state == "stable":
        line = L.RALEN_REACTIVE_LINES["stable_note"]
    else:
        line = character.get_msg()
    return _format_reply(character, line)


def malek_reactive(game, character):
    """Return Malek's reply adjusted by the player's stability."""
    player = game.player
    state = player.get_stability_state()
    if state in ("au bord de l'effondrement", "effondrement"):
        line = L.MALEK_REACTIVE_LINES["collapse"]
    elif state == "vacillant":
        line = L.MALEK_REACTIVE_LINES["vacillant"]
    else:
        line = character.get_msg()
    return _format_reply(character, line)


def nommera_reactive(game, character):
    """Return Nommera's reply when the player sacrificed the crew."""
    player = game.player
    state = player.get_stability_state()
    if player.merchant_sacrifice and state in (
        "vacillant",
        "au bord de l'effondrement",
        "effondrement",
    ):
        line = L.NOMMERA_REACTIVE_LINE
    else:
        line = character.get_msg()
    return _format_reply(character, line)


def yara_world1_reactive(game, character):
    """Return Yara's reply for world 1."""
    player = game.player
    if player.merchant_sacrifice:
        line = L.YARA_WORLD1_REACTIVE_LINE
    else:
        line = character.get_msg()
    return _format_reply(character, line)


def yara_world2_choice(game, character):
    """
    Propose un choix de méthode pour préparer l'attaque en monde 2.
    """
    player = game.player

    if player.velyra_method:
        return _format_reply(character, L.YARA_WORLD2_DECISION_TAKEN)

    lines = L.YARA_WORLD2_CHOICE_LINES
    print("\n" + "\n".join(lines) + "\n")

    choice = ""
    prompt_input = getattr(game, "input_func", input)
    while choice not in ("1", "2", "corrompre", "piller", "c", "p"):
        choice = prompt_input("> ").strip().lower()

    if choice in ("1", "corrompre", "c"):
        player.velyra_method = "corruption"
        player.velyra_negotiated = True
        player.velyra_method_applied = True
        game.adjust_stability(-1)
        print(L.YARA_WORLD2_CORRUPTION_RESULT)
    else:
        player.velyra_method = "pillage"
        player.velyra_brutal = True
        player.velyra_method_applied = True
        game.adjust_stability(-2)
        print(L.YARA_WORLD2_PILLAGE_RESULT)

    return None


def citizen_dore_reactive(game, character):
    """Return a Citizen reply based on the world 3 posture."""
    player = game.player
    if getattr(player, "ap_choice_infiltrate", False):
        line = L.CITIZEN_REACTIVE_LINES["infiltrate"]
    elif getattr(player, "ap_choice_reveal", False):
        line = L.CITIZEN_REACTIVE_LINES["reveal"]
    else:
        line = L.CITIZEN_REACTIVE_LINES["default"]
    return _format_reply(character, line)


def glitch_reactive(game, character):
    """Return the glitch NPC reply based on the hologram encounter."""
    player = game.player
    if not getattr(player, "attack_holo_done", False):
        line = L.GLITCH_REACTIVE_LINES["before"]
    else:
        line = L.GLITCH_REACTIVE_LINES["after"]
    return _format_reply(character, line)


def novaterra_companion_reactive(_game, character):
    """
    Dialogue du compagnon sur Nova Terra (Yara ou Narek).
    """
    if character.name.lower() == "yara":
        line = L.NOVATERRA_COMPANION_LINES["yara"]
    elif character.name.lower() == "narek":
        line = L.NOVATERRA_COMPANION_LINES["narek"]
    elif character.name.lower() == "le guide":
        line = L.NOVATERRA_COMPANION_LINES["guide"]
    else:
        line = character.get_msg()
    return _format_reply(character, line)


class Character:
    """Simple NPC model with optional movement and dialogue hooks."""

    def __init__(
        self,
        name,
        description,
        current_room,
        msgs,
        can_move=False,
        on_talk=None,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self._index = 0
        self.can_move = can_move
        self.on_talk = on_talk

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        """
        Retourne cycliquement les messages du PNJ en utilisant pop(0).
        On retire le premier message, on l'affiche, puis on le remet à la fin.
        """
        if not self.msgs:
            return L.NPC_NO_MESSAGE

        msg = self.msgs.pop(0)   # retire le premier
        self.msgs.append(msg)    # le remet à la fin (cycle)
        return msg

    def move(self):
        """Attempt to move the NPC to a connected room."""
        if not self.can_move:
            return False

        if random.choice([True, False]) is False:
            return False

        exits = [r for r in self.current_room.exits.values() if r]
        if not exits:
            return False

        new_room = random.choice(exits)
        self.current_room.characters.remove(self)
        new_room.characters.append(self)
        self.current_room = new_room
        return True
