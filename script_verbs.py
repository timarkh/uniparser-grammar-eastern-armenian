import re

#lex #pos #grams #grams2 #flextype #gloss
def main():
    dct_file = open('ArmDict6000_for_lexemes.txt', 'r', encoding = 'UTF-8')
    lex_file = open('lexemes.txt', 'a', encoding = 'UTF-8')
    for line in dct_file.readlines():
        lex_file.write(create(line.split('\t')))
    lex_file.close()
    dct_file.close()

def create(cells):
    nums = cells[4].split('/')
    inf = cells[0]
    lexeme = ''
    for num in nums:
        if num == 'V11' or num == 'V11a' or num == 'V11b' or num == 'V11c' or \
           num == 'V21' or num == 'V21a':
            lexeme = lexeme + wr_lexeme(cells, el_al(inf), num)
        if num == 'V12' or num == 'V12a' or num == 'V12b'\
           or num == 'V13'
           or num == 'V14' or num == 'V14a' or num == 'V14b' or num == 'V14c' or num == 'V14d'\
           or num == 'V22' or num == 'V22a' or num == 'V22b':
            lexeme = lexeme + wr_lexeme(cells, nel_nal_chel_chal(inf), num)
        else:
            lexeme = 'OOPS'
    return lexeme
    
def el_al(inf):
    r = re.search('(.*)(ե|ա)լ', inf)
    return r.group(1) + '.|' + r.group(1) + r.group(2) + '.'

def nel_nal_chel_chal(inf):
    r = re.search('(.*)(ն|չ)(ե|ա)լ', inf)
    return r.group(1) + '.|'\
           + r.group(1) + r.group(2) + '.|' + r.group(1) + r.group(2) + r.group(3) + '.|'\
           + r.group(1) + 'ր' + '.|' + r.group(1) + 'ր' + r.group(3) + '.'

def wr_lexeme(cells, stems, num):
    s = '-lexeme:'\
    + '\n lex: ' + cells[0]\
    + '\n stem: ' + stems\
    + '\n paradigm: ' + num\
    + '\n gramm: ' + cells[1] + ',' + cells[2] + ',' + cells[3]\
    + '\n gloss: ' + cells[5] + '\n\n'
    return s

if __name__ == '__main__':
    main()
