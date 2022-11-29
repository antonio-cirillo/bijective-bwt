from util.cfl import cfl
from util.suffix_array import suffix_array_manber_myers


class Rotation:
    def __init__(self, w: int, r: int):
        # index of factor
        self.w = w
        # index of the first character generating the rotation
        self.r = r

    def __str__(self):
        return f"w: {self.w}\n" \
               f"r: {self.r}"


def sort_rotations(factors: [str], rotations_of_all_factors: [[Rotation]]):
    # for all rotations of i-th factor
    for i, rotations in enumerate(rotations_of_all_factors):
        # get the suffix array on the factor
        suffix_array = suffix_array_manber_myers(factors[i])
        # use suffix_array for update order of the factor's rotations
        for j, r in enumerate(suffix_array):
            rotations[j].r = r


def encode(string: str) -> str:
    # get all lyndon factors of string
    factors: [str] = cfl(string)
    output = []  # ?

    rotations_of_factors: [[Rotation]] = []
    # for each i-th factor w
    for i, w in enumerate(factors):
        # declare array which contains all rotation of string w
        rotations_of_w: [Rotation] = [None] * len(w)
        # for each j-th character of w
        for j in range(len(w)):
            # j-th rotation of w is equal to (i, j)
            rotations_of_w[j] = Rotation(i, j)
        # append all rotation of w
        rotations_of_factors.append(rotations_of_w)

    sort_rotations(factors, rotations_of_factors)


if __name__ == "__main__":
    encode("banana")
