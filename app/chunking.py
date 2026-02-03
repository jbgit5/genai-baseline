def chunk_text(text: str, chunk_size: int = 200, overlap: int = 40):
    """
    Split text into overlapping chunks.
    - chunk_size: number of words per chunk
    - overlap: number of words shared between chunks
    """

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        start = end - overlap

    return chunks
