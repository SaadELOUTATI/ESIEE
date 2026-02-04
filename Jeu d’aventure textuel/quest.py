# -*- coding: utf-8 -*-
"""Define the Quest class."""

# pylint: disable=missing-function-docstring

import labels as L

STATE_LOCKED = "LOCKED"
STATE_AVAILABLE = "AVAILABLE"
STATE_ACTIVE = "ACTIVE"
STATE_COMPLETED = "COMPLETED"


class Quest:  # pylint: disable=too-many-instance-attributes
    """
    This class represents a quest in the game. A quest has a title, description,
    objectives, completion status, and optional rewards.

    Attributes:
        title (str): The title of the quest.
        description (str): The description of the quest.
        objectives (list): List of objectives to complete.
        is_completed (bool): Whether the quest is completed.
        is_active (bool): Whether the quest is currently active.
        reward (str): Optional reward for completing the quest.
    """

    def __init__(
        self,
        title,
        description,
        objectives=None,
        reward=None,
        quest_id=None,
        state=None,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.completed_objectives = []
        self.state = state or STATE_AVAILABLE
        self.is_active = self.state == STATE_ACTIVE
        self.is_completed = self.state == STATE_COMPLETED
        self.reward = reward
        self.quest_id = quest_id

    def set_state(self, state):
        """Set quest state and keep flags in sync."""
        self.state = state
        self.is_active = state == STATE_ACTIVE
        self.is_completed = state == STATE_COMPLETED

    def activate(self):
        self.set_state(STATE_ACTIVE)
        print(L.QUEST_ACTIVATED_TITLE.format(title=self.title))
        print(L.QUEST_ACTIVATED_DESC.format(description=self.description))

    def complete_objective(self, objective, player=None):
        if self.state != STATE_ACTIVE:
            return False

        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(L.QUEST_OBJECTIVE_DONE.format(objective=objective))

            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)

            return True
        return False

    def complete_quest(self, player=None):
        if not self.is_completed:
            self.set_state(STATE_COMPLETED)
            print(L.QUEST_COMPLETED_TITLE.format(title=self.title))
            if self.reward:
                print(L.QUEST_REWARD_LINE.format(reward=self.reward))
                if player:
                    player.add_reward(self.reward)
            print()

    def get_status(self):
        label = L.QUEST_STATUS_LABEL.get(self.state)
        if label:
            return f"{self.title} {label}"
        return self.title

    def get_status_label(self):
        return L.QUEST_STATUS_LABEL.get(self.state, "")

    def get_details(self, current_counts=None):
        details = L.QUEST_DETAILS_TITLE.format(title=self.title)
        details += L.QUEST_DETAILS_DESC.format(description=self.description)

        if self.objectives:
            details += L.QUEST_DETAILS_OBJECTIVES_HEADER
            for objective in self.objectives:
                objective_text = self._format_objective_with_progress(objective, current_counts)
                if objective in self.completed_objectives:
                    details += L.QUEST_DETAILS_OBJECTIVE_DONE.format(objective=objective_text)
                else:
                    details += L.QUEST_DETAILS_OBJECTIVE_TODO.format(objective=objective_text)

        if self.reward:
            details += L.QUEST_DETAILS_REWARD.format(reward=self.reward)

        return details

    def _format_objective_with_progress(self, objective, current_counts):
        if not current_counts:
            return objective

        for counter_name, current_count in current_counts.items():
            if counter_name not in objective:
                continue

            required = self._extract_number_from_text(objective)
            if required is not None:
                return f"{objective} (Progression : {current_count}/{required})"

        return objective

    def _extract_number_from_text(self, text):
        for word in text.split():
            if word.isdigit():
                return int(word)
        return None

    def check_room_objective(self, room_name, player=None):
        room_objectives = [
            f"Visiter {room_name}",
            f"Explorer {room_name}",
            f"Aller à {room_name}",
            f"Entrer dans {room_name}",
        ]

        for objective in room_objectives:
            if self.complete_objective(objective, player):
                return True
        return False

    def check_action_objective(self, action, target=None, player=None):
        if target:
            objective_variations = [
                f"{action} {target}",
                f"{action} avec {target}",
                f"{action} le {target}",
                f"{action} la {target}",
            ]
        else:
            objective_variations = [action]

        for objective in objective_variations:
            for real_objective in self.objectives:
                if objective.lower() == real_objective.lower():
                    self.complete_objective(real_objective, player)
                    return True

        return False

    def check_counter_objective(self, counter_name, current_count, player=None):
        for objective in self.objectives:
            if counter_name in objective and objective not in self.completed_objectives:
                words = objective.split()
                for word in words:
                    if word.isdigit():
                        required_count = int(word)
                        if current_count >= required_count:
                            self.complete_objective(objective, player)
                            return True
        return False

    def __str__(self):
        return self.get_status()


class QuestManager:
    """Store quests and evaluate objective completion."""
    def __init__(self, player=None):
        self.quests = []
        self.active_quests = []
        self.player = player
        self._next_id = 1

    def reset(self):
        """Clear quest lists and reset the next id counter."""
        self.quests = []
        self.active_quests = []
        self._next_id = 1

    def add_quest(self, quest):
        if quest.quest_id is None:
            quest.quest_id = self._next_id
            self._next_id += 1
        elif quest.quest_id >= self._next_id:
            self._next_id = quest.quest_id + 1
        self.quests.append(quest)

    def activate_quest(self, quest_identifier):
        if isinstance(quest_identifier, str) and quest_identifier.isdigit():
            quest_identifier = int(quest_identifier)

        if not isinstance(quest_identifier, int):
            return False

        for quest in self.quests:
            if quest.quest_id != quest_identifier:
                continue
            if quest.state != STATE_AVAILABLE:
                return False
            quest.activate()
            if quest not in self.active_quests:
                self.active_quests.append(quest)
            return True
        return False

    def get_quest_by_id(self, quest_id):
        for quest in self.quests:
            if quest.quest_id == quest_id:
                return quest
        return None

    def complete_objective(self, objective_text):
        for quest in self.active_quests:
            if quest.complete_objective(objective_text):
                if quest.is_completed:
                    self.active_quests.remove(quest)
                return True
        return False

    def check_room_objectives(self, room_name):
        for quest in self.active_quests[:]:
            quest.check_room_objective(room_name, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def check_action_objectives(self, action, target=None):
        for quest in self.active_quests[:]:
            quest.check_action_objective(action, target, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def check_counter_objectives(self, counter_name, current_count):
        for quest in self.active_quests[:]:
            quest.check_counter_objective(counter_name, current_count, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def get_active_quests(self):
        return self.active_quests

    def get_all_quests(self):
        return self.quests

    def show_quests(self):
        print(L.QUEST_LIST_HEADER)
        for quest in sorted(self.quests, key=lambda q: q.quest_id or 0):
            status = quest.get_status_label()
            print(
                L.QUEST_LIST_ITEM.format(
                    quest_id=quest.quest_id,
                    title=quest.title,
                    status=status,
                )
            )
        print()

    def show_quest_details(self, quest_id, current_counts=None):
        quest = self.get_quest_by_id(quest_id)
        if not quest:
            print(L.QUEST_NOT_FOUND.format(quest_id=quest_id))
            return False
        print(quest.get_details(current_counts))
        return True

    def get_quest_by_title(self, title):
        for quest in self.quests:
            if quest.title == title:
                return quest
        return None
