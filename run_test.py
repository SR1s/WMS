import unittest
from tests.accounts import AccountsTest

suite = unittest.TestLoader().loadTestsFromTestCase(AccountsTest)

unittest.TextTestRunner(verbosity=2).run(suite)