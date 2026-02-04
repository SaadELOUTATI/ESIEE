# -*- coding: utf-8 -*-
"""
Libellés centralisés pour la narration, les PNJ et les quêtes.
"""

# =========================
#   WORLD DESCRIPTIONS
# =========================

WORLD1_ROOM_DESCRIPTIONS = {
    "Eridani Prime": (
        "un district pauvre où des fumées noires s’élèvent au-dessus des toits. "
        "Des affiches de propagande couvrent les murs. "
        "Les habitants avancent avec un mélange de peur et de résignation."
    ),
    "Avant-poste minier": (
        "au milieu d’échafaudages branlants, de gardes épuisés et de mineurs au regard vide. "
        "L’air est lourd de poussière et d’électricité."
    ),
    "Marché labyrinthique": (
        "un dédale d’allées étroites, d’échoppes sombres et de murmures étouffés. "
        "Les hommes de main de Vorn rôdent à chaque coin d’ombre."
    ),
    "Cité-forteresse": (
        "des tours massives, des projecteurs écarlates et des soldats patrouillant sans relâche. "
        "C’est ici que le capitaine Vorn impose son règne."
    ),
}

WORLD1_PERCEPTION_LOW = {
    "Eridani Prime": (
        "un district qui vous semble plus étroit, "
        "les ombres collent aux murs et les voix se perdent."
    ),
    "Marché labyrinthique": (
        "un labyrinthe étouffant où chaque pas semble trop bruyant."
    ),
    "Cité-forteresse": (
        "des tours qui paraissent se pencher, "
        "les projecteurs vous écorchent plus que la lumière."
    ),
}

WORLD2_ROOM_DESCRIPTIONS = {
    "Base rebelle de Velyra": (
        "un bunker dissimulé sous les ruines d’un ancien quartier industriel. "
        "Des écrans grésillent, affichant les patrouilles de drones du gouverneur Karn."
    ),
    "Quartier civil": (
        "des immeubles serrés sous des néons blafards. "
        "Les habitants marchent tête baissée sous l’œil constant des caméras."
    ),
    "Entrepôts civils": (
        "de vastes hangars contenant les réserves d’énergie et de nourriture. "
        "Des gardes mécaniques veillent sans relâche."
    ),
    "Prison centrale": (
        "une forteresse de métal noir hérissée de tourelles automatiques. "
        "C’est ici que sont enfermés Narek et les chefs rebelles."
    ),
    "Citadelle de Karn": (
        "un gratte-ciel blindé entouré de drones, cœur du pouvoir du Gouverneur Karn. "
        "Les IA marchandes y supervisent chaque transaction, chaque mouvement."
    ),
}

WORLD3_ROOM_DESCRIPTIONS = {
    "District d'Or": (
        "un quartier luxueux où tout semble parfait : rues propres, jardins calibrés, "
        "habitants souriants, mais dont les yeux semblent vides."
    ),
    "Quartier des Hologrammes": (
        "des illusions mouvantes envahissent les rues : visages qui se dédoublent, "
        "publicités vivantes, faux souvenirs et ombres qui n'appartiennent à personne."
    ),
    "Le Nœud": (
        "un complexe gigantesque regroupant les serveurs neuronaux d'Aurelion Prime. "
        "Il régule émotions, souvenirs et réactions de toute la population."
    ),
    "Palais de Lumière": (
        "un ensemble de jardins flottants, ponts de cristal et escaliers étincelants. "
        "Les serviteurs semblent humains, mais agissent comme des programmes."
    ),
    "Salle du Trône": (
        "une vaste pièce circulaire baignée d’or, où Seren Taal attend, immobile, "
        "dans un halo d’illusions."
    ),
}

WORLD3_ALT_DESCRIPTIONS = {
    "District d'Or": {
        "infiltrate": (
            "Vous passez pour des habitants d’élite. Les regards sont admiratifs, mais vides."
        ),
        "reveal": (
            "Des drones vous surveillent. Les habitants gardent leurs distances, méfiants."
        ),
    },
    "Le Nœud": {
        "break": (
            "Les illusions se fissurent. Les habitants errent, effondrés, découvrant "
            "les horreurs qu’ils ignoraient. Cris, larmes, terreur."
        ),
        "keep": (
            "Les illusions brillent comme jamais : bonheur forcé, sourires figés, "
            "éclats de rire synthétiques."
        ),
    },
}

WORLD4_ROOM_DESCRIPTIONS = {
    "Orbital Station Ruins": (
        "une structure alien brisée, flottant au-dessus de Nova Terra. "
        "Des inscriptions anciennes vibrent faiblement."
    ),
    "Landing Valley": (
        "une vallée fertile, baignée de lumière. "
        "Herbes mouvantes, animaux paisibles, air parfaitement pur."
    ),
    "Crystal Plains": (
        "de vastes plaines remplies de cristaux luminescents réagissant à votre présence."
    ),
    "Ancient Nexus": (
        "un monolithe vivant, partiellement organique. "
        "Une conscience très ancienne vous observe."
    ),
    "The Heart of Terra": (
        "une salle circulaire, noyau énergétique de Nova Terra. "
        "L'esprit de la planète vous attend."
    ),
}

# =========================
#   NPC DEFINITIONS
# =========================

WORLD1_NPCS = {
    "ralen": {
        "description": "Un citoyen au regard vif malgré les cendres sur son visage.",
        "messages": [
            "Vous n’avez pas l’air d’ici.",
            "Les mines à l’est cachent bien des choses.",
        ],
    },
    "malek": {
        "description": "Un technicien nerveux qui tente de réparer une foreuse brisée.",
        "messages": [
            "Cette foreuse ne tiendra plus longtemps.",
            "Sans matériel, tout va s’effondrer.",
        ],
    },
    "marchand": {
        "description": "Un homme sec, aux yeux calculateurs, entouré de caisses verrouillées.",
        "messages": [
            "Tout a un prix.",
            "Même la loyauté.",
        ],
    },
    "yara": {
        "description": "Une femme encapuchonnée, regard déterminé, symbole rebelle au poignet.",
        "messages": [
            "Ne fais confiance à personne ici.",
            "Le Marchand vend des raccourcis. Le prix te suivra.",
            "La forteresse tombera.",
        ],
    },
    "nommera": {
        "description": (
            "Une jeune femme aux mains couvertes de poussière, "
            "le regard creux mais lucide."
        ),
        "messages": [
            "Ils ont tout pris.",
            "Il ne nous reste presque rien.",
        ],
    },
    "kael": {
        "description": "Un éclaireur taciturne, toujours en mouvement.",
        "messages": [
            "Je ne m'attarde jamais au même endroit.",
            "Les ruelles changent plus vite que les ordres.",
        ],
    },
}

WORLD2_NPCS = {
    "yara": {
        "description": "Cheffe rebelle d'Eridani, désormais en mission sur Velyra IX.",
        "messages": [
            "Les civils souffrent ici. On ne peut pas rester passifs.",
            "Choisissez une méthode : piller ou corrompre un général.",
        ],
    },
    "nommera": {
        "description": "Une survivante civile au regard fatigué, mais encore lucide.",
        "messages": [
            "Les entrepôts portent les traces de la peur.",
            "Certains traitent avec un général. D'autres pillent.",
        ],
    },
    "narek": {
        "description": "Un rebelle amaigri mais déterminé, encore marqué par sa captivité.",
        "messages": [
            "Merci de m'avoir sauvé. Je n'oublierai pas.",
            "Le pouvoir doit tomber, autrement on recommencera.",
        ],
    },
}

WORLD3_NPCS = {
    "citoyen_dore": {
        "description": (
            "Un habitant riche dont les émotions sont filtrées par les serveurs du Nœud."
        ),
        "messages": [
            "Aurelion est parfait. Les autres mondes souffrent ? Ils sont faibles.",
        ],
    },
    "habitant_glitche": {
        "description": (
            "Son corps scintille comme un hologramme mal calibré. Sa voix tremble, en écho."
        ),
        "messages": [
            "...v...v...vvous... n'êtes pas... attendus...",
        ],
    },
}

# =========================
#   CHARACTER REACTIONS
# =========================

MERCHANT_REPEAT_TEXT = (
    "\nLe Marchand vous jauge en silence, comme s'il pesait encore votre décision.\n"
    "Son sourire reste mince, et son regard passe déjà à autre chose.\n"
)

MERCHANT_DIALOGUE_LINES = [
    "Le marchand ne vous regarde pas vraiment ; il jauge votre ombre.",
    "Ses doigts jouent avec un sceau noirci, trop propre pour cette ruelle.",
    "« Tout a un prix », souffle-t-il, mais son sourire ne tient pas.",
    "« On dit que vous cherchez un cristal de propulsion. Je sais où il a glissé. »",
    "Il se penche, assez près pour que sa voix tranche le bruit.",
    "« Ce que je demande n'est pas de l'argent. »",
    "L'air se refroidit ; vous comprenez que ce marché vous suivra.",
    "Il ouvre sa main : une option sombre, une option lente.",
    "« Alors, capitaine... choisissez ce que vous acceptez de perdre. »",
    "- Accepter son échange, et laisser une part de vous dans sa balance.",
    "- Refuser, et porter le poids du manque en silence.",
]

MERCHANT_ACCEPT_TEXT = (
    "\nIl ferme sa main, comme s'il scellait une dette invisible.\n"
    "Vous sentez le poids du choix s'accrocher à vous.\n"
)

MERCHANT_REFUSE_TEXT = (
    "\nIl hoche la tête, un sourire bref au coin des lèvres.\n"
    "« Alors cherchez ailleurs », dit-il, sans vous quitter des yeux.\n"
)

RALEN_REACTIVE_LINES = {
    "collapse": "Il recule. Vos yeux le mettent mal à l'aise.",
    "vacillant": "Il parle bas. Vous semblez à bout.",
    "stable_note": "Il hoche la tête. Vous tenez encore debout.",
}

MALEK_REACTIVE_LINES = {
    "collapse": "Il évite votre regard. Il n'a rien à vous dire.",
    "vacillant": "Il soupire. Vous tenez à peine.",
}

NOMMERA_REACTIVE_LINE = "Elle se ferme. On murmure que tu as laissé des gens derrière."

YARA_WORLD1_REACTIVE_LINE = (
    "Tu as sacrifié des vies pour ce cristal. "
    "Ne me demande pas d'oublier."
)

YARA_WORLD2_DECISION_TAKEN = "La décision est prise. On avance."
YARA_WORLD2_CHOICE_LINES = [
    "Yara vous fixe, le ton bas.",
    "La citadelle ne tombera pas sans préparatifs.",
    "Deux options, une seule direction.",
    "1) Corrompre un général pour obtenir un passage discret.",
    "2) Piller les entrepôts civils pour s'armer vite.",
]
YARA_WORLD2_CORRUPTION_RESULT = "\nVous optez pour la corruption. Un accord sale, mais efficace.\n"
YARA_WORLD2_PILLAGE_RESULT = "\nVous optez pour le pillage. La peur circule, les stocks tombent.\n"

CITIZEN_REACTIVE_LINES = {
    "infiltrate": "Vous êtes splendides. Vous avez le rang pour être ici.",
    "reveal": "Vous êtes un intrus dangereux. Ne touchez à rien.",
    "default": "Aurelion est parfait. Les autres mondes souffrent ? Ils sont faibles.",
}

GLITCH_REACTIVE_LINES = {
    "before": "...v...v...vvous... n'êtes pas... attendus...",
    "after": "Les murs... regardent... attention à... Seren... Taa-- *signal perdu*.",
}

NOVATERRA_COMPANION_LINES = {
    "yara": "C'est le plus bel endroit que j'aie vu. Faisons-en un refuge juste.",
    "narek": "Nous avons tant perdu, mais ici tout peut recommencer.",
    "guide": "Nova Terra n'offre pas de certitudes, seulement un chemin.",
}

# =========================
#   ITEMS / LORE
# =========================

STABILITY_NOTE_NAME = "Note griffonnée"
STABILITY_NOTE_DESC = "Un papier froissé couvert d'une écriture hésitante."
STABILITY_NOTE_TEXT = (
    "Ici, on ne meurt pas seulement de blessures.\n"
    "Certains s'effondrent bien avant...\n"
    "Quand on renonce trop souvent à ce qu'on est,\n"
    "quand on sacrifie sans comprendre,\n"
    "quelque chose finit par lâcher."
)

# =========================
#   QUESTS
# =========================

QUESTS_WORLD1 = {
    1: {
        "title": "Comprendre Eridani",
        "description": "Établir un premier contact et comprendre ce monde.",
        "objectives": ["Parler à Ralen"],
    },
    2: {
        "title": "Survivre à l'Oppression",
        "description": "Résister aux patrouilleurs d'Eridani Prime.",
        "objectives": ["Survivre aux patrouilleurs"],
    },
    3: {
        "title": "Le Cristal de Propulsion",
        "description": "Obtenir le cristal de propulsion.",
        "objectives": ["Obtenir le cristal de propulsion"],
    },
    4: {
        "title": "Abattre Vorn",
        "description": "Mettre fin à la domination de Vorn.",
        "objectives": ["Abattre Vorn"],
    },
}

QUESTS_WORLD2 = {
    1: {
        "title": "Choisir une méthode d'attaque",
        "description": "Décider s'il faut piller ou corrompre un général.",
        "objectives": ["Choisir une méthode"],
    },
    2: {
        "title": "Ramasser la carte d'accès rouillée",
        "description": "Récupérer l'accès pour atteindre la prison.",
        "objectives": ["Prendre la Carte d'accès rouillée"],
    },
    3: {
        "title": "Parler à Narek",
        "description": "Obtenir sa reconnaissance après l'avoir sauvé.",
        "objectives": ["Parler avec Narek"],
    },
    4: {
        "title": "Tuer le Gouverneur Karn",
        "description": "Mettre fin au pouvoir de Karn dans la citadelle.",
        "objectives": ["Tuer le Gouverneur Karn"],
    },
}

QUESTS_WORLD3 = {
    1: {
        "title": "Choisir une posture",
        "description": "Décider comment se comporter face au système.",
        "objectives": ["Choisir une posture"],
    },
    2: {
        "title": "Découvrir Aurelion",
        "description": "Explorer les premiers signaux d'une paix trop parfaite.",
        "objectives": [
            "Entrer dans District d'Or",
            "Parler Citoyen doré",
            "Entrer dans Quartier des Hologrammes",
        ],
    },
    3: {
        "title": "Traverser les Illusions",
        "description": "Survivre à l'assaut des hologrammes et trouver un guide.",
        "objectives": [
            "Vaincre le spectre holographique",
            "Parler Habitant glitché",
        ],
    },
    4: {
        "title": "Le Nœud",
        "description": "Décider du sort des illusions d'Aurelion.",
        "objectives": ["Choisir le destin des illusions"],
    },
    5: {
        "title": "Le Palais du Mensonge",
        "description": "Remonter jusqu'au cœur du pouvoir.",
        "objectives": [
            "Entrer dans Palais de Lumière",
            "Entrer dans Salle du Trône",
        ],
    },
    6: {
        "title": "Face à Seren Taal",
        "description": "Affronter la maîtresse d'Aurelion Prime.",
        "objectives": [
            "Confronter Seren Taal",
            "Décider du sort de Seren Taal",
        ],
    },
}

QUESTS_WORLD4 = {
    1: {
        "title": "Fouler une Terre Nouvelle",
        "description": "Découvrir Nova Terra et ressentir ce que vous avez traversé.",
        "objectives": [
            "Arriver dans la vallée",
            "Observer la planète",
            "Parler au guide",
        ],
    },
    2: {
        "title": "Les Vestiges du Passé",
        "description": "Décider comment aborder les ruines orbitales.",
        "objectives": {
            "explore": ["Explorer la station"],
            "ignore": ["Ignorer la station"],
        },
    },
    3: {
        "title": "La Voix de Terra",
        "description": "Entendre la conscience planétaire de Nova Terra.",
        "objectives": [
            "Atteindre le Nexus",
            "Écouter la conscience planétaire",
            "Comprendre Terra",
        ],
    },
}

# =========================
#   NARRATION / TRANSITIONS
# =========================

INTRO_LINES = [
    "En 2239, l'ESIEE lance le vaisseau interstellaire 'Vigilant' pour trouver un monde habitable.",
    "Une onde gravitationnelle inconnue projette l'appareil vers un système lointain.",
    "Réparez le Vigilant, ralliez des alliés, et décidez du destin de l'humanité.",
]

CHOICE_ALERT_LINES = [
    "",
    "🌌 CHAPITRE I — ERIDANI PRIME 🌌",
    "Vous vous réveillez dans un caisson cryo… Le Vigilant tremble… Un crash est imminent.",
    "",
    "🔥 Le crash est inévitable. Vous devez faire un choix :",
    "1️⃣ Sauver tout l'équipage",
    "2️⃣ Sauver les ressources",
    "",
]

CHOICE_CREW_LINES = [
    "",
    "Vous arrachez des survivants des flammes… mais perdez une partie du matériel vital.",
    "➡️ Un membre d’équipage utilise sa puce neuronale traductrice.",
    "Le cristal de propulsion est perdu dans l'impact.",
    "",
]

CHOICE_RESOURCES_LINES = [
    "",
    "Vous scellez les compartiments pleins d’équipage pour sauver les soutes.",
    "Cependant, il vous reste quelques survivants.",
    "➡️ La puce neuronale d’un officier vous sert désormais de traducteur.",
    "➡️ Vous récupérez des modules, de l’énergie et des pièces intactes…",
    "➡️ Vous récupérez un cristal de propulsion intact dans les décombres.",
    "",
]

WORLD1_TRANSITION_TEXT = (
    "\n🧭 Les réserves de Vorn révèlent assez de minerai pour réparer le Vigilant. "
    "Les rebelles vous aident à préparer le départ d’Eridani Prime.\n"
    "🔷 Le cristal de propulsion reste essentiel pour stabiliser le cœur du vaisseau.\n"
    "\n🚀 Le Vigilant s’élève au-dessus d’Eridani Prime.\n"
    "👥 Les mineurs et les rebelles acclament votre nom alors que le vaisseau perce les nuages.\n"
    "🩺 Des techniciens improvisent une infirmerie, utilisant les derniers stocks médicaux.\n"
    "✅ Les blessés sont stabilisés. Les systèmes vitaux recalibrés.\n"
    "🛰️ Quelques jours plus tard, les capteurs détectent Velyra IX : "
    "une planète-machine sous la tyrannie de Karn.\n"
)

WORLD2_TRANSITION_TEXT = (
    "\nFIN DE LA LIBÉRATION DE VELYRA IX\n"
    "Les rebelles t’entourent. Certains pleurent, d’autres crient victoire.\n"
    "Les citoyens émergent des ruines, voyant pour la première fois un ciel sans drones.\n"
    "\nLa bannière de la liberté est hissée au sommet de la Citadelle brisée.\n"
    "Des milliers d’écrans projettent ton nom : le libérateur de Velyra.\n"
    "\nLe Vigilant décolle lentement, traversant les nuages rosés…\n"
    "Un nouveau monde t’attend.\n"
)

CRYSTAL_REALIZATION_TEXT = "\nVous comprenez enfin ce que vous aviez entre les mains...\n"

MERCHANT_CHOICE_LINES = [
    "",
    "Le Marchand propose un échange risqué.",
    "1) Accepter l'échange (sacrifice)",
    "2) Refuser l'échange (cohésion préservée)",
    "",
]
MERCHANT_ACCEPTED_TEXT = "\nVous acceptez l'échange. La confiance se fissure.\n"
MERCHANT_REFUSED_TEXT = "\nVous refusez l'échange. La cohésion se renforce.\n"
MERCHANT_NO_CRYSTAL_TEXT = (
    "\nSans cristal de propulsion, le vaisseau reste irréparable.\n"
    "La mission s'éteint ici.\n"
)

MENTAL_COLLAPSE_TEXT = (
    "\nCe n'est pas votre corps qui lâche.\n"
    "C'est votre volonté.\n"
    "Vous avez trop cédé, trop sacrifié, trop perdu sans comprendre.\n"
    "Ce n’est pas une défaite.\n"
    "C’est une fin.\n"
    "Le monde continue sans vous.\n"
)

VORN_LOCKED_TEXT = (
    "\nLe Capitaine Vorn reste immobile. Vous n'êtes pas encore autorisés à l'affronter.\n"
)

GAME_WIN_TEXT = "\n🎉 VOUS AVEZ GAGNÉ LA PARTIE 🎉\n"
GAME_LOSE_TEXT = "\n💀 Vous avez été capturé. Fin de partie.\n"

PRISON_RELEASE_TEXT = (
    "\nLes portes de la prison cèdent.\n"
    "Narek est libre.\n"
    "La résistance peut enfin renverser le régime.\n"
)

PRISON_TURRET_ALERT_LINES = [
    "\n🚨 ALERTE ! Vous êtes intercepté par les tourelles automatiques.",
    "Vous n'avez pas d'autorisation d'accès.\n",
]

KARN_AFTERMATH_PROMPT = (
    "\nKarn s'effondre. Yara et Narek sont tous deux amochés.\n"
    "Vous n'avez qu'une dose de nanomédecine.\n"
    "Qui sauvez-vous ?\n"
    "1) Yara\n"
    "2) Narek\n"
)
KARN_AFTERMATH_YARA = "\nVous stabilisez Yara. Narek ne tiendra pas.\n"
KARN_AFTERMATH_NAREK = "\nVous stabilisez Narek. Yara ne tiendra pas.\n"
KARN_AFTERMATH_NONE = (
    "\nKarn tombe. Yara et Narek sont tous deux amochés.\n"
    "Sans nanomédecine, vous ne pouvez rien faire.\n"
    "Ils meurent tous les deux.\n"
)

AURELION_POSTURE_LINES = (
    "\nUn drone de sécurité vous scanne brutalement.\n"
    "CHOIX IMMÉDIAT :\n"
)
AURELION_POSTURE_OPTIONS = [
    "1️⃣ S’infiltrer et se fondre dans la haute société.",
    "2️⃣ Révéler la vérité et devenir une menace.\n",
]
AURELION_POSTURE_INFILTRATE = "\nVous adoptez des identités locales et pénétrez la haute société.\n"
AURELION_POSTURE_REVEAL = "\nVous montrez la vérité devant une foule… qui éclate de rire.\n"

AURELION_NODE_LINES = "\nLe Nœud vibre autour de vous. Les illusions attendent votre décision.\n"
AURELION_NODE_OPTIONS = [
    "1️⃣ Briser les illusions et réveiller la population.",
    "2️⃣ Maintenir les illusions pour conserver un calme artificiel.\n",
]
AURELION_NODE_BREAK = "\nVous brisez le voile. La vérité blesse, mais elle est réelle.\n"
AURELION_NODE_KEEP = "\nVous maintenez le voile. La paix tient, mais elle est fausse.\n"

SEREN_CONFRONT_LINES = (
    "\n👑 Seren Taal se lève de son trône, un sourire calme au visage.\n"
    "« Te voilà enfin… Capitaine. »\n"
    "« J’ai bâti un monde parfait. Sans douleur. Sans guerre. »\n"
    "« Rejoins-moi. Gouvernons ensemble. »\n"
)
SEREN_CONFRONT_OPTIONS = [
    "1️⃣ Accepter l’alliance (fin sombre)",
    "2️⃣ Refuser (combat final)\n",
]
SEREN_ALLIANCE_TEXT = "\nVous acceptez l’alliance.\n"
SEREN_REFUSE_TEXT = (
    "\n🔥 Vous refusez.\n"
    "Seren Taal active son exo-armure : « Alors tu mourras comme les autres. »\n"
)
SEREN_ALLIANCE_ENDING = (
    "\nVous régnez désormais aux côtés de Seren Taal.\n"
    "Un empire parfait… mais oppressif.\n"
    "FIN SOMBRE — TYRANNIE ABSOLUE.\n"
)
SEREN_VICTORY_ENDING = (
    "\n⚔️ Seren Taal s’effondre. Les illusions se brisent pour toujours.\n"
    "Les habitants retrouvent leurs vraies émotions.\n"
    "Les rebelles des mondes 1 et 2 se regroupent autour de vous.\n"
    "🌅 LA LIBERTÉ RENAÎT.\n"
    "Tu es acclamé comme le Héros des Trois Mondes.\n"
    "Une nouvelle ère commence, fondée sur la justice et l’espoir.\n"
    "Le dernier mystère vous attend : Nova Terra.\n"
)

WORLD4_TRANSITION_INTRO = (
    "\n🚀 Le Vigilant traverse l’espace, guidé par les signaux mystérieux détectés autrefois.\n"
    "Les flottes alliées d’Eridani, Velyra et Aurelion vous accompagnent.\n"
    "Un cortège de lumière… une alliance nouvelle.\n"
)
WORLD4_TRANSITION_ORBITAL = (
    "Soudain, au-dessus d’une planète bleue et verte… une structure orbitale en ruine apparaît.\n"
    "Elle émet des signaux faibles, presque vivants.\n"
)
WORLD4_TRANSITION_CHOICE = "CHOIX IMMÉDIAT : explorer la station ou descendre directement ?\n"
WORLD4_TRANSITION_OPTIONS = [
    "1️⃣ Ignorer la station (descente immédiate, voie pacifique)",
    "2️⃣ Explorer la station (risqué mais bénéfique)\n",
]
WORLD4_CHOICE_PRUDENCE = "\nVous choisissez la prudence."
WORLD4_STATION_DOCK = "\nVous accostez la station abandonnée."
WORLD4_STATION_FLOAT = "Des fragments d'architecture alien flottent dans le vide.\n"
WORLD4_STATION_EXPLOSION = "Une explosion partielle vous blesse légèrement : PV -{dmg}"
WORLD4_STATION_ARTIFACT = "Vous découvrez un artefact alien augmentant votre puissance.\n"
WORLD4_GUIDE_INTRO = (
    "\nUne présence silencieuse se tient près de vous. Elle observe Nova Terra sans mot dire.\n"
)
WORLD4_CHAPTER_TITLE = "\nCHAPITRE IV — NOVA TERRA\n"

NEXUS_LISTEN_TEXT = (
    "\nUne voix profonde traverse votre esprit. "
    "Elle n'ordonne pas, elle attend.\n"
)

NEXUS_CHOICE_LINES = (
    "\nLe Nexus s'éveille. Une conscience ancestrale vous parle.\n"
    "\"Vous avez libéré trois mondes. Maintenant, façonnez votre avenir.\"\n"
)
NEXUS_OPTIONS = [
    "1) Harmonie - paix absolue",
    "2) Domination - puissance absolue",
    "3) Renoncer - sagesse\n",
]
NEXUS_DOMINATION_COMBAT = "\nCombat final contre le Terra Guardian !"

WORLD4_ENDING_TITLE = "\nFIN DE NOVA TERRA\n"
WORLD4_ENDING_HARMONY = [
    "La planète vous accepte. Une symbiose naît entre les humains et Terra.",
    "Une ère de paix commence. Vous devenez le guide moral d'un nouveau monde.",
    "FIN HARMONIEUSE — Renaissance de l'humanité.\n",
]
WORLD4_ENDING_DOMINATION = [
    "En maîtrisant Terra, vous bâtissez une forteresse vivante protégeant les mondes libérés.",
    "Votre civilisation devient une puissance galactique invincible.",
    "FIN DE PUISSANCE — L'empire protecteur de Nova Terra.\n",
]
WORLD4_ENDING_RENOUNCE = [
    "Vous refusez d'être un souverain. Le peuple élit son premier Conseil Interplanétaire.",
    "On vous nomme le Héros Fondateur, symbole éternel de liberté.",
    "FIN PHILOSOPHIQUE — La sagesse du renoncement.\n",
]
WORLD4_ENDING_FINAL = [
    "Le Vigilant s'élève une dernière fois, puis disparaît dans les cieux.",
    "L'humanité a trouvé sa nouvelle maison.\n",
    "FIN DU JEU - MERCI D'AVOIR JOUÉ\n",
]
# =========================
#   UI / SYSTEM TEXTS
# =========================

DEFAULT_PLAYER_NAME = "Orion Vale"
PLAYER_NAME_PROMPT = "Entrez votre nom (laisser vide pour '{default}') : "

INTRO_TRANSLATOR_NAME = "Puce neuronale traductrice"
INTRO_TRANSLATOR_DESC = "Implant qui traduit en temps réel les langues locales."
INTRO_CREW_KIT_NAME = "Trousse de secours"
INTRO_CREW_KIT_DESC = "Un kit de premiers soins récupéré dans la coque."
INTRO_RESOURCE_CRYSTAL_NAME = "Cristal de propulsion"
INTRO_RESOURCE_CRYSTAL_DESC = "Un cristal intact, essentiel pour réparer le vaisseau."
INTRO_RESOURCE_MODULE_NAME = "Module d'alimentation"
INTRO_RESOURCE_MODULE_DESC = "Une cellule d'énergie intacte, utile pour la survie."

ITEM_DEFINITIONS = {
    "battery": {
        "name": "Module de survie renforcé",
        "description": "Un module qui stabilise les systèmes vitaux (+10 PV max).",
        "effect_type": "max_hp",
        "effect_value": 10,
    },
    "shiv": {
        "name": "Dague improvisée",
        "description": "Une lame artisanale forgée à partir de ferraille (+5 ATK).",
        "effect_type": "atk",
        "effect_value": 5,
    },
    "medikit": {
        "name": "Medikit",
        "description": "Un kit médical portable pour soigner rapidement.",
    },
    "keycard": {
        "name": "Carte d'accès rouillée",
        "description": "Une vieille carte magnétique de sécurité.",
    },
    "transmitter": {
        "name": "Émetteur rebelle crypté",
        "description": "Un appareil de communication utilisé par la résistance.",
    },
    "nanomedicine": {
        "name": "Nanomédecine",
        "description": "Un gel médical capable de stabiliser une blessure critique.",
    },
    "mask": {
        "name": "Stimulant vital",
        "description": "Un injecteur qui renforce temporairement le corps (+20 PV).",
        "effect_type": "hp",
        "effect_value": 20,
    },
    "shard": {
        "name": "Fragment holographique",
        "description": "Un éclat instable qui garde une trace d'illusion.",
    },
    "core": {
        "name": "Noyau du Nœud",
        "description": "Un module scellé qui pulse comme un serveur vivant.",
    },
}

COMMAND_HELP_STRINGS = {
    "help": " : afficher cette aide",
    "quit": " : quitter le jeu",
    "go": " <direction> : se déplacer dans une direction cardinale (N, E, S, O)",
    "history": " : afficher l'historique des lieux visités",
    "back": " : revenir à la pièce précédente",
    "look": " : observer la pièce",
    "take": " <item_num> : prendre un item",
    "drop": " <item_num> : déposer un item",
    "use": " <item_num> : utiliser un item",
    "check": " : vérifier l'inventaire",
    "status": " : afficher l'état du personnage",
    "talk": " <num> : parler à un personnage dans la pièce",
    "attack": " <ennemi> : attaquer un ennemi",
    "map": " : afficher la carte",
    "quests": " : afficher la liste des quêtes",
    "quest": " <quest_num> : afficher les détails d'une quête",
    "activate": " <quest_num> : activer une quête",
    "rewards": " : afficher vos récompenses",
}

UNKNOWN_COMMAND_TEXT = (
    "\nCommande '{command}' non reconnue. "
    "Entrez 'help' pour voir la liste des commandes disponibles.\n"
)
WELCOME_LINES = [
    "\nBienvenue {name} dans ce jeu d'aventure !",
    "Entrez 'help' si vous avez besoin d'aide.\n",
]

COMMAND_NO_PARAM = "\nLa commande '{command}' ne prend pas de paramètre.\n"
COMMAND_ONE_PARAM = "\nLa commande '{command}' prend 1 seul paramètre.\n"
COMMAND_INVALID_CONTEXT = (
    "\nCommande invalide. Utilisez : take <num>, talk <num>, use <num>, drop <num>.\n"
)
COMMAND_INVALID_DIRECTION = "\nDirection '{direction}' non reconnue.\n"
COMMAND_BACK_NOT_POSSIBLE = "\nVous ne pouvez pas revenir en arrière.\n"
COMMAND_INVALID_INDEX = "\nIl n'y a rien ici correspondant à ce numéro.\n"
COMMAND_INVALID_INVENTORY_INDEX = "\nVous n'avez rien dans votre inventaire à cet emplacement.\n"
COMMAND_TAKE_TOO_HEAVY = "\nVous ne pouvez pas prendre {item}. Poids maximum dépassé !\n"
COMMAND_TAKE_SUCCESS = "\nVous avez pris : {item}\n"
COMMAND_DROP_SUCCESS = "\nVous avez déposé : {item}\n"
COMMAND_USE_NOT_USABLE = "Vous ne pouvez pas utiliser '{item}'."
COMMAND_NO_ENEMY = "\nIl n'y a aucun ennemi ici.\n"
COMMAND_UNKNOWN_ENEMY = "\nAucun ennemi nommé '{enemy}' ici.\n"
COMMAND_QUEST_ID_INVALID = "\nIdentifiant de quête invalide.\n"
COMMAND_QUEST_ACTIVATE_FAILED = (
    "\nImpossible d'activer la quête {quest_id}. "
    "Vérifiez l'identifiant ou si elle n'est pas déjà active.\n"
)
COMMAND_EXEC_ERROR = "\nUne erreur est survenue pendant l'exécution de la commande.\n"
STATUS_TEMPLATE = (
    "\nVotre état :\n"
    "– Points de vie : {hp} / {max_hp}\n"
    "– Attaque : {atk}\n"
    "– État mental : {state}\n"
    "– Quêtes accomplies : {completed} / {total}\n"
)
HELP_HEADER = "\nVoici les commandes disponibles:"
QUIT_MESSAGE = "\nMerci {name} d'avoir joué. Au revoir.\n"

ROOM_LONG_DESCRIPTION_TEMPLATE = (
    "\n======================\n"
    "{name}\n"
    "======================\n"
    "{body}\n\n"
    "{exits}\n"
)
ROOM_DESCRIPTION_PREFIX = "Vous êtes dans {description}"
ROOM_EXITS_PREFIX = "Sorties: "
ROOM_NO_CHARACTERS = "Il n'y a personne ici."
ROOM_CHARACTERS_HEADER = "Personnages :"
ROOM_NO_ENEMIES = "Il n'y a aucun ennemi ici."
ROOM_ENEMIES_HEADER = "Les ennemis présents sont :"
ROOM_NO_ITEMS = "Il n'y a aucun objet au sol."
ROOM_ITEMS_HEADER = "Objets au sol :"

PLAYER_NO_DOOR = "\nAucune porte dans cette direction !\n"
PLAYER_PRISON_SCANNER = "\n🚨 Les scanners détectent une intrusion non autorisée...\n"
PLAYER_INVENTORY_EMPTY = "\nVotre inventaire est vide.\n"
PLAYER_INVENTORY_HEADER = "\nVous disposez des items suivants :\n"
PLAYER_INVENTORY_WEIGHT = (
    "Le poids total des items est de {weight} kg sur une capacité maximale de {max_weight} kg.\n"
)
PLAYER_TAKE_SUCCESS = "\nVous avez pris : {item}\n"
PLAYER_TAKE_TOO_HEAVY = "\n🚫 Vous ne pouvez pas prendre {item}. Poids maximum dépassé !\n"
PLAYER_TAKE_NOT_HERE = "\nCet item n'est pas présent ici.\n"
PLAYER_DROP_SUCCESS = "\nVous avez déposé : {item}\n"
PLAYER_DROP_NOT_OWNED = "\nVous ne possédez pas cet item.\n"
PLAYER_USE_WHAT = "Utiliser quoi ?"
PLAYER_USE_NOT_USABLE = "Vous ne pouvez pas utiliser '{item}'."
PLAYER_USE_NOT_OWNED = "Vous ne possédez pas '{item}'."
PLAYER_USE_HEAL = "Vous utilisez {item}. HP : {before} -> {after}"
PLAYER_USE_NO_EFFECT = "Rien ne se passe lorsque vous utilisez {item}."
PLAYER_TALK_TEMPLATE = "\n{name} dit : '{line}'\n"
PLAYER_TALK_NOT_FOUND = "\nIl n'y a personne avec ce nom ici.\n"
PLAYER_REWARDS_EMPTY = "\n🎁 Aucune récompense obtenue pour le moment.\n"
PLAYER_REWARDS_HEADER = "\n🎁 Vos récompenses:"
PLAYER_REWARDS_ITEM = "  • {reward}"
PLAYER_HISTORY_EMPTY = "\nVous n'avez encore visité aucune autre pièce.\n"
PLAYER_HISTORY_HEADER = "\nVous avez déjà visité les pièces suivantes:\n"

ITEM_STR_TEMPLATE = "{name} : {description} ({weight} kg)"
ENEMY_STR_TEMPLATE = "{name} (PV {hp}, ATK {attack})"

STABILITY_GAIN_STRONG = "Une clarté nouvelle s'impose à vous."
STABILITY_GAIN_MEDIUM = "Vous reprenez pied, plus sûrement."
STABILITY_GAIN_LIGHT = "Vous reprenez légèrement pied."
STABILITY_LOSS_STRONG = "Votre esprit se crispe. Quelque chose cède."
STABILITY_LOSS_MEDIUM = "Un vertige sourd vous ronge."
STABILITY_LOSS_LIGHT = "Un malaise diffus vous traverse."
STABILITY_STATE_STABLE = "stable"
STABILITY_STATE_FRAGILE = "fragilisé"
STABILITY_STATE_UNSTABLE = "instable"
STABILITY_STATE_VACILLANT = "vacillant"
STABILITY_STATE_EDGE = "au bord de l'effondrement"
STABILITY_STATE_COLLAPSE = "effondrement"

COMBAT_START = "\n⚔️ Combat engagé contre {enemy} ! ⚔️\n"
COMBAT_AI_QUESTION = "\nIA de combat : {question}"
COMBAT_AI_FALLBACK_NOTICE = "\nIA de combat indisponible. Question de secours."
COMBAT_AI_FALLBACK_QUESTION = "Tapez 'ok' pour continuer."
COMBAT_AI_FALLBACK_ANSWER = "ok"
COMBAT_AI_EVAL_ERROR = "\nRéponse invalide. L'ennemi prend l'initiative."
COMBAT_PLAYER_ATTACK = "\nVous attaquez {enemy} et infligez {damage} dégâts."
COMBAT_PLAYER_HP = "PV Joueur : {hp}/{max_hp}"
COMBAT_ENEMY_HP = "{enemy} a encore {hp} PV.\n"
COMBAT_ENEMY_DEFEATED = "{enemy} est vaincu.\n"
COMBAT_ENEMY_ATTACK = "\n{enemy} vous attaque et inflige {damage} dégâts."
COMBAT_PLAYER_DEAD = "\nVous êtes mort. Fin de partie.\n"
COMBAT_SEREN_DEFEATED = (
    "\nSeren Taal s'effondre. Les illusions se brisent autour de vous.\n"
    "Aurelion Prime est libérée, mais le silence reste.\n"
)
COMBAT_TERRA_DEFEATED = (
    "\nLa conscience de Terra se dissipe.\n"
    "Nova Terra retrouve son silence.\n"
)

QUEST_ACTIVATED_TITLE = "\n🗡️ Nouvelle quête activée : {title}"
QUEST_ACTIVATED_DESC = "📝 {description}\n"
QUEST_OBJECTIVE_DONE = "✅ Objectif accompli : {objective}"
QUEST_COMPLETED_TITLE = "\n🏆 Quête terminée : {title}"
QUEST_REWARD_LINE = "🎁 Récompense : {reward}"
QUEST_LIST_HEADER = "\n📋 Liste des quêtes :\n"
QUEST_LIST_ITEM = "{quest_id}) {title} {status}"
QUEST_NOT_FOUND = "\nAucune quête avec l'identifiant {quest_id}.\n"
QUEST_STATUS_LABEL = {
    "LOCKED": "(Verrouillée) 🔒",
    "AVAILABLE": "(Disponible) 🟡",
    "COMPLETED": "(Terminée) ✅",
    "ACTIVE": "(Active) ⏳",
}
QUEST_DETAILS_TITLE = "\n📋 Quête : {title}\n"
QUEST_DETAILS_DESC = "📖 {description}\n"
QUEST_DETAILS_OBJECTIVES_HEADER = "\nObjectifs :\n"
QUEST_DETAILS_OBJECTIVE_DONE = "  ✅ {objective}\n"
QUEST_DETAILS_OBJECTIVE_TODO = "  ⬜ {objective}\n"
QUEST_DETAILS_REWARD = "\n🎁 Récompense : {reward}\n"

NPC_REPLY_TEMPLATE = "\n{name} dit : '{line}'\n"
NPC_NO_MESSAGE = "Rien à dire."
