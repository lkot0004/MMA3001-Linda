
"""
Temperature reconstruction and evaluation utilities.
uses forward fill, linear interpolation and
PCHIP.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator


def calculate_errors(actual, predicted):
    """
    Calculate mean absolute error and root mean squared error.

    Parameters:
    1.actual : array-like
        Observed temperature values.
    2.predicted : array-like
        Reconstructed temperature values.

    Returns:
    1.(MAE, RMSE), in the same units as the input data.

    Raises:
    1.ValueError
        If arrays have different shapes, are empty,
        or contain non-finite values.
    """
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    if actual.shape != predicted.shape:
        raise ValueError("Prediction shape mismatch")

    if actual.size == 0:
        raise ValueError("Input arrays cannot be empty")

    if not np.isfinite(actual).all() or not np.isfinite(predicted).all():
        raise ValueError("Non-finite temperature values")

    errors = actual - predicted

    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors ** 2))

    return float(mae), float(rmse)


def reconstruct_gap(series, gap_start, gap_length):
    """
    Evaluating the reconstruction of an artificial missing-data block.

    The specified observations are hidden, reconstructed using
    three methods, and compared against their original values.

    Parameters:
    1.series : pandas.Series
        Complete temperature measurements with a DatetimeIndex.
    2.gap_start : int
        Position of the first hidden observation.
    3.gap_length : int
        Number of consecutive observations to hide.

    Returns:
    1.pandas.DataFrame
        Error metrics for forward fill, linear and PCHIP
        reconstruction, including method and gap information.

    Notes*
    Gaps must be strictly inside the observed series.
    No extrapolation is performed.
    """

    if not isinstance(series, pd.Series):
        raise TypeError("series must be a pandas Series")

    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("series must use a DatetimeIndex")

    if not series.index.is_monotonic_increasing:
        raise ValueError("Timestamps must be increasing")

    if not series.index.is_unique:
        raise ValueError("Timestamps must be unique")

    if series.isna().any():
        raise ValueError("Input series must not contain missing values")

    if not np.isfinite(series.to_numpy(dtype=float)).all():
        raise ValueError("Input temperatures must be finite")

    if not isinstance(gap_start, (int, np.integer)):
        raise TypeError("gap_start must be an integer")

    if not isinstance(gap_length, (int, np.integer)):
        raise TypeError("gap_length must be an integer")

    if gap_length < 1:
        raise ValueError("gap_length must be positive")

    if gap_start < 1 or gap_start + gap_length >= len(series):
        raise ValueError("Gap must have observations on both sides")

    #preserving the original measurements
    original = series.copy()
    incomplete = original.copy()

    #identifying the observations to hide
    positions = np.arange(gap_start, gap_start + gap_length)
    actual = original.iloc[positions].to_numpy(dtype=float)

    #simulating a missing block
    incomplete.iloc[positions] = np.nan

    #converting timestamps to minutes
    t = (
        original.index - original.index[0]
    ).total_seconds().to_numpy() / 60

    #separating known and hidden measurements
    known = incomplete.notna().to_numpy()
    hidden = ~known

    x_known = t[known]
    y_known = incomplete.to_numpy(dtype=float)[known]
    x_hidden = t[hidden]

    #reconstructing missing temperatures
    forward = incomplete.ffill().iloc[positions].to_numpy()

    linear = np.interp(
        x_hidden,
        x_known,
        y_known
    )

    pchip = PchipInterpolator(
        x_known,
        y_known,
        extrapolate=False
    )(x_hidden)

    #calculating the errors for each method
    results = []

    for method, predicted in {
        "Forward fill": forward,
        "Linear": linear,
        "PCHIP": pchip
    }.items():

        mae, rmse = calculate_errors(actual, predicted)

        results.append({
            "method": method,
            "gap_start": gap_start,
            "gap_length": gap_length,
            "mae": mae,
            "rmse": rmse
        })

    return pd.DataFrame(results)
