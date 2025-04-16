
import dataclasses


@dataclasses.dataclass
class Standing:
    wins: int
    place: int
    points: int | None = None

    @property
    def prize(self):
        if not self.points:
            return None
        return f"'¤{self.points * 5}"

    TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES = [3, 1, 1, 1], [2, 2, 2, 0]
    STANDING_CONFIGURATIONS = {
        1: {
            'wins': ([1, 1, 0, 0], ),
            'place': ([1, 1, 3, 3], )
        },
        2: {
            'wins': ([2, 2, 0, 0], [2, 1, 1, 0], [1, 1, 1, 1]),
            'place': ([1, 1, 3, 3], [1, 2, 2, 4], [1, 1, 1, 1])
        },
        3: {
            'wins': ([3, 2, 1, 0], [2, 2, 1, 1], [3, 1, 1, 1], [2, 2, 2, 0]),
            'place': ([1, 2, 3, 4], [1, 1, 3, 3], [1, 2, 2, 2], [1, 1, 1, 4])
        },
        4: {  # final round if NO TIE after preliminaries
            'wins': ([4, 2, 2, 0], [4, 2, 1, 1], [3, 3, 2, 0], [3, 3, 1, 1], [3, 2, 2, 1]),
            'place': ([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]),
            'points': ([10, 6, 4, 0], [10, 6, 3, 1], [9, 7, 4, 0], [9, 7, 3, 1], [9, 6, 4, 1])
        },
        4+1: {  # final round IF TIE after preliminaries
            'wins': ([4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]),
            'place': ([1, 2, 3, 3], [1, 1, 3, 4], [1, 2, 2, 4]),
            'points': ([10, 6, 2, 2], [8, 8, 4, 0], [9, 5, 5, 1])
        }
    }

