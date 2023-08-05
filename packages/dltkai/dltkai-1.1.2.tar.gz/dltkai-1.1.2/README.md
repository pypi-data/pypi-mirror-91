# DLTK open-source SDK (Python)
[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)


[![](https://github.com/dltk-ai/dltkai-sdk/blob/master/python/dltk.png)](https://dltk.ai/)

DLTK renders a comprehensive spectrum of solutions that can be accessed by users on-demand from our pool of transformational technologies.

### Installation

DLTK SDK requires Python 3.5 + .

1. Fork the repo on GitHub
2. Download the project code files with:

   ```git clone https://github.com/dltk-ai/dltkai-sdk.git```

3. Go to the project directory

   ```cd dltkai-sdk/python```
   
4. Install all the required packages:

   ```pip install .```

### Usage
```sh
import dltkai as dl
response = dl.NaturalLanguage.sentiment_detect('I am feeling good.')
print(response)
```

or you can also checkout some samples by running test.py:
```python test.py```

For more details, visit https://dltk.ai/


## License

The content of this project itself is licensed under [GNU LGPL, Version 3 (LGPL-3)](https://github.com/dltk-ai/dltkai-sdk/blob/master/python/LICENSE)

