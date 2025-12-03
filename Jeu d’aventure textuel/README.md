🌌 Projet : La Révolte du Vigilant
Jeu d’aventure textuel – Python
📖 Présentation générale

Ce projet consiste à développer un jeu d’aventure textuel complet en Python, basé sur un système de commandes, exploration, choix moraux, combats, gestion des ressources et progression narrative.
Le joueur incarne un membre du vaisseau Vigilant, chargé de trouver une nouvelle planète habitable après la destruction de la Terre. Chaque décision influence le moral, les ressources, la réputation, les alliés et la suite de l’histoire.
Toutes les mécaniques, choix et arcs narratifs proviennent du document fourni (Projet INFO.pdf).

🗺️ Résumé des scénarios
🌑 Planète A — Eridani Prime

Le Vigilant s’écrase sur une planète minière dominée par le tyran Vorn.
Le joueur doit gérer un grand dilemme initial (sauver l'équipage ou les ressources), négocier avec un marchand douteux ou rejoindre des rebelles menés par Yara, puis traverser trois villes avant d’affronter Vorn dans la forteresse.
Les choix déterminent les alliés, les ressources disponibles et l’état moral du groupe.

🤖 Planète B — Velyra IX

Monde cybernétique contrôlé par Karn, ses IA et ses drones.
Le joueur choisit entre étudier la planète ou attaquer immédiatement, puis doit décider de voler les civils ou corrompre un général pour obtenir armes et accès militaires.
Libérer Narek, frère de Yara, mène à un dilemme final : sauver Yara ou Narek avec une seule dose de nanomédecine.

✨ Planète C — Aurelion Prime

Un paradis doré… fondé sur l’exploitation totale des autres mondes.
Le chef suprême est Seren Taal, ancienne capitaine du Vigilant, devenue dirigeante autoritaire.
Le joueur doit s’infiltrer dans cette société parfaite ou se révéler ouvertement, puis traverser le Nœud (centre de contrôle cérébral), avant de choisir entre accepter une alliance immorale ou affronter Seren Taal dans le combat le plus difficile du jeu.

🌍 Planète D — Nova Terra

La destination finale : une planète immense, fertile et habitable.
Le joueur peut ignorer ou explorer une station orbitale ancienne avant d’atterrir. Les peuples libérés des trois mondes prononcent leurs serments d’unité.
Dernier choix : devenir dirigeant suprême ou laisser un Conseil interplanétaire gouverner librement.
C’est la renaissance de l’humanité.

🧩 Structure du projet
my_TBA_project
|
|-- README.md                                   # ce fichier
|-- actions.py                                  # classe Actions : interactions et actions possibles
|-- character.py                                # classe Character : gestion des PNJ
|-- command.py                                  # classe Command : format et exécution d'une commande
|-- config.py                                   # configuration du jeu, ressources, paramètres, planètes
|-- game.py                                     # classe Game : moteur principal du jeu
|-- item.py                                     # classe Item : gestion des objets
|-- player.py                                   # classe Player : stats, inventaire, ressources, moral
|-- room.py                                     # classe Room : lieux, transitions, événements
|-- test.py                                     # tests automatisés (logique, combat, commandes)
|-- video.mp4                                   # vidéo de démonstration
|-- win.py                                      # conditions de victoire, défaite, fins possibles

🚀 Fonctionnalités attendues

– Système de commandes textuelles
– Gestion du joueur : moral, attaque, défense, réputation
– PNJ avec comportements et dialogues
– Objets, inventaire, utilisation d’items
– Combats avec conséquences
– Enchaînement des planètes et choix narratifs
– Conditions de victoire et fins alternatives
