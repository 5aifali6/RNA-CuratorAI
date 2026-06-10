import json
import re

with open(
    "outputs/articles.json",
    "r",
    encoding="utf-8"
) as f:

    papers = json.load(f)

rna_pattern = r"(?:hsa-)?(?:miR|miRNA|microRNA)-?\d+[a-zA-Z]*(?:-\d+[a-zA-Z]*)?"

for paper in papers:

    abstract = paper["abstract"]

    rnas = re.findall(
        rna_pattern,
        abstract,
        flags=re.IGNORECASE
    )

    paper["rnas"] = list(set(rnas))

print(papers[0]["rnas"])

print(papers[0])