import os
import csv
import re
import xml.etree.ElementTree as ET

# Folgende zwei Variablen nach Wunsch anpassen
path_to_directory = os.path.join('tagged') # Pfad zum Ordner kann hier angegeben werden, z.B.: os.path.join('..', 'ordner', 'subordner', 'tagged')
directory = 'entry' # Einen der folgenden Ordner auswählen: entry | det | res | au | ae | ae_se

# Struktur, in welchem Tag Titel oder Autor vorhanden ist. Dies unterscheidet sich je nach Ordner.
dictionary = {'entry':  {'title': ['ti'], 'author': ['au']},
              'det':    {'title': ['ti'], 'author': ['au']},
              'res':    {'title': ['ti'], 'author': ['au']},
              'au':     {'title': ['ti'], 'author': ['au', 'a']},
              'ae':     {'title': ['ti'], 'author': ['au', 'a']},
              'ae_se':  {'title': ['ti'], 'author': ['au', 'a']}
              }


def check_directory(directory='entry'):
    path_to_files = os.path.join(path_to_directory, directory)
    filenames = os.listdir(path_to_files)
    filenames.sort()

    entries = []
    missing_titles = []
    author_wrong = []
    corrupt_files = []

    for filename in filenames:
        if filename.endswith('.xml'):
            file_entries, file_missing_titles, file_author_wrong, corrupt_file = check_xml_file(directory, filename)
            entries.append(file_entries)
            missing_titles.append(file_missing_titles)
            author_wrong.append(file_author_wrong)
            if not corrupt_file is None:
                corrupt_files.append(corrupt_file)

    if len(corrupt_files) > 0:
        print('Folgende Dateien konnten nicht überprüft werden, womöglich sind diese keine validen XML-Dateien:')
        for corrupt_file in corrupt_files:
            print(corrupt_file)

    with open(directory + '_Entries.tsv', 'w') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['ID', 'Autor', 'Titel'])
        for file_entries in entries:
            for entry in file_entries:
                w.writerow([entry['id'], entry['author'], entry['title']])

    with open(directory + '_Fehlende_Titel.tsv', 'w') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['ID', 'Autor'])
        for file_missing_titles in missing_titles:
            for entry in file_missing_titles:
                w.writerow([entry['id'], entry['author']])

    with open(directory + '_Falscher_Autor.tsv', 'w') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['ID', 'Autor', 'Vorheriger Autor ID', 'Vorheriger Autor'])
        for file_author_wrong in author_wrong:
            for entry in file_author_wrong:
                w.writerow([entry['id'], entry['author'], entry['previous_author']['id'], entry['previous_author']['author']])


def use_regex(str):
    p_whitespace = re.compile('\s')
    p_c_accent_uppercase = re.compile('Ç')
    p_c_accent_lowercase = re.compile('ç')
    p_e_accent_uppercase = re.compile('[ÉÈÊË]')
    p_e_accent_lowercase = re.compile('[éèêë]')
    p_i_accent_uppercase = re.compile('[ÎÏÍÌ]')
    p_i_accent_lowercase = re.compile('[îïíì]')

    s = str
    s = p_whitespace.sub('', s)
    s = p_c_accent_uppercase.sub('C', s)
    s = p_c_accent_lowercase.sub('c', s)
    s = p_e_accent_uppercase.sub('E', s)
    s = p_e_accent_lowercase.sub('e', s)
    s = p_i_accent_uppercase.sub('I', s)
    s = p_i_accent_lowercase.sub('i', s)
    return s


def check_xml_file(directory, filename):
    entries = []
    missing_titles = []
    author_wrong = []
    previous_author = {}
    try:
        tree = ET.parse(os.path.join(path_to_directory, directory, filename))
    except ET.ParseError:
        return entries, missing_titles, author_wrong, filename
    root = tree.getroot()
    for document in root.findall('document'):
        entry = document.find('entry')
        id = extract(entry, ['id'])
        author = extract(entry, dictionary[directory]['author'])
        title = extract(entry, dictionary[directory]['title'])
        entries.append({'id': id, 'author': author, 'title': title})
        if title is None:
            missing_titles.append({'id': id, 'author': author})
        if author is not None:
            if previous_author and previous_author != '?':
                previous_to_compare = use_regex(previous_author['author'])
                author_to_compare = use_regex(author)
                if previous_to_compare > author_to_compare and \
                        not previous_to_compare.startswith(author_to_compare) and \
                        not author_to_compare.startswith(previous_to_compare):
                    author_wrong.append({'id': id, 'author': author, 'previous_author': previous_author.copy()})
            previous_author['id'] = id
            previous_author['author'] = author
        elif previous_author and previous_author != '?':
            author_wrong.append({'id': id, 'author': None, 'previous_author': previous_author.copy()})

    return entries, missing_titles, author_wrong, None


def extract(xml, path):
    while len(path) > 1:
        xml = xml.find(path[0])
        if xml is None:
            return None
        path = path[1:]
    if xml.find(path[0]) is None:
        return None
    return xml.find(path[0]).text


if __name__ == '__main__':
    check_directory(directory)
