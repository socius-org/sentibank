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
        if idx == "MASTER_v2022":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "MASTER", "MASTER_v2022.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)

        elif idx == "VADER_v2014":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "VADER", "VADER_v2014.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "AFINN_v2009":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "AFINN", "AFINN_v2009.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
                
        elif idx == "AFINN_v2011":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "AFINN", "AFINN_v2011.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "AFINN_v2015":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "AFINN", "AFINN_v2015.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)

        elif idx == "Aigents+_v2022":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "Aigents", "Aigents+_v2022.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "HarvardGI_v2000":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "Harvard_GI", "HarvardGI_v2000.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "WordNet-Affect_v2006": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "WordNet_Affect", "WordNet_Affect_v2006.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "SentiWordNet_v2010_simple": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "SentiWordNet", "SentiWordNet_v2010_simple.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "SentiWordNet_v2010_nuanced": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "SentiWordNet", "SentiWordNet_v2010_nuanced.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
                
        elif idx == "Henry_v2006": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "Henry", "Henry_v2006.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "OpinionLexicon_v2004": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "OpinionLexicon", "OpinionLexicon_v2004.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "ANEW_v1999_simple": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "ANEW", "ANEW_v1999_simple.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "ANEW_v1999_weighted": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "ANEW", "ANEW_v1999_weighted.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "DED_v2022": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "DED", "DED_v2022.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "DAL_v2009_norm": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "DAL", "DAL_v2009_norm.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        elif idx == "DAL_v2009_boosted": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "DAL", "DAL_v2009_boosted.pickle"
            )
            with open(file_path, "rb") as handle:
                self.lex_dict = pickle.load(handle)
        
        else: 
            raise ValueError
        
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

        if idx == "MASTER_v2022":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "MASTER", "MASTER_v2022.csv"
            )
            self.origin_df = pd.read_csv(file_path)

        elif idx == "VADER_v2014":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "VADER", "VADER_v2014.csv"
            )
            self.origin_df = pd.read_csv(file_path)

        elif idx == "AFINN_v2009":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "AFINN", "AFINN_v2009.csv"
            )
            self.origin_df = pd.read_csv(file_path)
        
        elif idx == "AFINN_v2011":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "AFINN", "AFINN_v2011.csv"
            )
            self.origin_df = pd.read_csv(file_path) 
            
        elif idx == "AFINN_v2015":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "AFINN", "AFINN_v2015.csv"
            )
            self.origin_df = pd.read_csv(file_path)

        elif idx == "Aigents+_v2022":
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "Aigents", "Aigents+_v2022.csv"
            )
            self.origin_df = pd.read_csv(file_path)
            
        elif idx == "HarvardGI_v2000": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "Harvard_GI", "HarvardGI_v2000.csv"
            )
            self.origin_df = pd.read_csv(file_path)
            
        elif idx == "WordNet-Affect_v2006": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "WordNet_Affect", "WordNet_Affect_v2006.csv"
            )
            self.origin_df = pd.read_csv(file_path)
        
        elif idx == "SentiWordNet_v2010": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "SentiWordNet", "SentiWordNet_v2010.csv"
            )
            self.origin_df = pd.read_csv(file_path)
        
        elif idx == "Henry_v2006": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "Henry", "Henry_v2006.csv"
            )
            self.origin_df = pd.read_csv(file_path)
        
        elif idx == "OpinionLexicon_v2004": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "OpinionLexicon", "OpinionLexicon_v2004.csv"
            )
            self.origin_df = pd.read_csv(file_path)
        
        elif idx == "ANEW_v1999": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "ANEW", "ANEW_v1999.csv"
            )
            self.origin_df = pd.read_csv(file_path, index_col=['Word', 'Gender'])
        
        elif idx == "DED_v2022": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "DED", "DED_v2022.csv"
            )
            self.origin_df = pd.read_csv(file_path)
        
        elif idx == "DAL_v2009": 
            file_path = os.path.join(
                self.script_dir, "dict_arXiv", "DAL", "DAL_v2009.csv"
            )
            self.origin_df = pd.read_csv(file_path)
            
        else:
            raise ValueError

        return self.origin_df
