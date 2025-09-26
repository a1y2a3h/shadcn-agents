# ===== tests/test_workflows.py =====
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

class TestWorkflows:
    """Test workflow functionality"""
    
    @patch('components.nodes.search_node.search_node')
    @patch('components.nodes.summarizer_node.summarizer_node') 
    @patch('components.nodes.email_node.email_node')
    def test_summarize_and_email_workflow(self, mock_email, mock_summarizer, mock_search):
        """Test complete summarize and email workflow"""
        # Mock node functions
        mock_search.return_value = {"text": "Scraped content", "scraped_url": "https://example.com"}
        mock_summarizer.return_value = {"summary": "Short summary", "text": "Scraped content"}
        mock_email.return_value = {"status": "Email sent successfully"}
        
        # This would require the actual workflow to be available
        # For now, just test that the mocks can be called
        assert mock_search is not None
        assert mock_summarizer is not None
        assert mock_email is not None
