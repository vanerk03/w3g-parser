from w3g import File, AbilityPositionObject

def eapm(f: File) -> list[tuple[str, float, float]]:
    """
    Args:
        f (File): file to analyze

    Returns:
        list[tuple[str, float, float]]: player name, apm, eapm
    """

    apm = [0] * 24
    eapm = [0] * 24
    prev = [False] * 24
    prev_click = [False] * 24

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
    return [(f.players[0].name, apm[1] / length_in_min, eapm[1] / length_in_min), (f.players[1].name, apm[2] / length_in_min, eapm[2] / length_in_min)]

def main():
    replay_path = ""
    f = File(replay_path)
    print(eapm(f))

if __name__ == "__main__":
    main()