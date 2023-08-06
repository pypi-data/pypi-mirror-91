from .gno_gen_stopwords import gno_generalstopwords
from .gno_gen_stopwords import gno_generalstopwords_cn
from .gno_name_stopwords import gno_inpersonname_remove
from .gno_name_stopwords import gno_honorifics_remove
from .gno_coname_stopwords import gno_inconame_stopwords
from .gno_uploadfile_clean import load_files

from .gno_stopwords import gno_generalstopwords, gno_generalstopwords_cn, gno_inpersonname_remove, gno_honorifics_remove, gno_inconame_stopwords
from .gno_stopwordcleaning import Remove_stopwords, Replace_CoStopwords

def joke():
    return (u'simi lan test test.')