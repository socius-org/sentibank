# sentibank
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?label=license)](https://opensource.org/licenses/MIT)
[![Github Stars](https://img.shields.io/github/stars/socius-org/sentibank?logo=github)](https://github.com/socius-org/sentibank)
[![Github Watchers](https://img.shields.io/github/watchers/socius-org/sentibank?style=flat&logo=github)](https://github.com/socius-org/sentibank)

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

|Sentiment Dictionary| Description | Predefined Identifiers |
|------------------------|---------------|------------------------|
|AFINN (Nielsen, 2011)| General purpose lexicon with sentiment ratings for common emotion words. | `AFINN_v2009`, `AFINN_v2011`, `AFINN_v2015` |
|Aigents+ (Raheman et al., 2022)| Lexicon optimised for social media posts related to cryptocurrencies. | `Aigents+_v2022`|
|General Inquirer (Stone et al., 1962)| Lexicon capturing broad psycholinguistic dimensions across semantics, values and motivations.  | `HarvardGI_v2000`|
|MASTER (Loughran and McDonland, 2011)| Financial lexicons covering expressions common in business writing. | `MASTER_v2022`|
|VADER (Hutto and Gilbert, 2014)| General purpose lexicon optimised for social media and microblogs. | `VADER_v2014`|
|WordNet-Affect (Strapparava and Valitutti, 2004)| Hierarchically organised affective labels providing a  granular emotional dimension. | `WordNet-Affect_v2006`|

Refer [documentation](docs_link) for details on usage.

## Contributing 

We welcome contributions of new expert-curated lexicons. Please refer to [guidelines](https://github.com/socius-org/sentibank/blob/main/CONTRIBUTION.md).
