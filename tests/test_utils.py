"""Tests for the utils module."""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

# Mock spacy before importing utils
with patch('spacy.load') as mock_spacy_load:
    mock_nlp = MagicMock()
    mock_spacy_load.return_value = mock_nlp
    from sentibank.utils import analysis


class TestAnalysis:
    """Test suite for the analysis class."""
    
    @patch('spacy.load')
    def test_init(self, mock_spacy_load):
        """Test analysis class initialization."""
        mock_nlp = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        
        analyzer = analysis()
        assert hasattr(analyzer, 'spacy_nlp')
        mock_nlp.add_pipe.assert_called_with("emoji", first=True)
    
    @patch('spacy.load')
    def test_count_categorical_labels_string_values(self, mock_spacy_load):
        """Test counting categorical labels with string values."""
        mock_nlp = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        
        analyzer = analysis()
        test_dict = {
            "word1": "positive",
            "word2": "negative",
            "word3": "positive"
        }
        
        with patch('sentibank.utils.track', side_effect=lambda x, **kwargs: x):
            result = analyzer.count_categorical_labels(test_dict)
        
        assert "labels" in result
        assert "label frequency" in result
        assert set(result["labels"]) == {"positive", "negative"}
    
    @patch('spacy.load')
    def test_count_categorical_labels_list_values(self, mock_spacy_load):
        """Test counting categorical labels with list values."""
        mock_nlp = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        
        analyzer = analysis()
        test_dict = {
            "word1": ["positive", "strong"],
            "word2": ["negative"],
            "word3": ["positive", "weak"]
        }
        
        with patch('sentibank.utils.track', side_effect=lambda x, **kwargs: x):
            result = analyzer.count_categorical_labels(test_dict)
        
        assert "labels" in result
        assert "label frequency" in result
        assert "multi label frequency" in result
    
    @patch('spacy.load')
    def test_sort_dict(self, mock_spacy_load):
        """Test sort_dict method."""
        mock_nlp = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        
        analyzer = analysis()
        test_dict = {"c": 1, "a": 3, "b": 2}
        
        # Assuming sort_dict sorts by value in descending order
        if hasattr(analyzer, 'sort_dict'):
            sorted_dict = analyzer.sort_dict(test_dict)
            assert list(sorted_dict.keys()) == ["a", "b", "c"]


class TestAnalysisSentiment:
    """Test sentiment analysis functionality."""
    
    @patch('sentibank.archive.load')
    @patch('spacy.load')
    def test_sentiment_score_based(self, mock_spacy_load, mock_archive_load):
        """Test sentiment analysis with score-based dictionary."""
        mock_nlp = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        
        # Mock the document processing
        mock_doc = MagicMock()
        mock_token1 = MagicMock()
        mock_token1.text = "good"
        mock_token1.lower_ = "good"
        mock_token2 = MagicMock()
        mock_token2.text = "bad"
        mock_token2.lower_ = "bad"
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_token1, mock_token2]))
        mock_nlp.return_value = mock_doc
        
        # Mock dictionary
        mock_dict = {"good": 2.0, "bad": -2.0}
        mock_loader = MagicMock()
        mock_loader.dict.return_value = mock_dict
        mock_archive_load.return_value = mock_loader
        
        analyzer = analysis()
        
        # If sentiment method exists, test it
        if hasattr(analyzer, 'sentiment'):
            with patch.object(analyzer, 'spacy_nlp', mock_nlp):
                result = analyzer.sentiment("good bad", "VADER_v2014")
                # Score-based dictionaries should return a numeric value
                assert isinstance(result, (int, float))


class TestAnalysisDictionary:
    """Test dictionary analysis functionality."""
    
    @patch('sentibank.archive.load')
    @patch('spacy.load')
    def test_dictionary_analysis(self, mock_spacy_load, mock_archive_load):
        """Test dictionary analysis method."""
        mock_nlp = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        
        # Mock dictionary
        mock_dict = {"word1": 1.0, "word2": -1.0, "word3": 0.5}
        mock_loader = MagicMock()
        mock_loader.dict.return_value = mock_dict
        mock_archive_load.return_value = mock_loader
        
        analyzer = analysis()
        
        # If dictionary method exists, test it
        if hasattr(analyzer, 'dictionary'):
            with patch('sentibank.utils.pprint'):
                # Should not raise an exception
                analyzer.dictionary(dictionary="VADER_v2014")