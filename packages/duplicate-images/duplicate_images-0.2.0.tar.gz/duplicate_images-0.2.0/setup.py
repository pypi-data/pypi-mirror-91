# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duplicate_images']

package_data = \
{'': ['*']}

install_requires = \
['Wand>=0.6.5,<0.7.0', 'imagehash>=4.2.0,<5.0.0', 'pillow>=8.1.0,<9.0.0']

entry_points = \
{'console_scripts': ['find-dups = duplicate_images.duplicate:main']}

setup_kwargs = {
    'name': 'duplicate-images',
    'version': '0.2.0',
    'description': '',
    'long_description': "# Finding Duplicate Images\n\nFinds equal or similar images in a directory containing (many) image files.\n\nNeeds Python3 and Pillow imaging library to run, additionally Wand for the test suite.\n\nUses Poetry for dependency management.\n\n## Usage\n```shell\n$ pip install duplicate_images\n$ find-dups -h\n<OR JUST>\n$ find-dups $IMAGE_ROOT \n```\n\n### Image comparison algorithms\n\nUse the `--algorithm` option to select how equal images are found.\n- `exact`: marks only binary exactly equal files as equal. This is by far the fasted, but most \n  restricted algorithm.\n- `histogram`: checks the images' color histograms for equality. Faster than the image hashing \n  algorithms, but tends to give a lot of false positives for images that are similar, but not equal.\n  Use the `--fuzziness` and `--aspect-fuzziness` options to fine-tune its behavior.\n- `ahash`, `colorhash`, `dhash` and `phash`: four different image hashing algorithms. See \n  https://pypi.org/project/ImageHash for an introduction on image hashing and \n  https://tech.okcupid.com/evaluating-perceptual-image-hashes-okcupid for some gory details which\n  image hashing algorithm performs best in which situation. For a start I recommend `ahash`.\n\n## Development\n### Installation\n\nFrom source:\n```shell\n$ git clone https://gitlab.com/lilacashes/DuplicateImages.git\n$ cd DuplicateImages\n$ pip3 install poetry\n$ poetry install\n```\n\n### Running\n\n```shell\n$ poetry run find-dups $PICTURE_DIR\n```\nor\n```shell\n$ poetry run find-dups -h\n```\nfor a list of all possible options.\n\n### Testing\n\nRunning:\n```shell\n$ poetry run mypy duplicate_images tests\n$ poetry run flake8\n$ poetry run pytest\n```\n\n### Publishing\n\n```shell\n$ poetry build\n$ poetry publish --username $PYPI_USER --password $PYPI_PASSWORD --repository testpypi\n$ poetry publish --username $PYPI_USER --password $PYPI_PASSWORD\n```\n\n### Profiling\n\n#### CPU time\nTo show the top functions by time spent, including called functions:\n```shell\n$ poetry run python -m cProfile -s tottime ./duplicate_images/duplicate.py \\ \n    --algorithm $ALGORITHM --action-equal none $IMAGE_DIR 2>&1 | head -n 15\n```\nor, to show the top functions by time spent in the function alone:\n```shell\n$ poetry run python -m cProfile -s cumtime ./duplicate_images/duplicate.py \\ \n    --algorithm $ALGORITHM --action-equal none $IMAGE_DIR 2>&1 | head -n 15\n```\n\n#### Memory usage\n```shell\n$ poetry run fil-profile run ./duplicate_images/duplicate.py \\\n    --algorithm $ALGORITHM --action-equal none $IMAGE_DIR 2>&1\n```\nThis will open a browser window showing the functions using the most memory (see \nhttps://pypi.org/project/filprofiler for more details).",
    'author': 'Lene Preuss',
    'author_email': 'lene.preuss@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lilacashes/DuplicateImages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
