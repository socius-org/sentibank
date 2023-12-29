from rich.progress import track
from rich import print as pprint
import itertools
from itertools import combinations, chain
import statistics
from collections import Counter
import spacy
from spacymoji import Emoji
from sentibank.dict_arXiv import emos


class analysis:
    def __init__(self):
        self.spacy_nlp = spacy.load(
            "en_core_web_sm",
            exclude=["parser", "senter", "attribute_ruler", "lemmatizer", "ner"],
        )
        # self.spacy_nlp.add_pipe("sentencizer")
        self.spacy_nlp.add_pipe("emoji", first=True)

    def count_categorical_labels(self, dictionary):
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

    def count_discrete_labels(self, dictionary):
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

                    multi_label_counts[multi_label] = multi_label_counts.get(
                        multi_label, 0
                    ) + 1

        output = {
            "labels": sorted(list(label_counts.keys())),
            "label frequency": self.sort_dict(label_counts),
            "multi label frequency": self.sort_dict(multi_label_counts),
        }

        if not output["multi label frequency"]:
            del output["multi label frequency"]

        return output

    def count_cont_variables(self, dictionary):
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

    def sort_dict(self, dictionary):
        return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

    def summarise_lex_dict(self, lexicon_dictionary):
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
                elif all(isinstance(item, int) for item in value):
                    lex_dict_type = "discrete (multi-label)"
                else:
                    lex_dict_type = "mixed"
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
                else:
                    granular_dict_adv["{} ({})".format(key, spacy.explain(key))] = value
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


class lexical_overview:
    def __init__(self, dictionary: dict = None):
        # dict:str = Consider if users simply come up with the lex_dict_idx
        if dict is None:
            raise ValueError
        else:
            analysis().summarise_lex_dict(dictionary)
