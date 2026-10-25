"""
USER SCANNER — 20 Network Username Availability Checker
Entry point for the application.
"""
import argparse
import sys
import os

# Ensure local modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import logger
from scanner.validator import sanitize_username
from scanner.platforms import PLATFORMS, dispatch_check
from scanner.models import CheckStatus
from utils.exporter import format_results_summary, export_to_csv


def run_cli_mode(username: str, export_path: str = None):
    """Headless CLI mode for quick checks and scripting."""
    import time
    import httpx
    from utils.network import DEFAULT_TIMEOUT

    clean_user = sanitize_username(username)
    print(f"\n[*] USER SCANNER v2.0 // Scanning target: @{clean_user}")
    print(f"[*] Platforms: {len(PLATFORMS)} | Concurrency: Active\n")

    start_time = time.perf_counter()
    results = []

    with httpx.Client(timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
        for p in PLATFORMS:
            res = dispatch_check(p, clean_user, client)
            results.append(res)

            if res.status == CheckStatus.AVAILABLE:
                symbol = "[+ AVAILABLE]"
            elif res.status == CheckStatus.TAKEN:
                symbol = "[- TAKEN    ]"
            elif res.status == CheckStatus.INVALID:
                symbol = "[! INVALID  ]"
            else:
                symbol = "[? UNKNOWN  ]"

            print(f"  {symbol} {res.platform_name:<16} -> {res.details} ({res.response_time_ms:.0f}ms)")

    elapsed = time.perf_counter() - start_time
    print(f"\n[*] Scan complete in {elapsed:.2f}s")

    summary = format_results_summary(clean_user, results, elapsed)
    if export_path:
        export_to_csv(results, export_path)
        print(f"[*] Results saved to: {export_path}")

    return results


def run_gui_mode():
    """Launch the CustomTkinter GUI."""
    try:
        from gui.app import UserScannerApp
        logger.info("Starting USER SCANNER GUI...")
        app = UserScannerApp()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Fatal error launching GUI: {e}", exc_info=True)
        print(f"[!] Fatal error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="USER SCANNER — Professional Multi-Platform Username Availability Checker"
    )
    parser.add_argument(
        "-u", "--username",
        type=str,
        help="Run in CLI headless mode for the given username.",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Optional CSV file destination when using CLI mode.",
    )

    args = parser.parse_args()

    if args.username:
        run_cli_mode(args.username, args.output)
    else:
        run_gui_mode()


if __name__ == "__main__":
    main()
