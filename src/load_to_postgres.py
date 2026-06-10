import json
import psycopg2

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="rna_curator_ai",
    user="postgres",
    password="hamlog512"
)

cursor = conn.cursor()

# Load extracted data
with open(
    "outputs/llm_extracted_articles.json",
    "r",
    encoding="utf-8"
) as f:
    papers = json.load(f)

for paper in papers:

    pmid = int(paper["pmid"])

    cursor.execute(
        """
        INSERT INTO papers
        (pmid, title, key_finding)
        VALUES (%s, %s, %s)
        ON CONFLICT (pmid) DO NOTHING
        """,
        (
            pmid,
            paper["title"],
            paper["key_finding"]
        )
    )

    for rna in paper["rnas"]:

        cursor.execute(
            """
            INSERT INTO rnas
            (pmid, rna_name)
            VALUES (%s, %s)
            """,
            (
                pmid,
                rna
            )
        )

    for gene in paper["genes"]:

        cursor.execute(
            """
            INSERT INTO genes
            (pmid, gene_name)
            VALUES (%s, %s)
            """,
            (
                pmid,
                gene
            )
        )

    for disease in paper["diseases"]:

        cursor.execute(
            """
            INSERT INTO diseases
            (pmid, disease_name)
            VALUES (%s, %s)
            """,
            (
                pmid,
                disease
            )
        )

conn.commit()

cursor.close()
conn.close()

print("Data loaded successfully.")