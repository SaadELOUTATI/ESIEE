"""Player state and inventory management."""

# Define the Player class.
from quest import QuestManager
import labels as L


class Player():  # pylint: disable=too-many-instance-attributes
    """
    Représente le joueur du jeu.


    Un Player possède un nom et se déplace de pièce en pièce
    en utilisant les sorties disponibles dans la Room courante.


    Attributs
    ----------
    name : str
        Nom du joueur.
    current_room : Room ou None
        Pièce dans laquelle se trouve actuellement le joueur.


    Méthodes
    --------
    move(direction)
        Déplace le joueur dans la direction indiquée si possible.


    Exceptions
    ----------
    KeyError
        Levée si la direction demandée n’existe pas dans les sorties
        de la pièce courante.


    Exemples
    --------
    >>> player = Player("Alice")
    >>> room1 = Room("Hall", "dans un grand hall")
    >>> room2 = Room("Salon", "dans un salon lumineux")
    >>> room1.exits["est"] = room2
    >>> player.current_room = room1
    >>> player.move("est")
    True
    """

    # Define the constructor.
    def __init__(self, name):  # pylint: disable=too-many-statements
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = []
        self.hp = 100
        self.max_hp = 100
        self.atk = 10
        self.stability = 10
        self.weight = 0  # Current weight of items carried
        self.max_weight = 5  # Maximum weight the player can carry
        self.quest_manager = QuestManager(self)
        self.current_world_quests = []
        self.move_count = 0 # Counter for player movements
        self.rewards = []  # List to store earned rewards

        #flags for world 1 progression
        self.met_ralen = False
        self.met_malek = False
        self.met_marchand = False
        self.met_yara = False
        self.met_nommera = False
        self.world1_npcs_bonus = False
        self.has_crystal = False
        self.merchant_refused = False
        self.merchant_sacrifice = False
        self.patrollers_defeated = False
        self.vorn_defeated = False
        self.karn_defeated = False
        self.read_stability_note = False
        self.karn_aftermath_done = False
        self.saved_yara = False
        self.saved_narek = False
        self.yara_dead = False
        self.narek_dead = False

        #flags for world 2 progression
        self.velyra_met_leader = False
        self.velyra_resources_secured = False
        self.velyra_negotiated = False
        self.velyra_brutal = False
        self.velyra_narek_resolved = False
        self.velyra_method = None
        self.velyra_method_applied = False

        #flags for world 3 progression
        self.ap_choice_infiltrate = False
        self.ap_choice_reveal = False
        self.attack_holo_done = False
        self.ap_citizen_spoken = False
        self.ap_glitch_spoken = False
        self.ap_break_illusions = False
        self.ap_keep_illusions = False
        self.ap_taal_confronted = False
        self.ap_taal_alliance = False
        self.ap_taal_dead = False

        #flags for world 4 progression
        self.world4_started = False
        self.novaterra_explored_station = False
        self.novaterra_final_done = False
        self.novaterra_choice_harmony = False
        self.novaterra_choice_domination = False
        self.novaterra_choice_renounce = False
        self.novaterra_terra_defeated = False
        self.novaterra_companion_spoken = False
        self.novaterra_observed_planet = False

    # Define the move method.
    def move(self, direction):
        """Move the player to a different room in the specified direction.
        Args:
            direction (str): the direction to move in.
        Returns:
            bool: True if the move was successful, False otherwise.
        Examples:
            >>> player = Player("Alice")
            >>> room1 = Room("Hall", "dans un grand hall")
            >>> room2 = Room("Salon", "dans un salon lumineux")
            >>> room1.exits["est"] = room2
            >>> player.current_room = room1
            >>> player.move("est")
            True
            >>> player.current_room == room2
            True
            >>> player.move("ouest")
            False
        """
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]


        # If the next room is None, print an error message and return False.
        if next_room is None:
            print(L.PLAYER_NO_DOOR)
            return False

        # Special check for "Prison centrale" access
        if next_room.name == "Prison centrale":
            if not any(
                item.name == L.ITEM_DEFINITIONS["keycard"]["name"]
                for item in self.inventory
            ):
                print(L.PLAYER_PRISON_SCANNER)


        self.history.append(self.current_room)


        # Set the current room to the next room.
        self.current_room = next_room



        print(self.current_room.get_long_description(self.stability))
        return True

    def get_inventory(self):
        """Get a string representation of the player's inventory.
        Returns:
            str: a string listing the items in the inventory and their total weight.
            Examples:
            >>> player = Player("Alice")
            >>> item1 = Item("Clé", "Une petite clé en métal.", weight=
            0.1)
            >>> item2 = Item("Livre", "Un vieux livre poussiéreux.", weight=
            0.5)
            >>> player.inventory.append(item1)
            >>> player.inventory.append(item2)
            >>> player.weight = item1.weight + item2.weight
            >>> print(player.get_inventory()) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Vous disposez des items suivants :
                - Clé
                - Livre
            Le poids total des items est de 0.6 kg sur une capacité maximale de
            5 kg.
            <BLANKLINE>
        """
        if not self.inventory:
            return L.PLAYER_INVENTORY_EMPTY

        res = L.PLAYER_INVENTORY_HEADER
        for index, item in enumerate(self.inventory, start=1):
            res += f"    {index}) {item}\n"
        res += L.PLAYER_INVENTORY_WEIGHT.format(weight=self.weight, max_weight=self.max_weight)
        return res

    def take(self, item_name):
        """take an item from the current room to the player's inventory by name.
        Args:
            item_name (str): the name of the item to take.
            Returns:
            str: a message indicating the result of the take action.
            Examples:
            >>> player = Player("Alice")
            >>> room = Room("Salle", "une salle vide")
            >>> item = Item("Clé", "Une petite clé en métal.")
            >>> room.inventory.append(item)
            >>> player.current_room = room
            >>> print(player.take("Clé")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Vous avez pris : Clé
            <BLANKLINE>
            >>> print(player.take("Livre")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Cet item n’est pas présent ici.
            <BLANKLINE>
        """
        room = self.current_room

        for item in room.inventory:
            if (
                item.name.lower() == item_name.lower()
                and (self.weight + item.weight) <= self.max_weight
            ):
                self.inventory.append(item)
                room.inventory.remove(item)
                self.weight += item.weight
                self.apply_passive_item_effect(item, 1)
                return L.PLAYER_TAKE_SUCCESS.format(item=item)
            if (
                item.name.lower() == item_name.lower()
                and (self.weight + item.weight) > self.max_weight
            ):
                return L.PLAYER_TAKE_TOO_HEAVY.format(item=item)

        return L.PLAYER_TAKE_NOT_HERE

    def drop(self, item_name):
        """drop an item from the player's inventory to the current room by name.
        Args:
            item_name (str): the name of the item to drop.
            Returns:
            str: a message indicating the result of the drop action.
            Examples:
            >>> player = Player("Alice")
            >>> room = Room("Salle", "une salle vide")
            >>> item = Item("Clé", "Une petite clé en métal.")
            >>> player.inventory.append(item)
            >>> player.current_room = room
            >>> print(player.drop("Clé")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Vous avez déposé : Clé
            <BLANKLINE>
            >>> print(player.drop("Livre")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Vous ne possédez pas cet item.
            <BLANKLINE>
        """
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                self.current_room.inventory.append(item)
                self.weight -= item.weight
                self.apply_passive_item_effect(item, -1)
                return L.PLAYER_DROP_SUCCESS.format(item=item)

        return L.PLAYER_DROP_NOT_OWNED

    def use_item(self, item_name):
        """Use an item from the player's inventory by name."""
        if not item_name:
            return L.PLAYER_USE_WHAT

        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if not item.usable:
                    return L.PLAYER_USE_NOT_USABLE.format(item=item.name)

                message, consume = self.apply_item_effect(item)
                if consume:
                    self.inventory.remove(item)
                    self.weight -= item.weight
                return message

        return L.PLAYER_USE_NOT_OWNED.format(item=item_name)

    def apply_item_effect(self, item):
        """Apply an item's effect to the player."""
        if item.effect_type == "heal":
            before = self.hp
            value = getattr(item, "effect_value", getattr(item, "value", 0))
            self.hp = min(self.max_hp, before + value)
            return L.PLAYER_USE_HEAL.format(item=item.name, before=before, after=self.hp), True

        return L.PLAYER_USE_NO_EFFECT.format(item=item.name), False

    def apply_passive_item_effect(self, item, sign):
        """Apply or remove a passive item bonus when it enters or leaves inventory."""
        effect_type = getattr(item, "effect_type", None)
        value = getattr(item, "effect_value", 0)
        if not effect_type or not value:
            return

        try:
            delta = int(value) * int(sign)
        except (TypeError, ValueError):
            return

        if effect_type == "hp":
            self.hp = max(1, min(self.max_hp, self.hp + delta))
            return

        if effect_type == "max_hp":
            self.max_hp = max(1, self.max_hp + delta)
            if delta > 0:
                self.hp = min(self.max_hp, self.hp + delta)
            else:
                self.hp = min(self.max_hp, self.hp)
            return

        if effect_type == "atk":
            self.atk = max(1, self.atk + delta)

    def modify_stability(self, delta, _game=None):
        """
        Apply a stability delta and return (message, died).
        No printing is done here; the caller handles output and end state.
        """
        if not delta:
            return None, False

        self.stability += int(delta)
        if self.stability <= 0:
            return None, True

        message = self._get_stability_feedback(delta)
        return message, False

    def _get_stability_feedback(self, delta):
        """Return a short narrative feedback based on the delta."""
        amount = abs(int(delta))
        if delta > 0:
            if amount >= 3:
                return L.STABILITY_GAIN_STRONG
            if amount == 2:
                return L.STABILITY_GAIN_MEDIUM
            return L.STABILITY_GAIN_LIGHT

        if amount >= 3:
            return L.STABILITY_LOSS_STRONG
        if amount == 2:
            return L.STABILITY_LOSS_MEDIUM
        return L.STABILITY_LOSS_LIGHT

    def get_stability_state(self):
        """Return a narrative label for the current stability value."""
        value = self.stability
        if value >= 9:
            return L.STABILITY_STATE_STABLE
        if value >= 7:
            return L.STABILITY_STATE_FRAGILE
        if value >= 5:
            return L.STABILITY_STATE_UNSTABLE
        if value >= 3:
            return L.STABILITY_STATE_VACILLANT
        if value >= 1:
            return L.STABILITY_STATE_EDGE
        return L.STABILITY_STATE_COLLAPSE

    def get_completed_quests_count(self):
        """Return (completed, total) for the current world's quests."""
        quests = self.current_world_quests or self.quest_manager.get_all_quests()
        total = len(quests)
        completed = sum(1 for quest in quests if quest.is_completed)
        return completed, total

    def activate_quest(self, quest_id):
        """Activate a quest by its numeric id."""
        return self.quest_manager.activate_quest(quest_id)

    def complete_quest(self, quest_id):
        """Complete a quest by its numeric id if present."""
        quest = self.quest_manager.get_quest_by_id(quest_id)
        if not quest:
            return False
        quest.complete_quest(self)
        if quest in self.quest_manager.active_quests:
            self.quest_manager.active_quests.remove(quest)
        return True

    def has_item(self, item_name):
        """Return True when the player owns an item by name."""
        return any(item.name.lower() == item_name.lower() for item in self.inventory)

    def has_flag(self, flag_name):
        """Return True when a boolean flag is set on the player."""
        return bool(getattr(self, flag_name, False))

    def talk(self, name):
        """talk to a character in the current room by name.
        Args:
            name (str): the name of the character to talk to.
        Returns:
            str: the message from the character or an error message if not found.
        Examples:
            >>> player = Player("Alice")
            >>> room = Room("Salle", "une salle vide")
            >>> character = Character("Bob", "Bonjour, je suis Bob.")
            >>> room.characters.append(character)
            >>> player.current_room = room
            >>> print(player.talk("Bob")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Bob dit : 'Bonjour, je suis Bob.'
            <BLANKLINE>
            >>> print(player.talk("Charlie")) # doctest: +NORMALIZE_WHITESPACE
            <BLANKLINE>
            Il n'y a personne avec ce nom ici.
            <BLANKLINE>
        """
        for character in self.current_room.characters:
            if character.name.lower() == name.lower():
                return L.PLAYER_TALK_TEMPLATE.format(name=character.name, line=character.get_msg())

        return L.PLAYER_TALK_NOT_FOUND

    def check(self):
        """Return the formatted inventory content."""
        return self.get_inventory()

    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.

        Args:
            reward (str): The reward to add.

        Examples:

        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
           # print(f"\n🎁 Vous avez obtenu: {reward}\n")    redondance ???

    def show_rewards(self):
        """
        Display all rewards earned by the player.

        Examples:

        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print(L.PLAYER_REWARDS_EMPTY)
        else:
            print(L.PLAYER_REWARDS_HEADER)
            for reward in self.rewards:
                print(L.PLAYER_REWARDS_ITEM.format(reward=reward))
            print()

    def get_history(self):
        """Return a formatted list of unique rooms visited by the player."""
        if not self.history:
            return L.PLAYER_HISTORY_EMPTY


        seen = []
        res = L.PLAYER_HISTORY_HEADER


        for room in self.history:
            if room not in seen:
                seen.append(room)
                res += f"    - {room.name}\n"


        return res
