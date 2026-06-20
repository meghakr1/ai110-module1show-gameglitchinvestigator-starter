from logic_utils import (
    check_guess,
    update_score,
    get_range_for_difficulty,
    parse_guess,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Regression tests for the fixed bug ---
# The original code sometimes compared the secret as a STRING, so it used
# alphabetical order instead of numeric order. These two cases are picked
# so that string comparison gives the WRONG answer, locking in the fix.

def test_single_digit_guess_compared_numerically():
    # Numerically 9 < 42, so the outcome must be "Too Low".
    # The old string bug compared "9" > "42" (because '9' > '4') and
    # wrongly returned "Too High".
    result = check_guess(9, 42)
    assert result == "Too Low"

def test_three_digit_guess_compared_numerically():
    # Numerically 100 > 42, so the outcome must be "Too High".
    # The old string bug compared "100" < "42" (because '1' < '4') and
    # wrongly returned "Too Low".
    result = check_guess(100, 42)
    assert result == "Too High"


# --- Regression tests for the scoring bug ---
# The original update_score gave +5 on a "Too High" guess when the attempt
# number was even, so a wrong guess could gain points. A wrong guess must
# ALWAYS lose points, no matter the attempt number.

def test_wrong_high_guess_loses_points_on_even_attempt():
    # Old bug: even attempt + "Too High" returned current_score + 5.
    assert update_score(100, "Too High", 2) == 95

def test_wrong_high_guess_loses_points_on_odd_attempt():
    assert update_score(100, "Too High", 3) == 95

def test_wrong_low_guess_loses_points():
    assert update_score(100, "Too Low", 4) == 95

def test_winning_guess_adds_points():
    # Winning should increase the score.
    assert update_score(0, "Win", 1) > 0


# --- Regression tests for the difficulty range bug ---
# The in-game banner ignored difficulty and always said "1 to 100". The
# range itself comes from this function, so we lock in the correct ranges.

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 50)


# --- Tests for input parsing ---

def test_parse_valid_number():
    assert parse_guess("42") == (True, 42, None)

def test_parse_empty_input_is_rejected():
    ok, value, _ = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_non_number_is_rejected():
    ok, value, _ = parse_guess("abc")
    assert ok is False
    assert value is None
