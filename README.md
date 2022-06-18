<p align="center">
  <img src="./src/assets/html/logo.svg" width="400" alt="">
</p>
  <h1 align="center"><a href="https://www.drivedroid.io/">DriveDroid</a> Repository Generator</h1>
  <p align="center">Generate a repository for the app that allow boot a PC using ISO files stored on your <a href="https://play.google.com/store/apps/details?id=com.softwarebakery.drivedroid">Android phone</a></p>
  </a>
  <p align="center">
    Check also an <a href="https://github.com/bobvanderlinden/distscraper">official scraper</a> written in JavaScript
  </p>
</p>

<br>

## Try Already Built Repo

Add the next link to image repositories in DriveDroid app:
```
https://flameshikari.github.io/ddrg/repo.json
```

## Contents
- [Requirements](#requirements)
- [Usage](#usage)
- [How to Make a Scraper](#how-to-make-a-scraper)
- [Misc](#misc)
- [Roadmap](#roadmap)
- [Credits](#credits)
- [License](#license)

## Requirements

Python 3.6+ with packages included in **[requirements.txt](./requirements.txt)**.

I recommend to create a venv then install packages there.

## Usage

```bash
python ./src/main.py [-i dir] [-o dir] [-g]
```

`-i dir` where **dir** is a directory with distro scrapers (**[./src/distros](./src/distros)** is default).

`-o dir` where **dir** is a directory where the built repo will be saved (**./build** is default).

`-g` will generate a webpage to present the content of repo.json.

`-h` option is available anyway.

## How to Make a Scraper

Create a folder in **[./src/distros](./src/distros)** with next structure:

```
distro_name
├── info.toml
├── logo.png
└── scraper.py
```

If **distro_name** starts with underscore (e.g. **_disabled**), it will not be counted.

Let's take a look for every file.

### `info.toml`

**info.toml** contains a distro name and a link to the official website. Arch Linux **[info.toml](./src/distros/arch/info.toml)** example:

```toml
name = "Arch Linux" # name of distro
url  = "https://example.com" # official site
```

If **info.toml** is missing or values ain't provided, fallback values will be used. Arch Linux fallback values will be next:

```toml
name = "arch" # distro folder name as value, also used in url
url  = "https://distrowatch.com/table.php?distribution=arch"
```

### `logo.png`

Should be 128x128px with transparent background. Arch Linux **[logo.png](./src/distros/arch/logo.png)** example:

<br><p align="center">
  <img src="./src/distros/arch/logo.png" alt="Arch Linux"/>
</p><br>

If **logo.png** is missing, the **[fallback logo](./src/distros/drivedroid/logo.png)** will be used:

<br><p align="center">
  <img src="./src/misc/fallback_logo.png" alt="DriveDroid Logo"/>
</p><br>

### `scraper.py`

A scraper can be written as you like, as long as it returns the desired values.

It must return an array of tuples (every tuple contains **iso_url**, **iso_arch**, **iso_size**, **iso_version** in order).

Arch Linux scraper returns next values:

```python
[
  (
    'https://mirror.yandex.ru/archlinux/iso/2021.05.01/archlinux-2021.05.01-x86_64.iso',
    'x86_64',
    792014848,
    '2021.05.01'
  ),
  (
    'https://mirror.yandex.ru/archlinux/iso/2021.06.01/archlinux-2021.06.01-x86_64.iso',
    'x86_64',
    811937792,
    '2021.06.01'
  ),
  (
    'https://mirror.yandex.ru/archlinux/iso/2021.07.01/archlinux-2021.07.01-x86_64.iso',
    'x86_64',
    817180672,
    '2021.07.01'
  ),
  (
    'https://mirror.yandex.ru/archlinux/iso/archboot/2020.07/archlinux-2020.07-1-archboot-network.iso',
    'x86_64',
    516947968,
    '2020.07'
  ),
  (
    'https://mirror.yandex.ru/archlinux/iso/archboot/2020.07/archlinux-2020.07-1-archboot.iso',
    'x86_64',
    1280491520,
    '2020.07'
  )
]
```

A scraper includes `from public import *` in top which imports next stuff to the namespace:

- **bs** (short for **BeautifulSoup**)
- **json**
- **re**
- **requests**

Also it includes these functions:

- **get_afh_url(iso_url)** — returns a download link for the file from AndroidFileHost<br>
**iso_url** must be like this: https://androidfilehost.com/?fid=8889791610682936459
- **get_iso_arch(iso_url)** — returns the used processor architecture of **iso_url**
- **get_iso_size(iso_url)** — returns the file size of **iso_url** in bytes

Arch Linux **[scraper.py](./src/distros/arch/scraper.py)** example:

```python
from public import *  # noqa


def init():

    array = []
    base_urls = [
        "https://mirror.yandex.ru/archlinux/iso/latest",
        "https://mirror.yandex.ru/archlinux/iso/archboot/latest"
    ]

    for base_url in base_urls:

        html = bs(requests.get(base_url).text, "html.parser")

        for filename in html.find_all("a", {"href": re.compile("^.*\.iso$")}):

            iso_url = f"{base_url}/{filename['href']}"
            iso_arch = get_iso_arch(iso_url)
            iso_size = get_iso_size(iso_url)
            iso_version = re.search(r"-(\d+.\d+(.\d+)?)", iso_url).group(1)

            array.append((iso_url, iso_arch, iso_size, iso_version))

    return array
```

## Misc

Here's a snippet for **[nginx](https://nginx.org/)** if you decided to self host the repository with website and you wanna access **repo.json** only by hostname via DriveDroid. Place it in **server** section of your config:

```nginx
location = / {
  if ($http_user_agent ~* 'okhttp') {
    rewrite ^/(.*)$ /repo.json break;
  }
}
```

## Roadmap

- [x] Option to generate a webpage
- [ ] Add a mechanism to retry scraping if a network error occurs
- [ ] Option to select mirrors (mainly uses mirrors based in Russia)
- [ ] Package this project perhaps
- [ ] Probably make the code better

## Credits

- [afh-dl](https://github.com/kade-robertson/afh-dl) by [kade-robertson](https://github.com/kade-robertson)
- [Yandex.Disk direct links](https://getfile.dokpub.com/yandex) by [DokPub](https://dokpub.com)



## License

**[MIT License](./LICENSE)**

Copyright © 2021 flameshikari
