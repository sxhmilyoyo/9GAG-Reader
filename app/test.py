import os
import unittest
import time

from app import app


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_feed_Awesome_page(self):
        time.sleep(5)
        response = self.client.get('/feeds/Awesome', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_feed_DarkHumor_page(self):
        time.sleep(5)
        response = self.client.get('/feeds/DarkHumor', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_feed_Funny_page(self):
        time.sleep(5)
        response = self.client.get('/feeds/Funny', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_feed_Hot_page(self):
        time.sleep(5)
        response = self.client.get('/feeds/Hot', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
