"""Command actions executed from parsed player input."""

# Description: The actions module.


# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.

from quest import STATE_ACTIVE
from command import parse_quest_id, parse_context_index, parse_status
import labels as L


# The error message is stored in the MSG0 and MSG1 variables and formatted with the
# command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = L.COMMAND_NO_PARAM
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = L.COMMAND_ONE_PARAM
INVALID_CONTEXT_CMD = L.COMMAND_INVALID_CONTEXT


class Actions:
    """Namespace for command handlers."""

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).


        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False


        """

        player = game.player
        l = len(list_of_words)


        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command=command_word))
            return False


        direction_input = list_of_words[1]


        # --- normalisation ---
        direction_map = {
            "N": "N", "NORD": "N", "Nord": "N", "nord": "N", "n": "N",
            "S": "S", "SUD": "S", "Sud": "S", "sud": "S", "s": "S",
            "E": "E", "EST": "E", "Est": "E", "est": "E", "e": "E",
            "O": "O", "OUEST": "O", "Ouest": "O", "ouest": "O", "o": "O",
            "U": "U", "UP": "U", "Up": "U", "up": "U", "u": "U",
            "D": "D", "DOWN": "D", "Down": "D", "down": "D", "d": "D",
        }


        # --- direction invalide ---
        if direction_input not in direction_map:
            print(L.COMMAND_INVALID_DIRECTION.format(direction=direction_input))
            # 👉 on réaffiche la salle actuelle
            print(game.get_room_view())
            return False


        direction = direction_map[direction_input]


        success = player.move(direction)
        # Check room visit objectives
        player.quest_manager.check_room_objectives(player.current_room.name)
        if success:
            room_callback = getattr(game, "room_change_callback", None)
            if callable(room_callback):
                room_callback()
            print(player.get_history())
        return success

    @staticmethod
    def back(game, list_of_words, _number_of_parameters):
        """Revenir à la pièce précédente dans l'historique du joueur.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> go(game, ["go", "N"], 1)
            True
            >>> back(game, ["back"], 0)
            True
            >>> back(game, ["back", "N"], 0)
            False
        """

        player = game.player
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False
        if not player.history:
            print(L.COMMAND_BACK_NOT_POSSIBLE)
            print(game.get_room_view())
            return False

        previous_room = player.history.pop()
        player.current_room = previous_room
        room_callback = getattr(game, "room_change_callback", None)
        if callable(room_callback):
            room_callback()

        print(game.get_room_view())
        print(player.get_history())

        return True

    @staticmethod
    def look(game, list_of_words, _number_of_parameters):
        """Regarder la pièce courante.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> look(game, ["look"], 0)
            True
        """
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False

        room = game.player.current_room
        res = game.get_room_view(room)
        res += "\n" + room.format_items() + "\n"
        res += "\n" + room.get_enemies() + "\n"
        res += "\n" + room.format_characters() + "\n"
        if game.current_world == 4 and room.name == "Landing Valley":
            game.player.novaterra_observed_planet = True
        print(res)
        return True

    @staticmethod
    def talk(game, list_of_words, _number_of_parameters):
        """Faire parler un personnage de la piece courante via un index."""
        index = parse_context_index(list_of_words)
        if index is None:
            print(INVALID_CONTEXT_CMD)
            return False

        room = game.player.current_room
        characters = room.get_characters()
        if index < 1 or index > len(characters):
            print(L.COMMAND_INVALID_INDEX)
            return False

        target = characters[index - 1]

        if getattr(target, "on_talk", None):
            response = target.on_talk(game, target)
            if response:
                print(response)
        else:
            print(L.PLAYER_TALK_TEMPLATE.format(name=target.name, line=target.get_msg()))

        game.handle_world1_talk(target.name)
        game.handle_world2_talk(target.name)
        game.handle_world3_talk(target.name)
        game.handle_world4_talk(target.name)
        game.player.quest_manager.check_action_objectives("parler", target.name)

        return True

    @staticmethod
    def take(game, list_of_words, _number_of_parameters):
        """Prendre un item de la piece courante via un index."""
        index = parse_context_index(list_of_words)
        if index is None:
            print(INVALID_CONTEXT_CMD)
            return False

        player = game.player
        room = player.current_room
        items = room.get_items()
        if index < 1 or index > len(items):
            print(L.COMMAND_INVALID_INDEX)
            return False

        item = items[index - 1]
        if (player.weight + item.weight) > player.max_weight:
            print(L.COMMAND_TAKE_TOO_HEAVY.format(item=item))
            return False

        player.inventory.append(item)
        room.inventory.remove(item)
        player.weight += item.weight
        player.apply_passive_item_effect(item, 1)
        print(L.COMMAND_TAKE_SUCCESS.format(item=item))
        if getattr(item, "on_pickup", None):
            message = item.on_pickup(player, game)
            if message:
                print(message)
        player.quest_manager.check_action_objectives("prendre", item.name)
        return True

    @staticmethod
    def drop(game, list_of_words, _number_of_parameters):
        """Deposer un item de l'inventaire via un index."""
        index = parse_context_index(list_of_words)
        if index is None:
            print(INVALID_CONTEXT_CMD)
            return False

        player = game.player
        items = player.inventory
        if index < 1 or index > len(items):
            print(L.COMMAND_INVALID_INVENTORY_INDEX)
            return False

        item = items[index - 1]
        player.inventory.remove(item)
        player.current_room.inventory.append(item)
        player.weight -= item.weight
        player.apply_passive_item_effect(item, -1)
        print(L.COMMAND_DROP_SUCCESS.format(item=item))
        return True

    @staticmethod
    def use(game, list_of_words, _number_of_parameters):
        """Utiliser un item de l'inventaire via un index."""
        index = parse_context_index(list_of_words)
        if index is None:
            print(INVALID_CONTEXT_CMD)
            return False

        player = game.player
        items = player.inventory
        if index < 1 or index > len(items):
            print(L.COMMAND_INVALID_INVENTORY_INDEX)
            return False

        item = items[index - 1]
        if not item.usable:
            print(L.COMMAND_USE_NOT_USABLE.format(item=item.name))
            return False

        message, consume = player.apply_item_effect(item)
        if consume:
            player.inventory.remove(item)
            player.weight -= item.weight
        print(message)
        return True


    # Ne sert à rien pour l'instant
    @staticmethod
    def attack(game, list_of_words, _number_of_parameters):
        """Attaquer un ennemi présent dans la pièce courante."""
        if len(list_of_words) < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command=command_word))
            return False

        target_name = " ".join(list_of_words[1:])
        room = game.player.current_room

        if not room.enemies:
            print(L.COMMAND_NO_ENEMY)
            return False

        enemy = None
        for candidate in room.enemies:
            if candidate.name.lower() == target_name.lower():
                enemy = candidate
                break

        if enemy is None:
            print(L.COMMAND_UNKNOWN_ENEMY.format(enemy=target_name))
            return False

        if enemy.name.lower() == "vorn":
            quest = game.player.quest_manager.get_quest_by_id(4)
            if not quest or quest.state != STATE_ACTIVE:
                print(L.VORN_LOCKED_TEXT)
                return False

        game.resolve_combat(game.player, enemy)
        return True

    @staticmethod
    def check(game, list_of_words, _number_of_parameters):
        """
        Vérifie l'état d'un objet dans la pièce courante.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> check(game, ["check"], 0)
            True
        """
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False

        print(game.player.check())
        return True

    @staticmethod
    def status(game, list_of_words, _number_of_parameters):
        """Afficher l'etat global du personnage."""
        if not parse_status(list_of_words):
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False

        player = game.player
        stability_state = player.get_stability_state()
        completed, total = player.get_completed_quests_count()
        print(
            L.STATUS_TEMPLATE.format(
                hp=player.hp,
                max_hp=player.max_hp,
                atk=player.atk,
                state=stability_state,
                completed=completed,
                total=total,
            )
        )
        return True

    @staticmethod
    def history(game, list_of_words, _number_of_parameters):
        """Affiche l'historique des actions du joueur.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise.
        Examples:
            >>> from game import Game
            >>> game = Game()
            >>> game.setup()
            >>> history(game, ["history"], 0)
            True
        """
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False


        print(game.player.get_history())
        return True

    @staticmethod
    def map(game, list_of_words, _number_of_parameters):
        """Afficher la carte ASCII et la position du joueur."""
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False

        current_room = game.player.current_room
        print(game.world.get_ascii_map(current_room.name))
        return True

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.


        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False


        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False

        # Set the finished attribute of the game object to True.
        player = game.player
        msg = L.QUIT_MESSAGE.format(name=player.name)
        print(msg)
        game.finished = True
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.


        Returns:
            bool: True if the command was executed successfully, False otherwise.


        Examples:


        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False


        """


        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False

        # Print the list of available commands.
        print(L.HELP_HEADER)
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True

    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command=command_word))
            return False

        quest_id = parse_quest_id(list_of_words)
        if quest_id is None:
            print(L.COMMAND_QUEST_ID_INVALID)
            return False

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_id, current_counts)
        return True

    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command=command_word))
            return False

        quest_id = parse_quest_id(list_of_words)
        if quest_id is None:
            print(L.COMMAND_QUEST_ID_INVALID)
            return False

        # Try to activate the quest
        if game.player.activate_quest(quest_id):
            game.update_world1_quests(activated_quest_id=quest_id)
            return True

        print(L.COMMAND_QUEST_ACTIVATE_FAILED.format(quest_id=quest_id))
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False

    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True
