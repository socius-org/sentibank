import itertools
import re
import statistics
import subprocess
import sys
from collections import Counter
from itertools import chain, combinations

import enchant
import spacy
from rich import print as pprint
from rich.progress import track
from spacymoji import Emoji

from sentibank import archive
from sentibank.dict_arXiv import emos

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
                    stderr=subprocess.STDOUT,
                )
                # Try loading again after download
                self.spacy_nlp = spacy.load(
                    "en_core_web_sm",
                    exclude=[
                        "parser",
                        "senter",
                        "attribute_ruler",
                        "lemmatizer",
                        "ner",
                    ],
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

    def shorten_word(self, word: str):
        """
        Shortens words with three or more consecutive identical alphabets to two consecutive identical alphabets.

        Args:
            word (str): The word to be shortened.

        Returns:
            str: The shortened word.
        """
        # Find sections with three or more consecutive identical alphabets
        matches = re.findall(r"(\w)\1{2,}", word)

        # Shorten each section to two alphabets
        for match in matches:
            replacement = match[:2]
            word = re.sub(r"(\w)\1{2,}", replacement * 2, word, count=1)

        return word

    def sentence(self, sentence: str):
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
            if re.search(r"(\w)\1{2,}", word):
                word = self.shorten_word(word)
                print(word)
                if word == "soo":  # Add more words that enchant wrongly spell checks
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

        return " ".join(spellchecked_words).lower()


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

    #: Dictionaries whose values are related concepts rather than sentiment scores or labels.
    UNSUPPORTED_SUFFIXES = ("_semantics",)

    @staticmethod
    def _dictionary_type(loaded_dictionary: dict) -> str:
        """Classify a dictionary by the shape of its values."""
        for value in itertools.islice(loaded_dictionary.values(), 1):
            if isinstance(value, bool):
                return "unknown"
            if isinstance(value, str):
                return "categorical"
            if isinstance(value, int):
                return "discrete"
            if isinstance(value, float):
                return "continuous"
            if isinstance(value, list) and value:
                if all(isinstance(item, str) for item in value):
                    return "categorical (multi-label)"
                if all(isinstance(item, (int, float)) for item in value):
                    return "vector representation"
        return "unknown"

    @staticmethod
    def _matched_values(text: str, loaded_dictionary: dict) -> list:
        """Values of the dictionary terms found in `text` (bag of words, non-overlapping)."""
        lowered = text.lower()
        matched_positions: set = set()
        values = []
        for key, value in loaded_dictionary.items():
            pattern = re.compile(r"\b" + re.escape(key) + r"\b", flags=re.IGNORECASE)
            for match in pattern.finditer(lowered):
                start, end = match.span()
                if any(start < pos < end for pos in matched_positions):
                    continue
                values.append(value)
                matched_positions.update(range(start, end))
        return values

    def sentiment(self, text: str, dictionary: str = None):
        """
        Performs bag-of-words sentiment analysis on the given text using the specified lexicon dictionary.
        It checks spelling of words if a word has three consecutive identical alphabets (e.g. "happppyyyy")

        Parameters:
            text (str): The input text for sentiment analysis.
            dictionary (str): The identifier of the lexicon dictionary to use. Any identifier
                returned by ``archive.load().list_available()["dictionaries"]`` is accepted,
                except the SenticNet ``_semantics`` dictionaries, whose values are related
                concepts rather than sentiment.

        Returns:
            Union[float, Dict[str, int], List[float]]:
                Score-based dictionaries: the summed score of the matched terms.
                Label-based dictionaries (single or multi-label): a count per label, with every
                label of the dictionary present (zero when unmatched).
                Vector-valued dictionaries (for example ``NoVAD_v2013_bidimensional`` or the
                SenticNet ``_attributes`` dictionaries): the per-dimension sums of the matched
                terms, in the dictionary's dimension order.
        """
        if dictionary is None:
            raise ValueError("The 'dictionary' parameter must be provided.")

        available = load.list_available()["dictionaries"]
        if dictionary not in available:
            raise ValueError(
                f"The provided dictionary '{dictionary}' is not available. "
                "Use archive.load().list_available() to see the available identifiers."
            )
        if dictionary.endswith(self.UNSUPPORTED_SUFFIXES):
            raise ValueError(
                f"The provided dictionary '{dictionary}' maps concepts to related concepts "
                "rather than to sentiment scores or labels, so it cannot be used for "
                "sentiment analysis."
            )

        loaded_dictionary = load.dict(dictionary)
        text = self.spellcheck.sentence(text)
        lex_dict_type = self._dictionary_type(loaded_dictionary)
        matched = self._matched_values(text, loaded_dictionary)

        if lex_dict_type in ("discrete", "continuous"):
            return round(sum(matched), 4)

        if lex_dict_type == "categorical":
            labels = list(dict.fromkeys(loaded_dictionary.values()))
            counts = {label: 0 for label in labels}
            for value in matched:
                counts[value] += 1
            return counts

        if lex_dict_type == "categorical (multi-label)":
            labels = list(
                dict.fromkeys(
                    label for value in loaded_dictionary.values() for label in value
                )
            )
            counts = {label: 0 for label in labels}
            for value in matched:
                for label in value:
                    counts[label] += 1
            return counts

        if lex_dict_type == "vector representation":
            dimensions = len(next(iter(loaded_dictionary.values())))
            totals = [0.0] * dimensions
            for value in matched:
                for i, component in enumerate(value[:dimensions]):
                    totals[i] += component
            return [round(total, 4) for total in totals]

        raise ValueError(
            f"The provided dictionary '{dictionary}' has values that sentiment analysis "
            "does not support."
        )
