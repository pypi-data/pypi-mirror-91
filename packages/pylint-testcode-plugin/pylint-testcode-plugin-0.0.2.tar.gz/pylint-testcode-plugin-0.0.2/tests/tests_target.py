'''
module doc-string
'''
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        '''
        method doc-string
        '''
        pass

    def tearDown(self):
        '''
        method doc-string
        '''
        pass

    def test_something(self):
        '''
        method doc-string
        '''
        some_variable = 1
        self.assertEqual(some_variable,1)
        # 1 + 1
        pass

    def testsomething(self):
        '''
        method doc-string
        '''
        pass

    def Testsomething(self):
        '''
        method doc-string
        '''
        pass
    

def test_example():
    '''
    function doc-string
    '''
    some_variable = 1
    assert some_variable == 1
    return some_variable

def no_test_example():
    '''
    function doc-string
    '''
    some_variable = 1
    return some_variable
