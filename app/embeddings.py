import hashlib
import random

VECTOR_DIM = 128

def fake_embedding(text: str):
    """
    Deterministically generate a vector from text.
    """
    seed = int(hashlib.sha256(text.encode()).hexdigest(), 16) % (10**8)
    random.seed(seed)

    return [random.random() for _ in range(VECTOR_DIM)]
