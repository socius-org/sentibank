#!/usr/bin/env python3
"""
Basic usage example for sentibank.

This example demonstrates:
1. Loading a sentiment dictionary
2. Analyzing text sentiment
3. Working with dictionary information
"""

from sentibank import archive
from sentibank.utils import analyze


def main():
    """Main example function."""
    print("🏦 Sentibank - Basic Usage Example\n")
    
    # Initialize loader and analyzer
    loader = archive.load()
    analyzer = analyze()
    
    # 1. List available dictionaries
    print("1. Available dictionaries:")
    available = loader.list_available()
    for i, dictionary in enumerate(available['dictionaries'][:5], 1):
        print(f"   {i}. {dictionary}")
    print(f"   ... and {len(available['dictionaries']) - 5} more\n")
    
    # 2. Load a dictionary
    print("2. Loading VADER dictionary...")
    try:
        vader_dict = loader.dict("VADER_v2014")
        print(f"   ✓ Loaded {len(vader_dict)} terms")
        
        # Show some examples
        print("   Sample terms and scores:")
        sample_terms = list(vader_dict.items())[:5]
        for term, score in sample_terms:
            print(f"     '{term}': {score}")
        print()
    except Exception as e:
        print(f"   ✗ Error loading dictionary: {e}\n")
        return
    
    # 3. Analyze sentiment
    print("3. Sentiment analysis examples:")
    
    test_texts = [
        "I love this product! It's absolutely amazing!",
        "This is terrible and disappointing.",
        "It's okay, nothing special.",
        "Best purchase ever! Highly recommend!",
        "Worst experience of my life."
    ]
    
    for text in test_texts:
        try:
            result = analyzer.sentiment(text=text, dictionary="VADER_v2014")
            sentiment = "positive" if result > 1 else "negative" if result < -1 else "neutral"
            print(f"   Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            print(f"   Score: {result:.2f} ({sentiment})\n")
        except Exception as e:
            print(f"   ✗ Error analyzing text: {e}\n")
    
    # 4. Dictionary information
    print("4. Dictionary information:")
    try:
        print("   VADER_v2014 statistics:")
        analyzer.dictionary(dictionary="VADER_v2014")
    except Exception as e:
        print(f"   ✗ Error getting dictionary info: {e}")


if __name__ == "__main__":
    main()