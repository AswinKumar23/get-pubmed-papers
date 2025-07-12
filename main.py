import argparse
import csv
from typing import List, Dict, Any
from get_papers.fetcher import search_pubmed, fetch_pubmed_articles, parse_articles


def save_to_csv(data: List[Dict[str, Any]], filename: str) -> None:
    """
    Save parsed article data to a CSV file.

    Args:
        data: List of article dictionaries.
        filename: Name of the output CSV file.
    """
    with open(filename, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "PubmedID",
            "Title",
            "Publication Date",
            "Non-academic Author(s)",
            "Company Affiliation(s)",
            "Corresponding Author Email(s)"
        ])
        for item in data:
            writer.writerow([
                item["pmid"],
                item["title"],
                item["date"],
                "; ".join(item["authors"]),
                "; ".join(item["affiliations"]),
                "; ".join(item["emails"])
            ])


def print_to_console(data: List[Dict[str, Any]]) -> None:
    """
    Print article data to the console in a formatted way.

    Args:
        data: List of article dictionaries.
    """
    for item in data:
        print("--------------------------------------------------")
        print(f"📘 Pubmed ID      : {item['pmid']}")
        print(f"📄 Title          : {item['title']}")
        print(f"📅 Date           : {item['date']}")
        print(f"👤 Author(s)      : {', '.join(item['authors'])}")
        print(f"🏢 Affiliation(s) : {', '.join(item['affiliations'])}")
        print(f"📧 Email(s)       : {', '.join(item['emails'])}")
    print("--------------------------------------------------")


def main() -> None:
    """
    Command-line interface entry point for fetching PubMed papers.
    """
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with company-affiliated authors.")
    parser.add_argument("--query", required=True, help="PubMed search query")
    parser.add_argument("-f", "--file", help="Output CSV filename. If not set, prints to console.")
    parser.add_argument("--max", type=int, default=20, help="Maximum number of results to fetch")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        print(f"🔍 Searching for: {args.query}")
        print(f"📦 Max results: {args.max}")
        print("⏳ Fetching article IDs...")

    try:
        ids = search_pubmed(args.query, args.max)
        if not ids:
            print("❌ No articles found for the given query.")
            return
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return

    if args.debug:
        print(f"✅ Found {len(ids)} articles")
        print("⏳ Fetching article metadata...")

    try:
        xml_data = fetch_pubmed_articles(ids)
        results = parse_articles(xml_data)
    except Exception as e:
        print(f"❌ Error fetching/parsing articles: {e}")
        return

    if args.debug:
        print(f"✅ {len(results)} articles with company authors found.")

    if not results:
        print("⚠️ No company-affiliated authors found in the articles.")
        return

    if args.file:
        save_to_csv(results, args.file)
        print(f"\n✅ Saved {len(results)} results to '{args.file}'")
    else:
        print_to_console(results)


if __name__ == "__main__":
    main()
