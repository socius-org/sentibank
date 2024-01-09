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

- **12+ (and counting) sentiment dictionaries** spanning domains and use cases
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

The predefined lexicon identifiers follow the convention {NAME}_{VERSION} - for example, "VADER_v2014". This naming structure indicates the lexicon name and its version for easy recognition and selection. 

See below for the available predefined lexicon identifier.

| Sentiment Dictionary | Associated Institution <br> (Principal Investigator) | Description | Genre | Domain | Predefined Identifiers (preprocessed) |
|------------------------|---------------------|---------------|------|-----|------------------------|
|**AFINN** <br> (Nielsen, 2011)| DTU Informatics <br> (Technical University of Denmark) | General purpose lexicon with sentiment ratings for common emotion words. |Social Media|General| `AFINN_v2009`, `AFINN_v2011`, `AFINN_v2015` |
|**Aigents+** <br> (Raheman et al., 2022)| Autonio Foundation | Lexicon optimised for social media posts related to cryptocurrencies. |Social Media|Cryptocurrency| `Aigents+_v2022`|
|**ANEW** <br> (Bradley and Lang, 1999)| NIMH Center for Emotion and Attention <br> (University of Florida) | Provides normative emotional ratings across pleasure, arousal, and dominance dimensions.|General|Psychology|`ANEW_v1999_simple`, `ANEW_v1999_weighted`|
|**Dictionary of Affect in Language (DAL)** <br> (Whissell, 1989; Whissell, 2009)| Laurentian University | Lexicon designed to quantify pleasantness, activation, and imagery dimensions across diverse everyday English words. | General | General | `DAL_v2009_norm`, `DAL_v2009_boosted`|
|**Discrete Emotions Dictionary (DED)** <br> (Fioroni et al., 2022)| Gallup | Lexicon focused on precisely distinguishing four key discrete emotions in political communication | News | Political Science | `DED_v2022` |
|**General Inquirer** <br> (Stone et al., 1962)| Harvard University | Lexicon capturing broad psycholinguistic dimensions across semantics, values and motivations.  |General|Psychology, Political Science| `HarvardGI_v2000`|
|**Henry** <br> (Henry, 2006) | University of Miami  | Leixcon designed for analysing tone in earnings press releases. |Corporate Communication (Earnings Press Releases)|Finance| `Henry_v2006`|
|**MASTER** <br> (Loughran and McDonland, 2011; Bodnaruk, Loughran and McDonald, 2015)| University of Notre Dame | Financial lexicons covering expressions common in business writing. |Regulatory Filings (10-K)|Finance| `MASTER_v2022`|
|**OpinionLexicon** <br> (Hu and Liu, 2004)| University of Illinois Chicago | Opinion words tailored for sentiment analysis of product reviews.|Product Reviews|Consumer Products|`OpinionLexicon_v2004`|
|**SentiWordNet** <br> (Esuli and Sebastiani, 2006; Baccianella, Esuli and Sebastiani, 2010)| Institute of Information Science and Technologies <br>(Consiglio Nazionale delle Ricerche) | Lexicon associating WordNet synsets with positive, negative, and objective scores. |General|General| `SentiWordNet_v2010_simple`, `SentiWordNet_v2010_nuanced` |
|**VADER** <br> (Hutto and Gilbert, 2014)| Georgia Institute of Technology | General purpose lexicon optimised for social media and microblogs. |Social Media|General| `VADER_v2014`|
|**WordNet-Affect** <br> (Strapparava and Valitutti, 2004; Valitutti, Strapparava and Stock, 2004; Strapparava, Valitutti and Stock, 2006)| Institute for Scientific and Technological Research <br> (Fondazione Bruno Kessler) | Hierarchically organised affective labels providing a  granular emotional dimension. |General|Psychology| `WordNet-Affect_v2006`|

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
