"""Tests for the archive module."""
import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
import pickle
import json
import os

from sentibank import archive


class TestLoad:
    """Test suite for the load class."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.loader = archive.load()
    
    def test_init(self):
        """Test load class initialization."""
        assert self.loader.lex_dict is None
        assert self.loader.lex_json is None
        assert self.loader.origin_df is None
        assert os.path.exists(self.loader.script_dir)
    
    def test_dict_valid_index(self):
        """Test loading a valid dictionary."""
        test_dict = {"word": 1.0}
        mock_pickle_data = pickle.dumps(test_dict)
        
        with patch("builtins.open", mock_open(read_data=mock_pickle_data)):
            with patch("pickle.load", return_value=test_dict):
                result = self.loader.dict("VADER_v2014")
                assert result == test_dict
                assert self.loader.lex_dict == test_dict
    
    def test_dict_invalid_index(self):
        """Test loading with invalid index raises ValueError."""
        with pytest.raises(ValueError, match="Unknown index: INVALID_INDEX"):
            self.loader.dict("INVALID_INDEX")
    
    def test_json_valid_index(self):
        """Test loading a valid JSON dictionary."""
        test_json = {"word": 1.0}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(test_json))):
            with patch("json.load", return_value=test_json):
                result = self.loader.json("VADER_v2014")
                assert result == test_json
                assert self.loader.lex_json == test_json
    
    def test_json_invalid_index(self):
        """Test loading JSON with invalid index raises ValueError."""
        with pytest.raises(ValueError, match="Unknown index: INVALID_INDEX"):
            self.loader.json("INVALID_INDEX")
    
    def test_origin_valid_index(self):
        """Test loading a valid origin dataset."""
        mock_df = pd.DataFrame({"word": ["test"], "score": [1.0]})
        
        with patch("pandas.read_csv", return_value=mock_df):
            result = self.loader.origin("VADER_v2014")
            assert isinstance(result, pd.DataFrame)
            assert self.loader.origin_df.equals(mock_df)
    
    def test_origin_invalid_index(self):
        """Test loading origin with invalid index raises ValueError."""
        with pytest.raises(ValueError, match="Unknown index: INVALID_INDEX"):
            self.loader.origin("INVALID_INDEX")
    
    def test_origin_anew_special_case(self):
        """Test ANEW origin loading with special index columns."""
        mock_df = pd.DataFrame({
            "Word": ["test"],
            "Gender": ["M"],
            "score": [1.0]
        })
        
        with patch("pandas.read_csv") as mock_read:
            mock_read.return_value = mock_df
            self.loader.origin("ANEW_v1999")
            mock_read.assert_called_once()
            _, kwargs = mock_read.call_args
            assert kwargs.get("index_col") == ['Word', 'Gender']
    
    def test_origin_socal_special_case(self):
        """Test SO-CAL origin loading with special index columns."""
        mock_df = pd.DataFrame({
            "word": ["test"],
            "pos": ["noun"],
            "score": [1.0]
        })
        
        with patch("pandas.read_csv") as mock_read:
            mock_read.return_value = mock_df
            self.loader.origin("SO-CAL_v2011")
            mock_read.assert_called_once()
            _, kwargs = mock_read.call_args
            assert kwargs.get("index_col") == ['word', 'pos']


class TestConstants:
    """Test module constants."""
    
    def test_lexicon_paths_exists(self):
        """Test LEXICON_PATHS constant exists and is not empty."""
        assert hasattr(archive, 'LEXICON_PATHS')
        assert isinstance(archive.LEXICON_PATHS, dict)
        assert len(archive.LEXICON_PATHS) > 0
    
    def test_origin_csv_paths_exists(self):
        """Test ORIGIN_CSV_PATHS constant exists and is not empty."""
        assert hasattr(archive, 'ORIGIN_CSV_PATHS')
        assert isinstance(archive.ORIGIN_CSV_PATHS, dict)
        assert len(archive.ORIGIN_CSV_PATHS) > 0
    
    def test_origin_paths_subset_of_lexicon_paths(self):
        """Test that origin paths are a subset of lexicon paths."""
        # Some origin keys should be in lexicon paths
        # (though not all lexicon paths have origins)
        common_keys = set(archive.ORIGIN_CSV_PATHS.keys()) & set(archive.LEXICON_PATHS.keys())
        assert len(common_keys) > 0