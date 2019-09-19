#In the dictionary file must be only these columns in this order:
#lex #pos #grams #grams2 #flextype #gloss

import re


def create(cells):
    nums = cells[4].split('/')
    nom = cells[0]
    lexeme = ''
    for num in nums:
        if num == 'N11' or num == 'N12' or num == 'P11':
            lexeme = wr_lexeme(cells, __e_a_o(nom), num)
        if num == 'N12a':
            lexeme = wr_lexeme(cells, __n_stem(nom), num)
        if num == 'N12c' or num == 'N52a':
            lexeme = wr_lexeme(cells, shwa__0_stem(nom), num)
        if num == 'N13':
            lexeme = wr_lexeme(cells, i_u_uy__0_stem(nom), num)
        if num == 'N13a' or \
           num == 'N64':
            lexeme = wr_lexeme(cells, e__i_stem(nom), num)
        if num == 'N14':
            lexeme = wr_lexeme(cells, i_u__0___e_a_stem(nom), num)
        if num == 'N14a' or \
           num == 'N22' or \
           num == 'N32' or num == 'N32a' or num == 'N32b' or num == 'N32e' or \
           num == 'N33' or \
           num == 'N34' or \
           num == 'N52' or \
           num == 'N54' or \
           num == 'N63':
            lexeme = wr_lexeme(cells, i_u__0_stem(nom), num)
        if num == 'N23' or num == 'N23a':
            lexeme = wr_lexeme(cells, i_u__0___e_stem(nom), num)
        if num == 'N15' or num == 'N15a':
            lexeme = wr_lexeme(cells, __ye_stem(nom), num)
        if num == 'N16' or num == 'N16a' or num == 'N17':
            lexeme = wr_lexeme(cells, u_i__v_stem(nom), num)
        if num == 'N18' or \
           num == 'N62':
            lexeme = wr_lexeme(cells, uy__0_stem(nom), num)
        if num == 'N18a':
            lexeme = wr_lexeme(cells, uy__u_stem(nom), num)
        if num == 'N26':
            lexeme = wr_lexeme(cells, a__0_stem(nom), num)
        if num == 'N36':
            lexeme = wr_lexeme(cells, ik__z_0_stem(nom), num)
        if num == 'N41' or num == 'N41a':
            lexeme = wr_lexeme(cells, un__an_am_stem(nom), num)
        if num == 'N42':
            lexeme = wr_lexeme(cells, un__van_stem(nom), num)
        if num == 'N43':
            lexeme = wr_lexeme(cells, un__an_n_stem(nom), num)
        if num == 'N51' or \
           num == 'N81a' or num == 'N81b':
            lexeme = wr_lexeme(cells, stem(nom), num)
        if num == 'N62a':
            lexeme = wr_lexeme(cells, a__e_stem(nom), num)
        if num == 'N62b':
            lexeme = wr_lexeme(cells, i__0_a_stem(nom), num)
        if num == 'N71' or num == 'N71a':
            lexeme = wr_lexeme(cells, ay__o_stem(nom), num)
        if num == 'N72':
            lexeme = wr_lexeme(cells, e__o_stem(nom), num)
        if num == 'N73':
            lexeme = wr_lexeme(cells, __e_stem(nom), num)
        if num == 'N73a':
            lexeme = wr_lexeme(cells, dustr_dstr_dster(nom), num)
        if num == 'N81':
            lexeme = wr_lexeme(cells, k__0_stem(nom), num)
        if num == 'N91':
            lexeme = wr_lexeme(cells, va__0_stem(nom), num)
        if num == 'N92':
            lexeme = wr_lexeme(cells, ser__sir_sug__sg_stem(nom), num)
        if num == 'P21':
            lexeme = wr_lexeme(cells, a__ra_ran(nom), num)\
                     + wr_with_glosses(cells, a__ra(nom), 'sg,gen', '.GEN')\
                     + wr_with_glosses(cells, a__ran(nom), 'sg,dat', '.DAT')
        if num == 'P22':
            lexeme = wr_lexeme(cells, 'ով.|ուն.', num)\
                     + wr_with_glosses(cells, 'ով.', 'sg,nom', '')\
                     + wr_with_glosses(cells, 'ուն.', 'sg,gen', '.OBL')
        if num == 'P23':
            lexeme = wr_lexeme(cells, 'ինք.|իրե.|իրա.', num)\
                     + wr_with_glosses(cells, 'ինք', 'sg,nom', '')\
                     + wr_with_glosses(cells, 'իր', 'sg,gen', '.GEN')\
                     + wr_with_glosses(cells, 'իրա', 'sg,gen', '.GEN')\
                     + wr_with_glosses(cells, 'իրեն', 'sg,dat', '.DAT')\
                     + wr_with_glosses(cells, 'իրան', 'sg,dat', '.DAT')
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


def make_lexeme(dictLex):
    gramm = dictLex['pos'] + ',' + dictLex['grams'] + ',' + dictLex['grams2']
    gramm = re.sub('(?<=,),+(?=.)|,+$', '', gramm)
    strLex = '-lexeme\n'
    strLex += ' lex: ' + dictLex['lex'] + '\n'
    strLex += ' stem: ' + dictLex['lex'] + '.\n'
    strLex += ' gramm: ' + gramm + '\n'
    strLex += ' gloss: ' + dictLex['gloss'] + '\n'
    strLex += ' paradigm: ' + dictLex['flextype'] + '\n'
    strLex += ' trans_en: ' + dictLex['trans'] + '\n\n'
    return strLex


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

    fOutLex = open('lexemes.txt', 'w', encoding='utf-8-sig')
    print(len(lexemes), 'lexemes will be written.')
    for lexID in sorted(lexemes):
        fOutLex.write(make_lexeme(lexemes[lexID]))
    fOutLex.close()


if __name__ == '__main__':
    process_source()
