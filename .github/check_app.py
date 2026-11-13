"""Opens the live app in a real browser and wakes it if asleep. Mode "test": checks one statement, runs the
12-statement accuracy test, and saves the AI's readings (test.json), screenshots and page text."""
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://loan-doc-checker.streamlit.app/"
mode = sys.argv[1] if len(sys.argv) > 1 else "wake"
out = Path("out"); out.mkdir(exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1366, "height": 900}, color_scheme="dark")
    page.goto(URL, timeout=120_000)
    page.wait_for_timeout(8_000)
    wake = page.get_by_role("button", name="Yes, get this app back up!")
    if wake.count():
        print("was asleep, waking up"); wake.click(); page.wait_for_timeout(90_000)
    app = page.frame_locator("iframe[title='streamlitApp']")
    app.locator(".k-name, h1").first.wait_for(timeout=240_000)
    print("awake:", app.locator(".k-name, h1").first.inner_text())
    if mode == "test":
        err = app.locator("[data-testid=stAlertContentError]").or_(app.locator("[data-testid=stException]"))
        try:
            app.get_by_role("button", name="Check the statement").click()
            app.get_by_text("Show the details").or_(err).or_(app.locator("[data-testid=stAlertContentWarning]")).first.wait_for(timeout=600_000)
            page.wait_for_timeout(2_000)
            print(f"single check done at {time.strftime('%H:%M:%S')}")
            page.screenshot(path=str(out / "1_check.png"))
            (out / "1_check.txt").write_text(app.locator("[data-testid=stMain]").inner_text())
            app.get_by_role("tab", name="Accuracy test").click()
            app.get_by_role("button", name="Run").first.click()
            print(f"test started at {time.strftime('%H:%M:%S')}")
            app.get_by_text("Right verdict").or_(err).first.wait_for(timeout=1_200_000)
            page.wait_for_timeout(3_000)
            page.screenshot(path=str(out / "2_test.png"))
            (out / "2_test.txt").write_text(app.locator("[data-testid=stMain]").inner_text())
            btn = app.get_by_role("button", name="Download this run (JSON)")
            if btn.count():
                with page.expect_download(timeout=60_000) as d:
                    btn.first.click()
                d.value.save_as(str(out / "test.json")); print("test: saved")
            if err.count():
                raise RuntimeError("app error: " + err.first.inner_text()[:800])
            print("test finished")
        except Exception as e:
            print("FAILED:", str(e)[:1000])
            try:
                print("PAGE:", app.locator("[data-testid=stMain]").inner_text()[-1500:])
            except Exception:
                pass
            page.screenshot(path=str(out / "error.png"))
            try:
                (out / "error.txt").write_text(app.locator("[data-testid=stMain]").inner_text())
            except Exception:
                pass
            raise
    b.close()
