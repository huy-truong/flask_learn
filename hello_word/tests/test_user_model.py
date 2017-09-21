import unittest
from hello.Models import User

class UserModelTestCase(unittest.Testcase):
    def test_password_setter(self):
        u=User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_setter(self):
        u = User(password='cat')
        with self.assertRaise(AttributeError):
            u.password

    def test_password_verification(self):
        u=User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u=User(password='cat')
        u1=User(password='cat')
        self.assertTrue(u.password_hash != u1.password_hash)



