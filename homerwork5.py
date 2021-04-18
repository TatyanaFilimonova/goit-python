import re


def normalize (translate_line):
   map = {ord('а'): 'a', ord('А'): 'A',
          ord('б'): 'b',ord('Б'): 'B',
          ord('в'): 'v',ord('В'): 'V',
          ord('г'): 'h',ord('Г'): 'H',
          ord('ґ'): 'g',ord('Ґ'): 'G', 
          ord('д'): 'd',ord('Д'): 'D',
          ord('е'): 'e',ord('Е'): 'E',
          ord('є'): 'ie',ord('Є'): 'Ye',
          ord('ж'): 'zh',ord('Ж'): 'Zh',
          ord('з'): 'z',ord('З'): 'Z', 
          ord('і'): 'i',ord('І'): 'Yi',
          ord('й'): 'i',ord('Й'): 'Y',
          ord('ї'): 'i',ord('Ї'): 'I',
          ord('и'): 'y',ord('И'): 'Y',
          ord('к'): 'k', ord('К'): 'K',
          ord('л'): 'l',ord('Л'): 'L',
          ord('м'): 'm',ord('М'): 'M',
          ord('н'): 'n',ord('Н'): 'N',
          ord('о'): 'o',ord('О'): 'O', 
          ord('п'): 'p',ord('П'): 'P',
          ord('р'): 'r',ord('Р'): 'R',
          ord('с'): 's',ord('С'): 'C',
          ord('т'): 't',ord('Т'): 'T', 
          ord('у'): 'u',ord('У'): 'U',
          ord('ф'): 'f',ord('Ф'): 'F',
          ord('х'): 'kh',ord('Х'): 'Kh',
          ord('ц'): 'ts',ord('Ц'): 'Ts',
          ord('ч'): 'ch',ord('Ч'): 'Ch',
          ord('ш'): 'sh',ord('Ш'): 'Sh', 
          ord('щ'): 'shch',ord('Щ'): 'Shch',
          ord('ю'): 'iu',ord('Ю'): 'Yu',
          ord('я'): 'ia',ord('Я'): 'Ya',
          ord('ь'): ''}
   translated = translate_line.translate(map)
   reg = re.compile ('[^A-Za-z0-9 ]')
   newtranslated = reg.sub('_',translated)
   return newtranslated

print(normalize('Тетяна Розумна !? + Найрозумніша дівчинка в університеті. І Python вона вивчить!!!'))
