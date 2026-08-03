from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV into a list of song dicts, converting numeric columns to int/float."""
    import csv

    # Columns that should be whole numbers vs. decimal numbers.
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

# Relative importance of each preference. Weights sum to 1.0 so the final
# score is an interpretable 0.0-1.0 "match", and no single term can swamp the
# others (the flaw the sensitivity experiment exposed with additive points).
# To re-run a weight-shift experiment, adjust these and keep them summing to 1.
WEIGHTS = {"genre": 0.45, "mood": 0.25, "energy": 0.30}

# Songs matching neither the requested genre nor mood get scaled down so a
# strong energy match alone cannot surface an otherwise-irrelevant song.
NO_MATCH_PENALTY = 0.5


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song vs. user prefs on a 0.0-1.0 scale, returning (score, reasons).

    Each specified preference contributes a sub-score in [0, 1]; the final score
    is their weighted average. Only the preferences the user actually gave are
    counted, and the weights are renormalized over them, so a partial profile
    (e.g. genre only) still spans the full 0-1 range.
    """
    reasons: List[str] = []
    subscores: Dict[str, float] = {}  # preference name -> sub-score in [0, 1]

    # Genre: exact match or nothing.
    if user_prefs.get("genre"):
        subscores["genre"] = 1.0 if user_prefs["genre"] == song.get("genre") else 0.0

    # Mood: exact match or nothing.
    if user_prefs.get("mood"):
        subscores["mood"] = 1.0 if user_prefs["mood"] == song.get("mood") else 0.0

    # Energy: numerical closeness on a 0-1 scale (1.0 = identical energy).
    if user_prefs.get("energy") is not None and song.get("energy") is not None:
        diff = abs(float(user_prefs["energy"]) - float(song["energy"]))
        subscores["energy"] = 1.0 - diff

    # No preferences given -> nothing to score against.
    if not subscores:
        return 0.0, ["no preferences given"]

    # Weighted average, renormalized over only the preferences that were given.
    total_weight = sum(WEIGHTS[key] for key in subscores)
    score = sum(WEIGHTS[key] * value for key, value in subscores.items()) / total_weight

    # Build human-readable reasons showing each term's contribution to `score`.
    for key, value in subscores.items():
        contribution = round(WEIGHTS[key] * value / total_weight, 2)
        if key == "energy":
            reasons.append(f"energy fit {round(value, 2)} (+{contribution})")
        elif value == 1.0:
            reasons.append(f"{key} match (+{contribution})")
        else:
            reasons.append(f"{key} mismatch (+0.0)")

    # Relevance gate: if genre and/or mood were requested but none matched,
    # this song is only surfacing on energy — scale it down.
    categorical = [subscores[k] for k in ("genre", "mood") if k in subscores]
    if categorical and not any(value == 1.0 for value in categorical):
        score *= NO_MATCH_PENALTY
        reasons.append(f"no genre/mood match (x{NO_MATCH_PENALTY})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score_song() and return the top k as (song, score, explanation) tuples."""
    # Judge every song in the catalog, building (song, score, explanation) tuples.
    scored = [
        (song, score, ", ".join(reasons) if reasons else "no strong matches")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # sorted() returns a NEW list (highest score first) without mutating `scored`.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return ranked[:k]