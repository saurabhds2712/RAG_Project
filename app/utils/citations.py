from pathlib import Path


def build_citations(docs):

    citations = []
    seen = set()

    try:
        for doc in docs:
            key = (
                doc.metadata.get("source"),
                doc.metadata.get("page")
            )
            if key in seen:
                continue
            seen.add(key)
            citations.append({
                "document": Path(doc.metadata["source"]).name,
                "page": doc.metadata.get("page", "N/A")
            })
    
        return citations

    except Exception as e:

        raise RuntimeError(
            f"Failed to build citations: {e}"
        )