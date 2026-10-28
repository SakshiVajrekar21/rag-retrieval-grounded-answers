
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import date

# Folder where the text files will be saved
OUTPUT_DIR = Path("data/documents")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Web articles to collect
articles = [
    {
        "filename": "02_nhs_mindfulness.txt",
        "title": "Mindfulness",
        "url": "https://www.nhs.uk/mental-health/self-help/tips-and-support/mindfulness/",
    },
    {
        "filename": "03_nccih_evidence.txt",
        "title": "Meditation and Mindfulness: Effectiveness and Safety",
        "url": "https://www.nccih.nih.gov/health/meditation-and-mindfulness-effectiveness-and-safety",
    },
    {
        "filename": "04_who_stress.txt",
        "title": "Stress",
        "url": "https://www.who.int/news-room/questions-and-answers/item/stress",
    },
    {
        "filename": "05_mindfulness_guide.txt",
        "title": "What is Mindfulness? - NHS Every Mind Matters",
        "url": "https://www.nhs.uk/every-mind-matters/mental-wellbeing-tips/what-is-mindfulness/",
    },
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

for article in articles:
    try:
        print(f"Downloading: {article['title']}")

        response = requests.get(
            article["url"],
            headers=headers,
            timeout=20
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove menus and other unnecessary webpage elements
        for element in soup.select(
            "nav, header, footer, script, style, "
            "aside, form, noscript"
        ):
            element.decompose()

        # Find the main article content
        content = (
            soup.find("article")
            or soup.find("main")
            or soup.body
            or soup
        )

        text = content.get_text("\n", strip=True)

        # Save the article with its source details
        file_content = (
            f"TITLE: {article['title']}\n"
            f"SOURCE: {article['url']}\n"
            f"ACCESS DATE: {date.today().isoformat()}\n\n"
            f"ARTICLE CONTENT:\n\n{text}\n"
        )

        output_file = OUTPUT_DIR / article["filename"]
        output_file.write_text(file_content, encoding="utf-8")

        print(f"Saved: {output_file}")

    except requests.RequestException as error:
        print(f"Could not download {article['title']}: {error}")

print("\nFinished. Check data/documents for the saved files.")
