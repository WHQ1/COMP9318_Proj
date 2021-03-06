import pandas as pd
import numpy as np
import pandas2arff as pd2a
import string
import nltk

# Phonemes
vowels= ('AA','AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH'
, 'IY', 'OW', 'OY', 'UH', 'UW')

consonants= ('P', 'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M','N',
 				'NG', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH')
suffixes=('inal','tion','sion','osis','oon','sce','que','ette','eer','ee','aire','able','ible','acy','cy','ade','age','al','al','ial','ical','an','ance','ence',
		'ancy','ency','ant','ent','ant','ent','ient','ar','ary','ard','art','ate','ate','ate','ation','cade','drome','ed','ed','en','en','ence','ency','er','ier',
		'er','or','er','or','ery','es','ese','ies','es','ies','ess','est','iest','fold','ful','ful','fy','ia','ian','iatry','ic','ic','ice','ify','ile',
		'ing','ion','ish','ism','ist','ite','ity','ive','ive','ative','itive','ize','less','ly','ment','ness','or','ory','ous','eous','ose','ious','ship','ster',
		'ure','ward','wise','ize','phy','ogy')

prefixes=('ac','ad','af','ag','al','an','ap','as','at','an','ab','abs','acer','acid','acri','act','ag','acu','aer','aero','ag','agi',
			'ig','act','agri','agro','alb','albo','ali','allo','alter','alt','am','ami','amor','ambi','ambul','ana','ano','andr','andro','ang',
			'anim','ann','annu','enni','ante','anthrop','anti','ant','anti','antico','apo','ap','aph','aqu','arch','aster','astr','auc','aug',
			'aut','aud','audi','aur','aus','aug','auc','aut','auto','bar','be','belli','bene','bi','bine','bibl','bibli','biblio','bio','bi',
			'brev','cad','cap','cas','ceiv','cept','capt','cid','cip','cad','cas','calor','capit','capt','carn','cat','cata','cath','caus','caut'
			,'cause','cuse','cus','ceas','ced','cede','ceed','cess','cent','centr','centri','chrom','chron','cide','cis','cise','circum','cit',
			'civ','clam','claim','clin','clud','clus claus','co','cog','col','coll','con','com','cor','cogn','gnos','com','con','contr','contra',
			'counter','cord','cor','cardi','corp','cort','cosm','cour','cur','curr','curs','crat','cracy','cre','cresc','cret','crease','crea',
			'cred','cresc','cret','crease','cru','crit','cur','curs','cura','cycl','cyclo','de','dec','deca','dec','dign','dei','div','dem','demo',
			'dent','dont','derm','di','dy','dia','dic','dict','dit','dis','dif','dit','doc','doct','domin','don','dorm','dox','duc','duct','dura',
			'dynam','dys','ec','eco','ecto','en','em','end','epi','equi','erg','ev','et','ex','exter','extra','extro','fa','fess','fac','fact',
			'fec','fect','fic','fas','fea','fall','fals','femto','fer','fic','feign','fain','fit','feat','fid','fid','fide','feder','fig','fila',
			'fili','fin','fix','flex','flect','flict','flu','fluc','fluv','flux','for','fore','forc','fort','form','fract','frag',
			'frai','fuge','fuse','gam','gastr','gastro','gen','gen','geo','germ','gest','giga','gin','gloss','glot','glu','glo','gor','grad','gress',
			'gree','graph','gram','graf','grat','grav','greg','hale','heal','helio','hema','hemo','her','here','hes','hetero','hex','ses','sex','homo',
			'hum','human','hydr','hydra','hydro','hyper','hypn','an','ics','ignis','in','im','in','im','il','ir','infra','inter','intra','intro','ty',
			'jac','ject','join','junct','judice','jug','junct','just','juven','labor','lau','lav','lot','lut','lect','leg','lig','leg','levi','lex',
			'leag','leg','liber','liver','lide','liter','loc','loco','log','logo','ology','loqu','locut','luc','lum','lun','lus','lust','lude','macr',
			'macer','magn','main','mal','man','manu','mand','mania','mar','mari','mer','matri','medi','mega','mem','ment','meso','meta','meter','metr',
			'micro','migra','mill','kilo','milli','min','mis','mit','miss','mob','mov','mot','mon','mono','mor','mort','morph','multi','nano','nasc',
			'nat','gnant','nai','nat','nasc','neo','neur','nom','nom','nym','nomen','nomin','non','non','nov','nox','noc','numer','numisma','ob','oc',
			'of','op','oct','oligo','omni','onym','oper','ortho','over','pac','pair','pare','paleo','pan','para','pat','pass','path','pater','patr',
			'path','pathy','ped','pod','pedo','pel','puls','pend','pens','pond','per','peri','phage','phan','phas','phen','fan','phant','fant','phe',
			'phil','phlegma','phobia','phobos','phon','phot','photo','pico','pict','plac','plais','pli','ply','plore','plu','plur','plus','pneuma',
			'pneumon','pod','poli','poly','pon','pos','pound','pop','port','portion','post','pot','pre','pur','prehendere','prin','prim','prime',
			'pro','proto','psych','punct','pute','quat','quad','quint','penta','quip','quir','quis','quest','quer','re','reg','recti','retro','ri','ridi',
			'risi','rog','roga','rupt','sacr','sanc','secr','salv','salu','sanct','sat','satis','sci','scio','scientia','scope','scrib','script','se',
			'sect','sec','sed','sess','sid','semi','sen','scen','sent','sens','sept','sequ','secu','sue','serv','sign','signi','simil','simul','sist','sta',
			'stit','soci','sol','solus','solv','solu','solut','somn','soph','spec','spect','spi','spic','sper','sphere','spir','stand','stant','stab',
			'stat','stan','sti','sta','st','stead','strain','strict','string','stige','stru','struct','stroy','stry','sub','suc','suf','sup','sur','sus',
			'sume','sump','super','supra','syn','sym','tact','tang','tag','tig','ting','tain','ten','tent','tin','tect','teg','tele','tem','tempo','ten',
			'tin','tain','tend','tent','tens','tera','term','terr','terra','test','the','theo','therm','thesis','thet','tire','tom','tor','tors','tort'
			,'tox','tract','tra','trai','treat','trans','tri','trib','tribute','turbo','typ','ultima','umber','umbraticum','un','uni','vac','vade','vale',
			'vali','valu','veh','vect','ven','vent','ver','veri','verb','verv','vert','vers','vi','vic','vicis','vict','vinc','vid','vis','viv','vita','vivi'
			,'voc','voke','vol','volcan','volv','volt','vol','vor','with','zo')

suffixes_set = {suffix.upper() for suffix in suffixes}
prefixes_set = {prefix.upper() for prefix in prefixes}

vector_map = vowels + consonants

def read_data(file_path):
    with open(file_path) as f:
        lines = f.read().splitlines()
    return lines

def as_tuple(list_to_convert):
    return tuple(list_to_convert)

# Filter numbers from string
def filter_stress(string):
    if type(string) in [list,tuple]:
        string = ' '.join(string)
    return ''.join([i for i in string if not i.isdigit()]).split()

# Maps the location of the stress, 1 if stress at position
# 0 otherwise
def stress_map(pronunciation,stress='1'):
    return [1 if stress in num else 0 for num in pronunciation]

# Maps the the location of phenom, 1 in phenom_list
# 0 otherwise
def phoneme_map(pronunciation, phoneme_list):
    return [1 if phoneme in phoneme_list else 0 for phoneme in pronunciation]

# Map existance of one iterable in another
def iterable_map(list_to_map, iterable):
    return [1 if iter_item in list_to_map else 0 for iter_item in iterable]


def get_pos_tag(word):
    return nltk.pos_tag([word])[0][1]

# Returning string as a classification
def get_stress_position(stress_map,stress=1):
    return str(stress_map.index(stress) + 1)

# Check if prefix exists
def check_prefix(word):
    for letter_idx in range(len(word) + 1):
        if word[:letter_idx] in prefixes_set:
            return 1
    return 0

# Check if suffix exists
def check_suffix(word):
    word_length = len(word)
    for letter_idx in range(word_length + 1):
        if word[abs(letter_idx-word_length) :] in suffixes_set:
            return 1
    return 0

def get_first_letter_idx(word):
    return string.ascii_lowercase.index(word[0].lower()) + 1

def get_stressed_vowel(pn_list):
    for vowel in pn_list:
        if '1' in vowel:
            return filter_stress(vowel)[0]

'''
Dataframe to hold list of words
word : Word
pronunciation: String of phonemes
pn_list: List of pronunciation phonemes
primary_stress_map: binary vecotr with position of primary stress
primary_stress_idx: Index of primary stress
secondary_stress_map: binary vector with position of secondary stress
vowel_map: binary vector with position of vowels
consonant_map: binary vector with position of consonants
vector_map: Binary vector for vowel and constant existance
type_tag: Pos_Tag for the word from nltk
first_letter_index: Alphabetic index of first letter
phenom_length: Number of phonemes
prefix: 1 if prefix exists 0 otherwise
suffix: 1 if suffix exists 0 otherwise
'''

def get_words(file_path):
    words = pd.read_csv(file_path,sep=':',names=['word','pronunciation'])
    words['pn_list'] = words.pronunciation.apply(str.split)
    words['destressed_pn_list'] = words.pronunciation.apply(filter_stress)
    words['primary_stress_map'] = words.pn_list.apply(stress_map)
    words['secondary_stress_map'] = words.pn_list.apply(stress_map,stress='2')
    words['vowel_map'] = words.destressed_pn_list.apply(phoneme_map,args=(vowels,))
    words['consonant_map'] = words.destressed_pn_list.apply(phoneme_map, args=(consonants,))
    words['vector_map'] = words.destressed_pn_list.apply(iterable_map, args=(vector_map,))
    words['vowel_count'] = words.vowel_map.apply(np.sum)
    words['consonant_count'] = words.consonant_map.apply(np.sum)
    words['type_tag'] = words.word.apply(get_pos_tag)
    words['1st_letter_idx'] = words.word.apply(get_first_letter_idx)
    words['phoneme_length'] = words.pn_list.str.len()
    words['prefix'] = words.word.apply(check_prefix)
    words['suffix'] = words.word.apply(check_suffix)
    #words['prefix_suffix_vector'] = words.
    words['primary_stress_idx'] = words.primary_stress_map.apply(get_stress_position)
    words['stressed_vowel'] = words.pn_list.apply(get_stressed_vowel)

    # Unpack vector map into single columns
    unpacked_vector_map = pd.DataFrame.from_records(words.vector_map.tolist(),columns=vector_map)
    words = pd.concat([words, unpacked_vector_map],axis=1)

    return words

if __name__ == '__main__':
    data_loc = 'asset/training_data.txt'
    words = get_words(data_loc)
    words.head()

    columns = ['word','type_tag','1st_letter_index','phoneme_length','suffix','prefix','primary_stress_idx']
    pd2a.pandas2arff(words_df[columns],'weka/word_typetag.arff','word_typetag')
