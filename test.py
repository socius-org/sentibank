# test_sentibank.py
print("Testing sentibank installation...")

try:
    from sentibank import archive
    print("[OK] Successfully imported archive")
    
    from sentibank.utils import analyze
    print("[OK] Successfully imported analyze")
    
    analyzer = analyze()
    print("[OK] Successfully created analyzer instance")
    
    analyzer.dictionary(dictionary="VADER_v2014")
    print("[OK] Successfully loaded VADER_v2014 dictionary")
    
    # Optional: test with a sample text
    # result = analyzer.score("This is a great test!")
    # print(f"[OK] Sample analysis result: {result}")
    
    print("\n[SUCCESS] All tests passed! Package is working correctly.")
    
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
except Exception as e:
    print(f"[ERROR] Error during testing: {e}")
    import traceback
    traceback.print_exc()