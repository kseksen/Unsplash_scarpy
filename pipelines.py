# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from scrapy.exceptions import DropItem

class CSVWriterPipeline:
    
    def open_spider(self, spider):
        # Open CSV file for writing
        self.file = open('images_data.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        # Write the header row to the CSV file
        self.writer.writerow(['image_url', 'image_path', 'title', 'category'])

    def close_spider(self, spider):
        # Close the CSV file when the spider is done
        self.file.close()

    def process_item(self, item, spider):
        # Ensure that the image has been downloaded successfully
        if 'images' in item:
            # Retrieve the downloaded image's path from the ImagesPipeline
            image_path = item['images'][0]['path']
            item['image_path'] = image_path
            # Write the item data (image_url, image_path, title, category) to the CSV file
            self.writer.writerow([item['image_url'], item['image_path'], item['title'], item['category']])
            return item
        else:
            # Drop the item if the image could not be downloaded
            raise DropItem("Missing image in %s" % item)
