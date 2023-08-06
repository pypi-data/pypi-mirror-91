import pyPasswordValidator
import unittest

class Test_pyPasswordValidator(unittest.TestCase):
    """
    Test the functions in the pyPasswordValidator module
    """

    def test_is_ascii(self):
        """
        Simply test if true or fales is retruned as expected
        """
        #Good ascii string
        self.assertEqual(pyPasswordValidator.is_ascii('agoodstring'),True)
        #bad ascii string
        self.assertEqual(pyPasswordValidator.is_ascii('строка'),False)
        #No string
        with self.assertRaises(TypeError):
            pyPasswordValidator.is_ascii()

    def test_remove_non_ascii(self):
        """
        Simply tests the removal of non ascii characters function
        """
        #test if int is passed
        with self.assertRaises(TypeError):
            pyPasswordValidator.remove_non_ascii(123)

        removed=pyPasswordValidator.remove_non_ascii('asdf¡Hola!')
        self.assertTrue(isinstance(removed, str))

if __name__ == '__main__':
    unittest.main()
