import requests
from bs4 import BeautifulSoup


def scrape_website(url: str) -> str:
    """
    Fetches a webpage and extracts readable text content.

    Args:
        url: The webpage URL to scrape.

    Returns:
        Cleaned webpage text, or an error message if scraping fails.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        for element in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "aside",
            "form",
            "iframe",
        ]):
            element.decompose()

        main_content = (
            soup.find("article")
            or soup.find("main")
            or soup.body
        )

        if not main_content:
            return f"No readable content found at {url}"

        clean_text = main_content.get_text(
            separator=" ",
            strip=True,
        )

        clean_text = " ".join(clean_text.split())

        if not clean_text:
            return f"No readable text found at {url}"

        return clean_text[:10000]

    except requests.exceptions.Timeout:
        return f"Failed to scrape {url}: request timed out."

    except requests.exceptions.RequestException as e:
        return f"Failed to scrape {url}: {str(e)}"

    except Exception as e:
        return f"Failed to process {url}: {str(e)}"
     