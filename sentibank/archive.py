import os
import pickle


class load:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.lex_dict = None

    def dict(self, idx: str):
        """_summary_

        Args:
            idx (str): _description_

        Returns:
            _type_: _description_
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
        
        else: 
            raise ValueError
        
        return self.lex_dict

    def origin(self, idx: str):
        """_summary_

        Args:
            idx (str): _description_

        Returns:
            _type_: _description_
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

        else:
            raise ValueError

        return self.origin_df
