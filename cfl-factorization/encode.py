from util.cfl import cfl
from util.suffix_array import suffix_array_manber_myers


class Rotation:
    def __init__(self, w: int, r: int):
        # index of factor
        self.w = w
        # index of the first character generating the rotation
        self.r = r
    # str to let classes print value instead of object
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
            #assign suffix value to "first character that generate rotation"
            rotations[j].r = r
    #return all rotations merged
    return merge_rots(factors,rotations_of_all_factors)

def merge_rots(factors, rots):
    merged = []
    while len(rots) > 0:
        #call merge_rot on every element of rots (Rotation object can contain multiple rotation based on the factor and coniugate numbers)
        merged = merge_rot(factors, merged, rots[0])
        #discard the first element of rots because it's already merged
        rots = rots[1:]
    return merged

def merge_rot(factors, a, b):
    #a will be a list of the factor merged since this execution
    #b will be the list of factor to merge
    la = len(a)
    lb = len(b)
    length = la + lb
    out = [None] * length
    i = 0
    j = 0
    k = 0
    #check if the index is less than lenght of the two factor 
    while i < la and j < lb:
        #less rot check if b[j] is greater or not than a[i] and return true if is less and false if is greater
        if less_rot(factors, b[j], a[i]):
            out[k] = b[j]
            j += 1
        else:
            out[k] = a[i]
            i += 1
        k += 1
    #this mean that we added to out all the element of lb or of la then we add from k all element of a from i and viceversa
    if i < la:
        out[k:] = a[i:]
    elif j < lb:
        out[k:] = b[j:]
    return out

    #less_rot take value from both rotation passed by parameters
def less_rot(factors, i, j):
    wi = i.w
    ri = i.r
    li = len(factors[wi])
    wj = j.w
    rj = j.r
    lj = len(factors[wj])
    for k in range(li * lj):
        #check if the factor to merge is less than factor already merged
        if factors[wi][ri] < factors[wj][rj]:
            return True
        #if is greater than return false
        elif factors[wi][ri] > factors[wj][rj]:
            return False
        #else all the factors are equals then this have to increment value 
        #if ri or rj are equal to lenght of one of two factor then will set to 0 the value
        #simply as modular increment
        ri += 1
        rj += 1
        if ri == li:
            ri = 0
        if rj == lj:
            rj = 0
    return False


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
    
    #merge and order by ascending all factors and coniugates
    s_rot = sort_rotations(factors, rotations_of_factors)
    out = [None] * len(string)
    #select the rightmost letters from factors
    for i, rotation in enumerate(s_rot):
        ri = rotation.r - 1
        if ri < 0:
            ri += len(factors[rotation.w])
        out[i] = factors[rotation.w][ri]
    return ''.join(out)