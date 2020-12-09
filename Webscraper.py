# !./venv/Scripts/python

import os
import re
import webbrowser

import pandas as pd
import pandas.io.formats.style
import requests
from bs4 import BeautifulSoup


def main():

    urlStr = r"http://eu.nkon.nl/rechargeable/li-ion/18650-size.html"  # Site to scrape and visualizue - the html tags are set up for nkon.nl
    battLink = []  # List for link
    battPrice = []  # List for crice
    battCapacity = []  # List for capacity
    battPower = []  # List for power
    battStock = []  # List for availability
    battRefurbished = []  # List for refurbished products

    proxies = {  # proxies if needed
        # "http": "http://user:pass@address:port",
        # "https": "http://user:pass@address:port",
    }

    # Parse website
    page = requests.get(urlStr, proxies=proxies)
    soup = BeautifulSoup(page.content, "html.parser")

    # Loop throug listed products and extract the information
    for batt in soup.find_all("div", {"class": "category-products-grid per-product"}):
        price = ""
        href = ""
        capacity = ""
        power = ""
        stock = ""
        refurbished = False

        # Price
        if batt.find("span", {"itemprop": "price"}) is not None:
            searchtext = batt.find("span", {"itemprop": "price"}).text
            m = re.search(r"[\d,.]+", searchtext)
            price = m.group(0).replace(",", ".") if m else None
        battPrice.append(float(price)) if price else battPrice.append(None)
        # Link
        if (
            batt.find("h2", {"class": "product-name"}).contents[0].get("href")
            is not None
        ):
            href = batt.find("h2", {"class": "product-name"}).contents[0].get("href")
        battLink.append(href) if href else battLink.append(None)
        # Capacity, power, refurbished
        battTitle = batt.find("h2", {"class": "product-name"}).contents[0].get("title")
        if battTitle is not None:
            # Capacity
            match = re.search(r"([\d,.]+)mAh(?=$| )", battTitle)
            capacity = match.group(1).replace(",", ".") if match is not None else ""
            # Power
            match2 = re.search(r"(?<= )([\d,.]+)A(?=$| )", battTitle)
            power = match2.group(1).replace(",", ".") if match2 is not None else ""
            # Refurbished
            refurbished = "refurbished" in battTitle.lower()
        battRefurbished.append(refurbished)
        battCapacity.append(float(capacity)) if capacity else battCapacity.append(None)
        battPower.append(float(power)) if power else battPower.append(None)
        # Availability
        if (
            batt.find("div", {"class": "actions-cart"}).contents[1].get("class")
            is not None
        ):
            if "out-of-stock" in batt.find("div", {"class": "actions-cart"}).contents[
                1
            ].get("class"):
                stock = False
            else:
                stock = True
        battStock.append(stock) if stock != "" else battStock.append(None)

    # Merge all lists into one dataframe
    df = pd.DataFrame(
        {
            r"Price in €": battPrice,
            "Capacity in mAh": battCapacity,
            "Power in A": battPower,
        }
    )
    df[r"Price per capacity in €/Ah"] = (
        df[r"Price in €"] * 1000 / df["Capacity in mAh"]
    )  # Add the price/Ah
    df["In Stock"] = battStock
    df["Refurbished"] = battRefurbished
    df["Product Link"] = battLink
    df.sort_values(  # Sort for availability, capacity, power
        by=["In Stock", "Price per capacity in €/Ah", "Power in A"],
        inplace=True,
        ascending=[False, True, True],
    )
    df.reset_index(drop=True, inplace=True)

    # Uncomment for .csv export
    # df.to_csv('Nkon.nl_battery_overview.csv',
    #           index=False, encoding='utf-8-sig', sep=';', decimal=',')

    # Export dataframe to htlm and open with browser for viewing
    df.index += 1  # Add 1 for index to start from 1 in table
    write_to_html_file(df.round(2), filename="18650-overview.html")

    # Finish
    print("Successful export.")


def write_to_html_file(df, title="", filename="out.html"):
    """
    Write an entire dataframe to an HTML file with nice formatting.
    """

    # Add the CSS styling
    result = """
<html>
<head>
<style>

    h2 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    table { 
        margin-left: auto;
        margin-right: auto;
    }
    table, th, td {
        border: 1px solid white;
        border-collapse: collapse;
    }
    th {
        position: -webkit-sticky;
        position: sticky;
        background-color: #dddddd;
        top: 0;
        z-index: 2;
        padding: 6px;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 90%;
    }
    td {
        padding: 6px;
        text-align: left;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 90%;
    }
    table tbody tr:hover {
        background-color: #dddddd;
    }
    .wide {
        width: 90%; 
    }

</style>
</head>
<body>
    """

    result += "<h2> %s </h2>\n" % title
    if type(df) == pd.io.formats.style.Styler:
        result += df.render()
    else:
        result += df.to_html(escape=False, render_links=True)  # classes='wide',

    result += """
</body>
</html>
"""

    # Write results and open the file in the browser
    with open(filename, "w") as f:
        f.write(result)

    filename = "file:///" + os.getcwd() + "/" + filename
    webbrowser.open_new_tab(filename)


if __name__ == "__main__":
    main()
