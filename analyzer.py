import pandas as pd
import re
from typing import Iterable
from w3g import W3gFile
from Eapm import eapm
from get_mmr import get_mmr

class Analyzer:
    """
    Analyzer class
    """

    def __init__(self, filename: str = "data.xlsx") -> None:
        self.filename = filename
        self.df = pd.read_excel(filename, index_col=0)

    def add_replays(self, lst: Iterable[W3gFile]):
        for file in lst:
            self.add_replay(file, save=False)
        self.df.to_excel(self.filename, sheet_name="data")

    def add_replay(self, file: W3gFile, save: bool = True, w3champ=True, w3g=True) -> None:
        if len(file.active_players) != 2 or not file.is_w3g or not re.search("W3Champions", file.mapname):
            print("Non-solo, .nwg and non-w3champions replays are ignored")
            return

        for battle_tag, acts, ef_acts, game_length in eapm(file):
            if battle_tag in self.df.index:
                ans = self.df.loc[battle_tag]
                self.df.loc[battle_tag] = [ans["acts"] + acts,
                                           ans["eff_acts"] + ef_acts,
                                           ans["length"] + game_length]
            else:
                self.df.loc[battle_tag] = [acts, ef_acts, game_length]
        if save:
            self.df.to_excel(self.filename, sheet_name="data")

    @property
    def working_dataset(self) -> pd.DataFrame:
        return self.df.assign(apm=lambda x: round(x.acts / x.length, 2),
                              epm=lambda x: round(x.eff_acts / x.length, 2),
                              mmr=lambda x: get_mmr(x.index))[["apm", "epm", "mmr"]]


def main():
    path = "C:\\Users\\User\\Downloads\\w3g-1.0.5\\1_32_replays\\Vanerk_Pogi.w3g"
    f = W3gFile(path)
    an = Analyzer()
    an.add_replay(f)
    print(an.working_dataset)


if __name__ == "__main__":
    main()
