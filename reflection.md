# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game it *looked* finished — title, difficulty selector, a guess box, Submit / New Game buttons, and a debug panel — but it was unplayable. The number feedback pointed me the wrong way, I could never actually win within the attempt limit, and once a game ended the "New Game" button didn't really start a fresh game.

I found three concrete bugs:

1. **The hints are backwards (and inconsistent).** I expected that after guessing too high the game would tell me to go *lower*. Instead, when my guess was too high it said "📈 Go HIGHER!", and when too low it said "📉 Go LOWER!" — the direction text is reversed (`app.py` lines 37–40). On top of that, every *even-numbered* attempt compares the secret as **text** instead of a number (`app.py` lines 158–161), so the hint flips around even more (e.g. guessing `9` against a secret of `42` reports "Too High"). The hints show up, but they're useless/misleading.

2. **You can never win the game.** Because the hints point the wrong way, following them walks you away from the answer until you run out of attempts. Two smaller issues make it worse: the on-screen range always says "between 1 and 100" even in Easy (1–20) or Hard (1–50) mode (`app.py` line 110), and the attempt counter starts at 1 instead of 0 (`app.py` line 96), so you effectively get one fewer real guess than the limit shown.

3. **"New Game" freezes after a win or loss.** I expected the New Game button to reset everything and let me play again. Instead it only resets `attempts` and `secret`, but **not** `status`, `score`, or `history` (`app.py` lines 134–138). After a win or loss the leftover `status` triggers the guard at lines 140–145, which calls `st.stop()` — so the app locks on the "You already won / Game over" screen and won't restart. (No Python traceback appears; it's a logic freeze, not a crash.)

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 1st guess of 60, secret is 42 | "Too High" → "📉 Go LOWER!" | "Too High" but shows "📈 Go HIGHER!" (direction reversed) | none |
| 2nd guess (even attempt) of 9, secret is 42 | "Too Low" → "Go HIGHER" | Reports "Too High" because secret is compared as the text "42" | none |
| Play in Easy mode (range is 1–20) | Banner reads "between 1 and 20" | Banner always reads "between 1 and 100" | none |
| Win or run out of attempts, then click "New Game 🔁" | Fresh game: counters reset, can guess again | Stuck on "You already won / Game over" screen; `st.stop()` halts the app and it won't restart | none (logic freeze, no traceback) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
 I used Claude AI tool
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Initially i ran the base application and identified the bugs and asked AI for cross checking and point the code logic of those bugs i reviewed comfirmed the code fixes given by AI
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
None of the bugs were'nt misleading i asked for extra test case where all the bug fixed code testcases were not give by AI for example : update_score() and input parsing AI only gave check_guess().


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I reran the application and tested for each bug fixed that AI gave.
- Describe at least one test you ran (manual or using pytest) 
I ran check_guess(),  update_score() and verified whether the final score is updating properly or not in the fixed bug.
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
yes I wanted to know how the score was updated it help me to analyse and verify the final score ,logic.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns are very quick and adapatble and loads the pages quickly after updating or fixed any bug
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
The testing startegy using pytest and also the analyzing the bug and fixing approach.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
I would try to use the opimtized prompt approach
- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI is very efficient in generating the code and refactoring the code files given the bug identified and logic is not proper.
