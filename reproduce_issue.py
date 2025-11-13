# reproduce_issue.py
import sys
import os
import json

# Add the current directory to Python path so we can import the package
sys.path.insert(0, os.path.abspath('.'))

# Try to import the config module
try:
    from json_config import Config
    print("✓ Successfully imported Config")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("Make sure you're in the project root directory")
    sys.exit(1)

def test_upsert_issue():
    """Test the specific issue: upserting to new nested paths"""
    print("\n" + "="*60)
    print("TESTING UPSERT ISSUE: Adding value to new nested path")
    print("="*60)
    
    # Test Case 1: Simple new nested path
    print("\n1. Testing: config.set('foo.bar', 'x') where 'foo' doesn't exist")
    print("-" * 50)
    
    config = Config({})  # Start with empty config
    print(f"Initial config: {config.data}")
    
    try:
        # This should fail with the current implementation
        config.set('foo.bar', 'x')
        print("✓ SUCCESS - Value was set without error")
        print(f"Result config: {config.data}")
        print(f"Expected: {{'foo': {{'bar': 'x'}}}}")
        print(f"Actual:   {config.data}")
        
        if config.data.get('foo', {}).get('bar') == 'x':
            print("🎉 ISSUE IS ALREADY FIXED!")
        else:
            print("❌ Value was not set correctly")
            
    except Exception as e:
        print(f"✗ ERROR (This demonstrates the issue): {type(e).__name__}: {e}")
        print("This is the bug we need to fix!")
    
    # Test Case 2: More complex nested path
    print("\n2. Testing: config.set('a.b.c.d', 'value') with empty config")
    print("-" * 50)
    
    config2 = Config({})
    print(f"Initial config: {config2.data}")
    
    try:
        config2.set('a.b.c.d', 'deep_value')
        print("✓ SUCCESS - Deep nested value was set")
        print(f"Result config: {config2.data}")
    except Exception as e:
        print(f"✗ ERROR: {type(e).__name__}: {e}")
    
    # Test Case 3: Mixed existing and new paths
    print("\n3. Testing: Mixed existing and new paths")
    print("-" * 50)
    
    config3 = Config({
        'existing': {
            'old_field': 'old_value'
        }
    })
    print(f"Initial config: {config3.data}")
    
    try:
        # This might work (adding to existing parent)
        config3.set('existing.new_field', 'new_value')
        print("✓ SUCCESS - Added to existing parent")
        print(f"After first set: {config3.data}")
        
        # This should fail (creating new parent)
        config3.set('completely.new.path', 'another_value')
        print("✓ SUCCESS - Created new nested path")
        print(f"Final config: {config3.data}")
        
    except Exception as e:
        print(f"✗ ERROR: {type(e).__name__}: {e}")

def test_current_behavior_detailed():
    """More detailed analysis of what's happening"""
    print("\n" + "="*60)
    print("DETAILED BEHAVIOR ANALYSIS")
    print("="*60)
    
    config = Config({})
    print(f"Starting with empty config: {config.data}")
    
    # Let's see what methods are available
    print(f"\nAvailable methods: {[m for m in dir(config) if not m.startswith('_')]}")
    
    # Test if basic set works
    print("\nTesting basic set operation:")
    try:
        config.set('simple_key', 'simple_value')
        print(f"✓ Basic set works: config.data = {config.data}")
    except Exception as e:
        print(f"✗ Basic set failed: {e}")
    
    # Now test the problematic case
    print("\nTesting the problematic nested set:")
    try:
        config.set('parent.child', 'nested_value')
        print(f"✓ Nested set worked: config.data = {config.data}")
    except Exception as e:
        print(f"✗ Nested set failed: {e}")
        print("\nThis confirms the issue exists!")

if __name__ == "__main__":
    test_upsert_issue()
    test_current_behavior_detailed()
