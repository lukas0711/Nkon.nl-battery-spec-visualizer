[![license-badge][]][license-link] [![stars-badge][]][star-link] [![issues-badge][]][issues-link] [![maintenance-badge]][maintenance-link]


# Nkon.nl-battery-spec-visualizer
The script summarizes the battery online shop [nkon.nl](https://eu.nkon.nl/rechargeable/li-ion/18650-size.html) in a readable table format. This offers a fast overview of the best battery offers for your project. The script creates a html table and opens it with your browser. The table is sorted for price per capacity in descending order. Batteries that are out of stock are shown at the botom.

The table shows ``Price in €``, ``Capacity in mAh``, ``Power in A``, ``Price per capacity in €/Ah``, ``In Stock``, ``Refurbished`` and the ``Product Link``.

## Configuration
Enter the page you want to summarize.
```python
urlStr = r"http://eu.nkon.nl/rechargeable/li-ion/18650-size.html"
```

Uncomment the lines to export the summarized data to .csv.
```python
# df.to_csv('Nkon.nl_battery_overview.csv',
#           index=False, encoding='utf-8-sig', sep=';', decimal=',')
```

Enter your proxy server.
```python
proxies = {  # proxies if needed
    "http": "http://user:pass@address:port",
    "https": "http://user:pass@address:port",
}
```

## Installation
Install all python package requirements through the pip command  
``pip install -r requirements.txt``

## Credits
This project was inspired by L0laapk3's [nkon.nl-spec-sorter](https://github.com/L0laapk3/nkon.nl-spec-sorter/).

[license-badge]:        https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square
[license-link]:         https://choosealicense.com/licenses/mit/
[stars-badge]:          https://img.shields.io/github/stars/lukas0711/Nkon.nl-battery-spec-visualizer?style=flat-square
[star-link]:            https://github.com/lukas0711/Nkon.nl-battery-spec-visualizer/
[issues-badge]:         https://img.shields.io/github/issues/lukas0711/Nkon.nl-battery-spec-visualizer?style=flat-square
[issues-link]:          https://github.com/lukas0711/Nkon.nl-battery-spec-visualizer/issues/
[maintenance-badge]:    https://img.shields.io/maintenance/yes/2021?style=flat-square
[maintenance-link]:     https://github.com/lukas0711/Nkon.nl-battery-spec-visualizer/graphs/commit-activity