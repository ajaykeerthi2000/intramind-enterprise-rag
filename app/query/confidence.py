def calculate_confidence(distances: list[float]) -> float:
    if not distances:
        return 0.0

    # Convert FAISS distance → similarity score
    similarities = [1 / (1 + d) for d in distances]

    confidence = sum(similarities) / len(similarities)

    # Clamp strictly to [0, 1]
    confidence = max(0.0, min(confidence, 1.0))

    return round(confidence, 2)
