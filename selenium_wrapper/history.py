import logging
import os

logger = logging.getLogger(__name__)


class History:
    class Entry:
        def __init__(self, url, page_source, screenshot):
            self.url = url
            self.page_source = page_source
            self.screenshot = screenshot

    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.history = []

    def record(self, url, page_source, screenshot):
        self.history.append(
            self.Entry(url, page_source, screenshot)
        )
        self.write(entry_idx=len(self.history) - 1)

    def write(self, entry_idx=None):
        if entry_idx is not None:
            self.write_entry(entry_idx)
        else:
            for idx, entry in enumerate(self.history):
                self.write_entry(idx)
        self.write_index()

    def write_entry(self, idx):
        entry = self.history[idx]
        fidx = f'{idx + 1:02d}'

        # save the page source
        with open(os.path.join(self.log_dir, f'{fidx}.htm'), 'w') as f:
            f.write(entry.page_source)

        # save the screenshot
        with open(os.path.join(self.log_dir, f'{fidx}.png'), 'wb') as f:
            f.write(entry.screenshot)

    def write_index(self):
        index_links = []
        for idx, entry in enumerate(self.history):
            fidx = f'{idx + 1:02d}'
            index_links.append(
                f"""
                <div>
                    <span>{fidx}:</span>
                    <a href="{fidx}.htm" target="iframe_main" title="{entry.url}">Source</a> |
                    <a href="{fidx}.png" target="iframe_main" title="{entry.url}">Screenshot</a>
                    <span>{entry.url}</span>
                </div>
                """
            )
        index_html = """
        <html>
            <body>
                <div id="sidebar" style="float:left">
                    {index_links}
                </div>
                <iframe name="iframe_main" src="" width="100%" height="100%">
                </iframe>
            <body>
        </html>
        """.format(index_links=''.join(index_links))
        with open(os.path.join(self.log_dir, 'index.htm'), 'w') as f:
            f.write(index_html)
