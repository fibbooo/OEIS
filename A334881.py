'''Creates the b file for  OEIS sequence A334881: The number of squares in an nxnxn cube.

To do this, the code first finds all of the vertices of squares of a certain maximum size which have a vertex at the
origin (though not neccesarily in the nxnxn cube). Afterwards we use this calculation to calculate the true number of
vertices in the whole cube, and then divide by 4 to count the number of squares.

In the nitty gritty:
Think of each square with sides as vectors, so that they make a cycle. Then, each vertex has one vector going into it,
and one vector leaving it. We will count each pair of vectors exactly once, corresponding to each vertex once in every
square of a certain class.

We are going to generate each vector with integer entries in [-n,+n] . As they're generated, put it into
a list with all other vectors of the same magnitude, and check which of those its orthogonal too (i.e. has a dot
product of 0). The vectors which are orthogonal and have the same length define some square, so this combination
counts one vertex in our oriented square. We will record the smallest box (oriented 'parallel' to the grid) that
this square fits in by taking the sum of the vectors componentwise absolute value. (i.e. the smallest box that the
square defined by vectors <1,-1,0>,<1,1,0> fits into has sides of length <2,2,0>)


Once all of these boxes are generated, count how many of these boxes fit in the cube; from the 2D work, we know it is
the product of (n-i) for each dimension, although because of the way we generated them some of them don't fit at
all. Then, we multiply it by the number of counts in that box; that is how many of the
squares that fit inside of that box fit inside the cube. Adding all of these up give us 4 times the answer,
so we divide by 4 to get the total answer.

This is O(n^5), I think. For each of the  (2n)^3  vectors we compare them to all of the vectors of the same length;
that is the surface area of a sphere, so O(n^2), for a total cost of O(Sum n^5). This is placed in a box (hash table has
constant access time). After we have all of the boxes, there are at most n^3 of them, and the
processing is constant time.

The big slow down I know of in this program is that it might be possible to reduce the number of vectors that are
checked and divide by a smaller amount. In particular, you should be able to only look at nonnegative entries in the
 first component and then in particular making use of the symmetry thats in a cube. I got too confused
to implement that.


The dot product and absolute sum are explicitly written out for speed; i got a 10% increase. I attempted to use
numpy; the main speed increase was expected to be the dot product of the new vector with all of the vectors of the
same length, but for me it was slower, probably because appending a vector requires rewriting the whole array.
However, I'm new to numpy so i might have just been inefficient.


Unfortunately, due to the way the code is run, there isn't really a 'partial result',though the code could be
restructured to do that

The code ran for the first 100 entries in 1653 seconds (28 minutes) on a Macbook Pro 

 '''

import itertools

from collections import defaultdict


def square_classes(n):
    '''
    finds all of the different 'classes' of squares that can exist by an nxn cube, along with their duplicity.
    Every squrae can be thought of as 2 orthogonal vectors; this function gnerates all vectors that could exist in
    an nxnxn cube, finds which of them are orthogonal (i.e. form a square),
    and collects them by their minimum bounding box (in terms of the directions of the original cube).

    :param n: maximum size cube to check
    :return: dictionary of box sizes with a count of how many square vertices have that box as their minimum bounds.
    Each should be divisible by 4, because there are 4 vertices in a square
    '''

    def absolute_sum(i, j):
        '''
        Takes the componentwise absolute value sum of i and j
        :param i: vector of length 3
        :param j: vector of length 3
        :return: componentwise absolute value sum
        '''
        return tuple(sorted([abs(i[0]) + abs(j[0]), abs(i[1]) + abs(j[1]), abs(i[2]) + abs(j[2])]))
        #return abs(i[0]) + abs(j[0]), abs(i[1]) + abs(j[1]), abs(i[2]) + abs(j[2]) Testing showed that teh sorting
        #was maybe 10% faster
    def is_orthogonal(i, j):
        '''

        :param i: vector of length 3
        :param j: vector of length 3
        :return: whether i and j are orthogonal
        '''
        return i[0] * j[0] + i[1] * j[1] + i[2] * j[2] == 0

    def length(i):
        '''

        :param i: vector of length 3
        :return: square of the euclidian distance of i
        '''
        return i[0] * i[0] + i[1] * i[1] + i[2] * i[2]

    vectors_by_size = defaultdict(list)  # key is vector length^2. Items in list are vectors with that length
    bounding_box_vertex_counts = defaultdict(int)
    # key is size of the box, i.e. componentwise sum of absolute values. Value is count of vectors pairs i.e. vertices.
    # counts each square 4 times, one for each 'oriented corner'
    for i in itertools.product(range(-n, n + 1), range(-n, n + 1), range(-n, n + 1)):
        same_length_vectors = vectors_by_size[length(i)]
        if same_length_vectors is not []:
            for j in same_length_vectors:
                if is_orthogonal(i, j):
                    bounding_box_vertex_counts[absolute_sum(i, j)] += 1

        same_length_vectors += [i]  # adds the vector to the list
    return bounding_box_vertex_counts


def countSquares(n, vertex_counts):
    '''
    Counts number of squares in a cube of size n
    :param n: size of cube (i.e. a 1 by 1 cube, with 2 vertices on a side, would be an n of 1)
    :parm squarecounts: how many squares are in each box
    :return: count of squares
    '''
    runningsum = 0
    for i in vertex_counts.items():
        if max(i[0]) < n :
            runningsum += (n - i[0][0]) * (n - i[0][1]) * (n - i[0][2]) * i[1]
            # the number of boxes that fit into the n x n xn cube, multiplied by the number of vertices found in it
    return int(runningsum / 4)  # should always be an int


def main(n):
    '''

    :param n: max size
    :return: a list of the number of squares in all cubes from range 0 to n, formatted for the b file in OEIS

    '''
    box_list = square_classes(n)

    with open(f'b334881.txt', 'w') as result_file:
        for i in range(0, n + 1):
            result_file.write(f'{i} {countSquares(i, box_list)}\n')


if __name__ == '__main__':
    import time

    n =60
    start_time = time.time()
    main(n)
    t = (time.time() - start_time)
    print(f'Calculated {n} in {t} seconds ---')
