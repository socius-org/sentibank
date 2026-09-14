"""End-to-end checks of analyze.sentiment() and CSV export against the real dictionaries."""

import argparse

import pandas as pd
import pytest

from sentibank import archive, cli
from sentibank.utils import analyze

IDENTIFIERS = archive.load().list_available()["dictionaries"]
SUPPORTED = [i for i in IDENTIFIERS if not i.endswith("_semantics")]
FAST = [i for i in SUPPORTED if not i.startswith("SenticNet")]
TEXT = "I am excited and happy about the new announcement, though the risk of loss worries me."


@pytest.fixture(scope="module")
def analyzer():
    return analyze()


@pytest.mark.parametrize("identifier", FAST)
def test_sentiment_runs_for_every_supported_dictionary(analyzer, identifier):
    result = analyzer.sentiment(text=TEXT, dictionary=identifier)
    assert isinstance(result, (int, float, dict, list))
    if isinstance(result, dict):
        assert result, "label-based dictionaries return one count per label"
        assert all(isinstance(count, int) for count in result.values())


@pytest.mark.slow
@pytest.mark.parametrize(
    "identifier",
    ["SenticNet_v2010", "SenticNet_v2020_mood", "SenticNet_v2022_attributes"],
)
def test_sentiment_senticnet_variants(analyzer, identifier):
    result = analyzer.sentiment(text=TEXT, dictionary=identifier)
    assert isinstance(result, (int, float, dict, list))


@pytest.mark.parametrize(
    "identifier", [i for i in IDENTIFIERS if i.endswith("_semantics")]
)
def test_semantics_dictionaries_are_rejected(analyzer, identifier):
    with pytest.raises(ValueError, match="cannot be used"):
        analyzer.sentiment(text=TEXT, dictionary=identifier)


def test_general_inquirer_uses_the_loader_identifier(analyzer):
    result = analyzer.sentiment(
        text="I am excited and happy.", dictionary="GeneralInquirer_v2000"
    )
    assert set(result) == {"positive", "negative"}
    assert result["positive"] >= 1


def test_unknown_identifier_is_rejected(analyzer):
    with pytest.raises(ValueError, match="not available"):
        analyzer.sentiment(text=TEXT, dictionary="HarvardGI_v2000")


def test_score_based_example_matches_readme(analyzer):
    assert (
        analyzer.sentiment(
            text="I am excited and happy about the new announcement!",
            dictionary="VADER_v2014",
        )
        == 4.1
    )


def test_vector_dictionary_returns_per_dimension_sums(analyzer):
    result = analyzer.sentiment(
        text="happy calm", dictionary="NoVAD_v2013_bidimensional"
    )
    assert isinstance(result, list) and len(result) == 2


def test_csv_export_of_label_based_dictionary(tmp_path):
    output = tmp_path / "master.csv"
    status = cli.cmd_export(
        argparse.Namespace(dictionary="MASTER_v2022", format="csv", output=str(output))
    )
    assert status == 0
    df = pd.read_csv(output)
    assert list(df.columns) == ["word", "score"]
    assert len(df) > 3000
    assert "Negative" in df["score"].iloc[0]
