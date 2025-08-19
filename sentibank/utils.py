from rich.progress import track
from rich import print as pprint
import itertools
from itertools import combinations, chain
import statistics
from collections import Counter
import spacy
from spacymoji import Emoji
from sentibank.dict_arXiv import emos
import re
import enchant 
from sentibank import archive
import subprocess
import sys

load = archive.load()


class analysis:
    """
    Class for analyzing sentiment dictionaries and generating summary insights.

    Attributes:
        spacy_nlp (spacy.lang.en.English): Spacy NLP pipeline with emoji detection.
    """

    def __init__(self):
        """
        Initializes the Analysis class by loading the Spacy NLP pipeline with emoji detection.
        """
        try:
            self.spacy_nlp = spacy.load(
                "en_core_web_sm",
                exclude=["parser", "senter", "attribute_ruler", "lemmatizer", "ner"],
            )
        except OSError:
            # Model not found, attempt to download it
            import subprocess
            import sys
            
            print("SpaCy model 'en_core_web_sm' not found. Downloading...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
                    stdout=subprocess.DEVNULL,  # Suppress output for cleaner experience
                    stderr=subprocess.STDOUT
                )
                # Try loading again after download
                self.spacy_nlp = spacy.load(
                    "en_core_web_sm",
                    exclude=["parser", "senter", "attribute_ruler", "lemmatizer", "ner"],
                )
                print("Successfully downloaded and loaded en_core_web_sm")
            except subprocess.CalledProcessError:
                raise RuntimeError(
                    "Failed to download spaCy model automatically.\n"
                    "Please install it manually by running:\n"
                    "    python -m spacy download en_core_web_sm"
                )
        
        # Add emoji detection pipeline (this stays the same)
        # self.spacy_nlp.add_pipe("sentencizer")
        self.spacy_nlp.add_pipe("emoji", first=True)

    def count_categorical_labels(self, dictionary: dict):
        """
        Counts the frequency of categorical sentiment labels in a given dictionary.

        Args:
            dictionary (dict): Input dictionary with sentiment labels.

        Returns:
            dict: Summary statistics of sentiment labels.
        """
        label_counts = Counter()
        multi_label_counts = Counter()

        for value_list in track(
            dictionary.values(),
            description="Computing Summary Statistics of Sentiment Scores",
            # transient=True,
        ):
            if isinstance(value_list, str):  # Handle string values
                label = value_list
                label_counts[label] = label_counts.get(label, 0) + 1
            elif isinstance(value_list, list):
                labels = value_list
                label_counts.update(labels)

                combinations_set = set(
                    chain.from_iterable(
                        combinations(labels, r) for r in range(2, len(labels) + 1)
                    )
                )
                multi_label_counts.update(combinations_set)

        output = {
            "labels": list(label_counts.keys()),
            "label frequency": self.sort_dict(label_counts),
            "multi label frequency": self.sort_dict(multi_label_counts),
        }

        if not output["multi label frequency"]:
            del output["multi label frequency"]

        return output

    def count_discrete_labels(self, dictionary: dict):
        """
        Counts the frequency of discrete sentiment labels in a given dictionary.

        Args:
            dictionary (dict): Input dictionary with sentiment labels.

        Returns:
            dict: Summary statistics of sentiment labels.
        """
        label_counts = {}
        multi_label_counts = {}

        for value_list in track(
            dictionary.values(),
            description="Computing Summary Statistics of Sentiment Scores",
            # transient=True,
        ):
            if isinstance(value_list, int):
                label = value_list
                label_counts[label] = label_counts.get(label, 0) + 1
            elif isinstance(value_list, list):
                unique_labels = set(value_list)

                for label in unique_labels:
                    label_counts[label] = label_counts.get(label, 0) + 1

                if len(unique_labels) > 1:
                    multi_label = tuple(sorted(unique_labels))

                    multi_label_counts[multi_label] = (
                        multi_label_counts.get(multi_label, 0) + 1
                    )

        output = {
            "labels": sorted(list(label_counts.keys())),
            "label frequency": self.sort_dict(label_counts),
            "multi label frequency": self.sort_dict(multi_label_counts),
        }

        if not output["multi label frequency"]:
            del output["multi label frequency"]

        return output

    def count_cont_variables(self, dictionary: dict):
        """
        Computes summary statistics for continuous sentiment scores in a given dictionary.

        Args:
            dictionary (dict): Input dictionary with sentiment scores.

        Returns:
            dict: Summary statistics of sentiment scores.
        """
        value_range = [min(dictionary.values()), max(dictionary.values())]
        neg, pos, neu = [], [], []

        for value in track(
            dictionary.values(),
            description="Computing Summary Statistics of Sentiment Scores",
            # transient=True,
        ):
            if value < 0:
                neg.append(value)
            elif value > 0:
                pos.append(value)
            else:
                neu.append(value)

        positive = {
            "frequency": len(pos),
            "mean": round(statistics.mean(pos), 3),
            "median": statistics.median(pos),
            "mode": statistics.multimode(pos),
            "std": round(statistics.stdev(pos), 3),
        }
        if len(positive["mode"]) == 1:
            positive["mode"] = positive["mode"][0]

        negative = {
            "frequency": len(neg),
            "mean": round(statistics.mean(neg), 3),
            "median": statistics.median(neg),
            "mode": statistics.multimode(neg),
            "std": round(statistics.stdev(neg), 3),
        }
        if len(negative["mode"]) == 1:
            negative["mode"] = negative["mode"][0]

        if not neu:
            output = {"range": value_range, "positive": positive, "negative": negative}
        else:
            output = {
                "range": value_range,
                "positive": positive,
                "negative": negative,
                "neutral": {"frequency": len(neu)},
            }
        return output

    def sort_dict(self, dictionary: dict):
        """
        Sorts a dictionary by values in descending order.

        Args:
            dictionary (dict): Input dictionary to be sorted.

        Returns:
            dict: Sorted dictionary.
        """
        return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

    def summarise_lex_dict(self, lexicon_dictionary: dict):
        """
        Summarizes sentiment scores and lexicon information.

        Args:
            lexicon_dictionary (dict): Input sentiment lexicon dictionary.

        Returns:
            None: Prints a summary of sentiment scores and lexicon information.
        """
        # Sentiment Score Summary
        lex_dict_type = None

        ##Check scoring type
        for key, value in itertools.islice(lexicon_dictionary.items(), 1):
            if isinstance(value, str):
                lex_dict_type = "categorical"
            elif isinstance(value, int):
                lex_dict_type = "discrete"
            elif isinstance(value, float):
                lex_dict_type = "continuous"
            elif isinstance(value, list):
                if all(isinstance(item, str) for item in value):
                    lex_dict_type = "categorical (multi-label)"
                elif all(isinstance(item, float) for item in value) or all(
                    isinstance(item, int) for item in value
                ):
                    lex_dict_type = "vector representation"
                else:
                    lex_dict_type = "unknown"
            else:
                lex_dict_type = "unknown"

        if "categorical" in lex_dict_type:
            score_summary = self.count_categorical_labels(lexicon_dictionary)
        elif "discrete" in lex_dict_type:
            score_summary = self.count_discrete_labels(lexicon_dictionary)
        elif "continuous" in lex_dict_type:
            score_summary = self.count_cont_variables(lexicon_dictionary)

        # Sentiment Lexicon (Part-of-Speech Tag) Summary
        pos_tags = []
        general_dict = {
            "verbs": 0,
            "adjectives": 0,
            "adverbs": 0,
            "prepositions": 0,
            "conjunctions": 0,
            "determiners": 0,
            "pronouns": 0,
            "numerals": 0,
            "nouns": 0,
            "particles": 0,
            "emos": 0,
            "miscellaneous": 0,
        }
        granular_dict = {}
        misc = []

        for key in track(
            lexicon_dictionary.keys(),
            description="Extracting Summary Insights from Sentiment Lexicons",
            # transient=True,
        ):
            # check if token is emoticons
            if key in emos.emoticons:
                pos_tags.append("EMOTICON")
            else:
                doc = self.spacy_nlp(key)
                for token in doc:
                    # check if token is emoji
                    if token._.is_emoji:
                        pos_tags.append("EMOJI")
                    else:
                        pos_tags.append(token.tag_)

        for element in pos_tags:
            if element in granular_dict:
                granular_dict[element] += 1
            else:
                granular_dict[element] = 1

        for key, value in granular_dict.items():
            if key.startswith("V"):
                general_dict["verbs"] += value
            elif key.startswith("JJ"):
                general_dict["adjectives"] += value
            elif key.startswith("RB"):
                general_dict["adverbs"] += value
            elif key.startswith("IN"):
                general_dict["prepositions"] += value
            elif key.startswith("N"):
                general_dict["nouns"] += value
            elif key.startswith("PRP") or key.startswith("WP"):
                general_dict["pronouns"] += value
            elif key == "CD":
                general_dict["numerals"] += value
            elif key == "CC":
                general_dict["conjunctions"] += value
            elif key == "DT" or key == "WDT":
                general_dict["determiners"] += value
            elif key == "RP":
                general_dict["particles"] += value
            elif key == "EMOTICON":
                general_dict["emos"] += value
            elif key == "EMOJI":
                general_dict["emos"] += value
            else:
                misc.append(key)
                general_dict["miscellaneous"] += value

        granular_dict_adv = {}

        if "EMOTICON" or "EMOJI" in granular_dict.keys():
            for key, value in granular_dict.items():
                if key == "EMOTICON":
                    granular_dict_adv[
                        "EMOTICON (textual representations of emotions)"
                    ] = value
                elif key == "EMOJI":
                    granular_dict_adv[
                        "EMOJI (pictorial symbols of emotions, objects, or concepts)"
                    ] = value
                elif key == "JJ":
                    granular_dict_adv["JJ (adjective)"] = value
                else:
                    granular_dict_adv["{} ({})".format(key, spacy.explain(key))] = value
        else:
            for key, value in granular_dict.items():
                if key == "JJ":
                    granular_dict_adv["JJ (adjective)"] = value
                else:
                    granular_dict_adv = dict(
                        ("{} ({})".format(key, spacy.explain(key)), value)
                        for (key, value) in granular_dict.items()
                    )

        part_of_speech = {
            "general": self.sort_dict(general_dict),
            "granular": self.sort_dict(granular_dict_adv),
            "misc": misc,
        }

        summary = {
            "Dictionary Type": lex_dict_type,
            "Sentiment Score": score_summary,
            "Sentiment Lexicon": part_of_speech,
        }

        return pprint(summary)

class spellcheck:
    """
    A class for spell-checking sentences.

    Attributes:
        spellchecker (enchant.Dict): An enchant dictionary for English.

    Methods:
        shorten_word(self, word: str) -> str:
            Shortens words with three or more consecutive identical alphabets to two consecutive identical alphabets.

        sentence(self, sentence: str) -> str:
            Spell-checks the given sentence, correcting misspelled words. Shortens words with three or more consecutive identical alphabets before spell-checking.
            Returns the spell-checked sentence in lowercase.

    Example:
        spellchecker = spellcheck()
        corrected_sentence = spellchecker.sentence("I am sooooo happppyyyy")
        print(corrected_sentence)
    """
    def __init__(self): 
        self.spellchecker = enchant.Dict("en_US")
    
    def shorten_word(self, word:str):
        """
        Shortens words with three or more consecutive identical alphabets to two consecutive identical alphabets.

        Args:
            word (str): The word to be shortened.

        Returns:
            str: The shortened word.
        """
        # Find sections with three or more consecutive identical alphabets
        matches = re.findall(r'(\w)\1{2,}', word)
        
        # Shorten each section to two alphabets
        for match in matches:
            replacement = match[:2]
            word = re.sub(r'(\w)\1{2,}', replacement * 2, word, count=1)
        
        return word 
    
    def sentence(self, sentence:str):
        """
        Spell-checks the given sentence, correcting misspelled words. 
        Shortens words with three or more consecutive identical alphabets before spell-checking.
        Returns the spell-checked sentence in lowercase.

        Args:
            sentence (str): The sentence to be spell-checked.

        Returns:
            str: The spell-checked sentence.
        """
        words = sentence.split()
        spellchecked_words = []

        for word in words:
            # Shorten word if it has three consecutive identical alphabets
            if re.search(r'(\w)\1{2,}', word):
                word = self.shorten_word(word)
                print(word)
                if word == "soo": #Add more words that enchant wrongly spell checks 
                    suggestions = ["so"]
                else: 
                    # Spell check the word
                    suggestions = self.spellchecker.suggest(word)
                if suggestions:
                    spellchecked_words.append(suggestions[0])
                else:
                    spellchecked_words.append(word)
            else:
                spellchecked_words.append(word)

        return ' '.join(spellchecked_words).lower()
class analyze: 
    """
    A class for sentiment analysis with lexicon dictionaries.

    Methods:
        __init__(): Initializes an instance of the analyze class.

        dictionary(dictionary: Union[dict, str] = None):
            Summarises overview of the provided lexicon dictionary.
            If dictionary is a string, it loads the dictionary using the 'sentibank.archive.load().dict' method.
            Raises ValueError if 'dictionary' parameter is not provided.

        sentiment(text: str, dictionary: str = None):
            Performs sentiment analysis on the given text using the specified lexicon dictionary.
            The dictionary can be selected from a list of available options.
            Returns a summary of sentiment scores or labels depending on the dictionary used.
    """
    def __init__(self):
        self.spellcheck = spellcheck()
    
    def dictionary(self, dictionary: dict or str = None): 
        """
        Summarises sentiment information based on the provided lexicon dictionary.

        Parameters:
            dictionary (Union[dict, str]): The lexicon dictionary to be analyzed.
                If a string, it loads the dictionary using the 'sentibank.archive.load().dict' method.

        Raises:
            ValueError: If 'dictionary' parameter is not provided.

        Returns:
            None
        """
        if dictionary is None: 
             raise ValueError("The 'dictionary' parameter must be provided.")
        else: 
            if isinstance(dictionary, str): 
                loaded_dictionary = load.dict(dictionary)
                analysis().summarise_lex_dict(loaded_dictionary)
            elif isinstance(dictionary, dict): 
                analysis().summarise_lex_dict(dictionary)
    
    def sentiment(self, text: str, dictionary: str = None):
        """
        Performs bag-of-words sentiment analysis on the given text using the specified lexicon dictionary.
        It checks spelling of words if a word has three consecutive identical alphabets (e.g. "happppyyyy")

        Parameters:
            text (str): The input text for sentiment analysis.
            dictionary (str): The lexicon dictionary to be used for sentiment analysis.
                Should be selected from the list of available options.

        Returns:
            Union[float, Dict[str, int]]: 
                If the lexicon dictionary is score-based, returns the total sentiment score as a float.
                If the lexicon dictionary is label-based, returns a dictionary with sentiment class counts.
        """
        text = self.spellcheck.sentence(text)
        
        avaliable_dictionary = [
            "MASTER_v2022",
            "VADER_v2014",
            "AFINN_v2009",
            "AFINN_v2011",
            "AFINN_v2015",
            "Aigents+_v2022",
            "HarvardGI_v2000",
            "WordNet-Affect_v2006",
            "SentiWordNet_v2010_simple",
            "SentiWordNet_v2010_logtransform",
            "Henry_v2006",
            "OpinionLexicon_v2004",
            "ANEW_v1999_simple",
            "ANEW_v1999_weighted",
            "DED_v2022",
            "DAL_v2009_norm",
            "DAL_v2009_boosted",
            "NoVAD_v2013_norm",
            "NoVAD_v2013_boosted",
            "SenticNet_v2010",
            "SenticNet_v2012",
            "SenticNet_v2012_attributes",
            "SenticNet_v2012_semantics",
            "SenticNet_v2014",
            "SenticNet_v2014_attributes",
            "SenticNet_v2014_semantics",
            "SenticNet_v2016",
            "SenticNet_v2016_attributes",
            "SenticNet_v2016_mood",
            "SenticNet_v2016_semantics",
            "SenticNet_v2018",
            "SenticNet_v2018_attributes",
            "SenticNet_v2018_mood",
            "SenticNet_v2018_semantics",
            "SenticNet_v2020",
            "SenticNet_v2020_attributes",
            "SenticNet_v2020_mood",
            "SenticNet_v2020_semantics",
            "SenticNet_v2022",
            "SenticNet_v2022_attributes",
            "SenticNet_v2022_mood",
            "SenticNet_v2022_semantics",
            "SO-CAL_v2011",
        ]
        # Add functions to analyse bidimensional dictionaries 
        if dictionary in avaliable_dictionary:
            if (
                dictionary == "SenticNet_v2012_attributes"
                or dictionary == "SenticNet_v2014_attributes"
                or dictionary == "SenticNet_v2016_attributes"
                or dictionary == "SenticNet_v2018_attributes"
                or dictionary == "SenticNet_v2020_attributes"
                or dictionary == "SenticNet_v2022_attributes"
            ):
                raise ValueError(
                    f"The provided dictionary '{dictionary}' is currently unsupported."
                )
            else:
                loaded_dictionary = load.dict(dictionary)
        else:
            if dictionary is None:
                raise ValueError("The 'dictionary' parameter must be provided.")
            else:
                raise ValueError(
                    f"The provided dictionary '{dictionary}' is not available."
                )

        # Check if dictionary is score-based or label-based
        for key, value in itertools.islice(loaded_dictionary.items(), 1):
            if isinstance(value, str):
                lex_dict_type = "categorical"
            elif isinstance(value, int):
                lex_dict_type = "discrete"
            elif isinstance(value, float):
                lex_dict_type = "continuous"
            elif isinstance(value, list):
                if all(isinstance(item, str) for item in value):
                    lex_dict_type = "categorical (multi-label)"
                elif all(isinstance(item, float) for item in value) or all(
                    isinstance(item, int) for item in value
                ):
                    lex_dict_type = "vector representation"
                else:
                    lex_dict_type = "unknown"
            else:
                lex_dict_type = "unknown"
        
        # If score-based, calculate sentiment
        if lex_dict_type == "discrete" or lex_dict_type == "continuous":
            total_score = 0
            matched_positions = set()
            for key, value in loaded_dictionary.items():
                pattern = re.compile(
                    r"\b" + re.escape(key) + r"\b", flags=re.IGNORECASE
                )
                matches = pattern.finditer(text.lower())
                for match in matches:
                    start, end = match.span()
                    # Check if there is any overlapping match
                    if any(start < pos < end for pos in matched_positions):
                        continue
                    total_score += value
                    # Add the positions of the current match to the set
                    matched_positions.update(range(start, end))
            return round(total_score, 4)

        # Else if label based, collect sentiment        
        elif lex_dict_type == "categorical":
            if (
                dictionary == "Aigents+_v2022"
                or dictionary == "Henry_v2006"
                or dictionary == "OpinionLexicon_v2004"
                or dictionary == "GeneralInquirer_v2000"
            ):
                sentiment_labels = ["positive", "negative"]
            elif dictionary == "DED_v2022":
                sentiment_labels = ["anger", "anxiety", "optimism", "sadness"]
            
            total_sentiment = []
            matched_positions = set()
            
            for key, value in loaded_dictionary.items():
                pattern = re.compile(
                    r"\b" + re.escape(key) + r"\b", flags=re.IGNORECASE
                )
                matches = pattern.finditer(text.lower())
                for match in matches: 
                    start, end = match.span()
                    # Check if there is any overlapping match
                    if any(start < pos < end for pos in matched_positions):
                        continue
                    total_sentiment.append(value)
                    # Add the positions of the current match to the set
                    matched_positions.update(range(start, end))
            
            class_counts = {word: 0 for word in sentiment_labels}

            # Count occurrences of each class in the list
            for class_name in total_sentiment:
                class_counts[class_name] += 1
            
            return class_counts
        
        elif lex_dict_type == "categorical (multi-label)": 
            if dictionary == "MASTER_v2022":
                sentiment_labels = [
                    "Negative",
                    "Uncertainty",
                    "Constraining",
                    "Positive",
                    "Litigious",
                    "Weak_Modal",
                    "Strong_Modal",
                ]
            elif dictionary == "WordNet-Affect_v2006":
                sentiment_labels = [
                    "general-dislike",
                    "anger",
                    "fury",
                    "negative-emotion",
                    "wrath",
                    "ambiguous-emotion",
                    "love",
                    "positive-emotion",
                    "worship",
                    "sadness",
                    "melancholy",
                    "world-weariness",
                    "wonder",
                    "astonishment",
                    "surprise",
                    "sorrow",
                    "lost-sorrow",
                    "mournfulness",
                    "woe",
                    "neutral-unconcern",
                    "indifference",
                    "neutral-emotion",
                    "withdrawal",
                    "oppression",
                    "depression",
                    "weight",
                    "weepiness",
                    "liking",
                    "preference",
                    "weakness",
                    "hostility",
                    "belligerence",
                    "hate",
                    "warpath",
                    "lovingness",
                    "warmheartedness",
                    "malevolence",
                    "vindictiveness",
                    "ambiguous-agitation",
                    "unrest",
                    "dislike",
                    "unfriendliness",
                    "diffidence",
                    "timidity",
                    "negative-fear",
                    "unassertiveness",
                    "umbrage",
                    "tumult",
                    "joy",
                    "exultation",
                    "triumph",
                    "apprehension",
                    "trepidation",
                    "calmness",
                    "tranquillity",
                    "closeness",
                    "belonging",
                    "togetherness",
                    "exhilaration",
                    "titillation",
                    "thing",
                    "compassion",
                    "tenderness",
                    "sympathy",
                    "resentment",
                    "sulkiness",
                    "stupefaction",
                    "stir",
                    "anxiety",
                    "negative-agitation",
                    "stewing",
                    "stage-fright",
                    "regret-sorrow",
                    "solicitude",
                    "positive-concern",
                    "softheartedness",
                    "affection",
                    "soft-spot",
                    "satisfaction",
                    "contentment",
                    "complacency",
                    "smugness",
                    "sinking",
                    "shyness",
                    "embarrassment",
                    "shame",
                    "shamefacedness",
                    "foreboding",
                    "shadow",
                    "sensation",
                    "self-pity",
                    "self-pride",
                    "self-esteem",
                    "self-disgust",
                    "humility",
                    "self-depreciation",
                    "self-consciousness",
                    "fearlessness",
                    "security",
                    "scruple",
                    "scare",
                    "positive-hope",
                    "optimism",
                    "sanguinity",
                    "reverence",
                    "ambiguous-fear",
                    "despair",
                    "resignation",
                    "disgust",
                    "repugnance",
                    "compunction",
                    "repentance",
                    "regard",
                    "puppy-love",
                    "protectiveness",
                    "satisfaction-pride",
                    "presage",
                    "plaintiveness",
                    "placidity",
                    "annoyance",
                    "pique",
                    "pessimism",
                    "pensiveness",
                    "peace",
                    "panic",
                    "nausea",
                    "murderousness",
                    "misopedia",
                    "misoneism",
                    "misology",
                    "misogyny",
                    "misogamy",
                    "misocainea",
                    "misery",
                    "misanthropy",
                    "mercifulness",
                    "meekness",
                    "malice",
                    "maleficence",
                    "loyalty",
                    "lividity",
                    "levity",
                    "apathy",
                    "neutral-languor",
                    "easiness",
                    "positive-languor",
                    "kindheartedness",
                    "cheerlessness",
                    "joylessness",
                    "merriment",
                    "jollity",
                    "jocundity",
                    "jitteriness",
                    "envy",
                    "jealousy",
                    "alienation",
                    "isolation",
                    "bad-temper",
                    "irascibility",
                    "insecurity",
                    "ingratitude",
                    "infuriation",
                    "indignation",
                    "fidget",
                    "impatience",
                    "empathy",
                    "identification",
                    "hysteria",
                    "huffiness",
                    "hopelessness",
                    "hopefulness",
                    "hilarity",
                    "hesitance",
                    "admiration",
                    "hero-worship",
                    "helplessness",
                    "heavyheartedness",
                    "negative-unconcern",
                    "heartlessness",
                    "heartburning",
                    "harassment",
                    "happiness",
                    "enthusiasm",
                    "gusto",
                    "guilt",
                    "grudge",
                    "grief",
                    "gravity",
                    "gratitude",
                    "gratefulness",
                    "friendliness",
                    "good-will",
                    "gloom",
                    "gloat",
                    "gladness",
                    "playfulness",
                    "fulfillment",
                    "frustration",
                    "positive-fear",
                    "frisson",
                    "forlornness",
                    "forgiveness",
                    "fondness",
                    "fit",
                    "ambiguous-expectation",
                    "fever",
                    "approval",
                    "favor",
                    "exuberance",
                    "elation",
                    "euphoria",
                    "encouragement",
                    "emotionlessness",
                    "electricity",
                    "ego",
                    "edginess",
                    "earnestness",
                    "eagerness",
                    "dysphoria",
                    "dudgeon",
                    "downheartedness",
                    "dolor",
                    "dolefulness",
                    "distress",
                    "distance",
                    "displeasure",
                    "disinclination",
                    "discouragement",
                    "discomfiture",
                    "disapproval",
                    "devotion",
                    "despondency",
                    "despisal",
                    "demoralization",
                    "defeatism",
                    "daze",
                    "dander",
                    "cynicism",
                    "cruelty",
                    "creeps",
                    "covetousness",
                    "coolness",
                    "contempt",
                    "conscience",
                    "confusion",
                    "confidence",
                    "negative-concern",
                    "compatibility",
                    "commiseration",
                    "comfortableness",
                    "class-feeling",
                    "cheerfulness",
                    "chagrin",
                    "carefreeness",
                    "captivation",
                    "buoyancy",
                    "buck-fever",
                    "brotherhood",
                    "bonheur",
                    "blue-devils",
                    "benevolence",
                    "beneficence",
                    "bang",
                    "attrition",
                    "attachment",
                    "enthusiasm-ardor",
                    "anxiousness",
                    "antipathy",
                    "positive-expectation",
                    "anticipation",
                    "antagonism",
                    "animosity",
                    "amour-propre",
                    "amorousness",
                    "amicability",
                    "alarm",
                    "aggression",
                    "aggravation",
                    "abhorrence",
                    "abashment",
                    "angst",
                    "horror",
                    "positive-suspense",
                    "awe",
                    "fear-intimidation",
                    "ambiguous-hope",
                ]
            elif (
                dictionary == "SenticNet_v2016_mood"
                or dictionary == "SenticNet_v2018_mood"
                or dictionary == "SenticNet_v2020_mood"
            ):
                sentiment_labels = [
                    "joy",
                    "surprise",
                    "admiration",
                    "disgust",
                    "interest",
                    "fear",
                    "sadness",
                    "anger",
                ]
            elif dictionary == "SenticNet_v2022_mood":
                sentiment_labels = [
                    "eagerness",
                    "pleasantness",
                    "calmness",
                    "serenity",
                    "contentment",
                    "fear",
                    "melancholy",
                    "grief",
                    "bliss",
                    "disgust",
                    "terror",
                    "dislike",
                    "sadness",
                    "annoyance",
                    "responsiveness",
                    "loathing",
                    "delight",
                    "anxiety",
                    "enthusiasm",
                    "anger",
                    "joy",
                    "rage",
                    "ecstasy",
                    "acceptance",
                ]

            total_sentiment = []
            matched_positions = set()
            
            for key, value in loaded_dictionary.items():
                pattern = re.compile(
                    r"\b" + re.escape(key) + r"\b", flags=re.IGNORECASE
                )
                matches = pattern.finditer(text.lower())
                for match in matches:
                    start, end = match.span()
                    # Check if there is any overlapping match
                    if any(start < pos < end for pos in matched_positions):
                        continue
                    total_sentiment.extend(value)
                    # Add the positions of the current match to the set
                    matched_positions.update(range(start, end))
            
            class_counts = {word: 0 for word in sentiment_labels}

            # Count occurrences of each class in the list
            for class_name in total_sentiment:
                class_counts[class_name] += 1
            
            return class_counts
        

# class lexical_overview:
#     """
#     Class for generating a lexical overview based on a sentiment lexicon dictionary.

#     Attributes:
#         dictionary (dict): Input sentiment lexicon dictionary for analysis.
#     """

#     def __init__(self, dictionary: dict = None):
#         """
#         Initializes the lexical_overview class with a sentiment lexicon dictionary.

#         Args:
#             dictionary (dict): Input sentiment lexicon dictionary for analysis.

#         Raises:
#             ValueError: Raised if no dictionary is provided.
#         """
#         # dict:str = Consider if users simply come up with the lex_dict_idx
#         if dict is None:
#             raise ValueError("The 'dictionary' parameter must be provided.")
#         else:
#             analysis().summarise_lex_dict(dictionary)


# class sentimentanalysis:
#     def __init__(self, method: str, text: str, dictionary: str = None):
#         if method.lower() == ("bow" or "bag-of-words" or "bag of words"):
#             self.result = self.bag_of_words(text=text, dictionary=dictionary)
#         else:
#             raise ValueError
    
#     def __str__(self): 
#         return str(self.result)
    
#     def bag_of_words(self, text: str, dictionary: str):
        
