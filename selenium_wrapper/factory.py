import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from .driver import Driver


def remote(url, browser="chrome", **kwargs):
    if browser != "chrome":
        raise ValueError(f"Browser {browser} not currently supported")

    options = _options(**kwargs)
    prefs = {
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "download.default_directory": "/home/seluser/Downloads",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)
    capabilities = getattr(DesiredCapabilities, browser.upper())
    driver = webdriver.Remote(url, capabilities, options=options)
    return Driver(driver, **kwargs)


def local(browser="chrome", **kwargs):
    if browser == "chrome":
        exec = "chromedriver"
    else:
        raise ValueError(f"Browser {browser} not currently supported")
    options = _options(**kwargs)
    driver = webdriver.Chrome(exec, options=options)
    if kwargs.get("headless", False):
        download_dir = kwargs.get("download-dir", os.path.expanduser("~/Downloads"))
        params = {"behavior": "allow", "downloadPath": download_dir}
        driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
    return Driver(driver, **kwargs)


def _options(**kwargs):
    options = Options()
    options.headless = kwargs.get("headless", False)
    default_user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/96.0.4664.110 Safari/537.36"
    )
    user_agent = kwargs.get("user_agent", default_user_agent)
    data_dir = kwargs.get(
        "user_data_dir", os.path.expanduser("~/.config/google-chrome-auto")
    )
    window_size = kwargs.get("window_size", "2560,1440")
    profile = kwargs.get("profile", "Default")
    options.add_argument("disable-gpu")
    options.add_argument(f"window-size={window_size}")
    options.add_argument(f"user-data-dir={data_dir}")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument(f"profile-directory={profile}")
    # options.add_argument("remote-debugging-port=9222")
    # options.add_argument("remote-debugging-address=0.0.0.0")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)
    return options
