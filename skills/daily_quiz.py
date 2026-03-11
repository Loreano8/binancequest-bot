"""
BinanceQuest AI — Daily Quiz Skill
Automated daily quiz sent every morning at 9:00 AM.
Keeps users engaged and builds learning streaks.
"""

from datetime import time

DAILY_QUIZ_HOUR = 9
DAILY_QUIZ_MINUTE = 0
DAILY_QUIZ_TIME = time(DAILY_QUIZ_HOUR, DAILY_QUIZ_MINUTE)

DAILY_MESSAGES = {
    "fr": "☀️ *Quiz du jour BinanceQuest !*\n\nC'est l'heure de tester tes connaissances crypto 🎯\n\nRéponds correctement pour gagner *+15 XP* !",
    "en": "☀️ *BinanceQuest Daily Quiz!*\n\nTime to test your crypto knowledge 🎯\n\nAnswer correctly to earn *+15 XP*!"
}

def get_daily_message(lang="fr"):
    return DAILY_MESSAGES.get(lang, DAILY_MESSAGES["fr"])
