from tetrisRoom import *
import unittest

test_room1 =   [[1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1]]
test_room2 =   [[1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1]]
test_room3 =   [[1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 1, 0, 1, 1],
                [1, 0, 0, 1, 1, 0, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1]]
test_room4 =   [[1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 1, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1]]


class TestTetris(unittest.TestCase):
    
    def test_input_to_tab(self):
        room_input2 =  ['#######',
                        '#.....#',
                        '#..#..#',
                        '#.##..#',
                        '#.....#',
                        '#.....#',
                        '#######']
        self.assertEqual(input_to_tab(room_input2), test_room2)
    
    def test_fit(self):
        self.assertEqual([fit(room_tab, (0, 0), i, 0),
                          fit(room_tab, (1, 1), t, 3),
                          fit(room_tab, (1, 4), i, 0),
                          fit(room_tab, (4, 4), o, 0),
                          fit(room_tab, (5, 5), o, 0),
                          fit(room_tab, (3, 3), o, 0),],
                         [False, True, False, True, False, False])
        
    def test_place(self):
        test_room = copy.deepcopy(test_room1)
        place(test_room, (1, 1), t, 0)
        expected_room =[[1, 1, 1, 1, 1, 1, 1],
                        [1, 0, 1, 0, 0, 0, 1],
                        [1, 1, 1, 1, 0, 0, 1],
                        [1, 0, 0, 1, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1]]
        self.assertEqual(test_room, expected_room)

    def test_neighbour(self):
        self.assertEqual([len(neighbours((1, 1))), len(neighbours((0, 0))), len(neighbours((0, 4))), len(neighbours((0, 6))), len(neighbours((6, 0)))], [4, 2, 3, 2, 2])
    
    def test_group(self):
        self.assertEqual([len(group(test_room3, (2, 1))), len(group(test_room3, (5, 5)))], [8, 3])
    
    def test_still_solvable(self):
        self.assertEqual([still_solvable(test_room1), still_solvable(test_room3), still_solvable(test_room4)], [True, False, True])




if __name__ == '__main__':
    unittest.main()