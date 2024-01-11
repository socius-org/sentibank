# sentibank
[![License](https://img.shields.io/badge/License-CC--BY--NC--SA--4.0-green.svg?style=flat-square)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Github Stars](https://img.shields.io/github/stars/socius-org/sentibank?style=flat-square&logo=github)](https://github.com/socius-org/sentibank)
[![Github Watchers](https://img.shields.io/github/watchers/socius-org/sentibank?style=flat-square&logo=github)](https://github.com/socius-org/sentibank)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sentibank?style=flat-square&logo=python)

**`sentibank`** is a comprehensive, open database of expert-curated sentiment dictionaries and lexicons to power sentiment analysis.

## Overview 

Sentiment analysis is the automated process of identifying and extracting subjective information such as opinions, emotions, and attitudes from textual data. It has become an increasingly critical technique across many social science domains such as business, politics, and economics. 

However, sentiment analysis today faces key challenges:
- Disparate, fragmented resources requiring laborious integration
- Lack of verified, high-quality lexicons spanning domains
- Inaccessibility limiting transparency and advancement

**`sentibank` tackles these issues by consolidating lexicons into an integrated, open-source database**

## Key Capabilities 

- **14+ (and counting) sentiment dictionaries** spanning domains and use cases
- Curation of dictionaries provided by **leading experts** in sentiment analysis
- Access **original lexicons** and **preprocessed versions**
- Customise existing dictionaries or contribute new ones
- Production-ready for integration into analyses

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

The predefined lexicon identifiers follow either a `{NAME}_{VERSION}` convention, meaning only compulsory processing was completed on the base lexicon, or a `{NAME}_{VERSION}_{refined}` structure specifying additional transformations that represent discretionary refinements. For example, `NoVAD_v2013_adjusted` applies arousal-based adjustments to intensify extreme valence values and dampen neutral ones, providing a richness-preserving single score.

See below for the available predefined lexicon identifier.

| Sentiment Dictionary | Description | Genre | Domain | Predefined Identifiers (preprocessed) |
|------------------------|---------------|------|-----|------------------------|
|**AFINN** <br> (Nielsen, 2011)| General purpose lexicon with sentiment ratings for common emotion words. |Social Media|General| `AFINN_v2009`, `AFINN_v2011`, `AFINN_v2015` |
|**Aigents+** <br> (Raheman et al., 2022)| Lexicon optimised for social media posts related to cryptocurrencies. |Social Media|Cryptocurrency| `Aigents+_v2022`|
|**ANEW** <br> (Bradley and Lang, 1999)| Provides normative emotional ratings across pleasure, arousal, and dominance dimensions.|General|Psychology|`ANEW_v1999_simple`, `ANEW_v1999_weighted`|
|**Dictionary of Affect in Language (DAL)** <br> (Whissell, 1989; Whissell, 2009)| Lexicon designed to quantify pleasantness, activation, and imagery dimensions across diverse everyday English words. | General | General | `DAL_v2009_boosted`, `DAL_v2009_norm` |
|**Discrete Emotions Dictionary (DED)** <br> (Fioroni et al., 2022)| Lexicon focused on precisely distinguishing four key discrete emotions in political communication | News | Political Science | `DED_v2022` |
|**General Inquirer** <br> (Stone et al., 1962)| Lexicon capturing broad psycholinguistic dimensions across semantics, values and motivations.  |General|Psychology, Political Science| `HarvardGI_v2000`|
|**Henry** <br> (Henry, 2006) | Leixcon designed for analysing tone in earnings press releases. |Corporate Communication (Earnings Press Releases)|Finance| `Henry_v2006`|
|**MASTER** <br> (Loughran and McDonland, 2011; Bodnaruk, Loughran and McDonald, 2015)| Financial lexicons covering expressions common in business writing. |Regulatory Filings (10-K)|Finance| `MASTER_v2022`|
|**Norms of Valence, Arousal and Dominance (NoVAD)** <br> (Warriner, Kuperman and Brysbaert, 2013; Warriner and Kuperman, 2014)| A lexicon of 14,000 common English lemmas across valence, arousal, and dominance dimensions.  | General | Psychology |  `NoVAD_v2013_adjusted`, `NoVAD_v2013_bidimensional`|
|**OpinionLexicon** <br> (Hu and Liu, 2004)| Opinion words tailored for sentiment analysis of product reviews.|Product Reviews|Consumer Products|`OpinionLexicon_v2004`|
|**SenticNet** <br> (Cambria et al., 2010; Cambria, Havasi and Hussain, 2012; Cambria, Olsher and Rajagopal, 2014; Cambria et al., 2016; Cambria et al., 2018; Cambria et al., 2020; Cambria et al., 2022) | Conceptual lexicon providing multidimensional sentiment analysis for commonsense concepts and expressions. | General | General | `SenticNet_v2010`, `SenticNet_v2012`, `SenticNet_v2012_attributes`, `SenticNet_v2012_semantics`, `SenticNet_v2014`, `SenticNet_v2014_attributes`, `SenticNet_v2014_semantics`, `SenticNet_v2016`, `SenticNet_v2016_attributes`, `SenticNet_v2016_mood`, `SenticNet_v2016_semantics`, `SenticNet_v2018`, `SenticNet_v2018_attributes`, `SenticNet_v2018_mood`, `SenticNet_v2018_semantics`, `SenticNet_v2020`, `SenticNet_v2020_attributes`, `SenticNet_v2020_mood`, `SenticNet_v2020_semantics`, `SenticNet_v2022`, `SenticNet_v2022_attributes`, `SenticNet_v2022_mood`, `SenticNet_v2022_semantics` |
|**SentiWordNet** <br> (Esuli and Sebastiani, 2006; Baccianella, Esuli and Sebastiani, 2010)| Lexicon associating WordNet synsets with positive, negative, and objective scores. |General|General| `SentiWordNet_v2010_logtransform`, `SentiWordNet_v2010_simple`|
|**VADER** <br> (Hutto and Gilbert, 2014)| General purpose lexicon optimised for social media and microblogs. |Social Media|General| `VADER_v2014`|
|**WordNet-Affect** <br> (Strapparava and Valitutti, 2004; Valitutti, Strapparava and Stock, 2004; Strapparava, Valitutti and Stock, 2006)| Hierarchically organised affective labels providing a  granular emotional dimension. |General|Psychology| `WordNet-Affect_v2006`|

Refer [documentation](docs_link) for details on usage.

### Analyse Dictionaries

Once you've loaded the sentiment dictionaries using `sentibank`, you can perform various analyses on them. The `lexical_overview` module provides insights into the structure and content of sentiment lexicons. Here's a quick example:

```python
from sentibank import archive
from sentibank.utils import lexical_overview

# Load dictionaries
load = archive.load()
vader = load.dict("VADER_v2014")

# Analyse the loaded dictionary
lexical_overview(vader)
```

This will provide you with a summary of the sentiment scores and lexicon structure. You can further explore and analyse other sentiment dictionaries using the same approach.

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

## Contributing 

We welcome contributions of new expert-curated lexicons. Please refer to [guidelines](https://github.com/socius-org/sentibank/blob/main/doc/CONTRIBUTING.md).
