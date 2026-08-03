# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

TuneFit 2.0: a "fit"-based music recommender. The 2.0 marks the switch from the original point-adding logic to a normalized, weighted "match score."

---

## 2. Intended Use  

TuneFit takes a few simple preferences — a favorite genre, a mood, and how energetic you want the music — and returns the five songs from a 50-song catalog that best fit them, along with a short reason for each pick. It is built for classroom exploration, not for real listeners. It's a sandbox for understanding how a recommender turns preferences into rankings, so the results are meant to be inspected and questioned rather than trusted. It assumes the user can describe their taste in those three fields, that a single "energy" number is a meaningful summary of loudness/intensity, and that a song's genre and mood are single fixed labels. Those are big simplifications, real listeners rarely fit them, which is part of what the project is designed to expose.

---

## 3. How the Model Works  

Think of it as a scorecard. For every song in the catalog, TuneFit asks three
questions and awards points:

1. Is it the genre you asked for?: This is worth the most (about 45% of the score) — a hit or a miss, nothing in between.
2. Does the mood match?: Worth a bit less (about 25%) also all or nothing.
3. Is the energy about right? Worth the middle amount (about 30%). This one is a sliding scale: the closer a song's energy is to what you asked for, the more points it earns. It adds those up into a single "match score" from 0 to 1, where 1 means a perfect fit on all three. The five highest-scoring songs are your recommendations, each shown with the reasons it earned its points.
4. What changed from the starter version. The original code just piled up raw points, and because the energy points could grow much larger than the genre or mood points, energy quietly took over the ranking — a song could reach the top purely by being the right loudness, even if it matched nothing you asked for. I rebuilt it as a weighted average that always lands between 0 and 1, so no single ingredient can dominate. I also added two safeguards: songs that match neither your genre nor your mood get their score cut in half (so an irrelevant song can't sneak in on energy alone), and empty or invalid input is now handled honestly instead of returning a meaningless list.

---

## 4. Data  

The catalog is [data/songs.csv](data/songs.csv): 50 songs, each with a title, artist, genre, mood, and four numeric audio features (energy, tempo_bpm, valence, danceability, acousticness). 24 genres are represented, weighted toward the mainstream: pop and rock have 4 songs each; hip hop, edm, jazz, r&b, and lofi have 3 each; ten more
genres (metal, classical, indie pop, folk, country, soul, funk, techno,synthwave, k-pop) have 2 each; and seven (reggae, punk, gospel, disco, bossa nova, blues, ambient) have 1 each. Moods span a wide emotional range: happy, aggressive, melancholy, peaceful, euphoric, wistful, and more.

The dataset went through two rounds:

1. It started as fictional placeholder songs shipped with the assignment.
2. I then replaced all 50 with real, well-known songs (e.g. Blinding Lights — The Weeknd, Bohemian Rhapsody — Queen, Take Five — The Dave Brubeck Quartet).

| Column | Provenance |
|--------|-----------|
| title, artist, genre | Real and verifiable — actual songs and artists |
| tempo_bpm | Close to documented tempos (a few reflect Spotify's half/double-time detection, e.g. *Take Five* at 174) |
| energy, valence, danceability, acousticness | Informed estimates, not measured. Spotify's audio-features API (the authoritative source) was deprecated for general access in late 2024, and third-party mirrors block automated access, so these were set by hand from each song's known character |
| mood | Subjective label assigned per song — no such field exists in any real dataset |

So the recommender runs on real songs but with hand-estimated audio features. On genuine Spotify data the numbers would be noisier and less cleanly genre-separable, so the system would likely look somewhat worse.

What's missing from the data: lyrics, language, release year, artist popularity, and any notion of listening history or context (time of day, activity). Taste is reduced to genre + mood + one energy number.

---

## 5. Strengths  

It works best for mainstream listeners with a clear, consistent taste. When someone asks for a well-stocked genre and a mood and energy that agree with each other like High-Energy Pop or Deep Intense Rock — the results are genuinely good: the perfect three-way match lands at #1 with a near 1.0 score, and the rest of the list is filled with sensible same-genre songs ranked by how well their energy fits. These matched my intuition closely (Nirvana topping an
aggressive-rock search felt exactly right).
A few patterns the scoring captures well:
- Energy ordering: Within a genre, songs sort cleanly from most to least energetic relative to what the user asked for, which feels natural.
- Explainability: Every recommendation comes with a plain reason string ("genre match, mood mismatch, energy fit 0.9"), so it's always clear why a song was chosen — a real strength for a teaching tool.
- No single feature can dominate. The weighted-average design keeps genre, mood, and energy in a sensible balance, which was the main flaw in v1.

---

## 6. Limitations and Bias 

The energy-gap calculation quietly under-serves low-energy listeners. The energy score is `1 - |user_energy - song_energy|`, which simply rewards songs close to the user's target — but the catalog itself is skewed loud: its mean energy is 0.60, and only 6 of the 50 songs fall below 0.3. So a calm listener (say, someone wanting 0.1-energy music for sleep or focus) has almost nothing close to match, and because genre is weighted more heavily (0.45 vs. energy's
0.30), their top results fill up with loud songs from the "right" genre that completely miss the mood they asked for. A high-energy pop fan, by contrast, sits right in the fat part of the distribution and gets a coherent, well-matched
list. In effect the scoring doesn't ignore low-energy users on purpose — the data imbalance plus the symmetric energy gap does it for us, and nothing in the code flags that the closest available song is still a poor fit.
Two related biases surfaced in the same experiments:

- Genre acts as a filter bubble. Genre is an exact-string match worth 45% of the score with no concept of adjacency, so a punk fan is never shown rock and a bossa nova fan never gets jazz. Combined with 7 genres having only a single song, niche-taste users get one real match and then the 0.14 relevance-gate floor — while mainstream (pop/rock) users get a rich top 5. The system reinforces existing taste instead of broadening it.
- Mood is nearly dead weight. 17 of the 31 moods appear on only one song, so mood rarely matches unless the user types the exact label — making the system effectively "genre + energy" for most people.

---


## 7. Evaluation  

I evaluated the recommender in two passes on the 50-song real-music catalog, using the normalized weighted-average scoring (genre 0.45, mood 0.25, energy 0.30; final score is a 0.0–1.0 "match"). First I ran three standard profiles for everyday tastes. Then, in a separate "System Evaluation" session, I asked my AI coding assistant to design adversarial / edge-case profiles meant to trick the scoring. All profiles live in [src/main.py](src/main.py) and
reproduce with `python -m src.main --demo`.

### Standard profiles

All three behave as expected: the song matching genre + mood + energy lands at
#1 with a near-perfect score, and same-genre songs follow, ranked by energy.

High-Energy Pop — `genre=pop, mood=happy, energy=0.9`

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

Chill Lofi — `genre=lofi, mood=chill, energy=0.35`

```
User profile: Chill Lofi
Preferences: genre=lofi, mood=chill, energy=0.35
Top recommendations:

  1. Feather — Nujabes
     Score: 0.97
     Reasons: genre match (+0.45), mood match (+0.25), energy fit 0.9 (+0.27)

  2. Luv(sic) Part 3 — Nujabes
     Score: 0.75
     Reasons: genre match (+0.45), mood mismatch (+0.0), energy fit 1.0 (+0.3)

  3. Aruarian Dance — Nujabes
     Score: 0.75
     Reasons: genre match (+0.45), mood mismatch (+0.0), energy fit 1.0 (+0.3)

  4. Take Five — The Dave Brubeck Quartet
     Score: 0.15
     Reasons: genre mismatch (+0.0), mood mismatch (+0.0), energy fit 1.0 (+0.3), no genre/mood match (x0.5)

  5. Bohemian Rhapsody — Queen
     Score: 0.14
     Reasons: genre mismatch (+0.0), mood mismatch (+0.0), energy fit 0.95 (+0.28), no genre/mood match (x0.5)

---

## 8. Future Work ##

The evaluation pointed to clear next steps, roughly in order of impact:

- Make genre a soft signal, not a hard filter. Right now genre is exact-match only, which creates the filter bubble from Section 6. I'd add a notion of genre adjacency (punk is close to rock, bossa nova close to jazz) so users get related discoveries instead of only their exact label.
- Fix the energy edge and the low-energy bias.** Clamp energy input to 0–1 in the scoring itself (not just the prompt), add a floor so a distant "closest" song is flagged as a poor fit, and add more low-energy songs to the catalog so calm listeners aren't underserved.
- Give mood real weight. Replace the 31 scattered mood labels with a small, controlled vocabulary and let moods be similar rather than exact, so mood stops being dead weight.
- Detect conflicting preferences. When a request can't be satisfied (loud + sad), say so, rather than silently letting energy win.
- Use the features already in the data.** valence, danceability, tempo, and acousticness are loaded but ignored folding them in would allow richer, more human tastes ("acoustic and danceable but calm").
- Improve diversity in the top 5. Add a rule that avoids returning three songs by the same artist (as happened with the three Nujabes tracks for Lofi).

---

## 9. Personal Reflection  

The most eye-opening lesson was that a recommender's weights are its opinions. Nothing about "genre matters more than mood" is a fact it's a choice I made and changing one number visibly reshuffled which songs people saw. Watching the
sensitivity experiment (doubling energy, halving genre) let a totally irrelevantsong jump into the top five made the stakes concrete. The biggest surprise was how invisible bias can be. I never decided to under-serve calm listeners, but the combination of a loud-skewed catalog and a symmetric energy formula did exactly that — and it only showed up because I went
looking with edge-case profiles. It made me realize that the recommenders I use every day are full of similar hidden choices, and that "the algorithm" is really just someone's scorecard, defaults and blind spots included.I'll trust those
feeds a little less and wonder about their weights a little more.
