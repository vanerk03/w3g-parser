"""
Module used to get player's MMR from w3champions
"""
import requests


def get_mmr(battle_tag: str) -> int:
    """
    Makes request to W3Champions and returns last solo MMR for the given player
    Returns last solo MMR available 
    (if a player has played a few races in that season, function returns maximal MMR among all of them)
    returns -1 if there is no solo mmr available
    """
    print(battle_tag)
    battle_tag = battle_tag.replace("#", "%23")
    url = f"https://website-backend.w3champions.com/api/players/{battle_tag}/game-mode-stats?gateWay=20&season="
    for season in range(12, 0, -1):
        response = requests.get(url + str(season)).json()
        lst = list(filter(lambda x: x["gameMode"] == 1, response))
        if lst:
            return max(lst, key=lambda x: x["mmr"])["mmr"]
    return 0
