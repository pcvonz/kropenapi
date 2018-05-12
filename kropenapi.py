import requests
from xml.etree import ElementTree
from urllib.parse import urlencode


class KROpenApi():
    headers = []
    krApiUrl = 'https://krdict.korean.go.kr/api/'

    sort = 'dict'  # either dict or popular
    sortOptions = {
            'Dictionary': 'dict',
            'Popular': 'popular'
            }

    method = 'exact'

    method_option = {
            'exact': 'exact',
            'include': 'include',
            'start': 'start',
            'end': 'end'
            }

    num = 10  # number of entries to return
    translationEnabled = 'y'
    advancedEnabled = 'n'

    trans = 'English'

    transOptions = {
            'Full Translation': '0',
            'English': '1',
            'Japanese': '2',
            'French': '3',
            'Spanish': '4',
            'Arabic': '5',
            'Mongolian': '6',
            'Vietnamese': '7',
            'Russian': '8',
            }

    part = 'Word'

    partOptions = {
            'Word': 'word',
            'IP': 'ip',
            'Definition': 'dfn',
            'Examples': 'exam'
            }

    target = 'Headword'

    targetOptions = {
            'Headword': 1,
            'Solve': 2,
            'Examples': 3,
            'Original Language': 4,
            'Pronunciation': 5,
            'Utilization': 6,
            'Idiom': 7,
            'Proverb': 8,
            }

    multimedia = 'Photo'

    multiMediaOptions = {
            'Full': 0,
            'Photo': 1,
            'Annealing': 2,
            'Video': 3,
            'Animation': 4,
            'Sound': 5,
            'None': 6
            }

    searchMethod = 'Exact'

    searchMethodOptions = {
            'Exact': 'exact',
            'Includ': 'include',
            'Start': 'start',
            'End': 'end'
            }

    start = 1

    viewMethod = 'Word Info'

    viewMethodOptions = {
            'Word Info': 'word_info',
            'Target Code': 'target_code'
            }

    def __init__(self, key):
        self.key = key

    # Searches and returns a korean word
    # Part: word, ip, dfn, exam
    def searchExamples(self, q):
        headers = {'content-type': 'application/xml',
                   'Accept': 'application/xml'
                   }
        params = urlencode({
            'key': self.key,
            'type_search': 'search',
            'part': self.partOptions['Examples'],
            'method': self.method,
            'q': q,
            'sort': 'dict'
        })
        url = self.krApiUrl + 'search?' + params
        response = requests.get(url, headers)
        tree = ElementTree.fromstring(response.text)
        try:
            return self.buildKoreanExamples(tree)
        except:
            return []

    # Searches and returns a korean word
    # Part: word, ip, dfn, exam
    def searchWord(self, q):
        headers = {'content-type': 'application/xml',
                   'Accept': 'application/xml'
                   }
        params = urlencode({
            'key': self.key,
            'part': self.partOptions['Word'],
            'q': q,
            'translated': self.translationEnabled,
            'trans_lang': self.transOptions[self.trans],
            'advanced': self.advancedEnabled,
            'target': self.targetOptions[self.target],
            'multimedia': self.searchMethodOptions[self.searchMethod],
            'start': self.start
        })
        url = self.krApiUrl + 'search?' + params
        r = requests.get(url, headers)
        tree = ElementTree.fromstring(r.text)
        try:
            return self.buildKoreanTranslations(tree)
        except:
            return []

    def buildKoreanExamples(self, tree):
        dictionary_entries = []
        for item in tree.findall('item'):
            entry = {'word': item.find('word').text}
            entry['example'] = item.find('example').text.strip()
            dictionary_entries.append(entry)
        return dictionary_entries

    def buildKoreanTranslations(self, tree):
        dictionary_entries = []
        for item in tree.findall('item'):
            entry = {'word': item.find('word').text}
            entry['pos'] = item.find('pos').text
            senses = item.findall('sense')
            entry_definition = {}
            entry['entry_definitions'] = []
            for sense in senses:
                entry_definition['definition_korean'] = sense.find('definition').text
                entry_definition['definitions_trans'] = sense.find('translation').find('trans_dfn').text
                entry['entry_definitions'].append(entry_definition)
            dictionary_entries.append(entry)
        return dictionary_entries

    def disableTranslation(self):
        self.translationEnabled = 'n'

    def enableTranslation(self):
        self.translationEnabled = 'y'

    def enableAdvanced(self):
        self.advancedEnabled = 'y'

    def disableAdvanced(self):
        self.advancedEnabled = 'y'

    def setPart(self, part):
        self.part = self.partOptions[part]

    def setTranslatedLanguage(self, trans):
        self.trans = trans

    def setTarget(self, target):
        self.target = target

    def setMultiMediaType(self, type):
        self.multimedia = self.multiMediaOptions[type]

    def setSort(self, sort):
        self.sort = self.sortOptions[sort]


if __name__ == "__main__":
    import sys

    k = KROpenApi()
    print(k.searchWord(sys.argv[1]))
    print(k.searchExamples(sys.argv[1]))

