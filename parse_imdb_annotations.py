import csv
import re


def get_category_list(category_string):
    if not re.search('[a-zA-Z]', category_string):
        return []
    category_string.lower()
    category_string.strip()
    return re.split('\*',category_string)

def title_string_to_file_name(title_string):
    title_string.strip()
    title_string = title_string.replace("'", "")
    title_string = title_string.replace('"',"")
    title_string = title_string.replace('/',"")
    title_string = title_string.replace('.',"")
    title_string = title_string.replace(',',"")
    title_string = title_string.replace('(',"")
    title_string = title_string.replace(')',"")
    title_string = re.sub("\s+", '-', title_string)
    title_string = title_string.lower()    
    return title_string


def get_annotation_map():
    annotation_map = {} 
    filename = 'imdb_annotation.csv'
    # filename = 'test.csv'
    with open(filename, encoding="ISO-8859-1") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        header = True
        for row in readCSV:
            if header:
                header = False
            else:
                #Remove all apostrophes, \, .
                title_string = row[0]
                file_name = title_string_to_file_name(title_string)
                category_list = get_category_list(row[2])
                annotation_map[file_name] = category_list
        csvfile.close()
    return annotation_map


# annotation_map = get_annotation_map()
# for a in annotation_map:
#     print(a)
#     print(annotation_map[a])
