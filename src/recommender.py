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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song vs. user prefs, returning (numeric score, list of reason strings)."""
    GENRE_POINTS = 2.0
    MOOD_POINTS = 1.5
    ENERGY_WEIGHT = 2.0

    score = 0.0
    reasons: List[str] = []

    # Genre match
    if user_prefs.get("genre") and user_prefs["genre"] == song.get("genre"):
        score += GENRE_POINTS
        reasons.append(f"genre match (+{GENRE_POINTS})")

    # Mood match
    if user_prefs.get("mood") and user_prefs["mood"] == song.get("mood"):
        score += MOOD_POINTS
        reasons.append(f"mood match (+{MOOD_POINTS})")

    # Energy fit: numerical closeness on a 0-1 scale.
    if user_prefs.get("energy") is not None and song.get("energy") is not None:
        diff = abs(float(user_prefs["energy"]) - float(song["energy"]))
        energy_points = round((1 - diff) * ENERGY_WEIGHT, 2)
        score += energy_points
        reasons.append(f"energy fit (+{energy_points})")

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