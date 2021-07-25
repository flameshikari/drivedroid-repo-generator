from public import *  # noqa


def init():

    array = []
    base_url = "https://siduction.org/installation-media"

    html = bs(requests.get(base_url).text, "html.parser")
    regex = re.compile("^.*stuttgart.de.*\.iso$")

    for target in html.find_all("a", {"href": regex}):

        iso_url = target["href"]
        iso_arch = get_iso_arch(iso_url)
        iso_size = get_iso_size(iso_url)
        iso_version = re.search(r"-(\d+\.\d+\.\d+)", iso_url).group(1)

        array.append((iso_url, iso_arch, iso_size, iso_version))

    return array