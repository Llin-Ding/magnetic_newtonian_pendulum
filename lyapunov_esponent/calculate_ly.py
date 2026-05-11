"""
Compute the largest Lyapunov exponent for each ball in the magnetic
Newtonian pendulum simulations using Rosenstein's algorithm (nolds.lyap_r).

Files
-----
simulation_results_3(1).csv  – 3 balls (M0, M1, M2)
simulation_results_5(1).csv  – 5 balls (M0 … M4)

Each ball's x-position time series is used as the 1-D input signal.
"""

import os
import numpy as np
import pandas as pd
import nolds

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {
    "3-body": os.path.join(BASE_DIR, "三个摆.csv"),
    "5-body": os.path.join(BASE_DIR, "三个摆新.csv"),
}


def ball_names(df: pd.DataFrame) -> list[str]:
    """Return unique ball prefixes (M0, M1, …) present in the DataFrame."""
    prefixes = sorted(
        {col.rsplit("_", 1)[0] for col in df.columns if col.startswith("M")},
        key=lambda s: int(s[1:]),
    )
    return prefixes


def compute_lyapunov(series: np.ndarray, fs: float) -> float:
    """
    Estimate the largest Lyapunov exponent via Rosenstein's method.

    Parameters
    ----------
    series : 1-D array of position values
    fs     : sampling frequency (Hz)

    Returns
    -------
    Largest Lyapunov exponent in units of 1/s
    """
    # nolds.lyap_r returns the exponent per sample; multiply by fs for 1/s
    le = nolds.lyap_r(series, emb_dim=6, lag=1, min_tsep=10, trajectory_len=20)
    return le * fs


def main() -> None:
    for label, path in FILES.items():
        print(f"\n{'=' * 60}")
        print(f"  {label}  →  {os.path.basename(path)}")
        print("=" * 60)

        df = pd.read_csv(path)

        # Sampling frequency from the time column
        dt = float(df["Time_s"].iloc[1] - df["Time_s"].iloc[0])
        fs = 1.0 / dt
        print(f"  Sampling frequency : {fs:.1f} Hz  (dt = {dt} s)")
        print(f"  Data points        : {len(df)}\n")

        balls = ball_names(df)
        results = {}

        for ball in balls:
            x_col = f"{ball}_x"
            series = df[x_col].to_numpy(dtype=float)

            le = compute_lyapunov(series, fs)
            results[ball] = le
            chaos = "chaotic" if le > 0 else "regular"
            print(f"  {ball:4s}  λ_max = {le:+.4f}  1/s   ({chaos})")

        avg = np.mean(list(results.values()))
        print(f"\n  Average λ_max = {avg:+.4f}  1/s")


if __name__ == "__main__":
    main()
