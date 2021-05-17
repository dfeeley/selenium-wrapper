import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from .driver import Driver


def remote(url, browser='chrome', headless=False, **kwargs):
    if browser != 'chrome':
        raise ValueError(f'Browser {browser} not currently supported')

    options = Options()
    options.headless = headless
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--remote-debugging-address=0.0.0.0')
    options.add_argument('--user-data-dir=/home/seluser/custom_profile')
    options.add_argument('--profile-directory=AutoProfile')

    prefs = {
        "profile.default_content_settings.popups": 0,
        'profile.default_content_setting_values.automatic_downloads': 1,
        "download.default_directory": "/home/seluser/Downloads",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option('prefs', prefs)
    capabilities = getattr(DesiredCapabilities, browser.upper())
    driver = webdriver.Remote(url, capabilities, options=options)
    return Driver(driver, **kwargs)


def local(browser='chrome', headless=False, **kwargs):
    if browser == 'chrome':
        exec = 'chromedriver'
    else:
        raise ValueError(f'Browser {browser} not currently supported')
    options = Options()
    options.headless = headless
    driver = webdriver.Chrome(exec, options=options)
    if headless:
        params = {'behavior': 'allow', 'downloadPath': os.path.expanduser('~/Downloads')}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    return Driver(driver, **kwargs)
