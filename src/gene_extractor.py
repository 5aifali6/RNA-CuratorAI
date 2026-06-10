import json
import re

with open(
    "outputs/disease_extracted_articles.json",
    "r",
    encoding="utf-8"
) as f:

    papers = json.load(f)

gene_pattern = r"\b[A-Z0-9]{2,10}\b"

for paper in papers:

    abstract = paper["abstract"]

    genes = re.findall(
        gene_pattern,
        abstract
    )

    blacklist = {
        "ASD",
        "RNA",
        "DNA",
        "FDR",
        "PC1",
        "DMFT"
    }

    genes = [
        gene for gene in genes
        if gene not in blacklist
    ]

    paper["genes"] = list(set(genes))

print(papers[0]["genes"][:20])

with open(
    "outputs/gene_extracted_articles.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        papers,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Gene extraction saved.")