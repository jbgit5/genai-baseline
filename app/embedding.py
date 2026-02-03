import hashlib
import numpy as np

VECTOR_DIM = 128  # small, fast, good for learning

def fake_embedding(text: str) -> list[float]:
    """
    Deterministic embedding generator.
    Same text always produces same vector.
    """
    vector = np.zeros(VECTOR_DIM, dtype=np.float32)

    for word in text.lower().split():
        h = int(hashlib.md5(word.encode()).hexdigest(), 16)
        index = h % VECTOR_DIM
        vector[index] += 1.0

    # normalize vector
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm

    return vector.tolist()
