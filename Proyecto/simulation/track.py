

class Track:
    def __init__(self, name: str = "Misano"):
        self.name = name


def default_tracks():
    misano = Track("Misano")
    return {"misano": misano}
