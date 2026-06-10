import json

disease_terms = [
    "autism",
    "autism spectrum disorder",
    "ASD",
    "cancer",
    "diabetes",
    "Alzheimer",
    "Parkinson"
]

with open(
    "outputs/rna_extracted_articles.json",
    "r",
    encoding="utf-8"
) as f:

    papers = json.load(f)

for paper in papers:

    abstract = paper["abstract"].lower()

    diseases = []

    for disease in disease_terms:

        if disease.lower() in abstract:
            diseases.append(disease)

    paper["diseases"] = list(set(diseases))

print(papers[0]["diseases"])

with open(
    "outputs/disease_extracted_articles.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        papers,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Disease extraction saved.")