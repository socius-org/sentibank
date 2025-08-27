# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sentibank is a Python package that provides a comprehensive database of expert-curated sentiment dictionaries and lexicons for sentiment analysis. It consolidates 15+ sentiment dictionaries spanning various domains (general, finance, social media, psychology, politics) into an integrated, open-source resource.

## Key Commands

### Development Setup
```bash
# Install the package in development mode
pip install -e ".[dev]"

# Install dependencies
pip install -r requirements.txt
pip install -r test_requirements.txt

# Run tests with coverage
pytest tests/ --cov=sentibank --cov-report=html

# Run legacy basic test
python test.py

# Lint and format code
black sentibank/
isort sentibank/
flake8 sentibank/
mypy sentibank/

# Build distribution (modern)
python -m build

# Build distribution (legacy)
python setup.py sdist bdist_wheel
```

### Package Installation (for users)
```bash
pip install sentibank
```

### CLI Usage
```bash
# List available dictionaries
sentibank list

# Analyze sentiment
sentibank analyze VADER_v2014 "I love this product!"

# Get dictionary info
sentibank info VADER_v2014

# Export dictionary
sentibank export VADER_v2014 --format json
```

## Architecture

### Core Components

**sentibank/archive.py** - Main data loading interface
- `load` class provides methods to:
  - `dict(idx)` - Load preprocessed sentiment dictionaries 
  - `origin(idx)` - Load original raw datasets
  - `json_dict(idx)` - Load JSON format dictionaries

**sentibank/utils.py** - Analysis utilities  
- `analysis` class for sentiment analysis operations
- `analyze()` provides:
  - `dictionary(dictionary)` - Analyze dictionary structure/stats
  - `sentiment(text, dictionary)` - Perform sentiment analysis on text

**sentibank/validate.py** - Dictionary validation functionality

**sentibank/dict_arXiv/** - Pre-processed sentiment dictionaries storage
- Each dictionary stored in multiple formats: CSV (original), JSON, Pickle
- Organized by dictionary name in subdirectories

### Dictionary Loading System

The package uses a path-based mapping system to load dictionaries. Each dictionary identifier maps to a specific subdirectory containing preprocessed versions. Dictionary identifiers follow patterns:
- `{NAME}_{VERSION}` - Base processed version
- `{NAME}_{VERSION}_{refinement}` - With additional transformations (e.g., "_boosted", "_norm", "_simple")

### Sentiment Analysis Approach

The package implements bag-of-words sentiment analysis:
- Score-based dictionaries: Returns sum of matched term scores (float/int)
- Label-based dictionaries: Returns dictionary with counts per sentiment category

## Development Notes

### Dependencies
- spacy==3.7.2 (with en_core_web_sm model)
- spacymoji==3.1.0 (emoji detection)
- pandas==2.1.4
- pyenchant==3.2.2 (spell checking)
- rich==13.4.2 (CLI display)

The package auto-downloads the spacy en_core_web_sm model if not present.

### Adding New Dictionaries

New sentiment dictionaries should:
1. Be placed in `sentibank/dict_arXiv/{DictionaryName}/`
2. Include CSV original, JSON, and Pickle formats
3. Add mapping in `archive.py` lexicon_paths dictionary
4. Follow naming convention: `{Name}_v{Year}` or with refinement suffix

### Testing

Run `python test.py` to verify:
- Package imports correctly
- Dictionary loading works
- Analyzer initializes properly

## Repository Structure

```
sentibank/
├── sentibank/           # Main package
│   ├── __init__.py
│   ├── archive.py       # Dictionary loading
│   ├── utils.py         # Analysis utilities  
│   ├── validate.py      # Validation functions
│   └── dict_arXiv/      # Dictionary data storage
├── docs/                # Documentation (Jupyter Book)
├── setup.py            # Package configuration
├── requirements.txt    # Dependencies
└── test.py            # Basic functionality tests
```