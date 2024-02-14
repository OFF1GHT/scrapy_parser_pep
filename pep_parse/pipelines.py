import csv
from collections import defaultdict
from datetime import datetime as dt

from .settings import BASE_DIR, RESULTS_DIR, DT_FORM


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses = defaultdict(int)
        self.processed_count = 0

    def process_item(self, item, spider):
        self.statuses[item['status']] += 1
        self.processed_count += 1
        return item

    def close_spider(self, spider):
        time = dt.now().strftime(DT_FORM)
        filename = f'status_summary_{time}.csv'
        results_dir = BASE_DIR / RESULTS_DIR
        results_dir.mkdir(parents=True, exist_ok=True)
        path = results_dir / filename
        rows = []
        headers = ['Status', 'Count']
        rows.append(headers)
        for status, count in self.statuses.items():
            rows.append([status, count])
        rows.append(['Total Processed Items', self.processed_count])

        with open(path, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(rows)
