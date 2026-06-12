class Retriever:

    def __init__(
        self,
        vector_db,
        top_k
    ):

        self.retriever = (
            vector_db.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": top_k,
                    "fetch_k": 10
                }
            )
        )

    def retrieve(
        self,
        query
    ):

        try:

            return self.retriever.invoke(
                query
            )

        except Exception as e:

            raise RuntimeError(
                f"Retrieval failed: {e}"
            )