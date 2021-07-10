from public import *  # noqa


base_urls = [
    "https://sourceforge.net/projects/archbang/rss?path=/ArchBang/",
    "https://sourceforge.net/projects/archbang/rss?path=/ArchBang32/",
    "https://sourceforge.net/projects/archbang/rss?path=/Vintage-ArchBang/"
]


def init():
    array = []
    for base_url in base_urls:
        xml = bs(requests.get(base_url).text, "xml")
        values = xml.find_all("item")
        for i in values:
            content = i.find("content")
            iso_url = content["url"][:-9]
            iso_arch = get_iso_arch(iso_url)
            iso_size = int(content["filesize"])
            if "Vintage-ArchBang" in base_url:
                iso_version = re.search(r"-(\d{4}.\d{2}.\d{2})", iso_url) \
                                .group(1)
            else:
                iso_version = re.search(r"-(\d{4})", iso_url).group(1)
            array.append((iso_url, iso_arch, iso_size, iso_version))
    return array
