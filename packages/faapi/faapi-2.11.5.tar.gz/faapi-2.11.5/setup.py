# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faapi']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'cfscrape>=2.1.1,<3.0.0',
 'lxml>=4.6.0,<5.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'faapi',
    'version': '2.11.5',
    'description': 'Python module to implement API-like functionality for the FurAffinity.net website.',
    'long_description': '# Fur Affinity API\n\n[![version_pypi](https://img.shields.io/pypi/v/faapi?logo=pypi)](https://pypi.org/project/faapi/)\n[![version_gitlab](https://img.shields.io/badge/dynamic/json?logo=gitlab&color=orange&label=gitlab&query=%24%5B%3A1%5D.name&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2Fmatteocampinoti94%252Ffaapi%2Frepository%2Ftags)](https://gitlab.com/MatteoCampinoti94/FAAPI)\n[![version_python](https://img.shields.io/pypi/pyversions/faapi?logo=Python)](https://www.python.org)\n\n[![issues_gitlab](https://img.shields.io/badge/dynamic/json?logo=gitlab&color=orange&label=issues&suffix=%20open&query=%24.length&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2Fmatteocampinoti94%252Ffaapi%2Fissues%3Fstate%3Dopened)](https://gitlab.com/MatteoCampinoti94/FAAPI/issues)\n[![issues_github](https://img.shields.io/github/issues/matteocampinoti94/faapi?logo=github&color=blue)](https://github.com/MatteoCampinoti94/FAAPI/issues)\n\nPython module to implement API-like functionality for the FurAffinity.net website\n\n## Requirements\n\nPython 3.8+ is necessary to run this module.\n\nThis module requires the following pypi modules:\n\n* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)\n* [cfscrape](https://github.com/Anorov/cloudflare-scrape)\n* [lxml](https://github.com/lxml/lxml/)\n* [requests](https://github.com/requests/requests)\n* [python-dateutil](https://github.com/dateutil/dateutil/)\n\n## Usage\n\nThe API is comprised of a main class `FAAPI` and two submission classes: `Submission` and `SubmissionPartial`.\nOnce `FAAPI` is initialized its method can be used to crawl FA and return machine-readable objects.\n\n```python\nimport faapi\nimport json\n\ncookies = [\n    {"name": "a", "value": "38565475-3421-3f21-7f63-3d341339737"},\n    {"name": "b", "value": "356f5962-5a60-0922-1c11-65003b703038"},\n]\n\napi = faapi.FAAPI(cookies)\nsub, sub_file = api.get_submission(12345678,get_file=True)\n\nprint(sub.id, sub.title, sub.author, f"{len(sub_file)/1024:02f}KiB")\n\nwith open(f"{sub.id}.json", "w") as f:\n    f.write(json.dumps(sub))\n\nwith open(sub.file_url.split("/")[-1], "wb") as f:\n    f.write(sub_file)\n\ngallery, _ = api.gallery("user_name", 1)\nwith open("user_name-gallery.json", "w") as f:\n    f.write(json.dumps(gallery))\n```\n\n### robots.txt\n\nAt init, the `FAAPI` object downloads the [robots.txt](https://www.furaffinity.net/robots.txt) file from FA to determine the `Crawl-delay` value set therein. If not set, a value of 1 second is used.\n\nTo respect this value, the default behaviour of of the `FAAPI` object is to wait when a get request is made if the last request was performed more recently then the crawl delay value.\n\nSee under [FAAPI](#faapi) for more details on this behaviour.\n\nFurthermore, any get operation that points to a disallowed path from robots.txt will raise an exception. This check should not be circumvented and the developer of this module does not take responsibility for violations of the TOS of Fur Affinity.\n\n### Cookies\n\nTo access protected pages, cookies from an active session are needed. These cookies must be given to the FAAPI object as a list of dictionaries, each containing a `name` and a `value` field. The cookies list should look like the following random example:\n\n```python\ncookies = [\n    {"name": "a", "value": "38565475-3421-3f21-7f63-3d341339737"},\n    {"name": "b", "value": "356f5962-5a60-0922-1c11-65003b703038"},\n]\n```\n\nOnly cookies `a` and `b` are needed.\n\nTo access session cookies, consult the manual of the browser used to login.\n\n*Note:* it is important to not logout of the session the cookies belong to, otherwise they will no longer work.\n\n## FAAPI\n\nThis is the main object that handles all the calls to scrape pages and get submissions.\n\nIt holds 6 different fields:\n\n* `cookies: List[dict] = []` cookies passed at init\n* `session: CloudflareScraper` cfscrape session used for get requests\n* `robots: Dict[str, List[str]]` robots.txt values\n* `crawl_delay: float` crawl delay from robots.txt, else 1\n* `last_get: float` time of last get (not UNIX time, uses `time.perf_counter` for more precision)\n* `raise_for_delay: bool = False` if set to `True`, raises an exception if a get call is made before enough time has passed\n\n### Init\n\n`__init__(cookies: List[dict] = None)`\n\nThe class init has a single optional argument `cookies` necessary to read logged-in-only pages.\nThe cookies can be omitted and the API will still be able to access public pages.\n\n*Note:* Cookies must be in the format mentioned above in [#Cookies](#cookies).\n\n### Methods & Properties\n\n* `load_cookies(cookies: List[Dict[str, Any]])`<br>\nLoad new cookies in the object and remake the `CloudflareScraper` session.\n* `connection_status -> bool`<br>\nReturns the status of the connection.\n* `get(path: str, **params) -> requests.Response`<br>\nThis returns a response object containing the result of the get operation on the given url with the optional `**params` added to it (url provided is considered as path from \'https://www.furaffinity.net/\').\n* `get_parse(path: str, **params) -> bs4.BeautifulSoup`<br>\nSimilar to `get()` but returns the parsed  HTML from the normal get operation.\n* `get_submission(submission_id: int, get_file: bool = False) -> Tuple[Submission, Optional[bytes]]`<br>\nGiven a submission ID, it returns a `Submission` object containing the various metadata of the submission itself and a `bytes` object with the submission file if `get_file` is passed as `True`.\n* `get_submission_file(submission: Submission) -> Optional[bytes]`<br>\nGiven a submission object, it downloads its file and returns it as a `bytes` object.\n* `userpage(user: str) -> Tuple[str, str, bs4.BeautifulSoup]`<br>\nReturns the user\'s full display name - i.e. with capital letters and extra characters such as "_" -, the user\'s status - the first character found beside the user name - and the parsed profile text as a parsed object.\n* `gallery(user: str, page: int = 1) -> Tuple[List[SubmissionPartial], int]`<br>\nReturns the list of submissions found on a specific gallery page and the number of the next page. The returned page number is set to 0 if it is the last page.\n* `scraps(user: str, page: int = 1) -> -> Tuple[List[SubmissionPartial], int]`<br>\nReturns the list of submissions found on a specific scraps page and the number of the next page. The returned page number is set to 0 if it is the last page.\n* `favorites(user: str, page: str = "") -> Tuple[List[SubmissionPartial], str]`<br>\nDownloads a user\'s favorites page. Because of how favorites pages work on FA, the `page` argument (and the one returned) are strings. If the favorites page is the last then an empty string is returned as next page. An empty page value as argument is equivalent to page 1.<br>\n*Note:* favorites page "numbers" do not follow any scheme and are only generated server-side.\n* `journals(user: str, page: int = 1) -> -> Tuple[List[Journal], int]`<br>\nReturns the list of submissions found on a specific journals page and the number of the next page. The returned page number is set to 0 if it is the last page.\n* `search(q: str = "", page: int = 0, **params) -> Tuple[List[SubmissionPartial], int, int, int, int]`<br>\nParses FA search given the query (and optional other params) and returns the submissions found and the next page together with basic search statistics: the number of the first submission in the page (0-indexed), the number of the last submission in the page (0-indexed), and the total number of submissions found in the search. For example if the the last three returned integers are 0, 47 and 437, then the the page contains submissions 1 through 48 of a search that has found a total of 437 submissions.<br>\n*Note:* as of October 2020 the "/search" path is disallowed by Fur Affinity\'s robots.txt.\n* `user_exists(user: str) -> int`<br>\nChecks if the passed user exists - i.e. if there is a page under that name - and returns an int result.\n    * 0 okay\n    * 1 account disabled\n    * 2 system error\n    * 3 unknown error\n    * 4 request error\n* `submission_exists(submission_id: int) -> int`<br>\nChecks if the passed submissions exists - i.e. if there is a page with that ID - and returns an int result.\n    * 0 okay\n    * 1 account disabled\n    * 2 system error\n    * 3 unknown error\n    * 4 request error\n* `journal_exists(journal_id: int) -> int`<br>\nChecks if the passed journal exists - i.e. if there is a page under that ID - and returns an int result.\n    * 0 okay\n    * 1 account disabled\n    * 2 system error\n    * 3 unknown error\n    * 4 request error\n\n\n## Journal\n\nThis object contains information gathered when parsing a journals page or a specific journal page. It contains the following fields:\n\n* `id` journal id\n* `title` journal title\n* `date` upload date in YYYY-MM-DD format\n* `author` journal author\n* `content` journal content\n\n`Journal` objects can be directly casted to a dict object or iterated through.\n\n### Init\n\n`__init__(journal_item: Union[bs4.element.Tag, bs4.BeautifulSoup] = None)`\n\n`Journal` takes one optional parameters: a journal section tag from a journals page or a parsed journal page. Parsing is then performed based on the class of the passed object.\n\nThe tag/page is saved as an instance variable of the same name\n\n### Methods\n\n* `parse()`<br>\nParses the stored journal tag/page for information.\n\n## SubmissionPartial\n\nThis lightweight submission object is used to contain the information gathered when parsing gallery, scraps, favorites and search pages. It contains only the following fields:\n\n* `id` submission id\n* `title` submission title\n* `author` submission author\n* `rating` submission rating [general, mature, adult]\n* `type` submission type [text, image, etc...]\n\n`SubmissionPartial` objects can be directly casted to a dict object or iterated through.\n\n### Init\n\n`__init__(submission_figure: bs4.element.Tag)`\n\n`SubmissionPartial` init needs a figure tag taken from a parsed page. The tag is saved as an instance variable of the same name.\n\n### Methods\n\n* `parse()`<br>\nParses the stored submission figure tag for information.\n\n## Submission\n\nThe main class that parses and holds submission metadata.\n\n* `id` submission id\n* `title` submission title\n* `author` submission author\n* `date` upload date in YYYY-MM-DD format\n* `tags` tags list\n* `category` category \\*\n* `species` species \\*\n* `gender` gender \\*\n* `rating` rating \\*\n* `description` the description as an HTML formatted string\n* `file_url` the url to the submission file\n\n\\* these are extracted exactly as they appear on the submission page\n\n`Submission` objects can be directly casted to a dict object and iterated through.\n\n### Init\n\n`__init__(submission_page: bs4.BeautifulSoup = None)`\n\nTo initialise the object, An optional `bs4.BeautifulSoup` object is needed containing the parsed HTML of a submission page.\n\nThe `submission_page` argument is saved as an instance variable and is then parsed to obtain the other fields.\n\nIf no `submission_page` is passed then the object fields will remain at their default - empty - value.\n\n### Methods\n\n* `parse()`<br>\nParses the stored submission page for metadata.\n\n## Contributing\n\nAl contributions and suggestions are welcome!\n\nThe only requirement is that any merge request must be sent to the GitLab project as the one on GitHub is only a mirror: [GitLab/FALocalRepo](https://gitlab.com/MatteoCampinoti94/FALocalRepo)\n\nIf you have suggestions for fixes or improvements, you can open an issue with your idea, see [#Issues](#issues) for details.\n\n## Issues\n\nIf any problem is encountered during usage of the program, an issue can be opened on the project\'s pages on [GitLab](https://gitlab.com/MatteoCampinoti94/FAAPI/issues) (preferred) or [GitHub](https://github.com/MatteoCampinoti94/FAAPI/issues) (mirror repository).\n\nIssues can also be used to suggest improvements and features.\n\nWhen opening an issue for a problem, please copy the error message and describe the operation in progress when the error occurred.\n',
    'author': 'Matteo Campinoti',
    'author_email': 'matteo.campinoti94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/MatteoCampinoti94/FAAPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
