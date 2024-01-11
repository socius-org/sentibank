import os
import pickle
import pandas as pd 

class load:
    """
    Class for loading sentiment lexicon dictionaries and their origin datasets.

    Attributes:
        script_dir (str): Directory of the script.
        lex_dict (dict): Loaded sentiment lexicon dictionary.
        origin_df (pd.DataFrame): Loaded origin dataset.

    Methods:
        load_dict(idx: str) -> dict:
            Load sentiment lexicon dictionary based on the provided index.

        load_origin(idx: str) -> pd.DataFrame:
            Load the origin dataset based on the provided index.
    """
    def __init__(self):
        """
        Initializes the load class.
        """
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.lex_dict = None
        self.origin_df = None 

    def dict(self, idx: str):
        """
        Load sentiment lexicon dictionary based on the provided index.

        Args:
            idx (str): Index identifying the sentiment lexicon dictionary.

        Returns:
            dict: Loaded sentiment lexicon dictionary.
        
        Raises:
            ValueError: Raised for an unknown index.
        """
        
        lexicon_paths = {
            "MASTER_v2022": "MASTER",
            "VADER_v2014": "VADER",
            "AFINN_v2009": "AFINN",
            "AFINN_v2011": "AFINN",
            "AFINN_v2015": "AFINN",
            "Aigents+_v2022": "Aigents",
            "HarvardGI_v2000": "Harvard_GI",
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
            "NoVAD_v2013_bidimensional": "NoVAD",
            "NoVAD_v2013_adjusted": "NoVAD",
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
        }
        
        if idx in lexicon_paths:
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", lexicon_paths[idx], f"{idx}.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        else: 
            raise ValueError(f"Unknown index: {idx}")
        
        return self.lex_dict

    def origin(self, idx: str):
        """
        Load the original dataset based on the provided index.

        Args:
            idx (str): Index identifying the origin dataset.

        Returns:
            pd.DataFrame: Loaded origin dataset.
        
        Raises:
            ValueError: Raised for an unknown index.
        """
        import pandas as pd

        csv_paths = {
            "MASTER_v2022": "MASTER",
            "VADER_v2014": "VADER",
            "AFINN_v2009": "AFINN",
            "AFINN_v2011": "AFINN",
            "AFINN_v2015": "AFINN",
            "Aigents+_v2022": "Aigents",
            "HarvardGI_v2000": "Harvard_GI",
            "WordNet-Affect_v2006": "WordNet_Affect",
            "SentiWordNet_v2010": "SentiWordNet",
            "Henry_v2006": "Henry",
            "OpinionLexicon_v2004": "OpinionLexicon",
            "ANEW_v1999": "ANEW",
            "DED_v2022": "DED",
            "DAL_v2009": "DAL",
            "NoVAD_v2013": "NoVAD",
            "SenticNet_v2022": "SenticNet"
        }

        if idx in csv_paths:
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", csv_paths[idx], f"{idx}.csv"
            )
            if idx == "ANEW_v1999":
                self.origin_df = pd.read_csv(file_path, index_col=['Word', 'Gender'])
            else:
                self.origin_df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unknown index: {idx}")

        return self.origin_df
