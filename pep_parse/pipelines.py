import csv
from collections import defaultdict
from datetime import datetime as dt
from .settings import BASE_DIR, RESULTS


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses = defaultdict(int)
        self.processed_count = 0

    def process_item(self, item, spider):
        self.statuses[item['status']] += 1
        self.processed_count += 1
        return item

    def close_spider(self, spider):
        time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{time}.csv'
        results_dir = BASE_DIR / RESULTS
        results_dir.mkdir(parents=True, exist_ok=True)
        path = results_dir / filename

        with open(path, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            headers = ['Status', 'Count']
            csv_writer.writerow(headers)
            for status, count in self.statuses.items():
                csv_writer.writerow([status, count])
            csv_writer.writerow(
                ['Total Processed Items', self.processed_count]
            )
