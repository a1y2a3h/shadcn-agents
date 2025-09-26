# ===== tests/test_cli.py =====
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open
from shadcn_agent.cli import (
    get_library_dir, 
    validate_workflow_inputs,
    fix_template_imports,
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
        assert "requires --url" in errors[0]
        
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
    
    def test_main_no_args(self):
        """Test main function with no arguments"""
        result = main([])
        assert result == 1  # Should return 1 when no command provided

class TestInitProject:
    """Test project initialization"""
    
    def test_init_project(self):
        """Test project initialization in temporary directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            
            # Test init command
            result = main(["init", "--dest", "test_components"])
            assert result == 0
            
            # Check if directories were created
            assert Path("test_components").exists()
            assert Path("test_components/nodes").exists()
            assert Path("test_components/workflows").exists()
            assert Path("test_components/__init__.py").exists()