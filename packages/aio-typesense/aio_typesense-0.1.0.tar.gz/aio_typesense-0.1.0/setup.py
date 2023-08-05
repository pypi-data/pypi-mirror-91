# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_typesense']

package_data = \
{'': ['*']}

install_requires = \
['httpx']

extras_require = \
{':python_version >= "3.6" and python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'aio-typesense',
    'version': '0.1.0',
    'description': 'Async library for Typesense',
    'long_description': '[![Tests](https://github.com/devtud/aio_typesense/workflows/Tests/badge.svg)](https://github.com/devtud/aio_typesense/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/devtud/aio_typesense/branch/main/graph/badge.svg)](https://codecov.io/gh/devtud/aio_typesense)\n![pypi](https://img.shields.io/pypi/v/aio_typesense.svg)\n![versions](https://img.shields.io/pypi/pyversions/aio_typesense.svg)\n[![](https://pypip.in/license/aio_typesense/badge.svg)](https://pypi.python.org/pypi/aio_typesense)\n\n# aio_typesense\n## Async Library for Typesense with type hints\n\n```bash\npip install aio_typesense\n```\n\n## Usage\n\n```python\n# examples/example.py\n\nimport asyncio\nfrom typing import TypedDict, List\n\nfrom aio_typesense import Client, Collection\n\n\nclass Movie(TypedDict):\n    id: str\n    name: str\n    year: int\n\n\nMOVIES: List[Movie] = [\n    {"id": "id1", "name": "Wonder Woman", "year": 2017, "year_facet": "2017"},\n    {"id": "id2", "name": "Justice League", "year": 2017, "year_facet": "2017"},\n    {"id": "id3", "name": "Wonder Woman 1984", "year": 2020, "year_facet": "2020"},\n    {"id": "id4", "name": "Death on the Nile", "year": 2021, "year_facet": "2021"},\n]\n\n\nasync def main():\n    client = Client(\n        node_urls=["http://localhost:8108"],\n        api_key="Rhsdhas2asasdasj2",\n    )\n\n    r = await client.collections.create(\n        {\n            "name": "movies",\n            "num_documents": 0,\n            "fields": [\n                {\n                    "name": "name",\n                    "type": "string",\n                },\n                {\n                    "name": "year",\n                    "type": "int32",\n                },\n                {\n                    "name": "year_facet",\n                    "type": "string",\n                    "facet": True,\n                },\n            ],\n            "default_sorting_field": "year",\n        }\n    )\n\n    collection: Collection[Movie] = client.collections["movies"]\n\n    r = await collection.documents.create_many(documents=MOVIES)\n    print(r)\n\n    search_r = await collection.documents.search(\n        {\n            "q": "wonder woman 2021",\n            "query_by": "year_facet,name",\n            "query_by_weights": "1,1",\n        }\n    )\n\n    print(search_r["hits"])\n\n    # [\n    #     {\n    #         "document": {\n    #             "id": "id3",\n    #             "name": "Wonder Woman 1984",\n    #             "year": 2020,\n    #             "year_facet": "2020",\n    #         },\n    #         "highlights": [\n    #             {\n    #                 "field": "year_facet",\n    #                 "matched_tokens": ["2020"],\n    #                 "snippet": "<mark>2020</mark>",\n    #             }\n    #         ],\n    #         "text_match": 1125899907169635,\n    #     },\n    #     {\n    #         "document": {\n    #             "id": "id1",\n    #             "name": "Wonder Woman",\n    #             "year": 2017,\n    #             "year_facet": "2017",\n    #         },\n    #         "highlights": [\n    #             {\n    #                 "field": "year_facet",\n    #                 "matched_tokens": ["2017"],\n    #                 "snippet": "<mark>2017</mark>",\n    #             }\n    #         ],\n    #         "text_match": 1125899907169379,\n    #     },\n    #     {\n    #         "document": {\n    #             "id": "id4",\n    #             "name": "Death on the Nile",\n    #             "year": 2021,\n    #             "year_facet": "2021",\n    #         },\n    #         "highlights": [\n    #             {\n    #                 "field": "year_facet",\n    #                 "matched_tokens": ["2021"],\n    #                 "snippet": "<mark>2021</mark>",\n    #             }\n    #         ],\n    #         "text_match": 562949953552128,\n    #     },\n    #     {\n    #         "document": {\n    #             "id": "id2",\n    #             "name": "Justice League",\n    #             "year": 2017,\n    #             "year_facet": "2017",\n    #         },\n    #         "highlights": [\n    #             {\n    #                 "field": "year_facet",\n    #                 "matched_tokens": ["2017"],\n    #                 "snippet": "<mark>2017</mark>",\n    #             }\n    #         ],\n    #         "text_match": 562949953551616,\n    #     },\n    # ]\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\n## Contributing\n\n**Prerequisites:**\n - **poetry**\n - **nox**\n - **nox-poetry**\n\nInstall them on your system:\n```bash\npip install poetry nox nox-poetry\n```\n\nRun tests:\n```bash\nnox\n```\n',
    'author': 'devtud',
    'author_email': 'devtud@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devtud/aio_typesense',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
