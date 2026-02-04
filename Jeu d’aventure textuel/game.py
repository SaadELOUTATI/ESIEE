"""Main game loop and orchestration for Vigilant."""

# pylint: disable=too-many-lines,too-many-public-methods,too-many-instance-attributes
# pylint: disable=too-many-branches,too-many-statements

# Import modules


from world import (
    World,
    PRISON,
    DISTRICT_OR,
    QUARTIER_HOLO,
    NOEUD,
    PALAIS_LUMIERE,
    SALLE_TRONE,
    LANDING_VALLEY,
    ANCIENT_NEXUS,
)
from player import Player
from character import Character, novaterra_companion_reactive
from command import Command
from actions import Actions
from quest import Quest, STATE_AVAILABLE, STATE_LOCKED, STATE_ACTIVE, STATE_COMPLETED
import labels as L
import ai_quiz
from item import Item
from enemy import Enemy


class Game:
    """Coordinate world state, commands, and narrative flow."""



    # Constructor
    def __init__(self):
        """Initialize the game state containers."""
        self.finished = False
        self.rooms = {}
        self.commands = {}
        self.player = None
        self.world = None
        self.world1_quests = {}
        self.world2_quests = {}
        self.world3_quests = {}
        self.world4_quests = {}
        self.current_world = 1
        self.input_func = input

   # Setup player and starting room
    def setup_player(self, player_name=None):
        """Prompt for the player's name and place them in the starting room."""
        name = player_name
        if not name:
            name = self.input_func(
                L.PLAYER_NAME_PROMPT.format(default=L.DEFAULT_PLAYER_NAME)
            ).strip()
        if not name:
            name = L.DEFAULT_PLAYER_NAME
        self.player = Player(name)
        self.player.current_room = self.world.get_starting_room()

    # Setup world
    def setup_world(self):
        """Create the initial world and load its rooms."""
        self.world = World(world_id=1)
        self.rooms = self.world.rooms

    def set_input_provider(self, provider):
        """Override the input function used for prompts and choices."""
        self.input_func = provider

    def intro(self):
        """Narration d'introduction et choix initial binaire."""
        for line in L.INTRO_LINES:
            print(line)
        print()

    def choice_intro(self):
        """Affiche le choix moral initial et applique les consequences."""
        for line in L.CHOICE_ALERT_LINES:
            print(line)

        choice = ""
        while choice not in ("1", "2"):
            choice = self.input_func("> ").strip()

        # Objet narratif commun
        translator = Item(
            L.INTRO_TRANSLATOR_NAME,
            L.INTRO_TRANSLATOR_DESC,
            1,
        )
        self.player.inventory.append(translator)
        self.player.weight += translator.weight

        if choice == "1":
            self.player.origin_choice = "crew"
            kit = Item(
                L.INTRO_CREW_KIT_NAME,
                L.INTRO_CREW_KIT_DESC,
                1,
                effect_type="heal",
                effect_value=25,
                usable=True,
            )
            self.player.inventory.append(kit)
            self.player.weight += kit.weight
            for line in L.CHOICE_CREW_LINES:
                print(line)
        else:
            self.player.origin_choice = "resources"
            cristal = Item(
                L.INTRO_RESOURCE_CRYSTAL_NAME,
                L.INTRO_RESOURCE_CRYSTAL_DESC,
                1,
            )
            self.player.inventory.append(cristal)
            self.player.weight += cristal.weight
            self.player.has_crystal = True
            module = Item(
                L.INTRO_RESOURCE_MODULE_NAME,
                L.INTRO_RESOURCE_MODULE_DESC,
                1,
            )
            self.player.inventory.append(module)
            self.player.weight += module.weight
            for line in L.CHOICE_RESOURCES_LINES:
                print(line)

        print(self.get_room_view())

    def get_room_view(self, room=None):
        """Retourne la description complete de la salle courante."""
        if room is None:
            room = self.player.current_room
        if self.current_world != 3:
            return room.get_long_description(self.player.stability)

        description_text = self._get_world3_room_description(room)
        lowered = description_text.lstrip().lower()
        if lowered.startswith(("un ", "une ", "des ", "du ", "de ", "d'")):
            body = L.ROOM_DESCRIPTION_PREFIX.format(description=description_text)
        else:
            body = description_text
        return L.ROOM_LONG_DESCRIPTION_TEMPLATE.format(
            name=room.name,
            body=body,
            exits=room.get_exit_string(),
        )

    def _get_world3_room_description(self, room):
        """Retourne une description alternative du Monde 3 selon les choix narratifs."""
        player = self.player
        if room.name == DISTRICT_OR:
            if player.ap_choice_infiltrate and getattr(room, "alt_description_infiltrate", None):
                return room.alt_description_infiltrate
            if player.ap_choice_reveal and getattr(room, "alt_description_reveal", None):
                return room.alt_description_reveal
        if room.name == NOEUD:
            if player.ap_break_illusions and getattr(room, "alt_description_break", None):
                return room.alt_description_break
            if player.ap_keep_illusions and getattr(room, "alt_description_keep", None):
                return room.alt_description_keep
        return room.description

    def setup_commands(self):
        """Register all available command handlers."""
        self.commands["help"] = Command(
            "help", L.COMMAND_HELP_STRINGS["help"], Actions.help, 0
        )
        self.commands["quit"] = Command(
            "quit", L.COMMAND_HELP_STRINGS["quit"], Actions.quit, 0
        )
        self.commands["go"] = Command(
            "go",
            L.COMMAND_HELP_STRINGS["go"],
            Actions.go,
            1,
        )
        self.commands["history"] = Command(
            "history", L.COMMAND_HELP_STRINGS["history"], Actions.history, 0
        )
        self.commands["back"] = Command(
            "back", L.COMMAND_HELP_STRINGS["back"], Actions.back, 0
        )
        self.commands["look"] = Command("look", L.COMMAND_HELP_STRINGS["look"], Actions.look, 0)
        self.commands["take"] = Command("take", L.COMMAND_HELP_STRINGS["take"], Actions.take, 1)
        self.commands["drop"] = Command("drop", L.COMMAND_HELP_STRINGS["drop"], Actions.drop, 1)
        self.commands["use"] = Command("use", L.COMMAND_HELP_STRINGS["use"], Actions.use, 1)
        self.commands["check"] = Command("check", L.COMMAND_HELP_STRINGS["check"], Actions.check, 0)
        self.commands["status"] = Command(
            "status",
            L.COMMAND_HELP_STRINGS["status"],
            Actions.status,
            0,
        )
        self.commands["talk"] = Command(
            "talk", L.COMMAND_HELP_STRINGS["talk"], Actions.talk, 1
        )
        self.commands["attack"] = Command(
            "attack", L.COMMAND_HELP_STRINGS["attack"], Actions.attack, 1
        )
        self.commands["map"] = Command("map", L.COMMAND_HELP_STRINGS["map"], Actions.map, 0)
        self.commands["quests"] = Command(
            "quests", L.COMMAND_HELP_STRINGS["quests"], Actions.quests, 0
        )
        self.commands["quest"] = Command(
            "quest", L.COMMAND_HELP_STRINGS["quest"], Actions.quest, 1
        )
        self.commands["activate"] = Command(
            "activate", L.COMMAND_HELP_STRINGS["activate"], Actions.activate, 1
        )
        self.commands["rewards"] = Command(
            "rewards", L.COMMAND_HELP_STRINGS["rewards"], Actions.rewards, 0
        )

    def _setup_quests(self):
        """Initialize all quests."""
        self._setup_world1_quests()


    def _setup_world1_quests(self):
        """Initialise les quetes specifiques au Monde 1 (Eridani Prime)."""
        data = L.QUESTS_WORLD1
        quest_1 = Quest(
            title=data[1]["title"],
            description=data[1]["description"],
            objectives=data[1]["objectives"],
            quest_id=1,
            state=STATE_AVAILABLE,
        )
        quest_2 = Quest(
            title=data[2]["title"],
            description=data[2]["description"],
            objectives=data[2]["objectives"],
            quest_id=2,
            state=STATE_LOCKED,
        )
        quest_3 = Quest(
            title=data[3]["title"],
            description=data[3]["description"],
            objectives=data[3]["objectives"],
            quest_id=3,
            state=STATE_LOCKED,
        )
        quest_4 = Quest(
            title=data[4]["title"],
            description=data[4]["description"],
            objectives=data[4]["objectives"],
            quest_id=4,
            state=STATE_LOCKED,
        )

        self.world1_quests = {
            1: quest_1,
            2: quest_2,
            3: quest_3,
            4: quest_4,
        }

        for quest in self.world1_quests.values():
            self.player.quest_manager.add_quest(quest)

        quest_1.set_state(STATE_ACTIVE)
        if quest_1 not in self.player.quest_manager.active_quests:
            self.player.quest_manager.active_quests.append(quest_1)

        self.player.current_world_quests = [quest_1, quest_2, quest_3, quest_4]

    def _setup_world2_quests(self):
        """Initialize world 2 quests and reset the quest manager."""
        data = L.QUESTS_WORLD2
        self.world2_quests = {}
        self.player.quest_manager.reset()

        quest_1 = Quest(
            title=data[1]["title"],
            description=data[1]["description"],
            objectives=data[1]["objectives"],
            quest_id=1,
            state=STATE_AVAILABLE,
        )
        quest_2 = Quest(
            title=data[2]["title"],
            description=data[2]["description"],
            objectives=data[2]["objectives"],
            quest_id=2,
            state=STATE_LOCKED,
        )
        quest_3 = Quest(
            title=data[3]["title"],
            description=data[3]["description"],
            objectives=data[3]["objectives"],
            quest_id=3,
            state=STATE_LOCKED,
        )
        quest_4 = Quest(
            title=data[4]["title"],
            description=data[4]["description"],
            objectives=data[4]["objectives"],
            quest_id=4,
            state=STATE_LOCKED,
        )

        self.world2_quests = {
            1: quest_1,
            2: quest_2,
            3: quest_3,
            4: quest_4,
        }

        for quest in self.world2_quests.values():
            self.player.quest_manager.add_quest(quest)

        quest_1.set_state(STATE_ACTIVE)
        if quest_1 not in self.player.quest_manager.active_quests:
            self.player.quest_manager.active_quests.append(quest_1)

        self.player.current_world_quests = [quest_1, quest_2, quest_3, quest_4]

    def _setup_world3_quests(self):
        """Initialise les quetes du Monde 3 (Aurelion Prime)."""
        data = L.QUESTS_WORLD3
        self.world3_quests = {}
        self.player.quest_manager.reset()

        quest_1 = Quest(
            title=data[1]["title"],
            description=data[1]["description"],
            objectives=data[1]["objectives"],
            quest_id=1,
            state=STATE_ACTIVE,
        )
        quest_2 = Quest(
            title=data[2]["title"],
            description=data[2]["description"],
            objectives=data[2]["objectives"],
            quest_id=2,
            state=STATE_LOCKED,
        )
        quest_3 = Quest(
            title=data[3]["title"],
            description=data[3]["description"],
            objectives=data[3]["objectives"],
            quest_id=3,
            state=STATE_LOCKED,
        )
        quest_4 = Quest(
            title=data[4]["title"],
            description=data[4]["description"],
            objectives=data[4]["objectives"],
            quest_id=4,
            state=STATE_LOCKED,
        )
        quest_5 = Quest(
            title=data[5]["title"],
            description=data[5]["description"],
            objectives=data[5]["objectives"],
            quest_id=5,
            state=STATE_LOCKED,
        )
        quest_6 = Quest(
            title=data[6]["title"],
            description=data[6]["description"],
            objectives=data[6]["objectives"],
            quest_id=6,
            state=STATE_LOCKED,
        )

        self.world3_quests = {
            1: quest_1,
            2: quest_2,
            3: quest_3,
            4: quest_4,
            5: quest_5,
            6: quest_6,
        }

        for quest in self.world3_quests.values():
            self.player.quest_manager.add_quest(quest)

        if quest_1 not in self.player.quest_manager.active_quests:
            self.player.quest_manager.active_quests.append(quest_1)

        self.player.current_world_quests = [
            quest_1,
            quest_2,
            quest_3,
            quest_4,
            quest_5,
            quest_6,
        ]

    def _setup_world4_quests(self):
        """Initialise les quetes du Monde 4 (Nova Terra)."""
        data = L.QUESTS_WORLD4
        self.world4_quests = {}
        self.player.quest_manager.reset()

        quest_1 = Quest(
            title=data[1]["title"],
            description=data[1]["description"],
            objectives=data[1]["objectives"],
            quest_id=1,
            state=STATE_ACTIVE,
        )
        station_objective = (
            data[2]["objectives"]["explore"][0]
            if self.player.novaterra_explored_station
            else data[2]["objectives"]["ignore"][0]
        )
        quest_2 = Quest(
            title=data[2]["title"],
            description=data[2]["description"],
            objectives=[station_objective],
            quest_id=2,
            state=STATE_LOCKED,
        )
        quest_3 = Quest(
            title=data[3]["title"],
            description=data[3]["description"],
            objectives=data[3]["objectives"],
            quest_id=3,
            state=STATE_LOCKED,
        )

        self.world4_quests = {
            1: quest_1,
            2: quest_2,
            3: quest_3,
        }

        for quest in self.world4_quests.values():
            self.player.quest_manager.add_quest(quest)

        if quest_1 not in self.player.quest_manager.active_quests:
            self.player.quest_manager.active_quests.append(quest_1)

        self.player.current_world_quests = [quest_1, quest_2, quest_3]

    def _is_current_world_complete(self):
        """Return True when the current world's quests are all completed."""
        quests = self.player.current_world_quests
        if not quests:
            return False
        return all(quest.state == STATE_COMPLETED for quest in quests)

    def _check_world_transition(self):
        """Trigger a world transition when the current world is complete."""
        if not self._is_current_world_complete():
            return
        self.transition_to_next_world()

    def transition_to_next_world(self):
        """Advance to the next world and initialize its content."""
        if self.current_world == 1:
            print(L.WORLD1_TRANSITION_TEXT)

            self.current_world = 2
            self.world = World(world_id=2)
            self.rooms = self.world.rooms
            self.player.current_room = self.world.get_starting_room()
            self.player.history = []
            self._setup_world2_quests()
            self.player.hp = self.player.max_hp
            print(self.get_room_view())
            return

        if self.current_world == 2:
            if not self.player.karn_aftermath_done:
                return
            print(L.WORLD2_TRANSITION_TEXT)
            self.current_world = 3
            self.world = World(world_id=3)
            self.rooms = self.world.rooms
            self.player.current_room = self.world.get_starting_room()
            self.player.history = []
            self._setup_world3_quests()
            self.player.hp = self.player.max_hp
            self._handle_aurelion_posture_choice()
            self.update_world3_quests()
            self.player.quest_manager.check_room_objectives(self.player.current_room.name)
            print(self.get_room_view())
            return

        if self.current_world == 3:
            self.transition_to_world4()
            return

    def update_world1_quests(self, activated_quest_id=None):
        """Met à jour l'état des quêtes Monde 1 en fonction des flags joueur."""
        if self.current_world != 1:
            return
        q1 = self.world1_quests.get(1)
        if q1 and q1.state == STATE_ACTIVE and not q1.is_completed and self.player.met_ralen:
            q1.complete_objective(q1.objectives[0], self.player)
            if q1.is_completed and q1 in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(q1)

        q2 = self.world1_quests.get(2)
        if q1 and q1.is_completed and q2 and q2.state == STATE_LOCKED:
            q2.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q2.quest_id)

        if (
            q2
            and q2.state == STATE_ACTIVE
            and not q2.is_completed
            and self.player.patrollers_defeated
        ):
            q2.complete_objective(q2.objectives[0], self.player)
            if q2.is_completed and q2 in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(q2)

        q3 = self.world1_quests.get(3)
        if q2 and q2.is_completed and q3 and q3.state == STATE_LOCKED:
            q3.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q3.quest_id)

        if q3 and q3.state == STATE_ACTIVE and not q3.is_completed:
            if self.player.has_crystal:
                if activated_quest_id == 3:
                    print(L.CRYSTAL_REALIZATION_TEXT)
                q3.complete_objective(q3.objectives[0], self.player)
                if q3.is_completed and q3 in self.player.quest_manager.active_quests:
                    self.player.quest_manager.active_quests.remove(q3)

        q4 = self.world1_quests.get(4)
        if q3 and q3.is_completed and q4 and q4.state == STATE_LOCKED:
            q4.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q4.quest_id)

        if q4 and q4.state == STATE_ACTIVE and not q4.is_completed and self.player.vorn_defeated:
            q4.complete_objective(q4.objectives[0], self.player)
            if q4.is_completed and q4 in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(q4)

        self._check_world_transition()

    def check_world1_npc_bonus(self):
        """Accorde le bonus de stabilité si tous les PNJ clés ont été rencontrés."""
        if self.current_world != 1:
            return
        player = self.player
        if player.world1_npcs_bonus:
            return

        if (
            player.met_ralen and player.met_malek and player.met_marchand
            and player.met_yara and player.met_nommera
        ):
            player.world1_npcs_bonus = True
            self.adjust_stability(1)

    def handle_merchant_choice(self):
        """Gere le choix moral du marchand et ses effets sur la stabilite."""
        player = self.player
        if player.merchant_sacrifice or player.merchant_refused:
            return

        for line in L.MERCHANT_CHOICE_LINES:
            print(line)
        choice = ""
        while choice not in ("1", "2"):
            choice = self.input_func("> ").strip()

        if choice == "1":
            self.adjust_stability(-3)
            if not player.has_crystal:
                cristal = Item(
                    "Cristal de propulsion",
                    "Un cristal intact, essentiel pour reparer le vaisseau.",
                    1,
                )
                player.inventory.append(cristal)
                player.weight += cristal.weight
            player.has_crystal = True
            player.merchant_sacrifice = True
            print(L.MERCHANT_ACCEPTED_TEXT)
        else:
            self.adjust_stability(1)
            player.merchant_refused = True
            player.met_yara = True
            print(L.MERCHANT_REFUSED_TEXT)
            if not player.has_crystal:
                print(L.MERCHANT_NO_CRYSTAL_TEXT)
                self.finished = True
                return

        self.update_world1_quests()
        self.check_world1_npc_bonus()

    def handle_world1_talk(self, character_name):
        """Met a jour les flags Monde 1 apres un dialogue."""
        if self.current_world != 1:
            return
        name = character_name.lower()
        if name == "ralen":
            self.player.met_ralen = True
        elif "malek" in name:
            self.player.met_malek = True
        elif name == "marchand":
            self.player.met_marchand = True
        elif name == "yara":
            self.player.met_yara = True
        elif name == "nommera":
            self.player.met_nommera = True

        self.update_world1_quests()
        self.check_world1_npc_bonus()

    def handle_world2_talk(self, character_name):
        """Met a jour les flags Monde 2 apres un dialogue."""
        if self.current_world != 2:
            return
        name = character_name.lower()
        if name == "yara":
            self.player.velyra_met_leader = True
        elif name == "narek":
            self.player.velyra_narek_resolved = True

        self.update_world2_quests()

    def handle_world3_talk(self, character_name):
        """Met a jour les flags Monde 3 apres un dialogue."""
        if self.current_world != 3:
            return
        name = character_name.lower()
        if name == "citoyen dore":
            self.player.ap_citizen_spoken = True
        elif name == "habitant glitche":
            self.player.ap_glitch_spoken = True

        self.update_world3_quests()

    def handle_world4_talk(self, character_name):
        """Met a jour les flags Monde 4 apres un dialogue."""
        if self.current_world != 4:
            return
        name = character_name.lower()
        if name in ("yara", "narek", "le guide"):
            self.player.novaterra_companion_spoken = True

        self.update_world4_quests()

    def update_world2_quests(self):
        """Met a jour l'etat des quetes Monde 2 en fonction des actions du joueur."""
        if self.current_world != 2:
            return

        player = self.player
        q1 = self.world2_quests.get(1)
        q2 = self.world2_quests.get(2)
        q3 = self.world2_quests.get(3)
        q4 = self.world2_quests.get(4)

        if not player.velyra_resources_secured and player.has_item(
            L.ITEM_DEFINITIONS["keycard"]["name"]
        ):
            player.velyra_resources_secured = True

        if q1 and q1.state == STATE_ACTIVE and not q1.is_completed:
            if player.velyra_method:
                q1.complete_objective(q1.objectives[0], player)
                if q1.is_completed and q1 in self.player.quest_manager.active_quests:
                    self.player.quest_manager.active_quests.remove(q1)

        if q1 and q1.is_completed and q2 and q2.state == STATE_LOCKED:
            q2.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q2.quest_id)

        if q2 and q2.state == STATE_ACTIVE and not q2.is_completed:
            if player.has_item(L.ITEM_DEFINITIONS["keycard"]["name"]):
                q2.complete_objective(q2.objectives[0], player)
                if q2.is_completed and q2 in self.player.quest_manager.active_quests:
                    self.player.quest_manager.active_quests.remove(q2)

        if q2 and q2.is_completed and q3 and q3.state == STATE_LOCKED:
            q3.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q3.quest_id)

        if q3 and q3.state == STATE_ACTIVE and not q3.is_completed:
            if player.velyra_narek_resolved:
                q3.complete_objective(q3.objectives[0], player)
                if q3.is_completed and q3 in self.player.quest_manager.active_quests:
                    self.player.quest_manager.active_quests.remove(q3)

        if q3 and q3.is_completed and q4 and q4.state == STATE_LOCKED:
            q4.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q4.quest_id)

        if q4 and q4.state == STATE_ACTIVE and not q4.is_completed:
            if player.karn_defeated:
                q4.complete_objective(q4.objectives[0], player)
                if q4.is_completed and q4 in self.player.quest_manager.active_quests:
                    self.player.quest_manager.active_quests.remove(q4)

        if q4 and q4.is_completed:
            self._check_world_transition()

    def update_world3_quests(self):
        """Met a jour l'etat des quetes Monde 3 en fonction des actions du joueur."""
        if self.current_world != 3:
            return

        player = self.player
        q1 = self.world3_quests.get(1)
        q2 = self.world3_quests.get(2)
        q3 = self.world3_quests.get(3)
        q4 = self.world3_quests.get(4)
        q5 = self.world3_quests.get(5)
        q6 = self.world3_quests.get(6)

        if q1 and q1.state == STATE_ACTIVE and not q1.is_completed:
            if not (player.ap_choice_infiltrate or player.ap_choice_reveal):
                self._handle_aurelion_posture_choice()
            if player.ap_choice_infiltrate or player.ap_choice_reveal:
                q1.complete_objective(q1.objectives[0], player)
                if q1.is_completed and q1 in self.player.quest_manager.active_quests:
                    self.player.quest_manager.active_quests.remove(q1)

        if q1 and q1.is_completed and q2 and q2.state == STATE_LOCKED:
            q2.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q2.quest_id)

        if q2 and q2.state == STATE_ACTIVE and not q2.is_completed:
            if player.current_room.name == DISTRICT_OR:
                q2.complete_objective(q2.objectives[0], player)
            if player.ap_citizen_spoken:
                q2.complete_objective(q2.objectives[1], player)
            if (
                player.current_room.name == QUARTIER_HOLO
                or any(room.name == QUARTIER_HOLO for room in player.history)
            ):
                q2.complete_objective(q2.objectives[2], player)
            if q2.is_completed and q2 in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(q2)

        if q2 and q2.is_completed and q3 and q3.state == STATE_LOCKED:
            q3.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q3.quest_id)

        if q3 and q3.state == STATE_ACTIVE and not q3.is_completed:
            if player.attack_holo_done:
                q3.complete_objective(q3.objectives[0], player)
            if player.ap_glitch_spoken:
                q3.complete_objective(q3.objectives[1], player)
            if q3.is_completed and q3 in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(q3)

        if q3 and q3.is_completed and q4 and q4.state == STATE_LOCKED:
            q4.set_state(STATE_AVAILABLE)

        if q4 and q4.state == STATE_AVAILABLE and player.current_room.name == NOEUD:
            self.player.quest_manager.activate_quest(q4.quest_id)

        if q4 and q4.state == STATE_ACTIVE and not q4.is_completed:
            if not (player.ap_break_illusions or player.ap_keep_illusions):
                self._handle_aurelion_node_choice()
            if player.ap_break_illusions or player.ap_keep_illusions:
                q4.complete_objective(q4.objectives[0], player)
                if q4.is_completed and q4 in self.player.quest_manager.active_quests:
                    self.player.quest_manager.active_quests.remove(q4)

        if q4 and q4.is_completed and q5 and q5.state == STATE_LOCKED:
            q5.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q5.quest_id)

        if q5 and q5.state == STATE_ACTIVE and not q5.is_completed:
            if (
                player.current_room.name == PALAIS_LUMIERE
                or any(room.name == PALAIS_LUMIERE for room in player.history)
            ):
                q5.complete_objective(q5.objectives[0], player)
            if (
                player.current_room.name == SALLE_TRONE
                or any(room.name == SALLE_TRONE for room in player.history)
            ):
                q5.complete_objective(q5.objectives[1], player)
            if q5.is_completed and q5 in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(q5)

        if q5 and q5.is_completed and q6 and q6.state == STATE_LOCKED:
            q6.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q6.quest_id)

        if q6 and q6.state == STATE_ACTIVE and not q6.is_completed:
            if player.ap_taal_confronted:
                q6.complete_objective(q6.objectives[0], player)
            if player.ap_taal_alliance or player.ap_taal_dead:
                q6.complete_objective(q6.objectives[1], player)
                if q6.is_completed and q6 in self.player.quest_manager.active_quests:
                    self.player.quest_manager.active_quests.remove(q6)

    def update_world4_quests(self):
        """Met a jour l'etat des quetes Monde 4 en fonction des actions du joueur."""
        if self.current_world != 4:
            return

        player = self.player
        q1 = self.world4_quests.get(1)
        q2 = self.world4_quests.get(2)
        q3 = self.world4_quests.get(3)

        if q1 and q1.state == STATE_ACTIVE and not q1.is_completed:
            if (
                player.current_room.name == LANDING_VALLEY
                or any(room.name == LANDING_VALLEY for room in player.history)
            ):
                q1.complete_objective(q1.objectives[0], player)
            if player.novaterra_observed_planet:
                q1.complete_objective(q1.objectives[1], player)
            if player.novaterra_companion_spoken:
                q1.complete_objective(q1.objectives[2], player)
            if q1.is_completed and q1 in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(q1)

        if q1 and q1.is_completed and q2 and q2.state == STATE_LOCKED:
            q2.set_state(STATE_AVAILABLE)
            self.player.quest_manager.activate_quest(q2.quest_id)

        if q2 and q2.state == STATE_ACTIVE and not q2.is_completed:
            objective = (
                L.QUESTS_WORLD4[2]["objectives"]["explore"][0]
                if player.novaterra_explored_station
                else L.QUESTS_WORLD4[2]["objectives"]["ignore"][0]
            )
            q2.complete_objective(objective, player)
            if q2.is_completed and q2 in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(q2)

        if q2 and q2.is_completed and q3 and q3.state == STATE_LOCKED:
            q3.set_state(STATE_AVAILABLE)

        if q3 and q3.state == STATE_AVAILABLE:
            if (
                player.current_room.name == ANCIENT_NEXUS
                or any(room.name == ANCIENT_NEXUS for room in player.history)
            ):
                self.player.quest_manager.activate_quest(q3.quest_id)
                q3.complete_objective(q3.objectives[0], player)
                listened = q3.complete_objective(q3.objectives[1], player)
                if listened:
                    print(L.NEXUS_LISTEN_TEXT)

    def check_global_defeat(self):
        """Verifie la condition de defaite globale liee a la stabilite."""
        if self.finished:
            return
        if self.player.stability <= 0:
            self._handle_mental_collapse()

    def adjust_stability(self, amount):
        """Ajuste la stabilite globale et declenche le feedback narratif."""
        message, died = self.player.modify_stability(amount)
        if message:
            print(f"\n{message}\n")
        if died:
            self._handle_mental_collapse()

    def _handle_mental_collapse(self):
        """Affiche la mort narrative liee a l'effondrement mental."""
        print(L.MENTAL_COLLAPSE_TEXT)
        self.finished = True

    def _handle_karn_aftermath(self):
        """Gere le choix final apres la chute de Karn."""
        player = self.player
        if player.karn_aftermath_done:
            return
        player.karn_aftermath_done = True

        nanomed_name = L.ITEM_DEFINITIONS["nanomedicine"]["name"]
        if player.has_item(nanomed_name):
            print(L.KARN_AFTERMATH_PROMPT)
            choice = ""
            while choice not in ("1", "2", "yara", "narek", "y", "n"):
                choice = self.input_func("> ").strip().lower()

            for item in list(player.inventory):
                if item.name.lower() == nanomed_name.lower():
                    player.inventory.remove(item)
                    player.weight -= item.weight
                    break

            if choice in ("1", "yara", "y"):
                player.saved_yara = True
                player.narek_dead = True
                print(L.KARN_AFTERMATH_YARA)
            else:
                player.saved_narek = True
                player.yara_dead = True
                print(L.KARN_AFTERMATH_NAREK)

            self.adjust_stability(1)
            return

        player.yara_dead = True
        player.narek_dead = True
        print(L.KARN_AFTERMATH_NONE)
        self.adjust_stability(-1)

    def _handle_aurelion_posture_choice(self):
        """Propose le choix d'infiltration ou de revelation en debut d'Aurelion."""
        player = self.player
        if player.ap_choice_infiltrate or player.ap_choice_reveal:
            return

        print(L.AURELION_POSTURE_LINES)
        for line in L.AURELION_POSTURE_OPTIONS:
            print(line)

        choice = ""
        while choice not in ("1", "2"):
            choice = self.input_func("> ").strip()

        if choice == "1":
            player.ap_choice_infiltrate = True
            print(L.AURELION_POSTURE_INFILTRATE)
        else:
            player.ap_choice_reveal = True
            print(L.AURELION_POSTURE_REVEAL)

    def _handle_aurelion_node_choice(self):
        """Gere le choix irreversible au Noeud."""
        player = self.player
        if player.ap_break_illusions or player.ap_keep_illusions:
            return

        print(L.AURELION_NODE_LINES)
        for line in L.AURELION_NODE_OPTIONS:
            print(line)

        choice = ""
        while choice not in ("1", "2"):
            choice = self.input_func("> ").strip()

        if choice == "1":
            player.ap_break_illusions = True
            self.adjust_stability(-1)
            print(L.AURELION_NODE_BREAK)
        else:
            player.ap_keep_illusions = True
            self.adjust_stability(1)
            print(L.AURELION_NODE_KEEP)

    def _handle_seren_taal_confrontation(self):
        """Gere la confrontation narrative avec Seren Taal dans la Salle du Trone."""
        player = self.player
        if player.ap_taal_alliance or player.ap_taal_dead:
            return True

        quest = None
        if hasattr(self, "world3_quests"):
            quest = self.world3_quests.get(6)
        if not quest or quest.state != STATE_ACTIVE:
            return False

        if not player.ap_taal_confronted:
            print(L.SEREN_CONFRONT_LINES)
            for line in L.SEREN_CONFRONT_OPTIONS:
                print(line)
            choice = ""
            while choice not in ("1", "2"):
                choice = self.input_func("> ").strip()

            if choice == "1":
                player.ap_taal_confronted = True
                player.ap_taal_alliance = True
                print(L.SEREN_ALLIANCE_TEXT)
                if quest:
                    quest.complete_objective(quest.objectives[0], player)
                    quest.complete_objective(quest.objectives[1], player)
                self.end_world3()
                return True

            print(L.SEREN_REFUSE_TEXT)
            player.ap_taal_confronted = True

        room = player.current_room
        seren = None
        for candidate in room.enemies:
            if candidate.name.lower() == "seren taal":
                seren = candidate
                break
        if seren is None:
            seren = Enemy("Seren Taal", hp=60, attack=25)
            room.enemies.append(seren)

        self.resolve_combat(player, seren)
        return True

    def end_world3(self):
        """Clot le monde 3 et lance la transition appropriee."""
        player = self.player
        if player.ap_taal_alliance:
            print(L.SEREN_ALLIANCE_ENDING)
            self.finished = True
            return
        if player.ap_taal_dead:
            print(L.SEREN_VICTORY_ENDING)
            self.transition_to_next_world()
            return

    def transition_to_world4(self):
        """Transition narrative vers Nova Terra avec un choix initial."""
        player = self.player
        if player.world4_started:
            return

        player.world4_started = True

        print(L.WORLD4_TRANSITION_INTRO)
        print(L.WORLD4_TRANSITION_ORBITAL)
        print(L.WORLD4_TRANSITION_CHOICE)
        for line in L.WORLD4_TRANSITION_OPTIONS:
            print(line)

        choice = ""
        while choice not in ("1", "2"):
            choice = self.input_func("> ").strip()

        if choice == "1":
            print(L.WORLD4_CHOICE_PRUDENCE)
            self.adjust_stability(1)
            print("")
        else:
            dmg = min(10, player.hp)
            player.hp = max(0, player.hp - dmg)
            player.novaterra_explored_station = True
            player.atk += 2
            artifact = Item(
                "Artefact alien",
                "Un fragment ancien qui pulse d'une energie inconnue.",
                1,
            )
            player.inventory.append(artifact)
            player.weight += artifact.weight
            print(L.WORLD4_STATION_DOCK)
            print(L.WORLD4_STATION_FLOAT)
            print(L.WORLD4_STATION_EXPLOSION.format(dmg=dmg))
            print(L.WORLD4_STATION_ARTIFACT)
            self.adjust_stability(2)

        self.current_world = 4
        self.world = World(world_id=4)
        self.rooms = self.world.rooms
        self.player.current_room = self.world.get_starting_room()
        self.player.history = []
        self._setup_world4_quests()
        self.player.hp = self.player.max_hp

        valley = self.player.current_room
        companion = None
        if player.saved_yara:
            companion = Character(
                "Yara",
                "Yara, cheffe rebelle d'Eridani, marche a vos cotes. "
                "Ses yeux brillent a la vue de cette nouvelle terre.",
                valley,
                [],
                on_talk=novaterra_companion_reactive,
            )
        elif player.saved_narek:
            companion = Character(
                "Narek",
                "Narek, survivant de Velyra et symbole de resistance, "
                "observe l'horizon avec un melange d'espoir et de nostalgie.",
                valley,
                [],
                on_talk=novaterra_companion_reactive,
            )
        else:
            companion = Character(
                "Le Guide",
                "Une silhouette inconnue vous accompagne, calme et attentive.",
                valley,
                [],
                on_talk=novaterra_companion_reactive,
            )

        if companion:
            valley.characters.append(companion)
            if companion.name.lower() == "le guide":
                print(L.WORLD4_GUIDE_INTRO)

        self.update_world4_quests()

        print(L.WORLD4_CHAPTER_TITLE)
        print(self.get_room_view())

    def _handle_novaterra_final_choice(self):
        """Declenche le choix final a l'Ancient Nexus."""
        player = self.player
        if player.novaterra_final_done:
            return

        quest = None
        if hasattr(self, "world4_quests"):
            quest = self.world4_quests.get(3)
        if quest and quest.state == STATE_ACTIVE and not quest.is_completed:
            quest.complete_objective(quest.objectives[-1], player)
            if quest.is_completed and quest in self.player.quest_manager.active_quests:
                self.player.quest_manager.active_quests.remove(quest)

        print(L.NEXUS_CHOICE_LINES)
        for line in L.NEXUS_OPTIONS:
            print(line)

        choice = ""
        while choice not in ("1", "2", "3"):
            choice = self.input_func("> ").strip()

        if choice == "1":
            player.novaterra_choice_harmony = True
            self.adjust_stability(2)
            self.end_world4()
            return
        if choice == "2":
            player.novaterra_choice_domination = True
            player.atk += 2
            print(L.NEXUS_DOMINATION_COMBAT)
            terra = Enemy("Terra Guardian", hp=70, attack=25)
            player.current_room.enemies.append(terra)
            self.resolve_combat(player, terra)
            if terra in player.current_room.enemies:
                player.current_room.enemies.remove(terra)
            return

        player.novaterra_choice_renounce = True
        self.adjust_stability(3)
        self.end_world4()

    def end_world4(self):
        """Clot le monde 4 et termine la partie."""
        player = self.player
        if player.novaterra_final_done:
            return
        player.novaterra_final_done = True

        print(L.WORLD4_ENDING_TITLE)
        if player.novaterra_choice_harmony:
            for line in L.WORLD4_ENDING_HARMONY:
                print(line)
        elif player.novaterra_choice_domination:
            for line in L.WORLD4_ENDING_DOMINATION:
                print(line)
        elif player.novaterra_choice_renounce:
            for line in L.WORLD4_ENDING_RENOUNCE:
                print(line)

        for line in L.WORLD4_ENDING_FINAL:
            print(line)
        self.finished = True

    def setup(self, player_name=None):
        """Initialize world, player, commands, quests, and intro."""

        # Setup commands
        self.setup_commands()
        # Setup world
        self.setup_world()
        # Setup player
        self.setup_player(player_name=player_name)
        # Setup quests
        self._setup_quests()

        # Print welcome message
        self.print_welcome()
        # Introduction and initial choice
        self.intro()





    # Play the game
    def play(self):
        """Run the main loop: read commands and process triggers."""
        self.setup()

        # Introduction + choix initial
        self.choice_intro()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(self.input_func("> "))

            # Check win/lose conditions
            if self.finished:
                return None
            if self.win():
                print(L.GAME_WIN_TEXT)
                self.finished = True
            elif self.lose():
                print(L.GAME_LOSE_TEXT)
                self.finished = True
            else:
                # Deplacement des PNJ apres chaque tour
                self.character_move()

        return None

    def character_move(self):
        """Move wandering NPCs when applicable."""
        for room in self.rooms.values():
            for character in room.characters:
                character.move()

    def check_auto_combat(self):
        """Declenche automatiquement un combat si un ennemi vivant est present."""
        if self.finished:
            return

        room = self.player.current_room
        if not room.enemies:
            if self.current_world == 4 and room.name == ANCIENT_NEXUS:
                self.update_world4_quests()
                self._handle_novaterra_final_choice()
            if self.current_world == 3 and room.name == SALLE_TRONE:
                quest = None
                if hasattr(self, "world3_quests"):
                    quest = self.world3_quests.get(6)
                if quest and quest.state == STATE_ACTIVE:
                    self._handle_seren_taal_confrontation()
            return

        if self.current_world == 3 and room.name == SALLE_TRONE:
            quest = None
            if hasattr(self, "world3_quests"):
                quest = self.world3_quests.get(6)
            if not quest or quest.state != STATE_ACTIVE:
                return
            if self._handle_seren_taal_confrontation():
                return

        for enemy in list(room.enemies):
            if not enemy.is_alive():
                room.enemies.remove(enemy)
                continue
            if enemy.name.lower() == "capitaine vorn":
                quest = self.player.quest_manager.get_quest_by_id(4)
                if not quest or quest.state != STATE_ACTIVE:
                    print(L.VORN_LOCKED_TEXT)
                    continue
            self.resolve_combat(self.player, enemy)
            if self.finished:
                return

    def resolve_combat(self, player, enemy):
        """Résout un combat automatique piloté par le quiz IA."""
        print(L.COMBAT_START.format(enemy=enemy.name))
        if not enemy.is_alive():
            if enemy in player.current_room.enemies:
                player.current_room.enemies.remove(enemy)
            return False

        severe_injury_applied = False

        while enemy.is_alive() and player.hp > 0:
            try:
                question, expected = ai_quiz.get_question()
                print(L.COMBAT_AI_QUESTION.format(question=question))
            except Exception:  # pylint: disable=broad-exception-caught
                print(L.COMBAT_AI_FALLBACK_NOTICE)
                question = L.COMBAT_AI_FALLBACK_QUESTION
                expected = L.COMBAT_AI_FALLBACK_ANSWER
                print(L.COMBAT_AI_QUESTION.format(question=question))
            answer = self.input_func("> ")
            debug_kill = answer.strip().lower() == "b"
            try:
                player_attacks = debug_kill or ai_quiz.evaluate_answer(None, answer, expected)
            except Exception:  # pylint: disable=broad-exception-caught
                print(L.COMBAT_AI_EVAL_ERROR)
                player_attacks = False

            if player_attacks:
                damage = enemy.hp if debug_kill else player.atk
                dealt = enemy.take_damage(damage)
                print(L.COMBAT_PLAYER_ATTACK.format(enemy=enemy.name, damage=dealt))
                print(L.COMBAT_PLAYER_HP.format(hp=player.hp, max_hp=player.max_hp))
                if enemy.is_alive():
                    print(L.COMBAT_ENEMY_HP.format(enemy=enemy.name, hp=enemy.hp))
                else:
                    print(L.COMBAT_ENEMY_DEFEATED.format(enemy=enemy.name))
                    enemy_name = enemy.name.lower()
                    if "patrouill" in enemy_name:
                        player.patrollers_defeated = True
                    if enemy_name == "spectre holographique":
                        player.attack_holo_done = True
                    if "vorn" in enemy_name:
                        player.vorn_defeated = True
                        self.adjust_stability(2)
                    if enemy_name == "gouverneur karn":
                        player.karn_defeated = True
                        self._handle_karn_aftermath()
                    if enemy_name == "seren taal":
                        player.ap_taal_confronted = True
                        player.ap_taal_dead = True
                        print(L.COMBAT_SEREN_DEFEATED)
                        quest = None
                        if hasattr(self, "world3_quests"):
                            quest = self.world3_quests.get(6)
                        if quest:
                            quest.complete_objective("Confronter Seren Taal", player)
                            quest.complete_objective("Decider du sort de Seren Taal", player)
                        self.end_world3()
                    if enemy_name == "terra guardian":
                        player.novaterra_terra_defeated = True
                        print(L.COMBAT_TERRA_DEFEATED)
                        self.end_world4()
                    if enemy in player.current_room.enemies:
                        player.current_room.enemies.remove(enemy)
                    self.update_world1_quests()
                    if self.current_world == 3:
                        self.update_world3_quests()
                    return True
            else:
                dmg = max(0, int(enemy.attack))
                player.hp = max(0, player.hp - dmg)
                print(L.COMBAT_ENEMY_ATTACK.format(enemy=enemy.name, damage=dmg))
                print(L.COMBAT_PLAYER_HP.format(hp=player.hp, max_hp=player.max_hp))
                if dmg > 0 and not severe_injury_applied and player.hp <= (player.max_hp // 2):
                    severe_injury_applied = True
                    self.adjust_stability(-1)
                    if self.finished:
                        return False
                if player.hp <= 0:
                    print(L.COMBAT_PLAYER_DEAD)
                    self.finished = True
                    return False

        return True

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        """Parse and execute a command string."""


        # Ignorer les commandes vides
        if command_string.strip() == "":
            return


        # Split the command string into a list of words
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]


        # If the command is not recognized, print an error message
        if command_word not in self.commands:
            print(L.UNKNOWN_COMMAND_TEXT.format(command=command_word))
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            try:
                command.action(self, list_of_words, command.number_of_parameters)
            except Exception:  # pylint: disable=broad-exception-caught
                print(L.COMMAND_EXEC_ERROR)
                return
            self.check_auto_combat()
            if self.current_world == 2:
                self.update_world2_quests()
            if self.current_world == 3:
                self.update_world3_quests()
            if self.current_world == 4:
                self.update_world4_quests()


    # Print the welcome message
    def print_welcome(self):
        """Print the welcome banner."""
        for line in L.WELCOME_LINES:
            print(line.format(name=self.player.name))
        #

    # Check if the player has won
    def win(self):
        """Return True when the win condition is met."""
        if self.current_world == 1:
            return False
        for quest in self.player.quest_manager.get_all_quests():
            if not quest.is_completed:
                return False

        print(L.PRISON_RELEASE_TEXT)
        return True

    def lose(self):
        """Return True when the lose condition is met."""
        if self.player.current_room.name == PRISON:
            if not any(
                item.name == L.ITEM_DEFINITIONS["keycard"]["name"]
                for item in self.player.inventory
            ):
                for line in L.PRISON_TURRET_ALERT_LINES:
                    print(line)
                return True
        return False

if __name__ == "__main__":
    game = Game()
    game.play()
