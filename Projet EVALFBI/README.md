Projet EvalFBI (Evalbot – TI LM3S9B92) 🚓🤖
Présentation générale

EvalFBI est un projet développé sur le robot Evalbot TI LM3S9B92, programmé entièrement en assembleur ARM, dont l’objectif est de reproduire le comportement d’une voiture de police autonome. 🚨

Le robot exécute une patrouille, réagit aux obstacles, et dispose d’un mode d’urgence imitant les gyrophares d’un véhicule prioritaire.
Ce projet a été réalisé dans le cadre du module IGI-3001.

Fonctionnalités principales
1. Mode patrouille normale 🚔

Après un appui sur Switch 1, le robot se met en marche avant et effectue une ronde continue.
Pendant la patrouille :
• Surveillance constante des deux bumpers.
• En cas d’obstacle, le robot :
– s’arrête ⛔
– recule ↩️
– active un clignotant lent (gauche ou droite) 🔁
– contourne l’obstacle
– reprend la marche avant ▶️

2. Mode urgence 🚨

Activé/désactivé par Switch 2.
• Les deux LEDs clignotent rapidement pour simuler les gyrophares d’un véhicule d’intervention.
• Le robot continue sa patrouille mais signale son passage en mode prioritaire.

Scénarios de fonctionnement
Scénario 1 – Démarrage 🔋

• LEDs éteintes, robot immobile.
• Pression Switch 1 → marche avant.

Scénario 2 – Mode urgence 🚨⚡

• Pression Switch 2 → LEDs clignotement rapide.
• Pression à nouveau → LEDs éteintes.

Scénario 3 – Obstacle côté gauche ⬅️

• arrêt → recul → clignotant gauche (lent) → rotation à droite → marche avant.

Scénario 4 – Obstacle côté droit ➡️

• arrêt → recul → clignotant droit (lent) → rotation à gauche → marche avant.

Scénario 5 – Reprise normale 🔄

• après chaque évitement, retour automatique à la boucle principale.

Architecture du code 🧩

Le projet est structuré en 5 modules assembleur ARM :

MOTEUR.s ⚙️

Gestion des moteurs :
• avancer
• reculer
• tourner gauche/droite
• stop

LEDS.s 💡

Pilotage des LEDs du port F :
• allumer/éteindre
• clignotement lent (directionnel)
• clignotement rapide (urgence)

SWITCH.s 🔘

Lecture des deux switches (port E) :
• Switch 1 → démarrage
• Switch 2 → urgence ON/OFF

BUMPERS.s 🛑

Détection obstacle via bumpers gauche/droit.

MAIN.s 🧠

Coordination générale :
• initialisations
• boucle de patrouille
• gestion des obstacles
• gestion du mode urgence
• reprise automatique de la marche avant

Structure du dépôt (exemple) 📁
/EvalFBI
│
├── src/
│   ├── MAIN.s
│   ├── MOTEUR.s
│   ├── LEDS.s
│   ├── SWITCH.s
│   └── BUMPERS.s
│
├── docs/
│   ├── Rapport-Projet.pdf
│   └── Références techniques
│
└── README.md   ← ce fichier

Compilation & Flash 🛠️
Compilation (exemple avec arm-none-eabi)
arm-none-eabi-as -mcpu=cortex-m3 -g -o MAIN.o MAIN.s
arm-none-eabi-ld -T LM3S9B92.ld -o MAIN.elf MAIN.o
arm-none-eabi-objcopy -O binary MAIN.elf MAIN.bin

Flash du programme

Selon votre configuration :
• via bootloader USB
• via JTAG
• via l’IDE Keil µVision

Références techniques 📚

• Texas Instruments – LM3S9B92
• ARM Architecture Reference Manual
• Keil µVision 5
• TI EVALBOT Documentation
