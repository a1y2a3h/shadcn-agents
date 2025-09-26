import os
import pytest
from unittest.mock import patch, MagicMock, Mock
import sys
from pathlib import Path

# Add both templates and project root to path
project_root = Path(__file__).parent.parent
templates_path = project_root / "templates"
sys.path.insert(0, str(project_root))
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
        
        # Import directly from templates
        from templates.nodes.search_node import search_node
        
        state = {"url": "https://example.com"}
        result = search_node(state)
        
        assert "text" in result
        assert "Test Content" in result["text"]
        assert result["scraped_url"] == "https://example.com"
    
    def test_search_node_no_url(self):
        """Test search node with no URL"""
        from templates.nodes.search_node import search_node
        
        state = {}
        result = search_node(state)
        
        assert "error" in result
        assert "No URL provided" in result["text"]

class TestSummarizerNode:
    """Test summarizer node functionality"""
    
    def test_summarizer_node_success(self):
        """Test successful text summarization"""
        from templates.nodes.summarizer_node import summarizer_node
        
        long_text = " ".join(["This is a test sentence."] * 20)
        state = {"text": long_text}
        result = summarizer_node(state)
        
        assert "summary" in result
        assert len(result["summary"]) < len(long_text)
        assert result["original_word_count"] > 0
        assert result["summary_word_count"] > 0
    
    def test_summarizer_node_no_text(self):
        """Test summarizer with no text"""
        from templates.nodes.summarizer_node import summarizer_node
        
        state = {}
        result = summarizer_node(state)
        
        assert result["summary"] == "No content to summarize"
        assert result["summary_method"] == "none"

class TestTranslateNode:
    """Test translate node functionality"""
    
    def test_translate_node_with_mock(self):
        """Test translation with mocked translator"""
        # Mock at the module level before import
        mock_translator_class = MagicMock()
        mock_translator = MagicMock()
        mock_translator.translate.return_value = "Bonjour le monde"
        mock_translator_class.return_value = mock_translator
        
        with patch.dict('sys.modules', {'deep_translator': MagicMock(GoogleTranslator=mock_translator_class)}):
            from templates.nodes.translate_node import translate_node
            
            state = {"text": "Hello world", "target_lang": "fr"}
            result = translate_node(state)
            
            assert "translation" in result
            assert result["target_language"] == "fr"
    
    def test_translate_node_no_text(self):
        """Test translate node with no text"""
        # Use fallback implementation when deep_translator is not available
        try:
            from templates.nodes.translate_node import translate_node
        except ImportError:
            # If import fails, that's ok for CI
            pytest.skip("deep_translator not available")
        
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
    def test_email_node_success_tls(self, mock_smtp_class):
        """Test successful email sending with TLS"""
        # Create mock SMTP instance
        mock_server = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_server
        
        from templates.nodes.email_node import email_node
        
        state = {
            "body": "Test email content",
            "recipient": "recipient@example.com"
        }
        result = email_node(state)
        
        assert result["status"] == "Email sent successfully"
        assert result["recipient"] == "recipient@example.com"
        assert mock_server.starttls.called
        assert mock_server.send_message.called
    
    @patch.dict(os.environ, {}, clear=True)
    def test_email_node_no_credentials(self):
        """Test email node without credentials"""
        from templates.nodes.email_node import email_node
        
        state = {"body": "Test content"}
        result = email_node(state)
        
        assert "no credentials configured" in result["status"]
    
    @patch.dict(os.environ, {
        "SENDER_EMAIL": "test@example.com",
        "SENDER_PASSWORD": "test_password"
    })
    def test_email_node_invalid_recipient(self):
        """Test email node with invalid recipient"""
        from templates.nodes.email_node import email_node
        
        state = {
            "body": "Test content",
            "recipient": "not-an-email"
        }
        result = email_node(state)
        
        assert "Email failed" in result["status"]
        assert "Invalid recipient email" in result["error"]