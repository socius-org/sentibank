import os
import pickle
import pandas as pd 
import json
import logging
from typing import Dict, Optional, Any, Union
from functools import lru_cache
from pathlib import Path 

# Single source of truth for lexicon mappings
LEXICON_PATHS = {
    "MASTER_v2022": "MASTER",
    "VADER_v2014": "VADER",
    "AFINN_v2009": "AFINN",
    "AFINN_v2011": "AFINN",
    "AFINN_v2015": "AFINN",
    "Aigents+_v2022": "Aigents",
    "GeneralInquirer_v2000": "GeneralInquirer",
    "WordNet-Affect_v2006": "WordNet_Affect",
    "SentiWordNet_v2010_simple": "SentiWordNet",
    "SentiWordNet_v2010_logtransform": "SentiWordNet",
    "Henry_v2006": "Henry",
    "OpinionLexicon_v2004": "OpinionLexicon",
    "ANEW_v1999_simple": "ANEW",
    "ANEW_v1999_weighted": "ANEW",
    "DED_v2022": "DED",
    "DAL_v2009_norm": "DAL",
    "DAL_v2009_boosted": "DAL",
    "NoVAD_v2013_norm": "NoVAD",
    "NoVAD_v2013_boosted": "NoVAD",
    "NoVAD_v2013_bidimensional": "NoVAD",
    "SenticNet_v2010": "SenticNet",
    "SenticNet_v2012": "SenticNet",
    "SenticNet_v2012_attributes": "SenticNet",
    "SenticNet_v2012_semantics": "SenticNet",
    "SenticNet_v2014": "SenticNet",
    "SenticNet_v2014_attributes": "SenticNet",
    "SenticNet_v2014_semantics": "SenticNet",
    "SenticNet_v2016": "SenticNet",
    "SenticNet_v2016_attributes": "SenticNet",
    "SenticNet_v2016_mood": "SenticNet",
    "SenticNet_v2016_semantics": "SenticNet",
    "SenticNet_v2018": "SenticNet",
    "SenticNet_v2018_attributes": "SenticNet",
    "SenticNet_v2018_mood": "SenticNet",
    "SenticNet_v2018_semantics": "SenticNet",
    "SenticNet_v2020": "SenticNet",
    "SenticNet_v2020_attributes": "SenticNet",
    "SenticNet_v2020_mood": "SenticNet",
    "SenticNet_v2020_semantics": "SenticNet",
    "SenticNet_v2022": "SenticNet",
    "SenticNet_v2022_attributes": "SenticNet",
    "SenticNet_v2022_mood": "SenticNet",
    "SenticNet_v2022_semantics": "SenticNet",
    "SO-CAL_v2011": "SO_CAL"
}

# Mappings for origin CSV files (subset of LEXICON_PATHS)
ORIGIN_CSV_PATHS = {
    "MASTER_v2022": "MASTER",
    "VADER_v2014": "VADER",
    "AFINN_v2009": "AFINN",
    "AFINN_v2011": "AFINN",
    "AFINN_v2015": "AFINN",
    "Aigents+_v2022": "Aigents",
    "GeneralInquirer_v2000": "GeneralInquirer",
    "WordNet-Affect_v2006": "WordNet_Affect",
    "SentiWordNet_v2010": "SentiWordNet",
    "Henry_v2006": "Henry",
    "OpinionLexicon_v2004": "OpinionLexicon",
    "ANEW_v1999": "ANEW",
    "DED_v2022": "DED",
    "DAL_v2009": "DAL",
    "NoVAD_v2013": "NoVAD",
    "SenticNet_v2022": "SenticNet",
    "SO-CAL_v2011": "SO_CAL"
}

# Set up logging
logger = logging.getLogger(__name__)


class load:
    """
    Class for loading sentiment lexicon dictionaries and their origin datasets.

    Attributes:
        script_dir (Path): Directory of the script.
        lex_dict (Optional[Dict]): Loaded sentiment lexicon dictionary.
        origin_df (Optional[pd.DataFrame]): Loaded origin dataset.
        _cache (Dict): Cache for loaded dictionaries.

    Methods:
        load.dict(idx: str) -> Dict:
            Load sentiment lexicon dictionary based on the provided index.

        load.origin(idx: str) -> pd.DataFrame:
            Load the origin dataset based on the provided index.
    """
    def __init__(self) -> None:
        """
        Initializes the load class.
        """
        self.script_dir: Path = Path(__file__).parent
        self.lex_dict: Optional[Dict[str, Any]] = None
        self.lex_json: Optional[Dict[str, Any]] = None 
        self.origin_df: Optional[pd.DataFrame] = None
        self._cache: Dict[str, Any] = {} 

    def dict(self, idx: str) -> Dict[str, Any]:
        """
        Load sentiment lexicon dictionary based on the provided index.

        Args:
            idx: Index identifying the sentiment lexicon dictionary.

        Returns:
            Loaded sentiment lexicon dictionary.
        
        Raises:
            ValueError: Raised for an unknown index.
            FileNotFoundError: If the dictionary file doesn't exist.
            IOError: If there's an error reading the file.
        """
        # Check cache first
        cache_key = f"dict_{idx}"
        if cache_key in self._cache:
            logger.debug(f"Loading {idx} from cache")
            self.lex_dict = self._cache[cache_key]
            return self.lex_dict
        
        if idx not in LEXICON_PATHS:
            raise ValueError(f"Unknown index: {idx}")
        
        file_path = self.script_dir / "dict_arXiv" / LEXICON_PATHS[idx] / f"{idx}.pickle"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Dictionary file not found: {file_path}")
        
        try:
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
                # Cache the loaded dictionary
                self._cache[cache_key] = self.lex_dict
                logger.info(f"Successfully loaded dictionary: {idx}")
        except (IOError, pickle.PickleError) as e:
            logger.error(f"Error loading dictionary {idx}: {e}")
            raise IOError(f"Failed to load dictionary {idx}: {e}") from e
        
        return self.lex_dict
    
    def json(self, idx: str) -> Dict[str, Any]:
        """
        Load sentiment lexicon from JSON file based on the provided index.

        Args:
            idx: Index identifying the sentiment lexicon dictionary.

        Returns:
            Loaded sentiment lexicon in JSON format.
        
        Raises:
            ValueError: Raised for an unknown index.
            FileNotFoundError: If the JSON file doesn't exist.
            JSONDecodeError: If the JSON file is invalid.
        """
        # Check cache first
        cache_key = f"json_{idx}"
        if cache_key in self._cache:
            logger.debug(f"Loading JSON {idx} from cache")
            self.lex_json = self._cache[cache_key]
            return self.lex_json
        
        if idx not in LEXICON_PATHS:
            raise ValueError(f"Unknown index: {idx}")
        
        file_path = self.script_dir / "dict_arXiv" / LEXICON_PATHS[idx] / f"{idx}.json"
        
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.lex_json = json.load(handle)
                # Cache the loaded JSON
                self._cache[cache_key] = self.lex_json
                logger.info(f"Successfully loaded JSON: {idx}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {idx}: {e}")
            raise
        except IOError as e:
            logger.error(f"Error loading JSON {idx}: {e}")
            raise IOError(f"Failed to load JSON {idx}: {e}") from e
        
        return self.lex_json

    def origin(self, idx: str) -> pd.DataFrame:
        """
        Load the original dataset based on the provided index.

        Args:
            idx: Index identifying the origin dataset.

        Returns:
            Loaded origin dataset.
        
        Raises:
            ValueError: Raised for an unknown index.
            FileNotFoundError: If the CSV file doesn't exist.
            pd.errors.ParserError: If the CSV file is malformed.
        """
        # Check cache first
        cache_key = f"origin_{idx}"
        if cache_key in self._cache:
            logger.debug(f"Loading origin {idx} from cache")
            self.origin_df = self._cache[cache_key]
            return self.origin_df
        
        if idx not in ORIGIN_CSV_PATHS:
            raise ValueError(f"Unknown index: {idx}")
        
        file_path = self.script_dir / "dict_arXiv" / ORIGIN_CSV_PATHS[idx] / f"{idx}.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Origin CSV file not found: {file_path}")
        
        try:
            if idx == "ANEW_v1999":
                self.origin_df = pd.read_csv(file_path, index_col=['Word', 'Gender'])
            elif idx == "SO-CAL_v2011": 
                self.origin_df = pd.read_csv(file_path, index_col=['word', 'pos'])
            else:
                self.origin_df = pd.read_csv(file_path)
            
            # Cache the loaded dataframe
            self._cache[cache_key] = self.origin_df
            logger.info(f"Successfully loaded origin dataset: {idx}")
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing CSV {idx}: {e}")
            raise
        except IOError as e:
            logger.error(f"Error loading origin {idx}: {e}")
            raise IOError(f"Failed to load origin {idx}: {e}") from e
        
        return self.origin_df
    
    def benchmark(self) -> Dict[str, pd.DataFrame]: 
        """Load benchmark datasets for sentiment analysis evaluation.
        
        Returns:
            Dictionary of benchmark datasets.
        
        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError(
            "Benchmark loading is not yet implemented. "
            "This will be added in a future version."
        )
    
    def clear_cache(self) -> None:
        """Clear the internal cache of loaded dictionaries."""
        self._cache.clear()
        logger.info("Cache cleared")
    
    def list_available(self) -> Dict[str, list]:
        """List all available dictionaries and origins.
        
        Returns:
            Dictionary with 'dictionaries' and 'origins' keys.
        """
        return {
            'dictionaries': sorted(list(LEXICON_PATHS.keys())),
            'origins': sorted(list(ORIGIN_CSV_PATHS.keys()))
        } 
