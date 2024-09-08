import os
import tempfile
from dataclasses import dataclass

from bs4 import BeautifulSoup
from PIL import Image
from utils import WWW, File, Log

log = Log('Parser')


@dataclass
class Candidate:
    row_num: int
    name: str

    @property
    def name_initials(self):
        return ''.join([word[0] for word in self.name.split()]).upper()

    @property
    def image_path(self):
        return os.path.join(
            'data', 'images', f'{self.row_num}-{self.name_initials}.png'
        )

    @property
    def image_path_unix(self):
        return self.image_path.replace(os.path.sep, '/')

    @property
    def readme_row(self):
        return (
            f'| <img src="{self.image_path_unix}" width="48" /> '
            + '| {self.name} |  |'
        )

    RAW_HTML_PATH = os.path.join('data', 'raw.html')
    URL_BASE = 'https://eservices.elections.gov.lk/pages/'

    def download(self, url_image):
        if os.path.exists(self.image_path):
            return

        temp_image_path = tempfile.mktemp(suffix='.png')
        WWW.download_binary(url_image, temp_image_path)
        im = Image.open(temp_image_path)
        im_rgba = im.convert('RGBA')

        for y in range(im_rgba.height):
            for x in range(im_rgba.width):
                r, g, b, __ = im_rgba.getpixel((x, y))
                brightness = (r + g + b) / 3
                if brightness > 128:
                    im_rgba.putpixel((x, y), (255, 255, 255, 0))
                else:
                    im_rgba.putpixel((x, y), (0, 0, 0, 255))

        # resize to 256 x 256
        im_rgba = im_rgba.resize((256, 256))

        im_rgba.save(self.image_path)
        log.info(f'Downloaded {url_image} to {self.image_path}')

    @staticmethod
    def list_all():
        html = File(Candidate.RAW_HTML_PATH).read()
        table = BeautifulSoup(html, 'html.parser')

        candidate_list = []
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) != 3:
                continue
            td_row_num, td_image, td_name = tds
            row_num = int(td_row_num.text)
            url_image = Candidate.URL_BASE + td_image.find('img')['src']
            name = td_name.text

            candidate = Candidate(row_num, name)
            candidate.download(url_image)

            candidate_list.append(candidate)

        log.info(f'Found {len(candidate_list)} candidates')
        return candidate_list


if __name__ == '__main__':
    Candidate.list_all()
