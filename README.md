# 🎵 Music Recommender Simulation

## Project Summary

TuneFit 2.0 is a small, explainable music recommender. You describe your taste in a few fields a favorite genre, a mood, and how energetic you want the music and it returns the five best-fitting songs from a 50 songs catalog, each with a plain-language reason for why it was picked.

This project builds and then interrogates that recommender:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into ranked recommendations
- Evaluate what the system gets right and wrong (including adversarial edge cases)
- Reflect on how those choices mirror real-world AI recommenders

---

## How The System Works

Think of it as a scorecard. For every song in the catalog, TuneFit asks
three questions and awards points:

1. Is it the genre you asked for?: Worth the most about 45% of the score (a hit or a miss, nothing in between).
2. Does the mood match?: Worth about 25%:  also all or nothing.
3. Is the energy about right? Worth about 30%, on a sliding scale: the closer a song's energy is to your target, the more points it earns. Those combine into a single match score from 0 to 1, where 1 is a perfect fit on all three. The five highest-scoring songs are your recommendations, each
shown with the reasons it earned its points. Two safeguards keep it honest: a song that matches neither your genre nor your mood has its score cut in half (so an irrelevant song can't sneak in on energy alone), and empty or invalid
input is handled gracefully instead of returning a meaningless list.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running the app

By default the app is **interactive** — it asks what you like and recommends
based on your answers (press Enter to skip any question):

```bash
python -m src.main
```

```bash
python -m src.main --demo
```

### Running Tests

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Sample output from `python -m src.main --demo` for the High-Energy Pop
profile (`genre=pop, mood=happy, energy=0.9`) against the 50-song catalog:

```
User profile: High-Energy Pop
Preferences: genre=pop, mood=happy, energy=0.9
Top recommendations:

  1. Shake It Off — Taylor Swift
     Score: 0.97
     Reasons: genre match (+0.45), mood match (+0.25), energy fit 0.9 (+0.27)

  2. Levitating — Dua Lipa
     Score: 0.73
     Reasons: genre match (+0.45), mood mismatch (+0.0), energy fit 0.93 (+0.28)

  3. Rolling in the Deep — Adele
     Score: 0.71
     Reasons: genre match (+0.45), mood mismatch (+0.0), energy fit 0.87 (+0.26)

  4. Blinding Lights — The Weeknd
     Score: 0.70
     Reasons: genre match (+0.45), mood mismatch (+0.0), energy fit 0.83 (+0.25)

  5. Dynamite — BTS
     Score: 0.51
     Reasons: genre mismatch (+0.0), mood match (+0.25), energy fit 0.87 (+0.26)
```

The top pick, Shake It Off, is the only song matching all three signals (pop genre, happy mood, energy ≈ 0.9), so it scores near-perfectly. Notice that Blinding Lights ranks #4 despite not being a happy song — it's pop and loud, and those two signals outweigh the mood. 

---

## Experiments You Tried

- Adversarial edge-case profiles. Built profiles designed to trick the scoring — a "loud but sad" conflict, an unknown genre/mood, out-of-range energy (1.8), and an empty profile — to see where the logic breaks.
- Weight-shift sensitivity test. Doubled the energy weight and halved genre. A song matching *nothing* the user asked for jumped into the top 5 on energy alone — which motivated the scoring rewrite.
- Scoring rewrite (v1 → v2). Replaced the additive point system with a normalized weighted average (genre 0.45 / mood 0.25 / energy 0.30) plus a relevance-gate penalty, so no single feature can dominate.
- Catalog expansion. Grew the catalog from a handful of songs per genre to 50 real, well-known songs across 24 genres, which gave genre-based ranking actual variety to work with.

---

## Limitations and Risks

- Tiny catalog. 50 songs is far too few to serve real, varied taste.
- Estimated audio features. The energy/valence/danceability/acousticness values are hand-estimated, not official measurements 
- Genre filter bubble.Genre is exact-match only, so a punk fan is never shown rock; the system reinforces existing taste instead of broadening it.
- Under-serves calm listeners. The catalog skews loud (mean energy 0.60),so low-energy requests get a poor selection.
- Mood is nearly dead weight. Most moods appear on only one song, so mood rarely influences the result.
- No lyrics, language, popularity, or listening history.



---

## Reflection

Building this made one thing concrete: a recommender's weights are its opinions. Nothing about "genre matters more than mood" is a fact it's a choice, and changing a single number visibly reshuffled which songs people saw. Turning raw data into a ranked prediction is really just deciding what counts and how much, then trusting the arithmetic. Watching a sensitivity experiment let a totally irrelevant song leap into the top five drove home how fragile those choices are. The part that stuck with me is how invisible bias can be. I never decided to
under-serve calm listeners, but a loud-skewed catalog plus a symmetric energy formula did exactly that and it only surfaced because I went looking with edge-case profiles. The recommenders we use every day are full of similar hidden
choices; "the algorithm" is really just someone's scorecard, defaults and blind spots included. I'll trust those feeds a little less, and wonder about their
weights a little more.


