import unittest
import testgame as t

class TyperTest(unittest.TestCase):
    def test_config_parser(self):
        configs = t.parse_config('test_texts/config.cfg')
        self.assertTrue(configs[0] == "480")
        self.assertTrue(configs[1] == "416")
        self.assertTrue(configs[2] == "Battle City")
        self.assertTrue(configs[3] == "25")

    def test_basic_enemy_movement(self):
        enemy = t.Enemy(10,10, (25,25), 'regular')
        player = t.Player(20,20, 8, (25,25), 100)
        self.assertTrue(enemy.make_move(player) == 'down')

if __name__ == '__main__':
    unittest.main()
