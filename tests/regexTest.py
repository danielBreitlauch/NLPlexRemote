import unittest
from NLPlexRemote import English


class RegExTestCase(unittest.TestCase):

    def setUp(self):
        self.lang = English()

    def tearDown(self):
        self.lang = None

    def findMatchingKeys(self, text, assert_keys):
        for priority, command in self.lang.match(text):
            missing = [item for item in assert_keys if item not in command.keys()]
            to_much = [item for item in command.keys() if item not in assert_keys]
            if not missing and not to_much:
                return
        # Readable error
        error = ''
        for priority, command in self.lang.match(text):
            missing = [item for item in assert_keys if item not in command.keys()]
            to_much = [item for item in command.keys() if item not in assert_keys]
            if missing:
                error += str(missing) + ' not found in: ' + str(command) + '\n'
            if to_much:
                error += str(to_much) + ' in: ' + str(command) + 'and not in: ' + str(assert_keys) + '\n'
        self.assertTrue(False, error)

    def findMatchingValues(self, text, assertions):
        for priority, command in self.lang.match(text):
            missing = [item for item in assertions.keys()
                       if item not in command.keys() or assertions[item] and assertions[item] != command[item]]
            to_much = [item for item in command.keys() if item not in assertions.keys()]
            if not missing and not to_much:
                return
        # Readable error
        error = ''
        for priority, command in self.lang.match(text):
            missing = [item for item in assertions.keys() if item not in command.keys()]
            to_much = [item for item in command.keys() if item not in assertions.keys()]
            if missing:
                error += str(missing) + ' not found in: ' + str(command) + '\n'
            elif to_much:
                error += str(to_much) + ' in: ' + str(command) + 'and not in: ' + str(assertions.keys()) + '\n'
            else:
                not_equal = [item for item in assertions.keys() if assertions[item] and assertions[item] != command[item]]
                if not_equal:
                    error += str(not_equal) + ' matched wrong: ' + str(command) + '\n'
        self.assertTrue(False, error)
