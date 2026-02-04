"""
ai_quiz.py - Minimal AI quiz used to decide who attacks in combat.
"""

import random

STATS = {
    "correct": 0,
    "wrong": 0,
}

QUESTIONS = [
    ("Quel est le nom du plus grand volcan du systeme solaire ?", "olympus mons"),
    ("Quel astronaute a ete le premier homme a marcher sur la Lune ?", "neil armstrong"),
    ("Qui est l'auteur du roman de science-fiction 'Dune' ?", "frank herbert"),
    ("Comment s'appelle notre galaxie ?", "voie lactée"),
    ("Quelle planete est la plus proche du Soleil ?", "mercure"),
    ("Quelle est la planete rouge ?", "mars"),
    ("Quelle planete a des anneaux visibles ?", "saturne"),
    ("Quel est le nom du satellite naturel de la Terre ?", "lune"),
    ("Qui a ecrit le roman de science-fiction 'Fondation' ?", "isaac asimov"),
    ("Quel est le nom du vaisseau de Han Solo ?", "faucon millenium"),
    ("Quel element chimique a le symbole O ?", "oxygène"),
    ("Comment s'appelle la station spatiale internationale ?", "iss"),
    ("Dans Star Wars, quel est le nom du pere de Luke Skywalker ?", "dark vador"),
    ("Quelle planete est surnommee la geante gazeuse ?", "jupiter"),
    ("Quelle planete a la duree du jour la plus longue ?", "venus"),
    ("Qui a ecrit '1984' ?", "george orwell"),
    ("Qui est l'auteur de 'La guerre des mondes' ?", "hg wells"),
    ("Quel est le nom du robot dans le film 'Interstellar' ?", "tars"),
    ("Quel est le nom du vaisseau dans 'Alien' ?", "nostromo"),
    ("Qui a ecrit 'Fahrenheit 451' ?", "ray bradbury"),
    ("Quelle est l'etoile la plus proche de la Terre ?", "soleil"),
    ("Quel est le nom de la galaxie d'Andromede ?", "andromede"),
    ("Quelle planete a la plus grande lune du systeme solaire ?", "jupiter"),
    ("Comment s'appelle la sonde qui a visite Pluton en 2015 ?", "new horizons"),
    ("Quel est le nom du telescope spatial lance en 1990 ?", "hubble"),
    ("Quelle est la capitale de Mars dans le film 'Total Recall' ?", "mars"),
    ("Quelle planete possede le plus de lunes connues ?", "saturne"),
    ("Quel est le nom du premier satellite artificiel ?", "spoutnik"),
    ("Qui a ecrit 'Le meilleur des mondes' ?", "aldous huxley"),
    ("Quel element chimique a le symbole Fe ?", "fer"),
    ("Quel est le nom du heros principal dans 'Matrix' ?", "neo"),
    ("Comment s'appelle l'ordinateur de bord de '2001, l'odyssee de l'espace' ?", "hal 9000"),
    ("Quel est le nom du vaisseau de 'Star Trek' ?", "enterprise"),
    ("Dans Star Wars, qui est le maitre de Luke ?", "yoda"),
    ("Quelle planete est la plus froide du systeme solaire ?", "uranus"),
    ("Quel est le nom du film ou un extraterrestre dit 'Telephone maison' ?", "et"),
    ("Qui a ecrit 'La main gauche de la nuit' ?", "ursula k le guin"),
    ("Quel est le nom du robot dans 'Wall-E' ?", "wall-e"),
    ("Quel est le nom du capitaine dans 'Star Trek' original ?", "kirk"),
    ("Quel est le symbole chimique du carbone ?", "c"),
    ("Quelle est la vitesse de la lumiere en km/s (arrondi) ?", "300000"),
    ("Quel est le nom du pere de Leia dans Star Wars ?", "dark vador"),
    ("Quel est le nom du droide d'Anakin ?", "r2-d2"),
    ("Quel est le nom du superordinateur dans 'Tron' ?", "mcp"),
    ("Qui a ecrit 'Solaris' ?", "stanislaw lem"),
    ("Quel est le nom de la planete d'origine de Superman ?", "krypton"),
    ("Quel est le nom du pilote dans 'Blade Runner 2049' ?", "k"),
    ("Qui a ecrit 'I, Robot' ?", "isaac asimov"),
    ("Quel est le nom de la planete des Na'vi dans 'Avatar' ?", "pandora"),
]

_remaining_questions = []


def get_question():
    """
    Return a question and its expected answer.
    """
    if not _remaining_questions:
        _remaining_questions.extend(QUESTIONS)
        random.shuffle(_remaining_questions)
    return _remaining_questions.pop()


def evaluate_answer(_player, user_answer, expected_answer):
    """
    Evaluate the user's answer and return True if correct.
    """
    normalized = user_answer.strip().lower()
    if normalized == expected_answer.lower():
        print("Bonne reponse. Vous prenez l'initiative.")
        STATS["correct"] += 1
        return True

    print(f"Mauvaise reponse. La bonne reponse etait : {expected_answer}.")
    STATS["wrong"] += 1
    return False


def get_ai_status(_player):
    """Return a short summary of quiz performance."""
    total = STATS["correct"] + STATS["wrong"]
    if total == 0:
        return "L'IA n'a encore pose aucune question."

    ratio = int((STATS["correct"] / total) * 100)
    return (
        f"IA de combat - bonnes reponses : {STATS['correct']}, "
        f"mauvaises : {STATS['wrong']}, "
        f"reussite {ratio}%"
    )
