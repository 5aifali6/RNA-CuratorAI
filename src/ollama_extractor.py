import json
import ollama
import time

# Load papers
with open(
    "outputs/articles.json",
    "r",
    encoding="utf-8"
) as f:
    papers = json.load(f)

results = []

total_papers = len(papers)

pipeline_start = time.time()

for index, paper in enumerate(papers, start=1):

    paper_start = time.time()

    print(f"\nProcessing paper {index}/{total_papers}")
    print(f"PMID: {paper['pmid']}")

    try:

        prompt = f"""
You are an expert bioinformatics literature curator.

Extract the following information from the scientific abstract.

Return ONLY valid JSON.

Required JSON structure:

{{
    "rnas": [],
    "genes": [],
    "diseases": [],
    "key_finding": ""
}}

Rules:

1. RNAs include:
   - miRNA
   - microRNA
   - lncRNA
   - circRNA
   - snRNA
   - snoRNA
   - piRNA
   - ncRNA

2. Genes should be listed separately.

3. Proteins should be classified as genes if they are gene symbols.

4. Do NOT place genes in the rnas field.

5. Do NOT place proteins in the rnas field.

6. Expand abbreviations where possible.
   Example:
   ASD → Autism Spectrum Disorder

7. Return only entities explicitly mentioned in the text.

8. Return ONLY valid JSON.
   No explanations.
   No markdown.
   No comments.

9. Do not return generic terms such as:
   miRNA
   microRNA
   ncRNA

Only return specific named RNA entities
such as:
   hsa-miR-145-5p
   miR-146a

10. Return every RNA as a plain string.
Never return nested JSON objects.

11. If no specific RNA or gene is mentioned,
return an empty list.

Abstract:

{paper['abstract']}
"""

        response = ollama.chat(
            model="qwen3:8b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        extracted_text = response["message"]["content"]

        try:
            extracted_json = json.loads(extracted_text)

        except Exception:
            extracted_json = {
                "rnas": [],
                "genes": [],
                "diseases": [],
                "key_finding": extracted_text
            }

        results.append(
            {
                "pmid": paper["pmid"],
                "title": paper["title"],
                "rnas": extracted_json.get("rnas", []),
                "genes": extracted_json.get("genes", []),
                "diseases": extracted_json.get("diseases", []),
                "key_finding": extracted_json.get(
                    "key_finding",
                    ""
                )
            }
        )

        paper_time = round(
            time.time() - paper_start,
            2
        )

        print(
            f"Completed paper {index}/{total_papers} "
            f"in {paper_time} seconds"
        )

    except Exception as e:

        print(f"Failed paper {paper['pmid']}: {e}")

        results.append(
            {
                "pmid": paper["pmid"],
                "title": paper["title"],
                "rnas": [],
                "genes": [],
                "diseases": [],
                "key_finding": "",
                "error": str(e)
            }
        )

# Save output
with open(
    "outputs/llm_extracted_articles.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )

total_time = round(
    time.time() - pipeline_start,
    2
)

avg_time = round(
    total_time / total_papers,
    2
)

print("\nExtraction complete.")
print("Saved to outputs/llm_extracted_articles.json")
print(f"Total time: {total_time} seconds")
print(f"Average time per paper: {avg_time} seconds")