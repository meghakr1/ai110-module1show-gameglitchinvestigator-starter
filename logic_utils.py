def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIX (Bug 1 - backwards/inconsistent hints): The original compared the
    # secret as a STRING on some turns (e.g. "9" > "42"), and hid the
    # resulting TypeError in a try/except. Pairing with the AI, we refactored
    # this into logic_utils and made it a plain numeric comparison.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX (scoring bug behind Bug 2): The original gave +5 on a "Too High"
    # guess when the attempt number was even, so a wrong guess could RAISE
    # the score. The AI flagged this while reviewing update_score; we made
    # every wrong guess cost a flat -5 regardless of direction or attempt.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
