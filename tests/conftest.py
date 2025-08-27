"""Pytest configuration and fixtures."""
import pytest
import sys
import os

# Add the parent directory to the path so we can import sentibank
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_dictionary():
    """Provide a sample sentiment dictionary for testing."""
    return {
        "good": 2.0,
        "bad": -2.0,
        "excellent": 3.0,
        "terrible": -3.0,
        "okay": 0.5
    }


@pytest.fixture
def sample_categorical_dictionary():
    """Provide a sample categorical sentiment dictionary for testing."""
    return {
        "happy": ["positive", "joy"],
        "sad": ["negative", "sorrow"],
        "angry": ["negative", "anger"],
        "excited": ["positive", "arousal"]
    }


@pytest.fixture
def sample_dataframe():
    """Provide a sample pandas DataFrame for testing."""
    import pandas as pd
    return pd.DataFrame({
        "word": ["test", "sample", "example"],
        "score": [1.0, 2.0, -1.0],
        "category": ["neutral", "positive", "negative"]
    })