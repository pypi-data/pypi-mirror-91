import os
import unittest

class DecoratorsTest(unittest.TestCase):

    def test_basic(self):
        os.environ['APP_ENV'] = 'test_azure'
        from databricksbundle.notebook.notebook_test import load_data

        result = load_data()

        self.assertEqual(155, result.result)

if __name__ == '__main__':
    unittest.main()
