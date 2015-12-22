import os
import re
import parse_imdb_annotations as annotation

ROOT_FOLDER = 'imdb_plot_data_set'
TEST_DATA_FOLDER = "test_data"
TRAIN_DATA_FOLDER = "train_data"
# PLOT_LIST_FILE_NAME = 'test_plot_list.txt' 
# PLOT_LIST_FILE_NAME = 'plot_list_short.txt' 
PLOT_LIST_FILE_NAME = 'plot.list' 
TRAIN_DATA_FILE_NO_DELIMETER = 'imdb_plot_data_set/all_plots_train_no_delimeter'
TRAIN_DATA_FILE_DELIMETER = 'imdb_plot_data_set/all_plots_train_delimeter'
NO_CATEGORY_FOLDER = "no_category"
DELIMETER = "-------------"

def is_title_line(line):
    title_line_matcher = '^MV:.*' 
    return re.match(title_line_matcher, line)

def is_plot_line(line):
    plot_line_matcher = '^PL:.*' 
    return re.match(plot_line_matcher, line)

def is_delimeter_line(line):
    break_line_matcher = '^---.*' 
    return re.match(break_line_matcher, line)

def get_plot_text(line):
    plot_line_matcher = 'PL:(.*)'
    plot_line = re.search(plot_line_matcher, line).group(1)
    return plot_line

def write_plot_to_file(filepath, plot_lines):  
    with open(filepath, 'w') as f:
        for line in plot_lines:
            text = get_plot_text(line)
            f.write(text+'\n')

def append_plot_to_file(file_path, plot_lines,delimeter=None):
    with open(file_path, 'a+') as f:
        for line in plot_lines:
            text = get_plot_text(line)
            f.write(text+'\n')
        if delimeter:
            f.write(delimeter+'\n')

def print_test_data_plot(plot_lines, movie_name, annotated_movies, categories, test_folder, train_folder, no_category_folder):
    if categories:
        #Create directories if necessery 
        for category in categories:
            folder = os.path.join(test_folder, category)
            if not os.path.exists(folder):
                os.makedirs(folder)
        # print plot to every category folder
        for category in categories:
            folder = os.path.join(test_folder, category)
            filepath = os.path.join(folder, movie_name)
            write_plot_to_file(filepath, plot_lines)
    else:
        filepath = os.path.join(no_category_folder,movie_name)
        write_plot_to_file(filepath, plot_lines)

def print_train_data_plot(plot_lines, movie_name, train_folder, train_data_file_delimeter, train_data_file_no_delimeter, delimeter):
    # Check if film belong to test set
    filepath = os.path.join(train_folder, movie_name)
    write_plot_to_file(filepath, plot_lines)
    append_plot_to_file(train_data_file_delimeter,plot_lines,delimeter)
    append_plot_to_file(train_data_file_no_delimeter, plot_lines)

def create_root_folders(root_folder,test_folder,train_folder,no_category_folder):
    # Create root foolders
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    if not os.path.exists(train_folder):
        os.makedirs(train_folder)
    if not os.path.exists(no_category_folder):
        os.makedirs(no_category_folder)

def mv_line_to_title_string(title_string):
    title_string = re.sub("^MV: ", '', title_string)
    title_string = title_string.strip()
    return title_string

def create_data_set(plot_list_file_name, root_folder, test_folder, train_folder, no_category_folder, train_data_file_delimeter,train_data_file_no_delimeter, delimeter):
    test_folder = os.path.join(root_folder, test_folder)
    train_folder = os.path.join(root_folder, train_folder)
    no_category_folder = os.path.join(test_folder, no_category_folder)

    create_root_folders(root_folder,test_folder,train_folder,no_category_folder)

    # get annotation list 
    annotation_map = annotation.get_annotation_map()
    annotated_movies = annotation_map.keys()

    title_string = None
    plot_lines = []
    file_name = None
    train_doc_id = 0
    #pdb.set_trace()
    with open(plot_list_file_name, encoding="ISO-8859-1") as f:
        for line in f:
            if is_title_line(line):
                title_string = mv_line_to_title_string(line)
                file_name = annotation.title_string_to_file_name(title_string)
            elif is_plot_line(line):
                plot_lines.append(line)
            elif is_delimeter_line(line) and file_name:
                if  file_name in annotated_movies:
                    # Is test data
                    categories = annotation_map[file_name]
                    print(categories)
                    print_test_data_plot(plot_lines, file_name, annotated_movies, categories, test_folder, train_folder, no_category_folder)
                else:
                    # Is train data
                    doc_delimeter = delimeter+str(train_doc_id)
                    print_train_data_plot(plot_lines, str(train_doc_id),train_folder,train_data_file_delimeter,train_data_file_no_delimeter, doc_delimeter)                                       
                    train_doc_id +=1
                # reset variables
                title_string = None
                plot_lines = []
                file_name = None
            else:
                pass

create_data_set(PLOT_LIST_FILE_NAME, ROOT_FOLDER, TEST_DATA_FOLDER, TRAIN_DATA_FOLDER, NO_CATEGORY_FOLDER, TRAIN_DATA_FILE_DELIMETER, TRAIN_DATA_FILE_NO_DELIMETER, DELIMETER)