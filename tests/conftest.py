# ===== tests/conftest.py =====
"""Pytest configuration and fixtures"""
import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd = os.getcwd()
        os.chdir(temp_dir)
        yield Path(temp_dir)
        os.chdir(old_cwd)

@pytest.fixture
def mock_env():
    """Mock environment variables"""
    return {
        "SENDER_EMAIL": "test@example.com",
        "SENDER_PASSWORD": "test_password",
        "DEFAULT_RECIPIENT": "recipient@example.com"
    }

@pytest.fixture
def sample_html():
    """Sample HTML content for testing"""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Heading</h1>
            <p>This is the first paragraph with important content.</p>
            <p>This is the second paragraph with more information.</p>
            <script>console.log('should be removed');</script>
            <style>body { color: red; }</style>
        </body>
    </html>
    """