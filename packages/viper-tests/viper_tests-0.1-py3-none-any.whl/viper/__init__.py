from colorama import Fore, Style
import time

class Viper:
    """ The Main Testing Framework """
    def __init__(self, name):
        self.name = name
        self.tests = []
        self.passed = 0
        print("This is Viper, a modern testing framework, created by Aarush Gupta (https://aarushgupta.tk)")

    def clean(self):
        for test in self.tests:
            if type(test["desiredOutput"]) == list:
                test["array"] = True
    
    def test(self, name, function, output):
        """
        Create a test\n
        :param str name: A short description of the test\n
        :param function: The function that will be tested\n
        :param output: The desired output
        """
        self.tests.append({
            "name" : name,
            "functionOutput" : function,
            "desiredOutput" : output
        })
        self.clean()

    def evaluate(self):
        """ Evaluate all the tests """
        print(f"Running tests for \"{self.name}\"")
        start = time.perf_counter()
        for test in self.tests:
            message = f"Testing \"{test['name']}\"... "
            print(message, end = "\r")
            if test.get("array", False):
                if test["functionOutput"] in test["desiredOutput"]:
                    print(message + Fore.GREEN + "Passed" + Style.RESET_ALL)
                    self.passed += 1
                else:
                    print(message + Fore.RED + "Failed" + Style.RESET_ALL)
                    print(f"   Desired Output: {test['desiredOutput']} | Test Ouput: \"{test['functionOutput']}\"")
            else:
                if test["functionOutput"] == test["desiredOutput"]:
                    print(message + Fore.GREEN + "Passed" + Style.RESET_ALL)
                    self.passed += 1
                else:
                    print(message + Fore.RED + "Failed" + Style.RESET_ALL)
                    print(f"   Desired Output: \"{test['desiredOutput']}\" | Test Ouput: \"{test['functionOutput']}\"")
        end = time.perf_counter()
        total = len(self.tests)
        print(f"\nRan {total} test(s) in {end - start:0.4f} seconds")
        print(f"{self.passed}/{total} passed")