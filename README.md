# Eastern Armenian morphological analyzer
This is a rule-based morphological analyzer for Modern Eastern Armenian (``hye``). It is based on a formalized description of literary Eastern Armenian morphology, which also includes a number of dialectal elements, and uses [uniparser-morph](https://github.com/timarkh/uniparser-morph) for parsing. It performs full morphological analysis of Eastern Armenian words (lemmatization, POS tagging, grammatical tagging, glossing).

## How to use
### Python package
The analyzer is available as a Python package. If you want to analyze Eastern Armenian texts in Python, install the module:

```
pip3 install uniparser-eastern-armenian
```

Import the module and create an instance of ``EasternArmenianAnalyzer`` class. After that, you can either parse tokens or lists of tokens with ``analyze_words()``, or parse a frequency list with ``analyze_wordlist()``. Here is a simple example:

```python
from uniparser_eastern_armenian import EasternArmenianAnalyzer
a = EasternArmenianAnalyzer()

analyses = a.analyze_words('Ձևաբանություն')
# The parser is initialized before first use, so expect
# some delay here (usually several seconds)

# You will get a list of Wordform objects
# The analysis attributes are stored in its properties
# as string values, e.g.:
for ana in analyses:
        print(ana.wf, ana.lemma, ana.gramm, ana.gloss)

# You can also pass lists (even nested lists) and specify
# output format ('xml' or 'json')
# If you pass a list, you will get a list of analyses
# with the same structure
analyses = a.analyze_words([['և'], ['Ես', 'սիրում', 'եմ', 'քեզ', ':']],
	                       format='xml')
analyses = a.analyze_words(['Ձևաբանություն', [['և'], ['Ես', 'սիրում', 'եմ', 'քեզ', ':']]],
	                       format='json')
```

Refer to the [uniparser-morph documentation](https://uniparser-morph.readthedocs.io/en/latest/) for the full list of options.

### Disambiguation
Apart from the analyzer, this repository contains a small set of [Constraint Grammar](https://visl.sdu.dk/constraint_grammar.html) rules that can be used for partial disambiguation of analyzed Armenian texts. If you want to use them, set ``disambiguation=True`` when calling ``analyze_words``:

```python
analyses = a.analyze_words(['Ես', 'սիրում', 'եմ', 'քեզ'], disambiguate=True)
```

In order for this to work, you have to install the ``cg3`` executable separately. On Ubuntu/Debian, you can use ``apt-get``:

```
sudo apt-get install cg3
```

On Windows, download the binary and add the path to the ``PATH`` environment variable. See [the documentation](https://visl.sdu.dk/cg3/single/#installation) for other options.

Note that each time you call ``analyze_words()`` with ``disambiguate=True``, the CG grammar is loaded and compiled from scratch, which makes the analysis even slower. If you are analyzing a large text, it would make sense to pass the entire text contents in a single function call rather than do it sentence-by-sentence, for optimal performance.

### Word lists
Alternatively, you can use a preprocessed word list. The ``wordlists`` directory contains a list of words from a 100-million-word [Eastern Armenian National Corpus](http://www.eanc.net/) (``wordlist.csv``), list of analyzed tokens (``wordlist_analyzed.txt``; each line contains all possible analyses for one word in an XML format), and list of tokens the parser could not analyze (``wordlist_unanalyzed.txt``). The recall of the analyzer on literary texts is about 93%, i.e. 93% of the tokens receive at least one analysis.

## Description format
The description is carried out in the ``uniparser-morph`` format and involves a description of the inflection (paradigms.txt), a grammatical dictionary (hye_lexemes_XXX.txt files), and a short list of analyses that should be avoided (bad_analyses.txt). The dictionary contains descriptions of individual lexemes, each of which is accompanied by information about its stem, its part-of-speech tag and some other grammatical/borrowing information, its inflectional type (paradigm), its English translation and (in some cases) its stem gloss. See more about the format [in the uniparser-morph documentation](https://uniparser-morph.readthedocs.io/en/latest/format.html).
