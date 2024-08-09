from dataclasses import dataclass


@dataclass
class GameState:
    gamestate_id: int
    major_stage: int
    minor_stage: int
    monsters_killed: int
    character_playing: int
