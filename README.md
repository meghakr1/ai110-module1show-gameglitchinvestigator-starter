# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**What the game is.** It's a number-guessing game built with Streamlit. You pick a difficulty (Easy, Normal, or Hard), the app picks a secret number in that range, and you get a limited number of guesses. After each guess it tells you whether to go higher or lower, tracks your score, and ends the game on a win or when you run out of attempts.

**Bugs I found.**

1. **The hints were backwards and inconsistent.** When a guess was too high, the game said "Go HIGHER!" — the opposite of what you need. On top of that, `check_guess` sometimes compared the secret as *text* instead of a number (e.g. `"9" > "42"` is `True` alphabetically), so the feedback flipped between guesses.
2. **The game was basically unwinnable.** Following the wrong hints walked me away from the answer. Two smaller issues made it worse: the range banner always said "between 1 and 100" even in Easy (1–20) / Hard (1–50) mode, and the attempt counter started at 1 instead of 0, so "Attempts left" was off by one.
3. **"New Game" froze the app.** After a win or loss, New Game only reset `attempts` and `secret` but left `status` stuck on `"won"`/`"lost"`, so the app locked on the end screen and wouldn't restart.
4. **Wrong guesses could *raise* your score.** `update_score` gave +5 for a too-high guess on even-numbered attempts, so guessing wrong sometimes earned points.

**Fixes I applied.**

- Moved the four logic functions into `logic_utils.py` so they can be unit-tested without Streamlit.
- Made `check_guess` a plain numeric comparison (removed the string comparison and the `try/except` that was hiding the type error), and put the higher/lower advice in a correct outcome→message map in `app.py`.
- Used the real difficulty range in the banner and started the attempt counter at 0.
- Made New Game reset *all* per-game state (`attempts`, `secret`, `score`, `status`, `history`) and use the difficulty range for the new secret.
- Made every wrong guess cost a flat −5 in `update_score`.
- Added `conftest.py` at the project root so `pytest` finds `logic_utils`, and added regression tests for the bugs above.

## 📸 Demo Walkthrough

Here's how to play the fixed game from start to a win:

1. **Start the app** with `python -m streamlit run app.py` and open it in the browser. Leave the difficulty on **Normal** (range 1–100, 8 attempts).
2. **Open "Developer Debug Info"** to peek at the secret number — handy for confirming the hints are now correct.
3. **Make a guess** that's too high (say the secret is 42 and you guess 60). The hint now correctly says **"📉 Go LOWER!"**, and the score drops by 5.
4. **Guess lower** (e.g. 30). It says **"📈 Go HIGHER!"** — the direction is consistent every time now, no more flipping between guesses.
5. **Guess the secret (42).** You get the 🎉 win message, balloons, and a final score that *adds* points based on how few guesses you used.
6. **Click "New Game 🔁".** The game fully resets — fresh secret, score back to 0, attempts cleared — and you can play again immediately instead of being stuck on the win screen.
7. **(Optional) Switch to Easy or Hard.** The on-screen range updates to match (1–20 or 1–50) instead of always saying 1–100.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

All 15 tests pass, including the regression tests written specifically for the bugs above:

```
$ python -m pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.13.0, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/rahulkowdeed/Documents/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 15 items

tests/test_game_logic.py ...............                                 [100%]

============================== 15 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
