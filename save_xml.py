from subprocess import call
from urllib import request
import xml.etree.ElementTree as ET
from conceptnet5.edges import make_edge
from conceptnet5.formats.msgpack_stream import MsgpackStreamWriter
from conceptnet5.uri import Licenses
from conceptnet5.nodes import standardized_concept_uri
from conceptnet5.formats.convert import msgpack_to_tab_separated

EMOJI_LANGUAGES = [
    'af', 'am', 'ar', 'as', 'az', 'be', 'bg', 'bn', 'bs', 'ca', 'cs', 'cy',
    'da', 'de', 'de_CH', 'el', 'en', 'en_001', 'es', 'es_419', 'et', 'eu',
    'fa', 'fi', 'fil', 'fr', 'ga', 'gl', 'gu', 'he', 'hi', 'hr', 'hu', 'hy',
    'id', 'is', 'it', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ky', 'lo', 'lt',
    'lv', 'mk', 'ml', 'mn', 'mr', 'ms', 'my', 'nb', 'ne', 'nl', 'or', 'pa',
    'pl', 'pt', 'pt_PT', 'ro', 'ru', 'si', 'sk', 'sl', 'sq', 'sr', 'sr_Latn',
    'sv', 'sw', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'zh',
    'zh_Hant', 'zu'
]

url = "http://unicode.org/repos/cldr/tags/latest/common/annotations/"
raw_path = "data/raw/emoji/"
reference_path = "testdata/reference/edges/emoji/"

REL = '/r/SymbolOf'
DATASET = '/d/emoji'
LICENSE = Licenses.cc_attribution
SOURCE = [{'contributor': '/s/resource/unicode/cldr/31'}]

def strip_words(text):
    """
    When multiple words (separated by '|') are
    used to describe emojis, we need to remove the
    '|' in order to create edges for each word.
    This function takes out the '|' and puts all
    the words into a list.
    """
    return text.split(' | ')

for lang in EMOJI_LANGUAGES:
	xml_file_to_save = open(raw_path + lang + ".xml", "w")
	print("<ldml>\n\t<identity>\n\t\t<version number=\"$Revision$\"/>\n\t\t<language type=\"{}\"/>\n\t</identity>".format(lang), file=xml_file_to_save)
	print("\t<annotations>", file=xml_file_to_save)
	out = MsgpackStreamWriter(reference_path + lang + ".msgpack")
	r = request.urlopen(url+ lang + ".xml")
	tree = ET.parse(r)
	root = tree.getroot()
	for i in range(10):
		text = root[1][i].text
		emoji = root[1][i].attrib['cp']
		for word in strip_words(root[1][i].text):
			start = standardized_concept_uri('mul', root[1][i].attrib['cp'])   
			end = standardized_concept_uri(lang, word)
			edge = make_edge(REL, start, end, DATASET, LICENSE, SOURCE)
			out.write(edge)
		print("\t\t<annotation cp=\"{}\" type=\"tts\">{}</annotation>".format(emoji, text), file=xml_file_to_save)
	print("\t</annotations>\n</ldml>", file=xml_file_to_save)
	xml_file_to_save.close()

for lang in EMOJI_LANGUAGES:
	msgpack_to_tab_separated(reference_path+lang+".msgpack",reference_path+lang+".csv")