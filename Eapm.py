from collections import namedtuple
from w3g import W3gFile, AbilityPositionObject

def eapm(f: W3gFile) -> list[tuple[str, int, int, float]]:
    """
    Args:
        f (W3gFile): file to analyze

    Returns:
        list[tuple[str, int, int, float]]
                   name, actions, effective actions, game length
    """
    apm = [0] * 24
    eapm = [0] * 24
    prev = [False] * 24
    prev_click = [False] * 24

    sr_players_id = {sr.player_id for sr in f.slot_records if sr.team < 12 and sr.player_id > 0}
    players = [x for x in f.players if x.id in sr_players_id]

    for event in f.events:
        id = event.player_id
        if event.apm:
            apm[id] += 1

            if isinstance(event, AbilityPositionObject):
                if prev_click[id] == event:
                    continue
                prev_click[id] = event

            if prev[id] != event:
                eapm[id] += 1
            
            prev[id] = event

    # number_of_players: TBA
    length_in_min = (f.replay_length / 60_000)
    
    for player in players:
        player.eff_actions = eapm[player.id]
        player.actions = apm[player.id]
        player.gaming_time = length_in_min

    
    return [(player.name, apm[player.id], eapm[player.id], length_in_min) for player in players]

def main():
    replay_path = ""
    f = W3gFile(replay_path)
    for x in eapm(f):
        print(x)


if __name__ == "__main__":
    main()