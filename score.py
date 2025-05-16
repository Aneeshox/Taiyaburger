def apogee_score(apogee_actual: float, 
                 apogee_target: float) -> float:

    error = abs(apogee_target - apogee_actual)
    max_error = 0.3 * apogee_target
    if error >= max_error:
        return 0.0

    # linear penalty
    penalty_per_ft = 350.0 / max_error
    points = 350.0 - penalty_per_ft * error
    return points


# --- Examples ---
if __name__ == "__main__":
    actual = 12321
    target = 10000
    pts = apogee_score(actual, target)
    print(f"Actual={actual:6.0f} ft, Target={target:6.0f} ft → {pts:6.1f} pts")
