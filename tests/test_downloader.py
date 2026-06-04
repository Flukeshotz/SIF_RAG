import pytest
import httpx
from ingestion.downloader import download_file, DownloadError
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_download_success():
    mock_request = httpx.Request("GET", "http://example.com/test.pdf")
    mock_response = httpx.Response(200, content=b"test data", headers={"content-type": "application/pdf"}, request=mock_request)
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        content, ctype = await download_file("http://example.com/test.pdf")
        assert content == b"test data"
        assert ctype == "application/pdf"

@pytest.mark.asyncio
async def test_download_retry_failure():
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = httpx.RequestError("Mock connection error", request=httpx.Request("GET", "http://example.com"))
        
        with pytest.raises(Exception):
            await download_file("http://example.com/test.pdf")
            
        assert mock_get.call_count == 1
