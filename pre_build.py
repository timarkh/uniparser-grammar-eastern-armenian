import re
import os
import shutil


def collect_lemmata(dirName):
    lemmata = ''
    lexrules = ''
    for fname in os.listdir(dirName):
        if fname.endswith('.txt') and fname.startswith('hye_lexemes_'):
            f = open(os.path.join(dirName, fname), 'r', encoding='utf-8-sig')
            lemmata += f.read() + '\n'
            f.close()
        elif fname.endswith('.txt') and fname.startswith('hye_lexrules_'):
            f = open(os.path.join(dirName, fname), 'r', encoding='utf-8-sig')
            lexrules += f.read() + '\n'
            f.close()
    lemmataSet = set(re.findall('-lexeme\n(?: [^\r\n]*\n)+', lemmata, flags=re.DOTALL))
    lemmata = '\n'.join(sorted(list(lemmataSet)))
    return lemmata, lexrules


def prepare_files():
    """
    Put all the lemmata to lexemes.txt. Put all the lexical
    rules to lexical_rules.txt.
    Put all grammar files to ../uniparser_eastern_armenian/data_strict/.
    """
    lemmata, lexrules = collect_lemmata('.')
    fOutLemmata = open('uniparser_eastern_armenian/data/lexemes.txt', 'w', encoding='utf-8')
    fOutLemmata.write(lemmata)
    fOutLemmata.close()
    fInParadigms = open('paradigms.txt', 'r', encoding='utf-8-sig')
    paradigms = fInParadigms.read()
    fInParadigms.close()
    fOutParadigms = open('uniparser_eastern_armenian/data/paradigms.txt', 'w', encoding='utf-8')
    fOutParadigms.write(paradigms)
    fOutParadigms.close()
    fOutLexrules = open('uniparser_eastern_armenian/data/lex_rules.txt', 'w', encoding='utf-8')
    fOutLexrules.write(lexrules)
    fOutLexrules.close()
    shutil.copy2('bad_analyses.txt', 'uniparser_eastern_armenian/data/')
    shutil.copy2('armenian_disambiguation.cg3', 'uniparser_eastern_armenian/data/')


def parse_wordlists():
    """
    Analyze wordlists/wordlist.csv.
    """
    from uniparser_eastern_armenian import EasternArmenianAnalyzer
    a = EasternArmenianAnalyzer()
    a.analyze_wordlist(freqListFile='wordlists/wordlist.csv',
                       parsedFile='wordlists/wordlist_analyzed.txt',
                       unparsedFile='wordlists/wordlist_unanalyzed.txt',
                       verbose=True)


if __name__ == '__main__':
    prepare_files()
    parse_wordlists()
