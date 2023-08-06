import astroid

from pylint import checkers
from pylint import interfaces


class AssertionsChecker(checkers.BaseChecker):
    '''
    This checker will track down all test-methods and functions and
    check if they include at least 1 assertion of any kind.
    '''
    __implements__ = interfaces.IAstroidChecker

    name = 'missing-assertion'

    msgs = {
        'W9999': ("Missing assertion(s) in test",
                  'missing-assertion',
                  'You have a test or testcase that has NO assertion. '
                  'Make sure every test function has an assertion!'
                  ),
        }
    def __init__(self, linter=None):
        super(AssertionsChecker, self).__init__(linter)
        self._testcount = 0

    def close(self):
        print(f'AssertionChecker finished: found and checked {self._testcount} tests!')

    def is_test(self, node):
        '''
        Identifies a test when a function or method name starts with the word 'test'
        '''
        if node.name[0:4].lower() == 'test':
            self._testcount += 1
            return True
        
        return False

    def visit_functiondef(self, node):
        '''
        Checks on occurence of the 'Assert' keyword or an assertion expression
        from the unittest standard library. 
        '''
        assertion = False
        if self.is_test(node):
            for child in node.body:
                # 1. Check it's a 'Assert' keyword
                if isinstance(child, astroid.Assert):
                    assertion = True
                # 2. Check for possible assertions expressions that may get used when
                # using the standard library
                elif (isinstance(child, astroid.Expr) and
                        isinstance(child.value, astroid.Call)):
                    attrname = child.value.func.attrname
                    if attrname[0:6] == 'assert':
                        assertion = True
        
            if not assertion:
                self.add_message('missing-assertion', node=node)
                       
def register(linter):
    '''
    Required method for pylint plugins
    '''
    linter.register_checker(AssertionsChecker(linter))
