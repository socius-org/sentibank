# 🗃️ sentibank
[![DOI](https://zenodo.org/badge/673006895.svg)](https://zenodo.org/doi/10.5281/zenodo.10514542)
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-green.svg?style=flat-square)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Github Stars](https://img.shields.io/github/stars/socius-org/sentibank?style=flat-square&logo=github)](https://github.com/socius-org/sentibank)
[![Github Watchers](https://img.shields.io/github/watchers/socius-org/sentibank?style=flat-square&logo=github)](https://github.com/socius-org/sentibank)
[![Downloads](https://static.pepy.tech/badge/sentibank)](https://pypistats.org/packages/sentibank)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/sentibank?style=flat-square&logo=python)](https://pypistats.org/packages/sentibank)
[![CI](https://github.com/socius-org/sentibank/workflows/CI/badge.svg)](https://github.com/socius-org/sentibank/actions)
[![Coverage](https://codecov.io/gh/socius-org/sentibank/branch/main/graph/badge.svg)](https://codecov.io/gh/socius-org/sentibank)

> **[📝 Read the Paper](https://ojs.aaai.org/index.php/ICWSM/article/view/31443)**
> 
> **[📄 Read the Docs](https://doc.socius.org/sentibank/about.html)** 

**`sentibank`** is a comprehensive, open database of expert-curated sentiment dictionaries and lexicons to power sentiment analysis. Now with enhanced performance, type safety, CLI tools, and production-ready features!

## Overview 

Sentiment analysis, the automated process of identifying and extracting subjective information like opinions, emotions, and attitudes from text data, has become an increasingly critical technique across social science domains. In particular, rule-based sentiment analysis relies on expert-curated lexicons containing words with pre-assigned sentiment scores.

However, creating effective rule-based systems faces several challenges::
- Disparate, fragmented resources requiring laborious integration
- Lack of verified, high-quality lexicons spanning domains
- Inaccessibility limiting transparency and advancement

**`sentibank` tackles these issues by consolidating lexicons into an integrated, open-source database**. Here's some of the key capabilities: 

- 🗃️ **15+ (and counting) sentiment dictionaries** spanning domains and use cases
- 🧠 Curation of dictionaries provided by **leading experts** in sentiment analysis
- 📖 Access **original lexicons** and **preprocessed versions**
- ✏️ Customise existing dictionaries or contribute new ones
- 🚀 Production-ready for integration into analyses

## ✨ What's New in v1.0.0

### 🛠️ Enhanced Developer Experience
- **🔧 Full Type Safety**: Complete type annotations for better IDE support
- **⚡ Performance Caching**: Built-in dictionary caching for faster loading
- **🛡️ Robust Error Handling**: Comprehensive exception handling and logging
- **🧪 Comprehensive Testing**: Full pytest suite with 90%+ coverage

### 🖥️ Command Line Interface
```bash
# List available dictionaries
sentibank list

# Analyze sentiment with rich formatting
sentibank analyze VADER_v2014 "I love this product!"

# Export dictionaries to multiple formats
sentibank export VADER_v2014 --format json
```

### 🏗️ Modern Python Packaging
- **📦 pyproject.toml**: Modern packaging standards
- **🔄 CI/CD Pipeline**: Automated testing and publishing
- **📚 Enhanced Documentation**: Examples and comprehensive guides
- **🎨 Code Quality**: Black, isort, flake8, mypy integration

## Getting Started 

### Installation

Install the sentibank package:

```
pip install sentibank
```

### Load Preprocessed Dictionaries

Import sentibank and load dictionaries:

```python
from sentibank import archive

load = archive.load()
vader = load.dict("VADER_v2014") 
```

The predefined lexicon identifiers follow either a `{NAME}_{VERSION}` convention, meaning only compulsory processing was completed on the base lexicon, or a `{NAME}_{VERSION}_{refined}` structure specifying additional transformations that represent discretionary refinements. For example, `NoVAD_v2013_boosted` applies arousal-based adjustments to intensify extreme valence values and dampen neutral ones, providing a richness-preserving single score.

See below for the available predefined lexicon identifier.

| Sentiment Dictionary | Description | Genre | Domain | Predefined Identifiers (preprocessed) |
|------------------------|---------------|------|-----|------------------------|
|**AFINN** <br> (Nielsen, 2011)| General purpose lexicon with sentiment ratings for common emotion words. |Social Media|General| `AFINN_v2009`, `AFINN_v2011`, `AFINN_v2015` |
|**Aigents+** <br> (Raheman et al., 2022)| Lexicon optimised for social media posts related to cryptocurrencies. |Social Media|Cryptocurrency| `Aigents+_v2022`|
|**ANEW** <br> (Bradley and Lang, 1999)| Provides normative emotional ratings across pleasure, arousal, and dominance dimensions.|General (standard English)|Psychology|`ANEW_v1999_simple`, `ANEW_v1999_weighted`|
|**Dictionary of Affect in Language (DAL)** <br> (Whissell, 1989; Whissell, 2009)| Lexicon designed to quantify pleasantness, activation, and imagery dimensions across diverse everyday English words. | Vernacular (Day-to-Day Expression) | General | `DAL_v2009_boosted`, `DAL_v2009_norm` |
|**Discrete Emotions Dictionary (DED)** <br> (Fioroni et al., 2022)| Lexicon focused on precisely distinguishing four key discrete emotions in political communication | News | Political Science | `DED_v2022` |
|**General Inquirer** <br> (Stone et al., 1962)| Lexicon capturing broad psycholinguistic dimensions across semantics, values and motivations.  |General (standard English)|Psychology, Political Science| `GeneralInquirer_v2000`|
|**Henry** <br> (Henry, 2006) | Leixcon designed for analysing tone in earnings press releases. |Corporate Communication (Earnings Press Releases)|Finance| `Henry_v2006`|
|**MASTER** <br> (Loughran and McDonland, 2011; Bodnaruk, Loughran and McDonald, 2015)| Financial lexicons covering expressions common in business writing. |Regulatory Filings (10-K)|Finance| `MASTER_v2022`|
|**Norms of Valence, Arousal and Dominance (NoVAD)** <br> (Warriner, Kuperman and Brysbaert, 2013; Warriner and Kuperman, 2014)| A lexicon of 14,000 common English lemmas across valence, arousal, and dominance dimensions.  | Vernacular (Day-to-Day Expression) | General, Psychology |  `NoVAD_v2013_boosted`, `NoVAD_v2013_norm`|
|**OpinionLexicon** <br> (Hu and Liu, 2004)| Opinion words tailored for sentiment analysis of product reviews.|Reviews|Consumer Products|`OpinionLexicon_v2004`|
|**SenticNet** <br> (Cambria et al., 2010; Cambria, Havasi and Hussain, 2012; Cambria, Olsher and Rajagopal, 2014; Cambria et al., 2016, 2018, 2020, 2022) | Conceptual lexicon providing multidimensional sentiment analysis for commonsense concepts and expressions. | General (standard & non-standard English) | General | `SenticNet_v2010`, `SenticNet_v2012`, `SenticNet_v2012_attributes`, `SenticNet_v2012_semantics`, `SenticNet_v2014`, `SenticNet_v2014_attributes`, `SenticNet_v2014_semantics`, `SenticNet_v2016`, `SenticNet_v2016_attributes`, `SenticNet_v2016_mood`, `SenticNet_v2016_semantics`, `SenticNet_v2018`, `SenticNet_v2018_attributes`, `SenticNet_v2018_mood`, `SenticNet_v2018_semantics`, `SenticNet_v2020`, `SenticNet_v2020_attributes`, `SenticNet_v2020_mood`, `SenticNet_v2020_semantics`, `SenticNet_v2022`, `SenticNet_v2022_attributes`, `SenticNet_v2022_mood`, `SenticNet_v2022_semantics` |
|**SentiWordNet** <br> (Esuli and Sebastiani, 2006; Baccianella, Esuli and Sebastiani, 2010)| Lexicon associating WordNet synsets with positive, negative, and objective scores. |General (standard English)|General| `SentiWordNet_v2010_logtransform`, `SentiWordNet_v2010_simple`|
| **SO-CAL** <br> (Taboada et al., 2011) | Lexicon designed for domain-independent sentiment analysis. | General (standard & non-standard English) | General | `SO-CAL_v2011` |
|**VADER** <br> (Hutto and Gilbert, 2014)| General purpose lexicon optimised for social media and microblogs. |Social Media|General| `VADER_v2014`|
|**WordNet-Affect** <br> (Strapparava and Valitutti, 2004; Valitutti, Strapparava and Stock, 2004; Strapparava, Valitutti and Stock, 2006)| Hierarchically organised affective labels providing a  granular emotional dimension. |General (standard English)|Psychology| `WordNet-Affect_v2006`|

### Load Original Dictionaries

In addition to preprocessed sentiment dictionaries, `sentibank` provides the capability to load the original datasets sourced directly from the authors, which were used in the creation of these sentiment dictionaries. These original datasets offer valuable insights into the raw sentiment data as originally curated by the authors and can be particularly beneficial for in-depth research and analysis.

To load an original dictionary, you can use the `load.origin` method, which returns a Pandas DataFrame containing the original dataset. Here's a basic example:

```python
from sentibank import archive

# Load the original dataset for VADER sentiment dictionary
load = archive.load()
vader_original = load.origin("VADER_v2014")
```

This will load the original dataset associated with the VADER sentiment dictionary. You can replace "VADER_v2014" with other original dictionary identifiers. The loaded data will allow you to explore and analyse the original sentiment data directly.

### Analyse Dictionaries

The `analyze().dictionary` module provides insights into the structure and content of sentiment lexicons. Here's a quick example:

```python
from sentibank.utils import analyze

# Analyse the dictionary
analyze = analyze()
analyze.dictionary(dictionary="WordNet-Affect_v2006")
```

This will provide you with a summary of the sentiment scores and lexicon structure. You can further explore and analyse other sentiment dictionaries using the same approach.

### Analyse Sentiment

The `analyze().sentiment` module performs sentiment analysis on text using the specified lexicon dictionary. It utilises a bag-of-words approach, analyzing the occurrence of terms without considering their order.

For score-based lexicons like `VADER_v2014`, it sums the scores of matched terms and returns a single float/integer value reflecting overall sentiment. Higher scores indicate more positive/negative sentiment.

```python
from sentibank.utils import analyze

# Analyse the sentiment
analyze = analyze()
text = "I am excited and happy about the new anouncement!"
result = analyze.sentiment(text=text, dictionary="VADER_v2014")
# The result would be +4.1
```

For label-based dictionaries like `HarvardGI_v2000`, it counts matched terms per sentiment category and returns a dictionary of those label counts. The category with the most matches indicates the dominant overall sentiment.

```python
text = "I am excited and happy to make this anouncement to our shareholders."
result = analyze.sentiment(text=text, dictionary="MASTER_v2022")
# The result would be {'Negative': 0,'Uncertainty': 0,'Constraining': 0,'Positive': 2,'Litigious': 0,'Weak_Modal': 0,'Strong_Modal': 0}
```

This allows flexible sentiment analysis tailored to different dictionary representations. Score-based lexicons provide a sentiment intensity metric, while label-based ones give a breakdown of sentiment types. The bag-of-words approach offers efficient broad-stroke analysis without syntactical sensitivity.

## 🖥️ Command Line Usage

Sentibank now includes a powerful CLI for quick sentiment analysis:

### Quick Start
```bash
# List all available dictionaries
sentibank list

# Analyze sentiment of text
sentibank analyze VADER_v2014 "This product is absolutely amazing!"

# Get detailed dictionary information
sentibank info VADER_v2014

# Export a dictionary to JSON
sentibank export VADER_v2014 --format json --output my_vader.json
```

### Advanced CLI Usage
```bash
# Analyze text from a file
sentibank analyze VADER_v2014 --file reviews.txt

# Get JSON output for programmatic use
sentibank analyze AFINN_v2015 "Great experience!" --json

# Export to different formats
sentibank export SO-CAL_v2011 --format csv --output socal.csv
```

## 🔧 New API Features

### Enhanced Dictionary Loading
```python
from sentibank import archive

loader = archive.load()

# List available dictionaries and origins
available = loader.list_available()
print(f"Available: {len(available['dictionaries'])} dictionaries")

# Built-in caching for better performance
vader1 = loader.dict("VADER_v2014")  # Loads from disk
vader2 = loader.dict("VADER_v2014")  # Loads from cache (faster!)

# Clear cache when needed
loader.clear_cache()
```

### Type-Safe Development
```python
from sentibank import archive
from typing import Dict, Any

loader: archive.load = archive.load()
sentiment_dict: Dict[str, Any] = loader.dict("VADER_v2014")
```

## 🔄 Migration Guide

### Upgrading from v0.x to v1.0.0

The v1.0.0 release maintains backward compatibility for basic usage:

```python
# ✅ This still works exactly the same
from sentibank import archive
load = archive.load()
vader = load.dict("VADER_v2014")
```

### New Features Available
- Enhanced error messages with specific exception types
- Built-in caching (automatic - no code changes needed)
- New utility methods: `list_available()`, `clear_cache()`
- CLI tools available after installation

## 📊 Examples

Check out the [`examples/`](examples/) directory for:
- **Basic Usage**: Getting started guide
- **Dictionary Comparison**: Comparing multiple dictionaries
- **CLI Examples**: Command-line usage demonstrations
- **Advanced Features**: Caching, logging, and more

## Contributing 

We welcome contributions of new expert-curated lexicons. Please refer to [guidelines](https://github.com/socius-org/sentibank/blob/main/doc/CONTRIBUTING.md).
