import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(
    page_title="RNA-CuratorAI",
    page_icon="🧬",
    layout="wide"
)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)


def get_paper_details(pmid):

    paper = pd.read_sql(
        f"""
        SELECT *
        FROM papers
        WHERE pmid = {pmid}
        """,
        conn
    )

    rnas = pd.read_sql(
        f"""
        SELECT rna_name
        FROM rnas
        WHERE pmid = {pmid}
        """,
        conn
    )

    genes = pd.read_sql(
        f"""
        SELECT gene_name
        FROM genes
        WHERE pmid = {pmid}
        """,
        conn
    )

    diseases = pd.read_sql(
        f"""
        SELECT disease_name
        FROM diseases
        WHERE pmid = {pmid}
        """,
        conn
    )

    return paper, rnas, genes, diseases


st.title("RNA-CuratorAI")
st.subheader(
    "AI-Assisted RNA Literature Curation Platform"
)

# -----------------------
# Metrics
# -----------------------

paper_count = pd.read_sql(
    "SELECT COUNT(*) AS count FROM papers",
    conn
).iloc[0]["count"]

rna_count = pd.read_sql(
    "SELECT COUNT(*) AS count FROM rnas",
    conn
).iloc[0]["count"]

gene_count = pd.read_sql(
    "SELECT COUNT(*) AS count FROM genes",
    conn
).iloc[0]["count"]

disease_count = pd.read_sql(
    "SELECT COUNT(*) AS count FROM diseases",
    conn
).iloc[0]["count"]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Papers", paper_count)
c2.metric("RNAs", rna_count)
c3.metric("Genes", gene_count)
c4.metric("Diseases", disease_count)

st.divider()

# -----------------------
# Sidebar Search
# -----------------------

st.sidebar.header("Search Database")

search_type = st.sidebar.selectbox(
    "Search By",
    [
        "RNA",
        "Gene",
        "Disease"
    ]
)

search_term = st.sidebar.text_input(
    "Enter Search Term"
)

# -----------------------
# Search Logic
# -----------------------

if search_term:

    if search_type == "RNA":

        query = f"""
        SELECT DISTINCT
            p.pmid,
            p.title,
            p.key_finding
        FROM papers p
        JOIN rnas r
            ON p.pmid = r.pmid
        WHERE LOWER(r.rna_name)
        LIKE LOWER('%{search_term}%')
        """

    elif search_type == "Gene":

        query = f"""
        SELECT DISTINCT
            p.pmid,
            p.title,
            p.key_finding
        FROM papers p
        JOIN genes g
            ON p.pmid = g.pmid
        WHERE LOWER(g.gene_name)
        LIKE LOWER('%{search_term}%')
        """

    else:

        query = f"""
        SELECT DISTINCT
            p.pmid,
            p.title,
            p.key_finding
        FROM papers p
        JOIN diseases d
            ON p.pmid = d.pmid
        WHERE LOWER(d.disease_name)
        LIKE LOWER('%{search_term}%')
        """

    results = pd.read_sql(
        query,
        conn
    )

    st.subheader(
        f"Search Results ({len(results)})"
    )

    st.dataframe(
        results,
        width="stretch"
    )

st.divider()

# -----------------------
# Data Browser
# -----------------------

view = st.selectbox(
    "Browse Data",
    [
        "Papers",
        "RNAs",
        "Genes",
        "Diseases"
    ]
)

if view == "Papers":

    df = pd.read_sql(
        """
        SELECT *
        FROM papers
        """,
        conn
    )

elif view == "RNAs":

    df = pd.read_sql(
        """
        SELECT *
        FROM rnas
        """,
        conn
    )

elif view == "Genes":

    df = pd.read_sql(
        """
        SELECT *
        FROM genes
        """,
        conn
    )

else:

    df = pd.read_sql(
        """
        SELECT *
        FROM diseases
        """,
        conn
    )

st.dataframe(
    df,
    width="stretch"
)

st.divider()

# -----------------------
# Paper Detail Viewer
# -----------------------

st.subheader("Paper Detail Viewer")

paper_ids = pd.read_sql(
    """
    SELECT pmid
    FROM papers
    ORDER BY pmid DESC
    """,
    conn
)

selected_pmid = st.selectbox(
    "Select PMID",
    paper_ids["pmid"]
)

paper, rnas, genes, diseases = get_paper_details(
    selected_pmid
)

st.markdown(
    f"### {paper.iloc[0]['title']}"
)

st.write(
    f"**PMID:** {selected_pmid}"
)

st.write(
    f"**RNAs:** {', '.join(rnas['rna_name'].tolist()) if len(rnas) > 0 else 'None'}"
)

st.write(
    f"**Genes:** {', '.join(genes['gene_name'].tolist()) if len(genes) > 0 else 'None'}"
)

st.write(
    f"**Diseases:** {', '.join(diseases['disease_name'].tolist()) if len(diseases) > 0 else 'None'}"
)

st.write(
    "**Key Finding:**"
)

st.info(
    paper.iloc[0]["key_finding"]
)

conn.close()