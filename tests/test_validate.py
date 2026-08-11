import unittest

from tools import validate


class RepositoryValidatorTests(unittest.TestCase):
    def test_repository_manifests_are_current(self):
        checks = (
            validate.check_local_override_inventory(),
            validate.check_map_data(),
            validate.check_localization(),
            validate.check_stale_symbols(),
            validate.check_delayed_lifecycle(),
        )
        failures = [f"{check.name}: {check.detail}" for check in checks if check.status != "PASS"]
        self.assertEqual([], failures)

    def test_delayed_inventory_counts_duplicate_dispatches(self):
        first = ("events/a.txt", "example.1", (("days", "3"),), "yes")
        second = ("events/b.txt", "example.1", (("months", "1"),), "default")

        count, digest, destinations = validate.delayed_inventory((first, second))
        reversed_count, reversed_digest, _ = validate.delayed_inventory((second, first))

        self.assertEqual(2, count)
        self.assertEqual({"example.1"}, destinations)
        self.assertEqual(count, reversed_count)
        self.assertEqual(digest, reversed_digest)

    def test_braced_parser_ignores_comment_and_quoted_braces(self):
        source = 'event = { text = "{quoted}" # } ignored\n effect = { value = 1 } }'
        self.assertEqual(source, validate.extract_braced(source, 0))


if __name__ == "__main__":
    unittest.main()
