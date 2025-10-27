#!/usr/bin/env python3
"""
Simple test script to verify the MCP server implementation.
This script checks that the server can be imported and that the basic structure is correct.
"""

import sys
import os

# Add the server directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all necessary imports work."""
    print("Testing imports...")
    try:
        import main
        print("✓ Main module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_server_structure():
    """Test that the server has the expected structure."""
    print("\nTesting server structure...")
    try:
        import main

        # Check that server instance exists
        assert hasattr(main, 'server'), "Server instance not found"
        print("✓ Server instance exists")

        # Check that handler functions exist
        assert hasattr(main, 'list_tools'), "list_tools function not found"
        print("✓ list_tools function exists")

        assert hasattr(main, 'call_tool'), "call_tool function not found"
        print("✓ call_tool function exists")

        # Check API configuration
        assert hasattr(main, 'API_KEY'), "API_KEY not found"
        print("✓ API_KEY variable exists")

        assert hasattr(main, 'BASE_URL'), "BASE_URL not found"
        print("✓ BASE_URL variable exists")

        return True
    except AssertionError as e:
        print(f"✗ Structure test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_helper_functions():
    """Test that helper functions exist."""
    print("\nTesting helper functions...")
    try:
        import main

        assert hasattr(main, 'make_api_request'), "make_api_request function not found"
        print("✓ make_api_request function exists")

        assert hasattr(main, 'format_current_weather'), "format_current_weather function not found"
        print("✓ format_current_weather function exists")

        assert hasattr(main, 'format_forecast'), "format_forecast function not found"
        print("✓ format_forecast function exists")

        assert hasattr(main, 'check_rate_limit'), "check_rate_limit function not found"
        print("✓ check_rate_limit function exists")

        return True
    except AssertionError as e:
        print(f"✗ Helper function test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_api_key_handling():
    """Test API key configuration."""
    print("\nTesting API key handling...")
    import main

    if main.API_KEY:
        print(f"✓ API key is configured (length: {len(main.API_KEY)})")
        return True
    else:
        print("⚠ API key is not set (OPENWEATHER_API_KEY environment variable)")
        print("  This is expected if you haven't set it yet.")
        print("  The server will exit with an error when run without it.")
        return True  # Not a failure, just a warning

def main_test():
    """Run all tests."""
    print("=" * 60)
    print("Weather MCP Server - Test Suite")
    print("=" * 60)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("Server Structure", test_server_structure()))
    results.append(("Helper Functions", test_helper_functions()))
    results.append(("API Key", test_api_key_handling()))

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")

    all_passed = all(result for _, result in results)

    print("=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("\nNext steps:")
        print("1. Set your OPENWEATHER_API_KEY environment variable")
        print("2. Run: python main.py")
        print("3. Configure Claude Desktop to use this server")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main_test())
