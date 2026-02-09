# Projet EvalFBI – Evalbot TI LM3S9B92 🚓🤖

## Présentation générale

**EvalFBI** est un projet embarqué développé sur le robot **Evalbot TI LM3S9B92**, programmé entièrement en **assembleur ARM (Cortex-M3)**.  
L’objectif est de reproduire le comportement d’une **voiture de police autonome**, capable de patrouiller, détecter des obstacles et signaler un mode d’urgence.

Ce projet a été réalisé dans le cadre du module **IGI-3001**.

Le robot exécute une patrouille autonome, réagit aux collisions via des bumpers et dispose d’un mode urgence simulant des gyrophares.

---

## Fonctionnalités principales

### 1. Mode patrouille normale 🚔

- Activation par **Switch 1**
- Le robot avance en continu et effectue une ronde autonome
- Surveillance permanente des **bumpers gauche et droit**

En cas d’obstacle :
- arrêt immédiat
- marche arrière
- activation d’un clignotant lent (gauche ou droit)
- manœuvre d’évitement
- reprise automatique de la marche avant

---

### 2. Mode urgence 🚨

- Activation / désactivation par **Switch 2**
- Les deux LEDs clignotent rapidement pour simuler des gyrophares
- Le robot continue sa patrouille tout en signalant son état prioritaire

---

## Scénarios de fonctionnement

### Scénario 1 – Démarrage 🔋
- Robot immobile, LEDs éteintes
- Appui sur **Switch 1** → démarrage de la patrouille

### Scénario 2 – Mode urgence 🚨
- Appui sur **Switch 2** → clignotement rapide des LEDs
- Nouvel appui → retour à l’état normal

### Scénario 3 – Obstacle côté gauche ⬅️
- arrêt → recul → clignotant gauche (lent)
- rotation à droite → marche avant

### Scénario 4 – Obstacle côté droit ➡️
- arrêt → recul → clignotant droit (lent)
- rotation à gauche → marche avant

### Scénario 5 – Reprise normale 🔄
- Après chaque évitement, retour automatique à la boucle principale

---

## Architecture du code

Le projet est structuré en **modules assembleur ARM** distincts afin de garantir clarté et maintenabilité.

### `MOTEUR.s`
Gestion des moteurs :
- avancer
- reculer
- tourner à gauche / droite
- arrêt

### `LEDS.s`
Pilotage des LEDs (port F) :
- allumage / extinction
- clignotement lent directionnel
- clignotement rapide (mode urgence)

### `SWITCH.s`
Lecture des switches (port E) :
- Switch 1 : démarrage
- Switch 2 : activation du mode urgence

### `BUMPERS.s`
Détection des obstacles :
- bumper gauche
- bumper droit

### `MAIN.s`
Coordination générale :
- initialisation du matériel
- boucle de patrouille
- gestion des obstacles
- gestion du mode urgence
- reprise automatique du déplacement

---

## Structure du dépôt

```text
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
└── README.md
