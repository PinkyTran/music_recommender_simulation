# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

My recommender works like a helpful friend who knows your taste and picks songs by matching, not guessing. First, I write down what you like, such as your favorite genre,your favorite mood, how energetic you want the music, and whether you prefer acoustic sounds. Then I go through every song and give it points for how well it fits. A song gets 2 points for matching your genre, up to 1.5 points for being close to your energy level, 1 point for matching your mood, and a small half point bonus if you like acoustic music and the song is acoustic too. So genre counts the most, then energy, then mood, then the acoustic bonus. I add up the points, jot down a plain reason for each one, sort the songs from best to worst, and hand you the top few with their reasons. One thing to watch out for is that genre is worth the most, so the system can focus too much on genre and miss a great mood match in a different genre. It also only counts exact matches, so "pop" gets no credit from "indie pop," which means songs that are close but not exact can get skipped unfairly.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Sample output from `python -m src.main` using the default **pop / happy / energy=0.8** profile:

```
Loaded songs: 27

User profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

  1. Sunrise City — Neon Echo
     Score: 5.46
     Reasons: genre match (+2.0), mood match (+1.5), energy fit (+1.96)

  2. Gym Hero — Max Pulse
     Score: 3.74
     Reasons: genre match (+2.0), energy fit (+1.74)

  3. Rooftop Lights — Indigo Parade
     Score: 3.42
     Reasons: mood match (+1.5), energy fit (+1.92)

  4. Concrete Kings — Blocktape
     Score: 1.96
     Reasons: energy fit (+1.96)

  5. Mirrorball Nights — Studio 45
     Score: 1.94
     Reasons: energy fit (+1.94)
```

The top pick, **Sunrise City**, is the only song that matches all three signals
(pop genre, happy mood, and energy ≈ 0.82 close to the target 0.8), so it scores
highest. Songs matching fewer signals rank lower.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



