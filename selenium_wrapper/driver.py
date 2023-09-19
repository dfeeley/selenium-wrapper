import logging
import os
import tempfile
import time

from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from .history import History
from .logger import Logger
from .exceptions import WrappedException

logger = Logger(logging.getLogger(__name__))


class Driver:
    BY_CONDITIONS = {
        "presence_of_element_located",
        "element_to_be_clickable",
    }

    def __init__(self, driver, debug=False, **kwargs):
        self.driver = driver
        self.debug = debug
        self.session_id = self.driver.session_id
        self.log_root = kwargs.get("log_root", tempfile.gettempdir())
        self.log_dir = os.path.join(self.log_root, self.session_id)
        self._ensure_log_dir_exists()
        self.default_wait = kwargs.get("page_load_wait", 5)
        self.handle_method = kwargs.get("handle_method", "break")
        self.history = History(self.log_dir)

    def get(self, url, wait=None):
        logger.debug("Get", url)
        try:
            self.driver.get(url)
        except WebDriverException as ex:
            logger.error("Error", f"Failed to get url {url}, underlying exception {ex}")
            if self.handle_method == "break":
                breakpoint()
            else:
                raise WrappedException("Failed to get url {url}", ex)
        wait = wait if wait is not None else self.default_wait
        if wait:
            logger.debug(
                "", f"Get complete, now waiting {wait} seconds for any JS updates"
            )
            self.sleep(wait)
            logger.debug("", "back from wait")
        if self.debug:
            self.history.record(
                url, self.full_page_source, self.driver.get_screenshot_as_png()
            )

    def quit(self, sleep=None):
        if self.debug:
            self.history.write()
        if sleep:
            self.sleep(sleep)
        self.driver.quit()

    def __getattr__(self, attr):
        if hasattr(self.driver, attr):
            return getattr(self.driver, attr)
        raise AttributeError(attr)

    @property
    def full_page_source(self):
        body = self.driver.execute_script("return document.body.innerHTML")
        return f"<html><body>{body}</body></html>"

    def sleep(self, seconds):
        logger.debug("Sleep", f"{seconds} seconds")
        time.sleep(seconds)

    def find(self, selector, by="css_selector", handle="raise"):
        logger.debug("Find", f"{selector!r}")
        method = getattr(self, f"find_element_by_{by}")
        try:
            elem = method(selector)
            logger.debug("", "Find successful")
            return elem
        except NoSuchElementException:
            logger.warn("", f"...{selector!r} not found!")
            if handle == "ignore":
                return
            elif handle == "raise":
                raise
            elif handle == "quit":
                self.quit()
            elif handle == "debug":
                breakpoint()
            else:
                raise ValueError(
                    f"Invalid handle value {handle!r} passed to find."
                    f"Options are raise, ignore, quit, debut"
                )

    def wait_for(
        self,
        selector,
        by="css_selector",
        condition="presence_of_element_located",
        timeout=20,
    ):
        logger.debug("Wait", f"{selector!r} / {condition!r}")
        cond = getattr(EC, condition)
        if condition in self.BY_CONDITIONS:
            by = getattr(By, by.upper())
            condition_param = (by, selector)
        else:
            condition_param = selector
        try:
            elem = WebDriverWait(self.driver, timeout).until(cond(condition_param))
            logger.debug("", f"Wait success, found the waited for element {selector!r}")
            return elem
        except TimeoutException:
            logger.warn(
                "",
                f"Wait fail, did not find the waited for element {selector!r} in {timeout} seconds",
            )
            if self.handle_method == "break":
                breakpoint()
            else:
                self.quit()

    def get_select(self, selector, by="css_selector"):
        elem = self.find(selector, by=by)
        return Select(elem)

    def _ensure_log_dir_exists(self):
        if os.path.exists(self.log_dir):
            # hmm, what to do here
            logger.warn("Setup", f"Log dir {self.log_dir!r} already exists!")
        else:
            logger.debug("Setup", f"Creating logdir {self.log_dir!r}")
            os.makedirs(self.log_dir)
        logger.debug("Setup", f"file://{self.log_dir}/index.htm")
