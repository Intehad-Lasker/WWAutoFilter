"""
WaterlooWorks Filter Automation
--------------------------------
Automatically applies "Targeted Degrees and Disciplines" filters on the WaterlooWorks job board.

Setup (run once):
    pip install playwright
    python -m playwright install chromium

Usage:
    python waterloo_filters.py

Customization:
    Edit FILTERS_TO_CHECK below — delete any lines you don't want.
"""

import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

URL = "https://waterlooworks.uwaterloo.ca/myAccount/co-op/full/jobs.htm"

# ─────────────────────────────────────────────────────────────────────────────
# FILTERS — delete any lines you don't want applied
# ─────────────────────────────────────────────────────────────────────────────
FILTERS_TO_CHECK = [

    # ── Themes ──────────────────────────────────────────────────────────────
    "Theme - Accounting and Auditing",
    "Theme - Agricultural and Food Sciences",
    "Theme - Architecture and Design",
    "Theme - Business Administration",
    "Theme - Computing: Hardware Development",
    "Theme - Computing: Information Systems and Data Management",
    "Theme - Computing: Software Development",
    "Theme - Computing: Systems Support",
    "Theme - Construction and Infrastructure Development",
    "Theme - Cybersecurity and Cryptography",
    "Theme - Data Science, Analytics, Reporting and Optimization",
    "Theme - Digital and Graphic Media and Web Site Design",
    "Theme - Environmental Management, Climate Change and Sustainability",
    "Theme - Finance and Investment",
    "Theme - Health Care: Therapy and Patient Care",
    "Theme - Health Promotion and Workplace Safety",
    "Theme - Human Resources",
    "Theme - Insurance and Risk Management",
    "Theme - Manufacturing and Process Engineering",
    "Theme - Marketing and Communication",
    "Theme - Pharmacy and Pharmaceuticals",
    "Theme - Project and Process Management",
    "Theme - Public Policy, Public Service and Government Relations",
    "Theme - Recreation, Event Planning and Hospitality",
    "Theme - Sales and Business Development",
    "Theme - Scientific Experimental Design and Laboratory Assistance",
    "Theme - Sport and Fitness",
    "Theme - Supply Chain Management and Logistics",
    "Theme - Transportation Planning and Transportation Engineering",
    "Theme - Waste, Water and Materials Management",

    # ── Arts ────────────────────────────────────────────────────────────────
    "ARTS - All Programs",
    "ARTS - Economics",
    "ARTS - English Language and Literature",
    "ARTS - Fine and Performing Arts",
    "ARTS - Global Business and Digital Arts",
    "ARTS - Humanities",
    "ARTS - Languages and Cultures",
    "ARTS - Political Science",
    "ARTS - Social Sciences",
    "ARTS - Sociology and Legal Studies",
    "ARTS/ENV/MATH/SCI - Chartered Professional Accounting",
    "ARTS/SCI - Psychology",

    # ── Engineering ─────────────────────────────────────────────────────────
    "ENG - Architectural Engineering",
    "ENG - Architecture",
    "ENG - Biomedical, Nanotechnology and Material Sciences",
    "ENG - Chemical Engineering",
    "ENG - Civil, Environmental and Geological Engineering",
    "ENG - Electrical and Computer Engineering",
    "ENG - Management Sciences",
    "ENG - Mechanical and Mechatronics Engineering",
    "ENG - Software Engineering",
    "ENG - Systems Design",

    # ── Environment ─────────────────────────────────────────────────────────
    "ENV - Business, Enterprise and Development",
    "ENV - Environment, Resources and Sustainability",
    "ENV - Geography and Environmental Management",
    "ENV - Geomatics",
    "ENV - Planning",

    # ── Health ──────────────────────────────────────────────────────────────
    "HEALTH - Kinesiology",
    "HEALTH - Recreation and Leisure Studies",
    "HEALTH - School of Public Health Sciences",

    # ── Math ────────────────────────────────────────────────────────────────
    "MATH - Applied Mathematics",
    "MATH - Business",
    "MATH - Combinatorics and Optimization",
    "MATH - Computer Science",
    "MATH - Computing and Financial Management",
    "MATH - Pure Mathematics",
    "MATH - Statistics and Actuarial Science",
    "MATH - Teaching",

    # ── Science ─────────────────────────────────────────────────────────────
    "SCI - Biological Sciences",
    "SCI - Business",
    "SCI - Chemical Sciences",
    "SCI - Earth, Environmental and Geological Sciences",
    "SCI - Pharmacy",
    "SCI - Physics",

]
# ─────────────────────────────────────────────────────────────────────────────


def wait_for_login(page):
    print("Waiting for login + Duo MFA... (5 minutes)")
    page.wait_for_url("**/jobs.htm**", timeout=300_000)
    page.wait_for_load_state("networkidle", timeout=30_000)
    print("Logged in.")


def click_all_jobs(page):
    print("Clicking 'All Jobs'...")
    for sel in ["text=All Jobs", "a:has-text('All Jobs')", "button:has-text('All Jobs')"]:
        try:
            page.click(sel, timeout=5_000)
            page.wait_for_load_state("networkidle", timeout=15_000)
            print("  Done.")
            return
        except PWTimeout:
            continue
    print("  WARNING: 'All Jobs' not found — continuing.")


def open_target_degrees(page):
    print("Opening 'Target Degrees and Disciplines'...")
    for sel in [
        "text=Target Degrees and Disciplines",
        "a:has-text('Target Degrees')",
        "button:has-text('Target Degrees')",
        "a:has-text('Disciplines')",
        "button:has-text('Disciplines')",
    ]:
        try:
            el = page.locator(sel).first
            if el.count() > 0 and el.is_visible():
                el.click()
                time.sleep(2)
                print("  Done.")
                return
        except Exception:
            continue
    print("  Could not find filter button.")


def apply_filters(page):
    missed = []
    for label in FILTERS_TO_CHECK:
        try:
            el = page.locator(f"label:has-text('{label}')").first
            if el.count() > 0:
                el.scroll_into_view_if_needed()
                el.click()
                time.sleep(0.2)
                print(f"  [✓] {label}")
                continue
        except Exception:
            pass
        missed.append(label)
        print(f"  [✗] {label}")
    return missed


def main():
    import sys
    # Use headless=False so you can log in interactively.
    # In a headless environment (e.g. GitHub Codespaces / CI), run:
    #   playwright install-deps chromium
    # and note that you must run this locally where a browser window can open.
    headless = "--headless" in sys.argv

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=80)
        page = browser.new_page()

        print(f"Opening {URL}")
        page.goto(URL, timeout=60_000)

        if "jobs.htm" not in page.url:
            wait_for_login(page)

        page.wait_for_load_state("networkidle", timeout=20_000)
        time.sleep(1)

        click_all_jobs(page)
        time.sleep(1)

        open_target_degrees(page)
        time.sleep(3)

        print(f"\nApplying {len(FILTERS_TO_CHECK)} filters...")
        missed = apply_filters(page)

        if missed:
            print(f"\n{len(missed)} filter(s) not found — check manually:")
            for m in missed:
                print(f"  - {m}")
        else:
            print("\nAll filters applied successfully!")

        print("\nDone. Browser stays open — press Enter to close.")
        input()
        browser.close()


if __name__ == "__main__":
    main()
