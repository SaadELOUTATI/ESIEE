"""World construction and static content placement."""

from typing import Dict, Optional

from character import (
    Character,
    citizen_dore_reactive,
    glitch_reactive,
    merchant_dialogue,
    ralen_reactive,
    malek_reactive,
    nommera_reactive,
    yara_world1_reactive,
    yara_world2_choice,
)
from enemy import Enemy
from item import Item, create_stability_note
import labels as L
from room import Room


STARTING_ROOM_NAME = "Eridani Prime"
ERIDANI = "Eridani Prime"
AVANT_POSTE = "Avant-poste minier"
MARCHE = "Marché labyrinthique"
FORTERESSE = "Cité-forteresse"
BASE_VELYRA = "Base rebelle de Velyra"
QUARTIER_CIVIL = "Quartier civil"
ENTREPOTS = "Entrepôts civils"
PRISON = "Prison centrale"
CITADELLE = "Citadelle de Karn"
DISTRICT_OR = "District d'Or"
QUARTIER_HOLO = "Quartier des Hologrammes"
NOEUD = "Le Nœud"
PALAIS_LUMIERE = "Palais de Lumière"
SALLE_TRONE = "Salle du Trône"
ORBITAL_STATION = "Orbital Station Ruins"
LANDING_VALLEY = "Landing Valley"
CRYSTAL_PLAINS = "Crystal Plains"
ANCIENT_NEXUS = "Ancient Nexus"
HEART_TERRA = "The Heart of Terra"

ROOM_IMAGES = {
    ERIDANI: "eridani_prime.png",
    AVANT_POSTE: "avant_poste_minier.png",
    MARCHE: "marche_labyrinthique.png",
    FORTERESSE: "cite_forteresse.png",
    BASE_VELYRA: "base_rebelle_velyra.png",
    QUARTIER_CIVIL: "quartier_civil.png",
    ENTREPOTS: "entrepots_civils.png",
    PRISON: "prison_centrale.png",
    CITADELLE: "citadelle_karn.png",
    DISTRICT_OR: "district_or.png",
    QUARTIER_HOLO: "quartier_hologrammes.png",
    NOEUD: "le_noeud.png",
    PALAIS_LUMIERE: "palais_lumiere.png",
    SALLE_TRONE: "salle_trone.png",
    ORBITAL_STATION: "orbital_station_ruins.png",
    LANDING_VALLEY: "landing_valley.png",
    CRYSTAL_PLAINS: "crystal_plains.png",
    ANCIENT_NEXUS: "ancient_nexus.png",
    HEART_TERRA: "heart_terra.png",
}


class World:
    """
    Représente la structure statique du monde : salles, connexions et contenu.

    Le World ne gère ni la boucle de jeu ni les interactions de gameplay.
    """

    def __init__(self, world_id: int = 1) -> None:
        self.world_id = world_id
        self.name = ""
        self.rooms: Dict[str, Room] = {}
        self.ascii_map = []
        self.room_positions = {}
        self._starting_room = self._build_world()

    def _build_world(self) -> Room:
        if self.world_id == 1:
            self.name = ERIDANI
            self._build_world1()
            return self.rooms[STARTING_ROOM_NAME]
        if self.world_id == 2:
            self.name = "Secteur Ext?rieur"
            self._build_world2()
            return self.rooms[BASE_VELYRA]
        if self.world_id == 3:
            self.name = "Aurelion Prime"
            self._build_world3()
            return self.rooms[DISTRICT_OR]
        if self.world_id == 4:
            self.name = "Nova Terra"
            self._build_world4()
            return self.rooms[LANDING_VALLEY]
        raise ValueError(f"World id inconnu: {self.world_id}")

    def _build_world1(self) -> None:
        self._create_world1_rooms()
        self._connect_world1_rooms()
        self._populate_world1_characters()
        self._populate_world1_items()
        self._populate_world1_enemies()
        self.ascii_map = [
            (
                " Eridani Prime             --  Avant-poste minier        --  "
                "Marché labyrinthique      --  Cité-forteresse"
            ),
        ]
        self.room_positions = {
            ERIDANI: (0, 0),
            AVANT_POSTE: (0, 30),
            MARCHE: (0, 60),
            FORTERESSE: (0, 90),
        }

    def _build_world2(self) -> None:
        self._create_world2_rooms()
        self._connect_world2_rooms()
        self._populate_world2_characters()
        self._populate_world2_items()
        self._populate_world2_enemies()
        self.ascii_map = [
            (
                " Base rebelle de Velyra    --  Quartier civil            --  "
                "Entrep?ts civils          --  Prison centrale        --  Citadelle de Karn"
            ),
        ]
        self.room_positions = {
            BASE_VELYRA: (0, 0),
            QUARTIER_CIVIL: (0, 30),
            ENTREPOTS: (0, 60),
            PRISON: (0, 90),
            CITADELLE: (0, 120),
        }

    def _build_world3(self) -> None:
        self._create_world3_rooms()
        self._connect_world3_rooms()
        self._populate_world3_characters()
        self._populate_world3_items()
        self._populate_world3_enemies()
        self.ascii_map = [
            (
                " District d'Or              --  Quartier des Hologrammes  --  "
                "Le Nœud                --  Palais de Lumière      --  Salle du Trône"
            ),
        ]
        self.room_positions = {
            DISTRICT_OR: (0, 0),
            QUARTIER_HOLO: (0, 30),
            NOEUD: (0, 60),
            PALAIS_LUMIERE: (0, 90),
            SALLE_TRONE: (0, 120),
        }

    def _build_world4(self) -> None:
        self._create_world4_rooms()
        self._connect_world4_rooms()
        self.ascii_map = [
            (
                " Orbital Station Ruins       --  Landing Valley           --  "
                "Crystal Plains           --  Ancient Nexus          --  The Heart of Terra"
            ),
        ]
        self.room_positions = {
            ORBITAL_STATION: (0, 0),
            LANDING_VALLEY: (0, 30),
            CRYSTAL_PLAINS: (0, 60),
            ANCIENT_NEXUS: (0, 90),
            HEART_TERRA: (0, 120),
        }

    def _create_world1_rooms(self) -> None:
        eridani = Room(
            ERIDANI,
            L.WORLD1_ROOM_DESCRIPTIONS[ERIDANI],
            image=ROOM_IMAGES.get(ERIDANI),
        )
        eridani.perception_descriptions["low"] = L.WORLD1_PERCEPTION_LOW[ERIDANI]

        avant_poste = Room(
            AVANT_POSTE,
            L.WORLD1_ROOM_DESCRIPTIONS[AVANT_POSTE],
            image=ROOM_IMAGES.get(AVANT_POSTE),
        )

        marche = Room(
            MARCHE,
            L.WORLD1_ROOM_DESCRIPTIONS[MARCHE],
            image=ROOM_IMAGES.get(MARCHE),
        )
        marche.perception_descriptions["low"] = L.WORLD1_PERCEPTION_LOW[MARCHE]

        forteresse = Room(
            FORTERESSE,
            L.WORLD1_ROOM_DESCRIPTIONS[FORTERESSE],
            image=ROOM_IMAGES.get(FORTERESSE),
        )
        forteresse.perception_descriptions["low"] = L.WORLD1_PERCEPTION_LOW[FORTERESSE]

        self.rooms = {
            ERIDANI: eridani,
            AVANT_POSTE: avant_poste,
            MARCHE: marche,
            FORTERESSE: forteresse,
        }
    def _connect_world1_rooms(self) -> None:
        eridani = self.rooms[ERIDANI]
        avant_poste = self.rooms[AVANT_POSTE]
        marche = self.rooms[MARCHE]
        forteresse = self.rooms[FORTERESSE]

        eridani.exits = {"E": avant_poste, "O": None, "U": None, "D": None}
        avant_poste.exits = {"E": marche, "O": eridani, "U": None, "D": None}
        marche.exits = {"E": forteresse, "O": avant_poste, "U": None, "D": None}
        forteresse.exits = {"E": None, "O": marche, "U": None, "D": None}

    def _populate_world1_characters(self) -> None:  # pylint: disable=too-many-locals
        ralen_room = self.rooms[ERIDANI]
        ralen_data = L.WORLD1_NPCS["ralen"]
        ralen = Character(
            "Ralen",
            ralen_data["description"],
            ralen_room,
            ralen_data["messages"],
            on_talk=ralen_reactive
        )
        ralen_room.characters.append(ralen)

        malek_room = self.rooms[AVANT_POSTE]
        malek_data = L.WORLD1_NPCS["malek"]
        malek = Character(
            "Ingénieur Malek",
            malek_data["description"],
            malek_room,
            malek_data["messages"],
            on_talk=malek_reactive
        )
        malek_room.characters.append(malek)

        marche_room = self.rooms[MARCHE]
        marchand_data = L.WORLD1_NPCS["marchand"]
        marchand = Character(
            "Marchand",
            marchand_data["description"],
            marche_room,
            marchand_data["messages"],
            on_talk=merchant_dialogue
        )
        marche_room.characters.append(marchand)

        yara_data = L.WORLD1_NPCS["yara"]
        yara = Character(
            "Yara",
            yara_data["description"],
            marche_room,
            yara_data["messages"],
            on_talk=yara_world1_reactive,
        )
        marche_room.characters.append(yara)

        nommera_room = self.rooms[AVANT_POSTE]
        nommera_data = L.WORLD1_NPCS["nommera"]
        nommera = Character(
            "Nommera",
            nommera_data["description"],
            nommera_room,
            nommera_data["messages"],
            on_talk=nommera_reactive
        )
        nommera_room.characters.append(nommera)

        kael_data = L.WORLD1_NPCS["kael"]
        kael = Character(
            "Kael",
            kael_data["description"],
            self.rooms[ERIDANI],
            kael_data["messages"],
            can_move=True
        )
        self.rooms[ERIDANI].characters.append(kael)
    def _populate_world1_items(self) -> None:
        battery = Item(
            L.ITEM_DEFINITIONS["battery"]["name"],
            L.ITEM_DEFINITIONS["battery"]["description"],
            2,
            effect_type=L.ITEM_DEFINITIONS["battery"]["effect_type"],
            effect_value=L.ITEM_DEFINITIONS["battery"]["effect_value"],
        )
        shiv = Item(
            L.ITEM_DEFINITIONS["shiv"]["name"],
            L.ITEM_DEFINITIONS["shiv"]["description"],
            1,
            effect_type=L.ITEM_DEFINITIONS["shiv"]["effect_type"],
            effect_value=L.ITEM_DEFINITIONS["shiv"]["effect_value"],
        )
        medikit = Item(
            L.ITEM_DEFINITIONS["medikit"]["name"],
            L.ITEM_DEFINITIONS["medikit"]["description"],
            1,
            effect_type="heal",
            effect_value=25,
            usable=True
        )
        self.rooms[AVANT_POSTE].inventory.append(battery)
        self.rooms[MARCHE].inventory.append(shiv)
        self.rooms[ERIDANI].inventory.append(medikit)
        self.rooms[ERIDANI].inventory.append(create_stability_note())

    def _populate_world1_enemies(self) -> None:
        sentry = Enemy("Sentry de patrouille", hp=20, attack=15)
        self.rooms[AVANT_POSTE].enemies.append(sentry)
        vorn = Enemy("Capitaine Vorn", hp=40, attack=25)
        self.rooms[FORTERESSE].enemies.append(vorn)

    def _create_world2_rooms(self) -> None:
        base = Room(
            BASE_VELYRA,
            L.WORLD2_ROOM_DESCRIPTIONS[BASE_VELYRA],
            image=ROOM_IMAGES.get(BASE_VELYRA),
        )
        quartier = Room(
            QUARTIER_CIVIL,
            L.WORLD2_ROOM_DESCRIPTIONS[QUARTIER_CIVIL],
            image=ROOM_IMAGES.get(QUARTIER_CIVIL),
        )
        entrepots = Room(
            ENTREPOTS,
            L.WORLD2_ROOM_DESCRIPTIONS[ENTREPOTS],
            image=ROOM_IMAGES.get(ENTREPOTS),
        )
        prison = Room(
            PRISON,
            L.WORLD2_ROOM_DESCRIPTIONS[PRISON],
            image=ROOM_IMAGES.get(PRISON),
        )
        citadelle = Room(
            CITADELLE,
            L.WORLD2_ROOM_DESCRIPTIONS[CITADELLE],
            image=ROOM_IMAGES.get(CITADELLE),
        )

        self.rooms = {
            BASE_VELYRA: base,
            QUARTIER_CIVIL: quartier,
            ENTREPOTS: entrepots,
            PRISON: prison,
            CITADELLE: citadelle,
        }
    def _connect_world2_rooms(self) -> None:
        base = self.rooms[BASE_VELYRA]
        quartier = self.rooms[QUARTIER_CIVIL]
        entrepots = self.rooms[ENTREPOTS]
        prison = self.rooms[PRISON]
        citadelle = self.rooms[CITADELLE]

        base.exits = {"E": quartier, "O": None, "U": None, "D": None}
        quartier.exits = {"E": entrepots, "O": base, "U": None, "D": None}
        entrepots.exits = {"E": prison, "O": quartier, "U": None, "D": None}
        prison.exits = {"E": citadelle, "O": entrepots, "U": None, "D": None}
        citadelle.exits = {"E": None, "O": prison, "U": None, "D": None}

    def _populate_world2_characters(self) -> None:
        base = self.rooms[BASE_VELYRA]
        entrepots = self.rooms[ENTREPOTS]
        prison = self.rooms[PRISON]

        yara_data = L.WORLD2_NPCS["yara"]
        yara = Character(
            "Yara",
            yara_data["description"],
            base,
            yara_data["messages"],
            on_talk=yara_world2_choice,
        )
        base.characters.append(yara)

        nommera_data = L.WORLD2_NPCS["nommera"]
        nommera = Character(
            "Nommera",
            nommera_data["description"],
            entrepots,
            nommera_data["messages"],
        )
        entrepots.characters.append(nommera)

        narek_data = L.WORLD2_NPCS["narek"]
        narek = Character(
            "Narek",
            narek_data["description"],
            prison,
            narek_data["messages"],
        )
        prison.characters.append(narek)
    def _populate_world2_items(self) -> None:
        keycard = Item(
            L.ITEM_DEFINITIONS["keycard"]["name"],
            L.ITEM_DEFINITIONS["keycard"]["description"],
            1
        )
        transmitter = Item(
            L.ITEM_DEFINITIONS["transmitter"]["name"],
            L.ITEM_DEFINITIONS["transmitter"]["description"],
            1
        )
        nanomedecine = Item(
            L.ITEM_DEFINITIONS["nanomedicine"]["name"],
            L.ITEM_DEFINITIONS["nanomedicine"]["description"],
            1
        )

        self.rooms[ENTREPOTS].inventory.append(keycard)
        self.rooms[BASE_VELYRA].inventory.append(transmitter)
        self.rooms[QUARTIER_CIVIL].inventory.append(nanomedecine)

    def _populate_world2_enemies(self) -> None:
        drone = Enemy("Drone de Karn", hp=30, attack=15)
        self.rooms[QUARTIER_CIVIL].enemies.append(drone)
        karn = Enemy("Gouverneur Karn", hp=50, attack=25)
        self.rooms[CITADELLE].enemies.append(karn)

    def _create_world3_rooms(self) -> None:
        district = Room(
            DISTRICT_OR,
            L.WORLD3_ROOM_DESCRIPTIONS[DISTRICT_OR],
            image=ROOM_IMAGES.get(DISTRICT_OR),
        )
        district.alt_description_infiltrate = (
            L.WORLD3_ALT_DESCRIPTIONS[DISTRICT_OR]["infiltrate"]
        )
        district.alt_description_reveal = (
            L.WORLD3_ALT_DESCRIPTIONS[DISTRICT_OR]["reveal"]
        )
        holo = Room(
            QUARTIER_HOLO,
            L.WORLD3_ROOM_DESCRIPTIONS[QUARTIER_HOLO],
            image=ROOM_IMAGES.get(QUARTIER_HOLO),
        )
        node = Room(
            NOEUD,
            L.WORLD3_ROOM_DESCRIPTIONS[NOEUD],
            image=ROOM_IMAGES.get(NOEUD),
        )
        node.alt_description_break = (
            L.WORLD3_ALT_DESCRIPTIONS[NOEUD]["break"]
        )
        node.alt_description_keep = (
            L.WORLD3_ALT_DESCRIPTIONS[NOEUD]["keep"]
        )
        palace = Room(
            PALAIS_LUMIERE,
            L.WORLD3_ROOM_DESCRIPTIONS[PALAIS_LUMIERE],
            image=ROOM_IMAGES.get(PALAIS_LUMIERE),
        )
        throne = Room(
            SALLE_TRONE,
            L.WORLD3_ROOM_DESCRIPTIONS[SALLE_TRONE],
            image=ROOM_IMAGES.get(SALLE_TRONE),
        )

        self.rooms = {
            DISTRICT_OR: district,
            QUARTIER_HOLO: holo,
            NOEUD: node,
            PALAIS_LUMIERE: palace,
            SALLE_TRONE: throne,
        }
    def _connect_world3_rooms(self) -> None:
        district = self.rooms[DISTRICT_OR]
        holo = self.rooms[QUARTIER_HOLO]
        node = self.rooms[NOEUD]
        palace = self.rooms[PALAIS_LUMIERE]
        throne = self.rooms[SALLE_TRONE]

        district.exits = {"E": holo, "O": None, "U": None, "D": None}
        holo.exits = {"E": node, "O": district, "U": None, "D": None}
        node.exits = {"E": palace, "O": holo, "U": None, "D": None}
        palace.exits = {"E": throne, "O": node, "U": None, "D": None}
        throne.exits = {"E": None, "O": palace, "U": None, "D": None}

    def _populate_world3_characters(self) -> None:
        district = self.rooms[DISTRICT_OR]
        holo = self.rooms[QUARTIER_HOLO]

        citizen_data = L.WORLD3_NPCS["citoyen_dore"]
        citizen = Character(
            "Citoyen dore",
            citizen_data["description"],
            district,
            citizen_data["messages"],
            on_talk=citizen_dore_reactive,
        )
        district.characters.append(citizen)

        glitch_data = L.WORLD3_NPCS["habitant_glitche"]
        glitch = Character(
            "Habitant glitche",
            glitch_data["description"],
            holo,
            glitch_data["messages"],
            on_talk=glitch_reactive,
        )
        holo.characters.append(glitch)
    def _populate_world3_enemies(self) -> None:
        spectre = Enemy("Spectre Holographique", hp=35, attack=15)
        self.rooms[QUARTIER_HOLO].enemies.append(spectre)

    def _populate_world3_items(self) -> None:
        mask = Item(
            L.ITEM_DEFINITIONS["mask"]["name"],
            L.ITEM_DEFINITIONS["mask"]["description"],
            1,
            effect_type=L.ITEM_DEFINITIONS["mask"]["effect_type"],
            effect_value=L.ITEM_DEFINITIONS["mask"]["effect_value"],
        )
        shard = Item(
            L.ITEM_DEFINITIONS["shard"]["name"],
            L.ITEM_DEFINITIONS["shard"]["description"],
            1
        )
        core = Item(
            L.ITEM_DEFINITIONS["core"]["name"],
            L.ITEM_DEFINITIONS["core"]["description"],
            1
        )

        self.rooms[DISTRICT_OR].inventory.append(mask)
        self.rooms[QUARTIER_HOLO].inventory.append(shard)
        self.rooms[NOEUD].inventory.append(core)

    def _create_world4_rooms(self) -> None:
        station = Room(
            ORBITAL_STATION,
            L.WORLD4_ROOM_DESCRIPTIONS[ORBITAL_STATION],
            image=ROOM_IMAGES.get(ORBITAL_STATION),
        )
        valley = Room(
            LANDING_VALLEY,
            L.WORLD4_ROOM_DESCRIPTIONS[LANDING_VALLEY],
            image=ROOM_IMAGES.get(LANDING_VALLEY),
        )
        plains = Room(
            CRYSTAL_PLAINS,
            L.WORLD4_ROOM_DESCRIPTIONS[CRYSTAL_PLAINS],
            image=ROOM_IMAGES.get(CRYSTAL_PLAINS),
        )
        nexus = Room(
            ANCIENT_NEXUS,
            L.WORLD4_ROOM_DESCRIPTIONS[ANCIENT_NEXUS],
            image=ROOM_IMAGES.get(ANCIENT_NEXUS),
        )
        heart = Room(
            HEART_TERRA,
            L.WORLD4_ROOM_DESCRIPTIONS[HEART_TERRA],
            image=ROOM_IMAGES.get(HEART_TERRA),
        )

        self.rooms = {
            ORBITAL_STATION: station,
            LANDING_VALLEY: valley,
            CRYSTAL_PLAINS: plains,
            ANCIENT_NEXUS: nexus,
            HEART_TERRA: heart,
        }
    def _connect_world4_rooms(self) -> None:
        station = self.rooms[ORBITAL_STATION]
        valley = self.rooms[LANDING_VALLEY]
        plains = self.rooms[CRYSTAL_PLAINS]
        nexus = self.rooms[ANCIENT_NEXUS]
        heart = self.rooms[HEART_TERRA]

        station.exits = {"E": valley, "O": None, "U": None, "D": None}
        valley.exits = {"E": plains, "O": station, "U": None, "D": None}
        plains.exits = {"E": nexus, "O": valley, "U": None, "D": None}
        nexus.exits = {"E": heart, "O": plains, "U": None, "D": None}
        heart.exits = {"E": None, "O": nexus, "U": None, "D": None}

    def get_starting_room(self) -> Room:
        """Retourne la salle de départ définie pour ce monde."""
        return self._starting_room

    def get_room(self, name: str) -> Optional[Room]:
        """Retourne une salle par nom, ou None si absente."""
        return self.rooms.get(name)

    def get_ascii_map(self, current_room_name: str) -> str:
        """
        Retourne la carte ASCII en remplaçant la salle courante par '@'.
        """
        rows = [list(line) for line in self.ascii_map]
        position = self.room_positions.get(current_room_name)
        if position:
            row, col = position
            rows[row][col] = "@"
        return "\n".join("".join(line) for line in rows)
