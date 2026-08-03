"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    profile = f"genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}"
    print(f"\nUser profile: {profile}")
    print("\nTop recommendations:\n")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score: {score:.2f}")
        print(f"     Reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()
