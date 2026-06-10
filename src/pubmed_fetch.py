from Bio import Entrez
import json

Entrez.email = "YOUR_EMAIL_HERE"

SEARCH_TERM = "microRNA autism"
MAX_RESULTS = 10

handle = Entrez.esearch(
    db="pubmed",
    term=SEARCH_TERM,
    retmax=MAX_RESULTS
)

record = Entrez.read(handle)
pmids = record["IdList"]

papers = []

for pmid in pmids:

    fetch_handle = Entrez.efetch(
        db="pubmed",
        id=pmid,
        rettype="abstract",
        retmode="xml"
    )

    article_data = Entrez.read(fetch_handle)

    article = article_data["PubmedArticle"][0]

    title = article["MedlineCitation"]["Article"]["ArticleTitle"]

    abstract = ""

    if "Abstract" in article["MedlineCitation"]["Article"]:
        abstract_sections = article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]

        abstract = " ".join(str(x) for x in abstract_sections)

    papers.append(
        {
            "pmid": pmid,
            "title": str(title),
            "abstract": abstract
        }
    )

print(f"Retrieved {len(papers)} papers")

with open(
    "outputs/articles.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        papers,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Saved to outputs/articles.json")