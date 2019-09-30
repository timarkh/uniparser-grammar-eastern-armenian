#In the dictionary file must be only these columns in this order:
#lex #pos #grams #grams2 #flextype #gloss

import re


def create(cells):
    nums = cells[4].split('/')
    nom = cells[0]
    lexeme = ''
    for num in nums:
        if num == 'P31a':
            lexeme = wr_lexeme(cells, 'ես.|իմ.|ինձ.|ինձն.|ինձնա.|ընձ', num)\
                     + wr_with_glosses(cells, 'ես.', 'sg,nom', '')\
                     + wr_with_glosses(cells, 'իմ.', 'sg,gen', '.GEN\n paradigm: P12')\
                     + wr_with_glosses(cells, 'ինձ.', 'sg,dat', '.DAT')
        if num == 'P31b':
            lexeme = wr_lexeme(cells, 'դու.|քո.|քեզ.|քեզն.|քեզնա.|քու.', num)\
                     + wr_with_glosses(cells, 'դու.', 'sg,nom', '')\
                     + wr_with_glosses(cells, 'քո.', 'sg,gen', '.GEN\n paradigm: P12b')\
                     + wr_with_glosses(cells, 'քեզ.', 'sg,dat', '.DAT')\
                     + wr_with_glosses(cells, 'քու.', 'sg,dat,որալ', '.GEN\n paradigm: P12b')
        if num == 'P31a':
            lexeme = wr_lexeme(cells, 'մենք.|ներ.|նեզ.|նեզն.|նեզնա.', num)\
                     + wr_with_glosses(cells, 'մենք.', 'sg,nom', '')\
                     + wr_with_glosses(cells, 'ներ.', 'sg,gen', '.GEN\n paradigm: P12')\
                     + wr_with_glosses(cells, 'նեզ.', 'sg,dat', '.DAT')
        if num == 'P31a':
            lexeme = wr_lexeme(cells, 'դուք.|ձեր.|ձեզ.|ձեզն.|ձեզնա.', num)\
                     + wr_with_glosses(cells, 'դուք.', 'sg,nom', '')\
                     + wr_with_glosses(cells, 'իմ.', 'sg,gen', '.GEN\n paradigm: P12')\
                     + wr_with_glosses(cells, 'ձեզ.', 'sg,dat', '.DAT')
        if num == 'V11' or \
           num == 'V21' or num == 'V21a':
            lexeme = wr_lexeme(cells, el_al(nom), num)
        if num == 'V11a' or num == 'V11b':
            lexeme = wr_lexeme(cells, el_al(nom), num) \
                     + wr_with_glosses(cells, del_el_al(nom), 'imp,sg,2', '.IMP.SG')
        if num == 'V11c':
            lexeme = wr_lexeme(cells, el_al__a(nom), num)
        if num == 'V12':
            lexeme = wr_lexeme(cells, nel_nal(nom), num)
        if num == 'V14' or num == 'V14a' or num == 'V14b'\
           or num == 'V22':
            lexeme = wr_lexeme(cells, nel_nal__rel_ral(nom), num)
        if num == 'V12a' or num == 'V12b':
            lexeme = wr_lexeme(cells, nel_nal__rel_ral(nom), num) \
                     + wr_with_glosses(cells, del_nel_nal(nom), 'imp,sg,2', '.IMP.SG')
        if num == 'V14c':
            lexeme = wr_lexeme(cells, nel_nal__rel_ral(nom), num) \
                     + wr_with_glosses(cells, del_nel_nal(nom), 'imp,sg,2,oral', '.IMP.SG')
        if num == 'V14d':
            lexeme = wr_lexeme(cells, nel_nal__rel_ral_el(nom), num) \
                     + wr_with_glosses(cells, del_nel_nal(nom), 'imp,sg,2', '.IMP.SG')
        if num == 'V13':
            lexeme = wr_lexeme(cells, chel_chal(nom), num)
        if num == 'V22a':
            lexeme = wr_lexeme(cells, nel_nal__rel_ral(nom), num) \
                     + wr_with_glosses(cells, del_nel_nal(nom), 'imp,sg,2', '.IMP.SG')
        if num == 'V22b':
            lexeme = wr_lexeme(cells, r__rj(nom), num) \
                     + wr_with_glosses(cells, del_nel_nal(nom), 'imp,sg,2', '.IMP.SG')
        if num == 'V22c':
            lexeme = wr_lexeme(cells, ken_kac_kan(nom), num) \
                     + wr_with_glosses(cells, 'կաց.', 'imp,sg,2', '.IMP.SG')
        if num == 'V31a':
            lexeme = wr_lexeme(cells, ut_ker(nom), num) \
                     + wr_with_glosses(cells, 'կեր.', 'imp,sg,2', '.IMP.SG')
        if num == 'V31b':
            lexeme = wr_lexeme(cells, lin_egh(nom), num)
        if num == 'V32a':
            lexeme = wr_lexeme(cells, g_ek_ari(nom), num) \
                     + wr_with_glosses(cells, 'գեկ.', 'imp,sg,2', '.IMP.SG') \
                     + wr_with_glosses(cells, 'գարի.', 'imp,sg,2', '.IMP.SG')
        if num == 'V32b':
            lexeme = wr_lexeme(cells, t_tv_tu(nom), num) \
                     + wr_with_glosses(cells, 'տու.', 'imp,sg,2,oral', '.IMP.SG')
        if num == 'V32c':
            lexeme = wr_lexeme(cells, lal__la(nom), num)\
                     + wr_with_glosses(cells, 'լա.', 'sbjv,pres,sg,3', '.SBJV.PRS.3SG')\
                     + wr_with_glosses(cells, 'լա.', 'conneg', '.CONNEG')
        if num == 'V41':
            lexeme = wr_lexeme(cells, e_e(nom), num)\
                     + wr_with_glosses(cells, 'ե.', 'pres,sg,3', '.PRS.3SG')\
                     + wr_with_glosses(cells, 'չ|ի.', 'neg,pres,sg,3', 'NEG|PRS.3SG')\
                     + wr_with_glosses(cells, 'ա.', 'pres,sg,3,oral', '.PRS.3SG')
        if num == 'V42':
            lexeme = wr_lexeme(cells, nom, num)\
                     + wr_with_glosses(cells, 'կա.', 'pres,sg,3', '.PRS.3SG')
        if num == 'V43':
            lexeme = wr_lexeme(cells, enal(nom), num)\
                     + wr_with_glosses(cells, 'կա.', 'pres,sg,3', '.PRS.3SG')
        if num == 'NEG':
            lexeme = wr_lexeme(cells, '.' + nom, num)
    return lexeme

def __e_a_o(nom):
    return nom + '.|' + nom + 'ե.|' + nom + 'ա.|' + nom + 'ո.'

def __n_stem(nom):
    return nom + '.|' + nom + 'ն.'

def shwa__0_stem(nom):
    res = re.search('(.*)ը', nom)
    return res.group(1) + '.'

def i_u_uy__0_stem(nom):
    res = re.search('(.*)(ի|ու|ույ)([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + res.group(3) + '.'

def i_u__0_stem(nom):
    res = re.search('(.*)(ի|ու)([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    if res:
        return nom + '.|' + res.group(1) + res.group(3) + '.'
    else:
        return nom + '.|' + nom + '.'

def i_u__0___e_stem(nom):
    res = re.search('(.*)(ի|ու)([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + res.group(3) + '.|' + nom + 'ե.'

def e__i_stem(nom):
    res = re.search('(.*)(ե)([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + 'ի' + res.group(3) + '.'

def i_u__0___e_a_stem(nom):
    res = re.search('(.*)(ի|ու|ե)([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + res.group(3) + '.|'\
           + res.group(1) + res.group(3) + 'ե.|' \
           + res.group(1) + res.group(3) + 'ա.'

def __ye_stem(nom):
    return nom + '.|' + nom + 'յ.|' + nom + 'յե.'

def u_i__v_stem(nom):
    res = re.search('(.*)(ու|ի)', nom)
    return nom + '.|' + res.group(1) + 'վ' + '.'

def uy__0_stem(nom):
    res1 = re.search('(.*)ույ([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    res2 = re.search('(.*)ու([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    if res1:
        return nom + '.|' + res1.group(1) + res1.group(2) + '.'
    elif res2:
        return nom + '.|' + res2.group(1) + res2.group(2) + '.'
    else:
        return nom + '.|' + nom + '.'    

def uy__u_stem(nom):
    res = re.search('(.*)ույ([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + 'ու' + res.group(2) + '.'

def a__0_stem(nom):
    res = re.search('(.*)ա', nom)
    if res:
        return nom + '.|' + res.group(1) + '.'
    else:
        return nom + '.|' + nom + '.'

def ik__z_0_stem(nom):
    res = re.search('(.*)իկ', nom)
    return nom + '.|' + res.group(1) + 'գ.|' + res.group(1) + '.'

def un__an_am_stem(nom):
    res = re.search('(.*)ուն', nom)
    return nom + '.|' + res.group(1) + 'ան.|' + res.group(1) + 'ամ.'

def un__van_stem(nom):
    res = re.search('(.*)ուն', nom)
    return nom + '.|' + res.group(1) + 'վան.'

def un__an_n_stem(nom):
    res = re.search('(.*)ուն', nom)
    return nom + '.|' + res.group(1) + 'ան.|' + res.group(1) + 'ն.'

def shwa__0_va_stem(nom):
    res = re.search('(.*)ը', nom)
    return res.group(1) + '.|' + res.group(1) + 'վա.'

def a__e_stem(nom):
    res = re.search('(.*)ա([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + 'ե' + res.group(2) + '.'

def i__0_a_stem(nom):
    res = re.search('(.*)ի([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + res.group(2) + '.|'\
            + res.group(1) + 'ա' + res.group(2) + '.'

def ay__o_stem(nom):
    res = re.search('(.*)այ([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + 'ո' + res.group(2) + '.'

def e__o_stem(nom):
    res = re.search('(.*)ե([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + 'ո' + res.group(2) + '.'

def __e_stem(nom):
    res = re.search('(.*)(ր)', nom)
    return nom + '.|' + res.group(1) + 'ե' + res.group(2) + '.'

def dustr_dstr_dster(nom):
    res = re.search('(.*)(դուստր)', nom)
    return nom + '.|' + res.group(1) + 'դստր.|' + res.group(1) + 'դստեր.'

def k__0_stem(nom):
    res = re.search('(.*)ք', nom)
    return res.group(1) + '.'

def ink__0_stem(nom):
    res = re.search('(.*)ինք', nom)
    return res.group(1) + '.'

def va__0_stem(nom):
    res = re.search('(.*)վա([բգդզթժլխծկհձղճմյնշչպջռսվտրցփքֆ]*)', nom)
    return nom + '.|' + res.group(1) + res.group(2) + '.'

def ser__sir_sug__sg_stem(nom):
    ser = re.search('սեր', nom)
    sug = re.search('սուգ', nom)
    if ser:
        stems = 'սեր.|սիր.'
    if sug:
        stems = 'սուգ.|սգ.'
    return stems

def a__ra_ran(nom):
    res = re.search('(.*)ա', nom)
    return res.group(1) + 'ա.|'+ res.group(1) + 'րա.|' + res.group(1) + 'րան.'

def el_al(inf):
    r = re.search('(.*)(ե|ա)լ', inf)
    return r.group(1) + '.|' + r.group(1) + r.group(2) + '.'

def el_al__a(inf):
    r = re.search('(.*)(ե|ա)լ', inf)
    return r.group(1) + '.|' + r.group(1) + r.group(2) + '.|' + r.group(1) + 'ա.'

def nel_nal(inf):
    r = re.search('(.*)(ն)(ե|ա)լ', inf)
    return r.group(1) + '.|'\
           + r.group(1) + r.group(2) + '.|' + r.group(1) + r.group(2) + r.group(3) + '.'

def nel_nal__rel_ral_el(inf):
    r = re.search('(.*)(ն)(ե|ա)լ', inf)
    return r.group(1) + '.|'\
           + r.group(1) + r.group(2) + '.|' + r.group(1) + r.group(2) + r.group(3) + '.|'\
           + r.group(1) + 'ր' + '.|' + r.group(1) + 'ր' + r.group(3) + '.|'\
           + r.group(1) + r.group(3) + '.'

def nel_nal__rel_ral(inf):
    r = re.search('(.*)(ն)(ե|ա)լ', inf)
    return r.group(1) + '.|'\
           + r.group(1) + r.group(2) + '.|' + r.group(1) + r.group(2) + r.group(3) + '.|'\
           + r.group(1) + 'ր' + '.|' + r.group(1) + 'ր' + r.group(3) + '.'

def chel_chal(inf):
    r = re.search('(.*)(չ)(ե|ա)լ', inf)
    return r.group(1) + '.|'\
           + r.group(1) + r.group(2) + '.|' + r.group(1) + r.group(2) + r.group(3) + '.|'\
           + r.group(1) + 'ն' + '.|' + r.group(1) + 'ն' + r.group(3) + '.'

def r__rj(inf):
    r = re.search('(.*)(ռ)(ն)(ե|ա)լ', inf)
    return r.group(1) + '.|'\
           + r.group(1) + r.group(2) + r.group(3) + '.|' \
           + r.group(1) + r.group(2) + r.group(3) + r.group(4) + '.|'\
           + r.group(1) + 'րձ.'

def ken_kac_kan(inf):
    r = re.search('(.*)(են)(ա)լ', inf)
    return 'կեն.|կենա.|կաց.|կացա.|կան.|կանա.'

def ut_ker(inf):
    return 'ուտ.|ուտե.|կեր.|կերե.'

def lin_egh(inf):
    return 'լին.|լինե.|եղ.|ըլն.|ըլնե|էղ.'

def g_ek_ari(inf):
    return 'գ.|գա.|եկ.|արի.'

def t_tv_tu(inf):
    return 'տ.|տա.|տվ.|տվե.|տու.'

def lal__la(inf):
    return 'լա.|լաց.|լացե.'

def e_e(inf):
    return 'է.|ե.'

def enal(inf):
    r = re.search('(.*)(ենա)լ', inf)
    return r.group(1) + '.|'\
           + r.group(1) + 'են.|' + r.group(1) + 'ենա.|'\
           + r.group(1) + 'ե.'

def del_el_al(inf):
    r = re.search('(.*)(ել|ալ)', inf)
    return r.group(1) + '.'

def del_nel_nal(inf):
    r = re.search('(.*)(նել|նալ)', inf)
    return r.group(1) + '.'

def a__ra(nom):
    r = re.search('(.*)(ա)', nom)
    return r.group(1) + 'րա.'

def a__ran(nom):
    r = re.search('(.*)(ա)', nom)
    return r.group(1) + 'րան.'

def stem(nom):
    return nom + '.'


def make_stems(lexeme, ft):
    """
    Return the stem (with all variants) for a lexeme,
    taking into account its flextype.
    """
    lex = lexeme['lex'].lower()
    if ft in ['N12c', 'N52a', 'N54', 'N81', 'N81b', 'P24']:
        return [lex[:-1] + '.']
    if ft in ['N13', 'N14', 'N14a', 'N18', 'N22', 'N23',
              'N23a', 'N32', 'N32a', 'N32b', 'N32e', 'N33',
              'N34', 'N52', 'N62', 'N63']:
        return [lex + '.|' +
                re.sub('(?:[իո]|ու|ույ(?=[^իու]))([^իու]*$)', '\\1', lex) + '.']
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
    if ft in ['N63a']:
        return [lex + '.|' + re.sub('ի([^ի]*)$', '\\1', lex) + '.|'
                + re.sub('ի([^ի]*)$', 'ա\\1', lex) + '.']
    if ft in ['N63b', 'N81a']:
        return [lex[:-3] + '.']
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
        return [lex + '.|' + lex[:-2] + 'ուն.']
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
    return [lex + '.']


def add_orth_variation(stems):
    newStems = ''
    for stem in stems.split('|'):
        newVars = set(stem.split('//'))
        for stemVar in stem.split('//'):
            varYun = re.sub('(?<=[աիօըեէ])վ', 'ւ', stemVar)
            if varYun not in newVars:
                newVars.add(varYun)
            varNoYun = re.sub('(?<=[աիօըեէ])ւ', 'վ', stemVar)
            if varNoYun not in newVars:
                newVars.add(varNoYun)
            varEw = re.sub('եւ', 'և', stemVar)
            if varEw not in newVars:
                newVars.add(varEw)
            varJ = re.sub('^\\.հա', '.յա', stemVar)
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
        'N72': 'N71'
    }
    for para in dictLex['flextype'].split('/'):
        for stem in make_stems(dictLex, para):
            if para in paraCollation:
                para = paraCollation[para]
            if para in ['N11', 'N12', 'N13', 'N14'] and gramm.startswith('A'):
                para = 'A' + para[1:]
                stem = '.' + stem.replace('|', '|.').replace('//', '//.')
            paradigms = [para]
            if 'apl' in gramm:
                gramm = re.sub(',apl\\+?', '', gramm)
                if dictLex['flextype'] in ['N11', 'N11-onk\'']:
                    paradigms.append('apl_o')
                if dictLex['flextype'] in ['N11', 'N12', 'N11-ank\'']:
                    paradigms.append('apl_a')
                if dictLex['flextype'] in ['N14']:
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
