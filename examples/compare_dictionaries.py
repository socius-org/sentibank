#!/usr/bin/env python3
"""
Dictionary comparison example for sentibank.

This example demonstrates:
1. Loading multiple dictionaries
2. Comparing sentiment scores across dictionaries
3. Visualizing differences
"""

import matplotlib.pyplot as plt
import pandas as pd
from sentibank import archive
from sentibank.utils import analyze


def main():
    """Main comparison function."""
    print("📊 Sentibank - Dictionary Comparison Example\n")
    
    # Initialize
    loader = archive.load()
    analyzer = analyze()
    
    # Select dictionaries to compare
    dictionaries = [
        "VADER_v2014",
        "AFINN_v2015",
        "SO-CAL_v2011"
    ]
    
    # Test texts
    test_texts = [
        "I absolutely love this amazing product!",
        "This is completely terrible and awful.",
        "It's an okay product, nothing special.",
        "Fantastic quality, highly recommended!",
        "Disappointing and overpriced.",
        "Perfect for my needs, very satisfied.",
        "Waste of money, poor quality.",
        "Good value, decent performance.",
        "Excellent customer service experience.",
        "Frustrating and confusing interface."
    ]
    
    print(f"Comparing {len(dictionaries)} dictionaries on {len(test_texts)} texts:\n")
    
    # Collect results
    results = []
    
    for i, text in enumerate(test_texts, 1):
        print(f"{i:2d}. '{text[:40]}{'...' if len(text) > 40 else ''}'")
        row = {"text": text, "text_id": i}
        
        for dictionary in dictionaries:
            try:
                score = analyzer.sentiment(text=text, dictionary=dictionary)
                row[dictionary] = score
                
                # Determine sentiment category
                if isinstance(score, dict):
                    # For categorical dictionaries, use positive/negative counts
                    pos_score = score.get('Positive', 0) + score.get('positive', 0)
                    neg_score = score.get('Negative', 0) + score.get('negative', 0)
                    net_score = pos_score - neg_score
                    sentiment = "positive" if net_score > 0 else "negative" if net_score < 0 else "neutral"
                    display_score = net_score
                else:
                    # For numeric dictionaries
                    sentiment = "positive" if score > 1 else "negative" if score < -1 else "neutral"
                    display_score = score
                
                print(f"    {dictionary}: {display_score:.2f} ({sentiment})")
                
            except Exception as e:
                print(f"    {dictionary}: Error - {e}")
                row[dictionary] = 0
        
        results.append(row)
        print()
    
    # Create DataFrame for analysis
    df = pd.DataFrame(results)
    
    # Summary statistics
    print("\n📈 Summary Statistics:")
    print("=" * 50)
    
    for dictionary in dictionaries:
        if dictionary in df.columns:
            scores = df[dictionary]
            numeric_scores = pd.to_numeric(scores, errors='coerce').dropna()
            
            if not numeric_scores.empty:
                print(f"\n{dictionary}:")
                print(f"  Mean score: {numeric_scores.mean():.3f}")
                print(f"  Std deviation: {numeric_scores.std():.3f}")
                print(f"  Min score: {numeric_scores.min():.3f}")
                print(f"  Max score: {numeric_scores.max():.3f}")
    
    # Correlation analysis (if possible)
    print("\n🔗 Dictionary Correlations:")
    print("=" * 30)
    
    numeric_df = df[dictionaries].apply(pd.to_numeric, errors='coerce')
    correlation_matrix = numeric_df.corr()
    
    print(correlation_matrix.round(3))
    
    # Optional: Save results to CSV
    output_file = "dictionary_comparison_results.csv"
    df.to_csv(output_file, index=False)
    print(f"\n💾 Results saved to {output_file}")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        if "matplotlib" in str(e):
            print("Note: Install matplotlib for visualization features: pip install matplotlib")
        print("Running without visualization...")
        # Could run a simplified version here