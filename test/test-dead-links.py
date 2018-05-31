import unittest
from io import StringIO

from dead_links import *


class TestDeadLinks(unittest.TestCase):
    def test_url(self):
        dead_links = DeadLinks("https://try.github.io/levels/1/challenges/1")
        self.assertEqual(dead_links.url, "https://try.github.io/levels/1/challenges/1")

    def test_json_output(self):
        saved_stdout = sys.stdout
        dead_links = DeadLinks("https://try.github.io/levels/1/challenges/1")
        try:
            capturedOutput = StringIO()
            sys.stdout = capturedOutput
            dead_links.get_links()
            dead_links.get_responses()
            json_out = json.loads(json.dumps(dead_links.dead_data, indent=1, sort_keys=True))
            print(json_out['404']['urls'][0])
            sys.stdout = sys.__stdout__
            self.assertEqual(capturedOutput.getvalue(), "https://twitter.com/share?url=http://bit.ly/TryGit&via=codeschool&text=I'm%20learning%20how%20to%20push%20it%20with%20Try%20Git!%20#trygit\n")
        finally:
            sys.stdout = saved_stdout

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'])