# About

sentibank is an open database of expert-curated sentiment dictionaries and lexicons, distributed as a Python package. It consolidates 15 original sentiment dictionaries and 43 preprocessed dictionaries, spanning 7 genres and 6 domains, behind a single loading interface. The resource is described in [Oh (2024)](https://doi.org/10.1609/icwsm.v18i1.31443), published at ICWSM 2024.

## Overview

### Sentiment analysis

Sentiment analysis is the automated process of identifying and extracting subjective information such as opinions, emotions, and attitudes from textual data. It has become an increasingly important technique across many social science domains such as business, politics, and economics.

While deep learning models have achieved high accuracy, often surpassing simpler lexicon models in sentiment analysis tasks (Al-Qablan et al. 2023), their opaque nature poses challenges for applications in high-stakes domains such as government policy making or mental health diagnosis, where transparent and interpretable decision-making is essential (Rudin 2019). Rule-based sentiment analysis therefore remains important, particularly in computational social science, and improving it remains worthwhile.

### sentibank

Rule-based sentiment analysis relies on expert-curated lexicons containing words with pre-assigned sentiment scores, because human expertise is required to annotate the sentiment of words across contexts. Applying these lexicons in practice faces several challenges:

- **Fragmented resources** that require laborious integration
- **A lack of verified, high-quality lexicons** spanning domains
- **Inaccessibility** that limits transparency and further development

By consolidating lexicons into an open and public resource, sentibank gives users access to a large body of sentiment knowledge through one interface. Its main capabilities are:

- **15 sentiment dictionaries** (and counting) spanning domains and use cases
- Dictionaries curated by **leading experts** in sentiment analysis
- Access to both the **original lexicons** and**preprocessed versions**
- The ability to customise existing dictionaries or contribute new ones
- A tested package ready for integration into analyses

## Navigating the documentation

This documentation provides researchers, data scientists and developers with both conceptual and practical guidance for using sentibank. The main sections are:

- **[Getting Started](getting_started/installation.ipynb)**: installation, loading dictionaries, and analysing dictionaries and text
- **[Archive](archive/intro.md)**: a page for each included lexicon, covering its composition, methodology, evaluation and usage
- **[Contributions](Contributions.md)**: how to contribute new lexicons or request changes

sentibank is developed at [socius](https://socius.org). The source code is on [GitHub](https://github.com/socius-org/sentibank) and releases are published on [PyPI](https://pypi.org/project/sentibank/).
