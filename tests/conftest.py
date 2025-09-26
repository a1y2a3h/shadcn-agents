"""Pytest configuration and fixtures"""
import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Add templates to path for testing
templates_path = project_root / "templates"
if str(templates_path) not in sys.path:
    sys.path.insert(0, str(templates_path))

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            yield Path(temp_dir)
        finally:
            # Always restore the original directory
            os.chdir(old_cwd)

@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables using monkeypatch"""
    env_vars = {
        "SENDER_EMAIL": "test@example.com",
        "SENDER_PASSWORD": "test_password",
        "DEFAULT_RECIPIENT": "recipient@example.com"
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars

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

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Ensure components directory exists for import tests
    components_path = Path("components")
    if not components_path.exists():
        components_path.mkdir(parents=True, exist_ok=True)
        (components_path / "__init__.py").touch()
        (components_path / "nodes").mkdir(exist_ok=True)
        (components_path / "nodes" / "__init__.py").touch()
        (components_path / "workflows").mkdir(exist_ok=True)
        (components_path / "workflows" / "__init__.py").touch()

# Configure pytest to handle import errors gracefully
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "requires_langgraph: marks tests that require langgraph"
    )