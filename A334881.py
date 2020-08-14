'''Computes OEIS sequence A334881 Counts the number of squares in an nxn cube. This code has an offset of 2,
i.e. it skips the 2 leading 0's of the posted sequence

Here is how this program works: As a large overview, we are going to count each vertex of an 'oriented square', i.e.
one where we make each side a vector such that the vectors form a loop. After counting all of these vertices, we
divide by 4 to count the number of squares.

In the nitty gritty:
We are going to generate each vector with integer entries in [-n,+n] in some order.
As they're generated, put it into a list with all other vectors of the same magnitude, and check which of those its
orthogonal too (i.e. has a dot product of 0). The vectors which are orthogonal and have the same length define some
square, which fits, as oriented by the vectors, in the box with side lengths equal to the componentwise sum of the
absolute values, so count how many squares fit in each of these boxes

Once all of these boxes are generated, count how many of these boxes fit in the cube; from our 2d work, we know it is
the product of (n+1-i) for each dimension, although because of the way we generated them some of them don't fit at
all, which has to be dealt with. Then, we multiply it by the number of counts in that box; that is how many of the
squares that fit inside of that box fit inside the cube. Adding all of these up give us 4 times the answer,
so we divide by 4 to get hte total answer.

This is O(n^5), I think. For each of the  (2n)^3  vectors we compare them to all of the vectors of the same length;
that is the surface area of a sphere, so O(n^2), for a total cost of O(m^5). This is placed in a box (hash table has
constant access time). After we have all of the boxes, there are at most n^3 of them, and the processing is constant

The big slow down I know of in this program is that it might be possible to reduce the number of vectors that are
checked and divide by a smaller amount. In particular, you should be able to only look at nonnegative entries in the
 first component and then verin particular making use of the symmetry thats in a cube. I got too confused
to implement that.
git
The code ran for the first 100 entries in 2006 seconds (33 minutes) on a Macbook Pro

 '''

import itertools

from collections import defaultdict


def absolutesum(i, j):
    '''
    Takes the componentwise absolute value sum of i and j
    :param i: vector of length 3
    :param j: vector
    :return: componentwise absolute value sum
    '''
    return tuple([abs(i[0]) + abs(j[0]), abs(i[1]) + abs(j[1]), abs(i[2]) + abs(j[2])])


def squareclasses(n):
    '''
    finds all of the different 'classes' of squares that can exist by an nxn cube, along with their duplicity.
    Every squrae can be thought of as 2 orthogonal vectors; this function gnerates all vectors that could exist in
    an nxnxn cube, finds which of them are orthogonal (i.e. form a square),
    and collects them by their minimum bounding box (in terms of the directions of the original cube).

    :param n: maximum size cube to check
    :return: dictionary of box sizes with a count of how many squares have that box as their minimum bounds.
    Each should be divisible by 4
    '''

    vectorsbysize = defaultdict(list)  # key is vector length^2. Items in list are vectors with that length
    boundingbox = defaultdict(int)
    # key is size of the box, i.e. componentwise sum of absolute values. Value is count of vectors.
    # counts each square 4 times, one for each 'oriented corner'
    for i in itertools.product(range(-n, n + 1), range(-n, n + 1), range(-n, n + 1)):
        length = i[0] * i[0] + i[1] * i[1] + i[2] * i[2]
        samelengthvectors = vectorsbysize[length]  # euclidean distance ^2
        if samelengthvectors is not []:
            for j in samelengthvectors:
                if i[0] * j[0] + i[1] * j[1] + i[2] * j[2] == 0:  # dot product
                    boundingbox[absolutesum(i, j)] += 1  # absolute value sum

        samelengthvectors += [i]
    return boundingbox

def countSquares(n,squarecounts):
    '''
    Counts number of squares in a cube of size n
    :param n: size of cube (i.e. a 1 by 1 cube, with 2 vertices on a side, would be an n of 1)
    :parm squarecounts: how many squares are in each box
    :return: count of squares
    '''
    runningsum=0
    for i in squarecounts.items():
        if max(i[0])<n+1:
            runningsum+=(n+1-i[0][0])*(n+1-i[0][1])*(n+1-i[0][2])*i[1]
    return runningsum/4 #should always be an int


def main(n):
    '''

    :param n: max size
    :return: a list of the number of squares in all cubes from range 0 to n
    '''
    box_list=squareclasses(n)


    with open(f'A334881_{n}.csv', 'w') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        for i in range(1,n+1):
            wr.writerow([i,countSquares(i,box_list)])

if __name__ == '__main__':
    import time
    n=500
    start_time = time.time()
    main(n)
    t = (time.time() - start_time)
    print(f'Calculated {n} in {t} seconds ---')

