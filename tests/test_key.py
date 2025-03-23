import unittest
from app import create_app

class KeyRoutesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_generate_key(self):
        response = self.app.post('/key/generate-key', json={"key_type": "AES", "key_size": 256})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
