# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypertag']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<9.0.0',
 'PyPDF2>=1.26.0,<2.0.0',
 'cairocffi>=1.2.0,<2.0.0',
 'filetype>=1.0.7,<2.0.0',
 'fire>=0.3.1,<0.4.0',
 'ftfy>=5.8,<6.0',
 'fuzzywuzzy[speedup]>=0.18.0,<0.19.0',
 'python-igraph>=0.8.3,<0.9.0',
 'rpyc>=5.0.0,<6.0.0',
 'sentence-transformers>=0.4.1,<0.5.0',
 'textract>=1.6.3,<2.0.0',
 'torchvision>=0.8.2,<0.9.0',
 'tqdm>=4.55.0,<5.0.0',
 'watchdog>=1.0.2,<2.0.0',
 'wordninja>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'hypertag',
    'version': '0.5.3.4',
    'description': 'File organization made easy using tags',
    'long_description': '# HyperTag\n\nFile organization made easy. HyperTag let\'s humans intuitively express how they think about their files using tags.\n\n**Objective Function**: Minimize time between a thought and access to all relevant files.\n\n## Install\nAvailable on [PyPI](https://pypi.org/project/hypertag/)\n\n`$ pip install hypertag`\n\n## Community\nJoin the HyperTag [matrix chat room](https://matrix.to/#/#hypertag:matrix.neotree.uber.space?via=matrix.neotree.uber.space) to stay up to date on the latest developments.\n\n## Overview\nHyperTag offers a slick CLI but more importantly it creates a directory called ```HyperTagFS``` which is a file system based representation of your files and tags using symbolic links and directories.\n\n**Directory Import**: Import your existing directory hierarchies using ```$ hypertag import path/to/directory```. HyperTag converts it automatically into a tag hierarchy using metatagging.\n\n**Semantic Text & Image Search  (Experimental)**: Search for **images** (jpg, png) and **text documents** (yes, even PDF\'s) content with a simple text query. Text search is powered by the awesome [Sentence Transformers](https://github.com/UKPLab/sentence-transformers) library. Text to image search is powered by OpenAI\'s [CLIP model](https://openai.com/blog/clip/). Currently only English queries are supported.\n\n**HyperTag Daemon  (Experimental)**: Monitors `HyperTagFS` for user changes. Currently supports file and directory (tag) deletions + directory (name as query) creation with automatic query result population. Also spawns the DaemonService which speeds up semantic search significantly.\n\n**Fuzzy Matching Queries**: HyperTag uses fuzzy matching to minimize friction in the unlikely case of a typo.\n\n**File Type Groups**: HyperTag automatically creates folders containing common files (e.g. Images: jpg, png, etc., Documents: txt, pdf, etc., Source Code: py, js, etc.), which can be found in ```HyperTagFS```.\n\n**HyperTag Graph**: Quickly get an overview of your HyperTag Graph! HyperTag visualizes the metatag graph on every change and saves it at `HyperTagFS/hypertag-graph.pdf`.\n\n![HyperTag Graph Example](https://raw.githubusercontent.com/SeanPedersen/HyperTag/master/images/hypertag-graph.jpg)\n\n## CLI Functions\n\n### Import existing directory recursively\nImport files with tags inferred from the existing directory hierarchy\n\n```$ hypertag import path/to/directory```\n\n### Tag file/s\nManually tag files\n\n```$ hypertag tag humans/*.txt with human "Homo Sapiens"```\n\n### Untag file/s\nManually remove tag/s from file/s\n\n```$ hypertag untag humans/*.txt with human "Homo Sapiens"```\n\n### Tag a tag\nMetatag tag/s to create tag hierarchies\n\n```$ hypertag metatag human with animal```\n\n### Merge tags\nMerge all associations (files & tags) of tag A into tag B\n\n```$ hypertag merge human into "Homo Sapiens"```\n\n### Query using Set Theory\nPrint file names of the resulting set matching the query. Queries are composed of tags and operands. Tags are fuzzy matched for convenience. Nesting is currently not supported, queries are evaluated from left to right\n\nPrint paths: ```$ hypertag query human --path```<br>\nPrint fuzzy matched tag: ```$ hypertag query man --verbose``` <br>\nDisable fuzzy matching: ```$ hypertag query human --fuzzy=0```\n\nDefault operand is AND (intersection): <br>\n```$ hypertag query human "Homo Sapiens"``` is equivalent to ```$ hypertag query human and "Homo Sapiens"```\n\nOR (union): <br>\n```$ hypertag query human or "Homo Sapiens"```\n\nMINUS (difference): <br>\n```$ hypertag query human minus "Homo Sapiens"```\n\n### Index supported image and text files\nOnly indexed files can be searched.\n\n```$ hypertag index```\n\nTo parse even unparseable PDF\'s, install tesseract: `# pacman -S tesseract tesseract-data-eng`\n\nIndex only image files: ```$ hypertag index --image```<br>\nIndex only text files: ```$ hypertag index --text```\n\n### Semantic search for text files\nPrint text file names sorted by matching score.\nPerformance benefits greatly from running the HyperTag daemon.\n\n```$ hypertag search "your important text query" --path --score --top_k=10```\n\n### Semantic search for image files\nPrint image file names sorted by matching score.\nPerformance benefits greatly from running the HyperTag daemon.\n\nText to image:\n```$ hypertag search_image "your image content description" --path --score --top_k=10```\n\nImage to image:\n```$ hypertag search_image "path/to/image.jpg" --path --score --top_k=10```\n\n### Start HyperTag Daemon\nStart daemon process with dual function:\n- Watches `HyperTagFS` directory for user changes\n  - Maps file and directory deletions into tag / metatag removal/s\n  - On directory creation: Interprets name as set theory tag query and automatically populates it with results\n  - On directory creation in `Search Images` or `Search Texts`: Interprets name as semantic search query (add top_k=42 to limit result size) and automatically populates it with results\n- Spawns DaemonService to load and expose models used for semantic search, speeding it up significantly\n\n```$ hypertag daemon```\n\n### Print all tags of file/s\n\n```$ hypertag tags filename1 filename2```\n\n### Print all metatags of tag/s\n\n```$ hypertag metatags tag1 tag2```\n\n### Print all tags\n\n```$ hypertag show```\n\n### Print all files\n\nPrint names:\n```$ hypertag show files```\n\nPrint paths:\n```$ hypertag show files --path```\n\n### Visualize HyperTag Graph\nVisualize the metatag graph hierarchy (saved at HyperTagFS root)\n\n```$ hypertag graph```\n\nSpecify [layout algorithm](https://igraph.org/python/doc/tutorial/tutorial.html#layout-algorithms) (default: fruchterman_reingold):\n\n```$ hypertag graph --layout=kamada_kawai```\n\n### Generate HyperTagFS\nGenerate file system based representation of your files and tags using symbolic links and directories\n\n```$ hypertag mount```\n\n### Set HyperTagFS directory path\nDefault is the user\'s home directory\n\n```$ hypertag set_hypertagfs_dir path/to/directory```\n\n## Architecture\n- Python and it\'s vibrant open-source community power HyperTag\n- Many other awesome open-source projects make HyperTag possible (listed in `pyproject.toml`)\n- SQLite3 serves as the meta data storage engine (located at `~/.config/hypertag/hypertag.db`)\n- Symbolic links are used to create the HyperTagFS directory structure\n- Semantic text search is powered by the awesome [DistilBERT](https://arxiv.org/abs/1910.01108)\n- Text to image search is powered by OpenAI\'s impressive [CLIP model](https://openai.com/blog/clip/)\n\n## Development\n- Clone repo: ```$ git clone https://github.com/SeanPedersen/HyperTag.git```\n- `$ cd HyperTag/`\n- Install [Poetry](https://python-poetry.org/docs/#installation)\n- Install dependencies: `$ poetry install`\n- Activate virtual environment: `$ poetry shell`\n- Run all tests: ```$ pytest -v```\n- Run formatter: ```$ black hypertag/```\n- Run linter: ```$ flake8```\n- Run type checking: ```$ mypy **/*.py```\n- Run security checking: ```$ bandit --exclude tests/ -r .```\n- Run HyperTag: ```$ python -m hypertag```\n\n## Inspiration\n\n**What is the point of HyperTag\'s existence?**<br/>\nHyperTag offers many unique features such as the import, semantic search for images and texts, graphing and fuzzy matching functions that make it very convenient to use. All while HyperTag\'s code base staying tiny at <1300 LOC in comparison to TMSU (>10,000 LOC) and SuperTag (>25,000 LOC), making it easy to hack on.\n\nThis project is partially inspired by these open-source projects:\n- [TMSU](https://github.com/oniony/TMSU): Written in Go\n- [SuperTag](https://github.com/amoffat/supertag): Written in Rust\n',
    'author': 'Sean',
    'author_email': 'sean-p-96@hotmail.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SeanPedersen/HyperTag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
