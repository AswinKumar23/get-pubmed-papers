import requests
import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Any


def search_pubmed(query: str, max_results: int = 20) -> List[str]:
    """
    Search PubMed for article IDs using a query.

    Args:
        query (str): PubMed search query.
        max_results (int): Maximum number of results to fetch.

    Returns:
        List[str]: List of PubMed article IDs.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retmax": max_results
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching PubMed search results: {e}")

    root = ET.fromstring(response.content)
    return [id_elem.text for id_elem in root.findall(".//Id")]


def fetch_pubmed_articles(ids: List[str]) -> bytes:
    """
    Fetch full article metadata from PubMed for given IDs.

    Args:
        ids (List[str]): List of PubMed IDs.

    Returns:
        bytes: Raw XML data from PubMed.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching PubMed articles: {e}")


def has_company_affiliation(affiliation: str) -> bool:
    """
    Determine if an affiliation string belongs to a company rather than an academic institution.

    Args:
        affiliation (str): Affiliation text.

    Returns:
        bool: True if it appears to be company-affiliated.
    """
    if not affiliation:
        return False
    keywords = ["Inc", "Ltd", "Corporation", "Pharma", "Biotech", "LLC"]
    excluded = ["University", "Hospital", "School", "Institute"]
    return any(k in affiliation for k in keywords) and not any(e in affiliation for e in excluded)


def parse_articles(xml_data: bytes) -> List[Dict[str, Any]]:
    """
    Parse XML data to extract articles with company-affiliated authors.

    Args:
        xml_data (bytes): XML response from PubMed API.

    Returns:
        List[Dict[str, Any]]: List of filtered article metadata.
    """
    results = []
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        raise RuntimeError("Error parsing XML data from PubMed")

    for article in root.findall(".//PubmedArticle"):
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "No Title"

        pmid_elem = article.find(".//PMID")
        pmid = pmid_elem.text if pmid_elem is not None else "N/A"

        date_elem = article.find(".//PubDate")
        pub_date = "Unknown"
        if date_elem is not None:
            year = date_elem.find("Year")
            medline_date = date_elem.find("MedlineDate")
            pub_date = year.text if year is not None else (medline_date.text if medline_date is not None else "Unknown")

        authors = article.findall(".//Author")
        company_authors = []

        for author in authors:
            affil_elem = author.find(".//AffiliationInfo/Affiliation")
            if affil_elem is not None and has_company_affiliation(affil_elem.text):
                last = author.find("LastName")
                first = author.find("ForeName")
                full_name = (first.text + " " if first is not None else "") + (last.text if last is not None else "")
                affiliation_text = affil_elem.text

                # Extract email from affiliation string
                email_match = re.search(r'[\w\.-]+@[\w\.-]+', affiliation_text)
                email = email_match.group(0) if email_match else "N/A"

                company_authors.append((full_name, affiliation_text, email))

        if company_authors:
            results.append({
                "pmid": pmid,
                "title": title,
                "date": pub_date,
                "authors": [a[0] for a in company_authors],
                "affiliations": [a[1] for a in company_authors],
                "emails": [a[2] for a in company_authors]
            })

    return results
