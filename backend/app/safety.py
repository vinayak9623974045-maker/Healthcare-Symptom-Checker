RED_FLAGS = [
    "chest pain",
    "severe shortness of breath",
    "sudden weakness",
    "difficulty breathing",
    "loss of consciousness",
    "severe bleeding",
]

def contains_red_flag(text: str) -> bool:
    t = text.lower()
    return any(flag in t for flag in RED_FLAGS)
