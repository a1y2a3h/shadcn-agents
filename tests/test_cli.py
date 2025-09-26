import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import sys

# Import CLI functions
sys.path.insert(0, str(Path(__file__).parent.parent))
from shadcn_agent.cli import (
    get_library_dir, 
    validate_workflow_inputs,
    fix_template_imports,
    init_project,
    main
)

class TestCLI:
    """Test cases for CLI functionality"""
    
    def test_get_library_dir_default(self):
        """Test default library directory"""
        result = get_library_dir()
        assert result == Path("components")
    
    def test_get_library_dir_custom(self):
        """Test custom library directory"""
        result = get_library_dir("my_agents")
        assert result == Path("my_agents")
    
    def test_validate_workflow_inputs_summarize(self):
        """Test validation for summarize workflow"""
        errors = validate_workflow_inputs("summarize_and_email_graph", {})
        assert len(errors) == 1
        assert "url" in errors[0].lower() or "URL" in errors[0]
        
        errors = validate_workflow_inputs("summarize_and_email_graph", {"url": "https://example.com"})
        assert len(errors) == 0
    
    def test_validate_workflow_inputs_translate(self):
        """Test validation for translate workflow"""
        errors = validate_workflow_inputs("translate_and_email_graph", {})
        assert len(errors) == 2
        
        errors = validate_workflow_inputs("translate_and_email_graph", {
            "text": "Hello",
            "target_lang": "fr"
        })
        assert len(errors) == 0
    
    def test_fix_template_imports(self):
        """Test import fixing functionality"""
        content = "from ..nodes.search_node import search_node"
        fixed = fix_template_imports(content)
        assert "from components.nodes.search_node import search_node" in fixed
        
        # Test multiple import types
        content = """
from ..nodes.search_node import search_node
from ..workflows.test import test
"""
        fixed = fix_template_imports(content)
        assert "from components.nodes" in fixed
        assert ".." not in fixed or "from .." not in fixed.replace("from components", "")
    
    def test_main_no_args(self):
        """Test main function with no arguments"""
        result = main([])
        assert result == 1  # Should return 1 when no command provided
    
    def test_main_help(self):
        """Test help command"""
        with patch('sys.stdout'):
            try:
                main(["--help"])
            except SystemExit as e:
                # Help command exits with 0
                assert e.code == 0

class TestInitProject:
    """Test project initialization"""
    
    def test_init_project_in_temp_dir(self):
        """Test project initialization in temporary directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Test init with default components folder
                success = init_project()
                assert success is True
                
                # Check if directories were created
                assert Path("components").exists()
                assert Path("components/nodes").exists()
                assert Path("components/workflows").exists()
                assert Path("components/__init__.py").exists()
                assert Path("components/nodes/__init__.py").exists()
                assert Path("components/workflows/__init__.py").exists()
                
            finally:
                # Always restore working directory
                os.chdir(old_cwd)
    
    def test_init_project_custom_dest(self):
        """Test project initialization with custom destination"""
        with tempfile.TemporaryDirectory() as temp_dir:
            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Test init command with custom destination
                result = main(["init", "--dest", "my_agents"])
                assert result == 0
                
                # Check if directories were created
                assert Path("my_agents").exists()
                assert Path("my_agents/nodes").exists()
                assert Path("my_agents/workflows").exists()
                
            finally:
                os.chdir(old_cwd)

class TestAddCommand:
    """Test add command functionality"""
    
    @patch('requests.get')
    def test_add_node_command(self, mock_get):
        """Test adding a node from GitHub"""
        with tempfile.TemporaryDirectory() as temp_dir:
            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Initialize project first
                init_project()
                
                # Mock GitHub response
                mock_response = MagicMock()
                mock_response.text = "def search_node(state):\n    return state"
                mock_response.raise_for_status.return_value = None
                mock_get.return_value = mock_response
                
                # Test add command
                result = main(["add", "node", "search_node"])
                assert result == 0
                
                # Check if file was created
                assert Path("components/nodes/search_node.py").exists()
                
            finally:
                os.chdir(old_cwd)

class TestListCommand:
    """Test list command functionality"""
    
    @patch('requests.get')
    def test_list_command(self, mock_get):
        """Test listing components"""
        # Mock GitHub API responses
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "search_node.py", "type": "file"},
            {"name": "email_node.py", "type": "file"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with tempfile.TemporaryDirectory() as temp_dir:
            old_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Initialize project
                init_project()
                
                # Test list command (should not fail)
                with patch('builtins.print'):
                    result = main(["list"])
                    assert result == 0
                
            finally:
                os.chdir(old_cwd)