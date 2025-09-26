# ===== tests/test_nodes.py =====
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add templates to path for testing
templates_path = Path(__file__).parent.parent / "templates"
if str(templates_path) not in sys.path:
    sys.path.insert(0, str(templates_path))

class TestSearchNode:
    """Test search node functionality"""
    
    @patch('requests.get')
    def test_search_node_success(self, mock_get):
        """Test successful web scraping"""
        # Mock response
        mock_response = MagicMock()
        mock_response.content = b"<html><body><h1>Test Content</h1><p>This is test content for scraping.</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Import and test node
        from nodes.search_node import search_node
        
        state = {"url": "https://example.com"}
        result = search_node(state)
        
        assert result["scrape_success"] is True
        assert "Test Content" in result["text"]
        assert result["scraped_url"] == "https://example.com"
    
    def test_search_node_no_url(self):
        """Test search node with no URL"""
        from nodes.search_node import search_node
        
        state = {}
        result = search_node(state)
        
        assert "error" in result
        assert "No URL provided" in result["text"]

class TestSummarizerNode:
    """Test summarizer node functionality"""
    
    def test_summarizer_node_success(self):
        """Test successful text summarization"""
        from nodes.summarizer_node import summarizer_node
        
        long_text = " ".join(["This is a test sentence."] * 20)
        state = {"text": long_text}
        result = summarizer_node(state)
        
        assert "summary" in result
        assert len(result["summary"]) < len(long_text)
        assert result["original_word_count"] > 0
        assert result["summary_word_count"] > 0
    
    def test_summarizer_node_no_text(self):
        """Test summarizer with no text"""
        from nodes.summarizer_node import summarizer_node
        
        state = {}
        result = summarizer_node(state)
        
        assert result["summary"] == "No content to summarize"
        assert result["summary_method"] == "none"

class TestTranslateNode:
    """Test translate node functionality"""
    
    @patch('nodes.translate_node.GoogleTranslator')
    def test_translate_node_success(self, mock_translator_class):
        """Test successful translation"""
        # Mock translator
        mock_translator = MagicMock()
        mock_translator.translate.return_value = "Bonjour le monde"
        mock_translator_class.return_value = mock_translator
        
        from nodes.translate_node import translate_node
        
        state = {"text": "Hello world", "target_lang": "fr"}
        result = translate_node(state)
        
        assert result["translation"] == "Bonjour le monde"
        assert result["target_language"] == "fr"
        assert result["translation_status"] == "success"
    
    def test_translate_node_no_text(self):
        """Test translate node with no text"""
        from nodes.translate_node import translate_node
        
        state = {"target_lang": "fr"}
        result = translate_node(state)
        
        assert result["translation"] == ""
        assert result["translation_status"] == "no_input"

class TestEmailNode:
    """Test email node functionality"""
    
    @patch.dict(os.environ, {
        "SENDER_EMAIL": "test@example.com",
        "SENDER_PASSWORD": "test_password"
    })
    @patch('smtplib.SMTP')
    def test_email_node_success(self, mock_smtp):
        """Test successful email sending"""
        from nodes.email_node import email_node
        
        # Mock SMTP
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        state = {
            "body": "Test email content",
            "recipient": "recipient@example.com"
        }
        result = email_node(state)
        
        assert result["status"] == "Email sent successfully"
        assert result["recipient"] == "recipient@example.com"
    
    def test_email_node_no_credentials(self):
        """Test email node without credentials"""
        with patch.dict(os.environ, {}, clear=True):
            from nodes.email_node import email_node
            
            state = {"body": "Test content"}
            result = email_node(state)
            
            assert "no credentials configured" in result["status"]