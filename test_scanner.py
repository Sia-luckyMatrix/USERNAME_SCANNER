"""
Comprehensive unit tests for USER SCANNER with 20 platforms.
"""
import unittest
import os
import tempfile
import time
from scanner.models import CheckResult, CheckStatus, PlatformDefinition
from scanner.validator import sanitize_username, validate_username_for_platform
from scanner.platforms import PLATFORMS, PLATFORM_MAP
from scanner.engine import ScannerEngine
from utils.exporter import export_to_csv, format_results_summary


class TestUserScanner(unittest.TestCase):

    def test_platform_count(self):
        # Verify exactly the top 20 requested platforms
        self.assertEqual(len(PLATFORMS), 20)
        expected_ids = [
            "instagram", "github", "x_twitter", "snapchat", "youtube",
            "facebook", "telegram", "pinterest", "reddit", "tiktok",
            "linkedin", "twitch", "medium", "soundcloud", "dev_to",
            "gitlab", "spotify", "vimeo", "patreon", "dribbble",
        ]
        for pid in expected_ids:
            self.assertIn(pid, PLATFORM_MAP, f"Platform {pid} must be in PLATFORM_MAP")

    def test_sanitize_username(self):
        self.assertEqual(sanitize_username("  @cyber_user  "), "cyber_user")
        self.assertEqual(sanitize_username("@neo"), "neo")
        self.assertEqual(sanitize_username("test"), "test")

    def test_github_validation(self):
        gh = PLATFORM_MAP["github"]
        valid, _ = validate_username_for_platform("octocat", gh)
        self.assertTrue(valid)

        invalid, _ = validate_username_for_platform("-octocat", gh)
        self.assertFalse(invalid)

        invalid, _ = validate_username_for_platform("octo--cat", gh)
        self.assertFalse(invalid)

        invalid, _ = validate_username_for_platform("octo_cat", gh)
        self.assertFalse(invalid)

    def test_snapchat_validation(self):
        sc = PLATFORM_MAP["snapchat"]
        valid, _ = validate_username_for_platform("snapuser12", sc)
        self.assertTrue(valid)

        invalid, _ = validate_username_for_platform("9snapuser", sc)
        self.assertFalse(invalid)

        invalid, _ = validate_username_for_platform("snapuser.", sc)
        self.assertFalse(invalid)

    def test_x_twitter_validation(self):
        x = PLATFORM_MAP["x_twitter"]
        valid, _ = validate_username_for_platform("jack", x)
        self.assertTrue(valid)

        invalid, _ = validate_username_for_platform("this_is_longer_than_fifteen", x)
        self.assertFalse(invalid)

    def test_csv_export_and_summary(self):
        res1 = CheckResult(
            platform_id="github",
            platform_name="GitHub",
            category="Developer",
            username="alex",
            status=CheckStatus.TAKEN,
            profile_url="https://github.com/alex",
            http_status=200,
            response_time_ms=150.0,
            details="Profile found",
        )
        res2 = CheckResult(
            platform_id="youtube",
            platform_name="YouTube",
            category="Video / Media",
            username="alex",
            status=CheckStatus.AVAILABLE,
            profile_url="https://youtube.com/@alex",
            http_status=404,
            response_time_ms=180.0,
            details="Available",
        )

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
            temp_path = tf.name

        try:
            success = export_to_csv([res1, res2], temp_path)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
                self.assertIn("GitHub", content)
                self.assertIn("YouTube", content)
                self.assertIn("AVAILABLE", content)
                self.assertIn("TAKEN", content)

            summary = format_results_summary("alex", [res1, res2], elapsed_seconds=0.33)
            self.assertIn("USER SCANNER", summary)
            self.assertIn("AVAILABLE TO REGISTER", summary)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_scanner_engine_concurrency(self):
        engine = ScannerEngine(max_workers=6)
        collected = []
        done_flag = []

        def on_res(r, cur, tot):
            collected.append(r)

        def on_done(all_res, dur):
            done_flag.append(dur)

        # Test with invalid inputs that resolve instantly via validator
        test_platforms = [PLATFORM_MAP["github"], PLATFORM_MAP["x_twitter"]]
        engine.scan_username_async(
            username="-invalid_start",  # triggers fast local validation
            platforms=test_platforms,
            on_result=on_res,
            on_complete=on_done,
        )

        for _ in range(50):
            if done_flag:
                break
            time.sleep(0.1)

        self.assertTrue(len(done_flag) > 0)
        self.assertEqual(len(collected), 2)
        self.assertEqual(collected[0].status, CheckStatus.INVALID)


if __name__ == "__main__":
    unittest.main()
