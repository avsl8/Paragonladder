from dataclasses import asdict
from typing import List
from tinydb import TinyDB, Query
from diablo_api import Region
from extractor import AccountInfo
from pathlib import Path

class Database:
    def __init__(self, season: int, region: Region):
        self.season = season
        self.region = Region
        
        Path(f"../database/{season}").mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(f"../database/{season}/{region.value}.json")

    def update_account_infos(self, infos: List[AccountInfo]) -> None:
        for info in infos:
            self.db.update(asdict(info), Query().battletag == info.battletag)

    def insert_battletags(self, battletags: List[str]) -> None:
        i = 0
        for btag in battletags:
            if not self.db.search(Query().battletag == btag):
                self.db.insert(asdict(AccountInfo(btag)))
                i += 1

        print(f"Inserted {i} new battletags")

    def get_account_infos(self) -> List[AccountInfo]:
        return [AccountInfo(**d) for d in self.db.all() if d["paragon_season"]]

    def get_battltags(self) -> List[str]:
        return [x["battletag"] for x in self.db.all()]
