#In the dictionary file must be only these columns in this order:
#lex #pos #grams #grams2 #flextype #gloss

import re


def make_stems(lexeme, ft):
    """
    Return the stem (with all variants) for a lexeme,
    taking into account its flextype.
    """
    lex = lexeme['lex'].lower()
    if ft in ['N12c', 'N52a', 'N81', 'P24']:
        return [lex[:-1] + '.']
    if ft in ['N13', 'N14', 'N14a', 'N18', 'N22', 'N23',
              'N23a', 'N32', 'N32a', 'N32b', 'N32e', 'N33',
              'N34', 'N52', 'N54', 'N62', 'N63']:
        return [lex + '.|' +
                re.sub('(?:[իոեա]|ույ(?=[^իու])|ու)([^իուեա]*$)', '\\1', lex) + '.']
    if ft in ['N13a', 'N64', 'N92']:
        return [lex + './/' + re.sub('ե([^ե]*)$', 'է\\1', lex) + '.|' + re.sub('ե([^ե]*)$', 'ի\\1', lex) + '.']
    if ft in ['N72']:
        return [lex + '.|' + re.sub('ե([^ե]*)$', 'ո\\1', lex) + '.']
    if ft in ['N16', 'N16a']:
        return [lex + '.|' + re.sub('ու([^ու]*)$', 'վ\\1', lex) + '.']
    if ft in ['N17', 'N17/N23']:
        return [lex + '.|' + re.sub('ի([^ի]*)$', '\\1', lex) + '.|'
                + re.sub('ի([^ի]*)$', 'վ\\1', lex) + '.']
    if ft in ['N18a']:
        return [lex + '.|' +
                re.sub('յ([^յ]*$)', '\\1', lex) + '.']
    if ft in ['N26']:
        return [lex + '.|' + re.sub('ա([^ա]*)$', '\\1', lex) + '.']
    if ft in ['N32c', 'N32d']:
        return [lex + '.|' + lex[:-1] + 'ա' + lex[-1] + '.']
    if ft in ['N36']:
        return [lex + '.|' + lex[:-2] + 'գ.|'
                + lex[:-2] + '.']
    if ft in ['N41']:
        return [lex + './/' + lex[:-4] + 'ի' + lex[-2:] + '.|'
                + lex[:-3] + 'ան.//' + lex[:-4] + 'եան.|'
                + lex[:-3] + 'ամ.//' + lex[:-4] + 'եամ.']
    if ft in ['N41a']:
        return [lex + '.|' + lex[:-3] + 'ան.']
    if ft in ['N42']:
        return [lex + '.|' + lex[:-3] + 'վան.|' + lex[:-3] + 'վամ.']
    if ft in ['N43']:
        return [lex + '.|' + lex[:-3] + 'ան.|' + lex[:-3] + 'ն.']
    if ft in ['N62a']:
        return [lex + '.|' + re.sub('ա([^ա]*)$', 'ե\\1', lex) + '.']
    if ft in ['N63']:
        return [lex + '.|' + re.sub('ի([^ի]*)$', '\\1', lex) + '.|'
                + re.sub('ի([^ի]*)$', '\\1', lex) + '.']
    if ft in ['N63a', 'N63'] and lex.endswith('կին'):
        return [lex + '.|' + re.sub('ի([^ի]*)$', '\\1', lex) + '.|'
                + re.sub('ի([^ի]*)$', 'ա\\1', lex) + '.']
    # if ft in ['N63b']:
    #     return [lex[:-3] + '.']
    if ft in ['N71', 'N71a']:
        return [lex + '.|' + re.sub('այ([^ա]*)$', 'ո\\1', lex) + '.']
    if ft in ['N72']:
        return [lex + '.|' + re.sub('ե([^ե]*)$', 'ո\\1', lex) + '.']
    if ft in ['N73']:
        return [lex + '.|' + lex[:-1] + 'ե' + lex[-1] + '.']
    if ft in ['N73a']:
        return [lex + '.|' + lex.replace('ու', '')
                + '.|' + lex.replace('ու', '')[:-1] + 'ե' + lex[-1] + '.']
    if ft in ['N91']:
        return [lex + '.|' + lex[:-3] + lex[-1] + '.']
    if ft in ['P21']:
        return [lex + '.|' + lex[:-1] + 'ր.']
    if ft in ['P22']:
        return [lex + '.|' + lex[:-2] + 'ում.']
    if ft in ['P23']:
        return [lex[:-1] + '.|' + lex[:-3] + 'ր.']
    if ft in ['V12', 'V13', 'V14', 'V22', 'V12a', 'V12b',
              'V14a', 'V14b', 'V14c', 'V14d', 'V22a']:
        return ['.' + lex[:-3] + '.']
    if ft in ['V32c']:
        return ['.' + lex[:-1] + '.']
    if ft in ['V22b']:
        return ['.' + lex[:-3] + '.|.' + lex[:-4] + 'րձ.']
    if ft in ['V22c']:
        return ['.' + lex[:-2] + '.|.' + lex[:-4] + 'աց.|.' + lex[:-4] + 'ան.']
    if ft in ['V31a']:
        return ['.' + lex[:-2] + '.|.կեր.']
    if ft in ['V31b'] and lexeme['lex'] == 'լինել':
        return ['.' + lex[:-2] + '.|.եղ.']
    if ft in ['V31b'] and lexeme['lex'] == 'ըլնել':
        return ['.' + lex[:-2] + '.|.էղ.']
    if ft in ['V32a']:
        return ['.' + lex[:-2] + '.|.եկ.//.էկ.|.արի.']
    if ft in ['V32d']:
        return ['.NONE.|.էկ.|.NONE.']
    if ft in ['V32b']:
        return ['.' + lex[:-2] + '.|.' + lex[:-2] + 'վ.|.' + lex[:-2] + 'ու.']
    if ft in ['V41']:
        return ['.է.|.ե.|.ի.|.ա.']
    if ft in ['V42']:
        return ['.' + lex + '.']
    if ft in ['V43']:
        return ['.' + lex[:-3] + '.|.' + lex[:-4] + 'ի.']
    if ft.startswith('V'):
        return ['.' + lex[:-2] + '.']
    if ft in ['P31a', 'P31'] and lex == 'ես':
        return ['ես.|իմ.|ինձ.|ինձն.|ինձան.|ընձ.']
    if ft in ['P31c', 'P31'] and lex == 'մենք':
        return ['մենք.|մեր.|մեզ.|մեզն.|մեզան.']
    if ft in ['P31b', 'P31'] and lex == 'դու':
        return ['դու.|քո.|քեզ.|քեզն.|քեզան.|քու.']
    if ft in ['P31d', 'P31'] and lex == 'դուք':
        return ['դուք.|ձեր.|ձեզ.|ձեզն.|ձեզան.']
    if ft in ['NEG']:
        return ['.' + lex + '.']
    return [lex + '.']


def add_orth_variation(stems):
    newStems = ''
    for stem in stems.split('|'):
        newVars = set(stem.split('//'))
        for stemVar in stem.split('//'):
            varYun = re.sub('(?<=[աիօըեէ])վ', 'ւ', stemVar)
            if varYun not in newVars:
                newVars.add(varYun)
            varNoYun = re.sub('(?<=[աօըեէ])ւ', 'վ', stemVar)
            if varNoYun not in newVars:
                newVars.add(varNoYun)
            varEw = re.sub('եւ', 'և', stemVar)
            if varEw not in newVars:
                newVars.add(varEw)
            varJ = re.sub('^\\.հա', '.յա', stemVar)
            if varJ not in newVars:
                newVars.add(varJ)
            varJ = re.sub('^([^.<>]+)ե([^աիօըեէո]*)$', '\\1է\\2', stemVar)
            if varJ not in newVars:
                newVars.add(varJ)
        if len(newStems) > 0:
            newStems += '|'
        newStems += '//'.join(newVars)
    return newStems


def make_lexemes(dictLex):
    gramm = dictLex['pos'] + ',' + dictLex['grams'] + ',' + dictLex['grams2']
    gramm = re.sub('(?<=,),+(?=.)|,+$', '', gramm)
    lexemesOut = []
    paraCollation = {
        '0': 'Empty',
        '31b': 'P31b',
        'N11-onk\'': 'N11',
        'N11-ank\'': 'N11',
        'N13a': 'N13',
        'N15': 'N12',
        'N15a': 'N11',
        'N16': 'N14',
        'N16a': 'N13',
        'N18': 'N14a',
        'N42': 'N41',
        'N63a': 'N63',
        'N72': 'N71',
        'V32d': 'V32',
        'P31a': 'P31',
        'P31b': 'P31',
        'P31c': 'P31',
        'P31d': 'P31'
    }
    for para in dictLex['flextype'].split('/'):
        for stem in make_stems(dictLex, para):
            paraNonCollated = para
            if para in paraCollation:
                para = paraCollation[para]
            if para in ['N11', 'N12', 'N13', 'N14'] and gramm.startswith('A'):
                para = 'A' + para[1:]
                stem = '.' + stem.replace('|', '|.').replace('//', '//.')
            paradigms = [para]
            if 'apl' in gramm:
                gramm = re.sub(',apl\\+?', '', gramm)
                if paraNonCollated in ['N11', 'N11-onk\'']:
                    paradigms.append('apl_o')
                if paraNonCollated in ['N11', 'N12', 'N11-ank\'']:
                    paradigms.append('apl_a')
                if paraNonCollated in ['N14']:
                    paradigms.append('apl_2a')
                    paradigms.append('apl_2e')
                else:
                    paradigms.append('apl_e')
            if para in ['V11a', 'V11b', 'V11c']:
                paradigms.append('V11')
            elif para in ['V12a', 'V12b']:
                paradigms.append('V12')
            elif para in ['V14a', 'V14b', 'V14c', 'V14d']:
                paradigms.append('V14')
            elif para in ['V21a']:
                paradigms.append('V21')
            elif para in ['V22a']:
                paradigms.append('V22')
            elif para in ['V31a', 'V31b']:
                paradigms.append('V31')
            elif para in ['V32a', 'V32b']:
                paradigms.append('V32')
            elif para in ['V11']:
                paradigms.append('V11_main')
            elif para in ['V12']:
                paradigms.append('V12_main')
            elif para in ['V14']:
                paradigms.append('V14_main')
            elif para in ['V22']:
                paradigms.append('V22_main')

            strLex = '-lexeme\n'
            strLex += ' lex: ' + dictLex['lex'] + '\n'
            strLex += ' stem: ' + add_orth_variation(stem) + '\n'
            strLex += ' gramm: ' + gramm + '\n'
            strLex += ' gloss: ' + dictLex['gloss'] + '\n'
            for para in paradigms:
                strLex += ' paradigm: ' + para + '\n'
            strLex += ' trans_en: ' + dictLex['trans'] + '\n\n'
            lexemesOut.append(strLex)
    return lexemesOut


def process_source():
    fInFull = open('source/dict.csv', 'r', encoding='utf-8-sig')
    fInShort = open('source/dict6000.csv', 'r', encoding='utf-8-sig')
    lexemes = {}
    iLine = 0
    for line in fInFull:
        iLine += 1
        line = line.strip()
        if len(line) < 5 or line.startswith('#'):
            continue
        line += '\t' * 15
        rev, lex, lex_freq, homonym, pos, grams, grams2, flextype,\
            number, form2, form3, trans, comment, labels, gloss, rest = line.split('\t', 15)
        flextype = flextype.strip()
        if flextype == 'N11/N18a':
            flextype = 'N18a'
        if flextype == 'V43':
            flextype = 'V43/V22'
        lexID = (lex, pos, homonym, grams, grams2)
        if lexID in lexemes:
            print('Duplicate lexeme: ' + line)
        elif len(lex) <= 0 or '#' in lex:
            continue
        else:
            lexemes[lexID] = {
                'lex': lex,
                'pos': pos,
                'grams': grams,
                'grams2': grams2,
                'flextype': flextype,
                'trans': trans,
                'gloss': gloss
            }
            if iLine >= 6000:
                lexemes[lexID]['gloss'] = re.sub('[/,] *', '_', trans).replace(' ', '.')
            if len(lexemes[lexID]['gloss']) <= 0:
                lexemes[lexID]['gloss'] = 'STEM'
            if len(lexemes[lexID]['flextype']) <= 0:
                lexemes[lexID]['flextype'] = 'Empty'
    for line in fInShort:
        line = line.strip()
        if len(line) < 5 or line.startswith('#'):
            continue
        line += '\t' * 15
        rev, lex, lex_freq, homonym, pos, grams, grams2, flextype,\
            number, form2, form3, trans, comment, labels, gloss, rest = line.split('\t', 15)
        lexID = (lex, pos, homonym, grams, grams2)
        if lexID not in lexemes:
            print('New lexeme: ' + line)
        elif lexemes[lexID]['gloss'] != gloss and len(gloss) > 0:
            print('New gloss: ' + lexemes[lexID]['gloss'] + ' -> ' + gloss)
            lexemes[lexID]['gloss'] = gloss
    fInFull.close()
    fInShort.close()

    fOutLexN = open('hye-lexemes-N.txt', 'w', encoding='utf-8-sig')
    fOutLexV = open('hye-lexemes-V.txt', 'w', encoding='utf-8-sig')
    fOutLexA = open('hye-lexemes-A.txt', 'w', encoding='utf-8-sig')
    fOutLexADV = open('hye-lexemes-ADV.txt', 'w', encoding='utf-8-sig')
    fOutLexRest = open('hye-lexemes-rest.txt', 'w', encoding='utf-8-sig')
    print(len(lexemes), 'lexemes will be written.')
    for lexID in sorted(lexemes):
        for l in make_lexemes(lexemes[lexID]):
            if 'gramm: N' in l:
                fOutLexN.write(l)
            elif 'gramm: ADV' in l:
                fOutLexADV.write(l)
            elif 'gramm: V' in l:
                fOutLexV.write(l)
            elif 'gramm: A' in l:
                fOutLexA.write(l)
            else:
                fOutLexRest.write(l)
    fOutLexN.close()
    fOutLexV.close()
    fOutLexA.close()
    fOutLexADV.close()
    fOutLexRest.close()


if __name__ == '__main__':
    process_source()
