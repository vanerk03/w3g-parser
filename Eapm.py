from collections import deque, namedtuple
from w3g import W3gFile, AbilityPositionObject
import matplotlib.pyplot as plt

def eapm(f: W3gFile | str) -> list[tuple[str, int, int, float]]:
    """
    Args:
        f (W3gFile): file to analyze

    Returns:
        list[tuple[str, int, int, float]]
                   name, actions, effective actions, game length
    """
    if isinstance(f, str):
        f = W3gFile(f)
    
    apm = [0] * 24
    eapm = [0] * 24
    prev = [False] * 24
    prev_click = [False] * 24

    actions_time = [[] for _ in range(24)]
    actions = [deque() for _ in range(24)]

    
    sr_players_id = {
        sr.player_id for sr in f.slot_records if sr.team < 12 and sr.player_id > 0}
    
    players = [x for x in f.players if x.id in sr_players_id]

    
    for event in f.events:
        id = event.player_id

        if event.apm:
            apm[id] += 1
            
            actions[id].append(apm[id] / (event.time / 60_000))
            actions_time[id].append(event.time / 1000)

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
        plt.plot(actions_time[player.id], actions[player.id], label=player.name, linewidth=2)
    
    plt.legend(loc="upper right")
    plt.xlabel("Sec")
    plt.ylabel("APM")

    plt.show()

    return [(player.name, apm[player.id], eapm[player.id], length_in_min) for player in players]


def main():
    replay_path = "1.33.w3g"
    f = W3gFile(replay_path)

    for x in eapm(f):
        print(x)


if __name__ == "__main__":
    main()
