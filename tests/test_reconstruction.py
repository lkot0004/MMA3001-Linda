
#Automated verification tests for temperature reconstruction

import numpy as np
import pandas as pd
import pytest

from src.reconstruction import calculate_errors, reconstruct_gap


@pytest.fixture
def linear_temperature_series():
    """Create a time series with a known linear trend."""
    timestamps = pd.date_range(
        "2024-01-01",
        periods=12,
        freq="10min",
        tz="UTC"
    )
    temperatures = 20.0 + 0.2 * np.arange(12)

    return pd.Series(temperatures, index=timestamps)


def test_error_metrics_exact_answer():
    """MAE and RMSE must match manually calc values"""
    actual = [20.0, 22.0, 24.0]
    predicted = [21.0, 21.0, 22.0]

    mae, rmse = calculate_errors(actual, predicted)

    assert np.isclose(mae, 4 / 3)
    assert np.isclose(rmse, np.sqrt(2))


def test_perfect_prediction():
    """Perfect predictions have zero error"""
    actual = [20.0, 21.0, 22.0]

    mae, rmse = calculate_errors(actual, actual)

    assert mae == 0.0
    assert rmse == 0.0


def test_error_metrics_reject_mismatched_shapes():
    """Arrays of different sizes rejected"""
    with pytest.raises(ValueError, match="shape"):
        calculate_errors([20.0, 21.0], [20.0])


def test_error_metrics_reject_nan():
    """Undefined measurements rejected"""
    with pytest.raises(ValueError, match="Non-finite"):
        calculate_errors([20.0, np.nan], [20.0, 21.0])


def test_error_metrics_reject_empty_arrays():
    """MAE and RMSE cannot be calculated on empty arrays."""
    with pytest.raises(ValueError, match="empty"):
        calculate_errors([], [])


def test_reconstruction_on_linear_series(linear_temperature_series):
    """Linear interpolation and PCHIP must recover a straight line."""
    result = reconstruct_gap(
        linear_temperature_series,
        gap_start=4,
        gap_length=3
    )

    assert set(result["method"]) == {
        "Forward fill", "Linear", "PCHIP"
    }

    for method in ["Linear", "PCHIP"]:
        row = result.loc[result["method"] == method].iloc[0]

        assert np.isclose(row["mae"], 0.0, atol=1e-10)
        assert np.isclose(row["rmse"], 0.0, atol=1e-10)


def test_forward_fill_has_error_on_trend(linear_temperature_series):
    """Forward fill should not perfectly reconstruct a rising trend."""
    result = reconstruct_gap(
        linear_temperature_series,
        gap_start=4,
        gap_length=3
    )

    forward = result.loc[
        result["method"] == "Forward fill"
    ].iloc[0]

    assert forward["mae"] > 0
    assert forward["rmse"] > 0


def test_reconstruction_does_not_modify_original(linear_temperature_series):
    """Artificial masking must not overwrite the original observations."""
    original = linear_temperature_series.copy()

    reconstruct_gap(linear_temperature_series, 4, 3)

    pd.testing.assert_series_equal(
        linear_temperature_series, original
    )


def test_reject_gap_at_boundary(linear_temperature_series):
    """Gaps requiring extrapolation must be rejected."""
    with pytest.raises(ValueError, match="both sides"):
        reconstruct_gap(linear_temperature_series, 0, 3)

    with pytest.raises(ValueError, match="both sides"):
        reconstruct_gap(linear_temperature_series, 10, 2)


def test_reject_missing_input_data(linear_temperature_series):
    """Input gaps not specified for the experiment must be rejected."""
    series = linear_temperature_series.copy()
    series.iloc[2] = np.nan

    with pytest.raises(ValueError, match="missing"):
        reconstruct_gap(series, 4, 3)


def test_reject_unsorted_timestamps(linear_temperature_series):
    """Unordered timestamps must be rejected."""
    series = linear_temperature_series.iloc[::-1]

    with pytest.raises(ValueError, match="increasing"):
        reconstruct_gap(series, 4, 3)


def test_reject_zero_gap_length(linear_temperature_series):
    """A missing block must contain at least one observation."""
    with pytest.raises(ValueError, match="positive"):
        reconstruct_gap(linear_temperature_series, 4, 0)
