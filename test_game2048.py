def test_zip_func():
    m = zip([1,2,3],[4,5,6],[7,8,9])

    assert next(m) == (1,4,7)
    assert next(m) == (2,5,8)
    assert next(m) == (3,6,9)

def test_zip_func_2d():
    m = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
        ]
    s=zip(*m)

    assert next(s) == (1,4,7)
    assert next(s) == (2,5,8)
    assert next(s) == (3,6,9)

def test_cw90():
    m = [[1,2,3], [4,5,6], [7,8,9]]
    s = zip(*m[::-1])
    assert next(s)==(7,4,1)
    assert next(s)==(8,5,2)
    assert next(s)==(9,6,3)

def test_ccw90():
    m = [[1,2,3], [4,5,6], [7,8,9]]
    s = list(zip(*m))[::-1]
    assert s[0] == (3, 6, 9)
    assert s[1] == (2, 5, 8)
    assert s[2] == (1, 4, 7)

from game2048 import rotate

def test_2048_cw90():
    m = [[1,2,3], [4,5,6], [7,8,9]]
    s = rotate(True, m)

    assert s[0]==[7,4,1]
    assert s[1]==[8,5,2]
    assert s[2]==[9,6,3]

def test_2048_ccw90():
    m = [[1,2,3], [4,5,6], [7,8,9]]
    s = rotate(False,m)

    assert s[0] == [3, 6, 9]
    assert s[1] == [2, 5, 8]
    assert s[2] == [1, 4, 7]

from game2048 import merge_row
def test_merge_row():
    new_row = merge_row([2,2,4,0,0])
    assert [4,4,0,0,0] == new_row
    assert 5 == len(new_row)

    new_row = merge_row([0,0,0,0,4])
    assert [4,0,0,0,0] == new_row
    assert 5 == len(new_row)

    new_row = merge_row([2,4,8,16,32])
    assert [2,4,8,16,32] == new_row
    assert 5 == len(new_row)

    new_row = merge_row([0,2,4,0,0])
    assert [2,4,0,0,0] == new_row
    assert 5 == len(new_row)

from game2048 import rotate_merge
#left
def test_left_key_move():
    board = [
        [2, 2, 4, 0, 0],
        [0 ,0, 0, 0, 4],
        [0 ,4, 0, 0, 0],
        [0 ,0, 0, 0, 0],
        [0 ,0, 0, 0, 0]
    ]
    new_board = rotate_merge(0,board)

    exp_board = [
        [4, 4, 0, 0, 0],
        [4, 0, 0, 0, 0],
        [4, 0, 0, 0, 0],
        [0 ,0, 0, 0, 0],
        [0 ,0, 0, 0, 0]
    ]

    assert new_board==exp_board

#down
def test_down_key_move():
    board = [
        [2, 2, 4, 0, 0],
        [0 ,0, 0, 0, 4],
        [0 ,4, 0, 0, 0],
        [0 ,0, 0, 0, 0],
        [0 ,0, 0, 0, 0]
    ]
    new_board = rotate_merge(1,board)

    exp_board = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0 ,2, 0, 0, 0],
        [2 ,4, 4, 0, 4]
    ]

    assert new_board==exp_board

#right
def test_right_key_move():
    board = [
        [2, 2, 4, 0, 0],
        [0, 0, 0, 0, 4],
        [0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    new_board = rotate_merge(2, board) 

    exp_board = [
        [0, 0, 0, 4, 4],
        [0, 0, 0, 0, 4],
        [0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    assert new_board == exp_board