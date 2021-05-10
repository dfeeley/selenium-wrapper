# Selenium Wrapper

Convenience wrapper for Selenium webdriver.

Wraps the basic functionality of get, find, and wait for logging and 
exception handling.

Also includes a factory for constructing either local or remote webdrivers.

In local mode console will be viewable at http://localhost:4444/wd/hub/static/resource/hub.html

```python
from selenium_wrapper import factory

driver = factory.local(debug=True, handle_method='break', log_root='/tmp/selenium', headless=True)

driver.get('http://www.example.com', wait=0)

driver.find('#username').send_keys('myuser')
driver.find('#password').send_keys('mypassword')
driver.find('#login').click()

driver.wait('.some .selector')

driver.get('https://www.example.com/next', wait=4)

elem = driver.find('table tbody tr td:nth-child(2)')
print(elem.text)

driver.quit()
```
