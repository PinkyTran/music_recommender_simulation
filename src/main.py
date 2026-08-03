"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

The recommender lives in recommender.py:
- load_songs
- score_song
- recommend_songs

Run it with:  python -m src.main   (from the project root)
"""

# Support both `python -m src.main` (package import) and `python src/main.py`.
try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard user profiles: everyday tastes we expect the system to serve well.
# ---------------------------------------------------------------------------
STANDARD_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "aggressive", "energy": 0.9},
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles: designed to try to "trick" the scoring
# logic and expose unexpected behavior. See model_card.md > Evaluation for the
# reasoning behind each one.
# ---------------------------------------------------------------------------
ADVERSARIAL_PROFILES = {
    # Conflicting signals: wants maximum energy but a sad/low-energy mood.
    # The catalog has no genuinely "sad" high-energy song, so the energy term
    # and the mood term pull in opposite directions.
    "Conflicting: High-Energy Sad": {"genre": "pop", "mood": "melancholy", "energy": 0.95},
    # Nothing in this profile exists in the catalog. Genre and mood can never
    # match, so ranking collapses onto the energy term alone.
    "Unknown Genre & Mood": {"genre": "polka", "mood": "ecstatic", "energy": 0.5},
    # Energy is outside the expected 0.0-1.0 range. The scoring never clamps
    # input, so this quietly biases the whole catalog toward its loudest songs.
    "Out-of-Range Energy": {"genre": "edm", "mood": "energetic", "energy": 1.8},
    # No preferences at all. Every song scores 0.0, so "top 5" is really just
    # whatever order the catalog happened to load in.
    "Empty Profile": {},
}


def _format_profile(user_prefs: dict) -> str:
    """Human-readable one-liner for a preference dict (handles empty dict)."""
    if not user_prefs:
        return "(no preferences)"
    return ", ".join(f"{key}={value}" for key, value in user_prefs.items())


def run_profile(name: str, user_prefs: dict, songs: list) -> None:
    """Run the recommender for one profile and print the top 5 results."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"User profile: {name}")
    print(f"Preferences: {_format_profile(user_prefs)}")
    print("Top recommendations:\n")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score: {score:.2f}")
        print(f"     Reasons: {explanation}")
        print()


def _ask_energy() -> float | None:
    """Prompt for an energy value in 0.0-1.0, re-asking on bad input. Blank = skip."""
    while True:
        raw = input("Energy 0.0 (calm) to 1.0 (intense)? [Enter to skip] ").strip()
        if not raw:
            return None
        try:
            value = float(raw)
        except ValueError:
            print("  Please enter a number like 0.7 (or press Enter to skip).")
            continue
        if not 0.0 <= value <= 1.0:
            print("  Energy must be between 0.0 and 1.0.")
            continue
        return value


def prompt_user() -> dict:
    """Ask the user what they like and build a preference dict from their answers."""
    print("Tell me what you're in the mood for. Press Enter to skip any question.\n")

    user_prefs: dict = {}

    genre = input("Favorite genre? (e.g. pop, lofi, rock) ").strip().lower()
    if genre:
        user_prefs["genre"] = genre

    mood = input("Mood? (e.g. happy, chill, intense) ").strip().lower()
    if mood:
        user_prefs["mood"] = mood

    energy = _ask_energy()
    if energy is not None:
        user_prefs["energy"] = energy

    return user_prefs


def run_interactive(songs: list) -> None:
    """Ask the user for their preferences, then show recommendations."""
    user_prefs = prompt_user()

    if not user_prefs:
        print("\nNo preferences entered, so every song scores the same. "
              "Try again and tell me at least one thing you like!")
        return

    print()
    print("-" * 70)
    run_profile("You", user_prefs, songs)


def run_demo(songs: list) -> None:
    """Run the fixed standard + adversarial profiles (used to build model_card.md)."""
    print("=" * 70)
    print("STANDARD PROFILES")
    print("=" * 70 + "\n")
    for name, prefs in STANDARD_PROFILES.items():
        run_profile(name, prefs, songs)
        print("-" * 70 + "\n")

    print("=" * 70)
    print("ADVERSARIAL / EDGE-CASE PROFILES")
    print("=" * 70 + "\n")
    for name, prefs in ADVERSARIAL_PROFILES.items():
        run_profile(name, prefs, songs)
        print("-" * 70 + "\n")


def main() -> None:
    import sys

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # `--demo` reproduces the fixed profiles used in model_card.md.
    # Default is the interactive flow: ask the user what they like.
    if "--demo" in sys.argv:
        run_demo(songs)
    else:
        run_interactive(songs)


if __name__ == "__main__":
    main()
