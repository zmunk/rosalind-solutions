import re
import requests
from urllib.parse import quote

from utils import get_dataset


def create_url(start_date, end_date, org_name):
    """
    param start_date / end_date: e.g. "2003/7/25"
    """
    date_filter = f'"{start_date}"[Publication Date] : "{end_date}"[Publication Date]'
    org_filter = f" AND {org_name}[Organism]"
    return (
        "https://www.ncbi.nlm.nih.gov/nuccore"
        + "?"
        + "term="
        + "(("
        + quote(date_filter, safe="")
        + "))"
        + quote(org_filter)
    )


assert (
    create_url("2003/7/25", "2005/12/27", "Anthoxanthum")
    == "https://www.ncbi.nlm.nih.gov/nuccore?term=((%222003%2F7%2F25%22%5BPublication%20Date%5D%20%3A%20%222005%2F12%2F27%22%5BPublication%20Date%5D))%20AND%20Anthoxanthum%5BOrganism%5D"
)


def count_results(url, verbose=0):
    if verbose > 0:
        print("making request...")
    res = requests.get(url)
    assert res.status_code == 200
    if verbose > 1:
        print(res.text)
    items_text = next(
        re.finditer(r'<h2 class="result_count">(.*)</h2>', res.text)
    ).group(1)
    if verbose > 0:
        print(items_text)
    assert items_text.split()[0] == "Items:"
    return int(items_text.split()[-1])


def test():
    assert count_results(create_url("2003/7/25", "2005/12/27", "Anthoxanthum")) == 7
    assert (
        count_results(
            "https://www.ncbi.nlm.nih.gov/nuccore?term=(((%222003/7/25%22%5BPublication%20Date%5D%20:%20%222005/12/27%22%5BPublication%20Date%5D))%20AND%20Anthoxanthum)"
        )
        == 54
    )


sample = """
Anthoxanthum
2003/7/25
2005/12/27
""".strip()

if __name__ == "__main__":
    inp = (get_dataset(__file__) or sample).split("\n")
    org_name = inp[0]
    start_date = inp[1]
    end_date = inp[2]
    print(count_results(create_url(start_date, end_date, org_name)))
