import os
import re
import parse_imdb_annotations as annotation



ROOT_FOLDER = 'imdb_plot_data_set'
TEST_DATA_FOLDER = "test_data"
TRAIN_DATA_FOLDER = "train_data"
#PLOT_LIST_FILE_NAME = 'test_plot_list.txt' 
#PLOT_LIST_FILE_NAME = 'plot_list_short.txt' 
PLOT_LIST_FILE_NAME = 'plot.list' 

NO_CATEGORY_FOLDER = "no_category"

def is_title_line(line):
    title_line_matcher = '^MV:.*' 
    return re.match(title_line_matcher, line)

def is_plot_line(line):
    plot_line_matcher = '^PL:.*' 
    return re.match(plot_line_matcher, line)

def is_break_line(line):
    break_line_matcher = '^---.*' 
    return re.match(break_line_matcher, line)

def get_plot_text(line):
    plot_line_matcher = 'PL:(.*)'
    plot_line = re.search(plot_line_matcher, line).group(1)
    return plot_line

def print_plot_to_file(filepath, plot_lines):  
    with open(filepath, 'w') as f:
        for line in plot_lines:
            text = get_plot_text(line)
            f.write(text+'\n')

def print_test_data_plot(plot_lines, file_name, annotated_movies, categories, test_folder, train_folder, no_category_folder):
    if categories:
        #Create directories if necessery 
        for category in categories:
            folder = os.path.join(test_folder, category)
            if not os.path.exists(folder):
                os.makedirs(folder)
        # print plot to every category folder
        for category in categories:
            folder = os.path.join(test_folder, category)
            filepath = os.path.join(folder, file_name)
            print_plot_to_file(filepath, plot_lines)
    else:
        filepath = os.path.join(no_category_folder,file_name)
        print_plot_to_file(filepath, plot_lines)

def print_train_data_plot(plot_lines, file_name, train_folder):
    # Check if film belong to test set
    filepath = os.path.join(train_folder,file_name)
    print_plot_to_file(filepath, plot_lines)

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

def create_data_set(plot_list_file_name, root_folder, test_folder, train_folder, no_category_folder):
    test_folder = os.path.join(root_folder, test_folder)
    train_folder = os.path.join(root_folder, train_folder)
    no_category_folder = os.path.join(test_folder, no_category_folder)

    create_root_folders(root_folder,test_folder,train_folder,no_category_folder)

    # get annotation list 
    annotation_map = annotation.get_annotation_map()
    annotated_movies = annotation_map.keys()

    plot_lines = []
    file_name = None
    #pdb.set_trace()
    with open(plot_list_file_name, encoding="ISO-8859-1") as f:
        for line in f:
            if is_title_line(line):
                title_string = mv_line_to_title_string(line)
                file_name = annotation.title_string_to_file_name(title_string)
            elif is_plot_line(line):
                plot_lines.append(line)
            elif is_break_line(line) and file_name:
                letters_in_plot = [item for sublist in plot_lines for item in sublist]
                if(len(letters_in_plot)>160):
                    if  file_name in annotated_movies:
                        categories = annotation_map[file_name]
                        print(categories)
                        print_test_data_plot(plot_lines, file_name, annotated_movies, categories, test_folder, train_folder, no_category_folder)
                    else:
                        print_train_data_plot(plot_lines,file_name,train_folder)                
                # reset variables
                title_string = None
                plot_lines = []
                file_name = None
            else:
                pass


import pdb
create_data_set(PLOT_LIST_FILE_NAME, ROOT_FOLDER, TEST_DATA_FOLDER, TRAIN_DATA_FOLDER, NO_CATEGORY_FOLDER)