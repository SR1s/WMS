#!/usr/bin/python

import unittest
from tests.accounts import AccountsTest
from tests.utils import UtilsTest

accounts = unittest.TestLoader().loadTestsFromTestCase(AccountsTest)
utils = unittest.TestLoader().loadTestsFromTestCase(UtilsTest)

unittest.TextTestRunner(verbosity=2).run(accounts)
unittest.TextTestRunner(verbosity=2).run(utils)