# sentibank
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square&label=license)](https://opensource.org/licenses/MIT)
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

**sentibank tackles these issues by consolidating lexicons into an integrated, open-source database**

## Key Capabilities 

- **6+ (and counting) sentiment dictionaries** spanning domains and use cases
- Curation of dictionaries provided by **leading experts** in sentiment analysis
- Access original lexicons and **preprocessed versions**
- Customize existing dictionaries or contribute new ones
- Production-ready for integration into analyses

## Getting Started 

### Installation

Install the sentibank package:

```
pip install sentibank
```

### Load Dictionaries

Import sentibank and load dictionaries:

```python
from sentibank import archive

load = archive.load()
vader = load.dict("VADER_v2014") 
```

The predefined lexicon identifiers follow the convention {NAME}_{VERSION} - for example, "VADER_v2014". This naming structure indicates the lexicon name and its version for easy recognition and selection. 

See below for the available predefined lexicon identifier.

| Sentiment Dictionary | Description | Genre | Domain | Predefined Identifiers |
|------------------------|---------------|------|-----|------------------------|
|**AFINN** <br> (Nielsen, 2011)| General purpose lexicon with sentiment ratings for common emotion words. |Social Media|General| `AFINN_v2009`, `AFINN_v2011`, `AFINN_v2015` |
|**Aigents+** <br> (Raheman et al., 2022)| Lexicon optimised for social media posts related to cryptocurrencies. |Social Media|Cryptocurrency| `Aigents+_v2022`|
|**General Inquirer** <br> (Stone et al., 1962)| Lexicon capturing broad psycholinguistic dimensions across semantics, values and motivations.  |General|Psychology| `HarvardGI_v2000`|
|**MASTER** <br> (Loughran and McDonland, 2011; Bodnaruk, Loughran and McDonald, 2015)| Financial lexicons covering expressions common in business writing. |Corporate Filings|Finance| `MASTER_v2022`|
|**VADER** <br> (Hutto and Gilbert, 2014)| General purpose lexicon optimised for social media and microblogs. |Social Media|General| `VADER_v2014`|
|**WordNet-Affect** <br> (Strapparava and Valitutti, 2004; Valitutti, Strapparava and Stock, 2004; Strapparava, Valitutti and Stock, 2006)| Hierarchically organised affective labels providing a  granular emotional dimension. |General|Psychology| `WordNet-Affect_v2006`|

Refer [documentation](docs_link) for details on usage.

## Contributing 

We welcome contributions of new expert-curated lexicons. Please refer to [guidelines](https://github.com/socius-org/sentibank/blob/main/CONTRIBUTION.md).
