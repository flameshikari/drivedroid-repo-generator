from public import *


base_urls = [
    "https://mirror.yandex.ru/mirrors/voidlinux/live/current/"
]


def init():
    array = []
    for base_url in base_urls:
        html = bs(requests.get(base_url).text, "html.parser")
        for filename in html.find_all("a"):
            filename = filename.get("href")
            if filename.endswith(".iso"):
                iso_url = base_url + filename
                iso_arch = get_iso_arch(iso_url)
                iso_size = get_iso_size(iso_url)
                iso_version = re.search(r"-(\d{8})", iso_url).group(1)
                array.append((iso_url, iso_arch, iso_size, iso_version))
    return array
