#! python3
import glob
import os
import re
import sys
import shutil

## List the files that are edited (thus files that are not copied) in each step


def list_file():
  for entry, dirs, files in sorted(os.walk('lesson_snaps')):
    dirs[:] = [d for d in dirs if not "shared" in d]

    # find test.js
    for file in files:
      if file == "test.js":
        pattern = re.compile("lesson_editor")

        # get the file name we're editing
        for line in open(os.path.join(entry, file), "r"):
          for match in re.finditer(pattern, line):
            file_pattern = "'(.*?)\'"
            edit_file = re.search(file_pattern, line).group(1)
            path = os.path.join(entry, file)
            step_dir = path.split("/")[1]
            step = step_dir.split("-")[0]
            print(step + ":", edit_file)


def walklevel(some_dir, level=1):
  some_dir = some_dir.rstrip(os.path.sep)
  assert os.path.isdir(some_dir)
  num_sep = some_dir.count(os.path.sep)
  for root, dirs, files in os.walk(some_dir):
    yield root, dirs, files
    num_sep_this = root.count(os.path.sep)
    if num_sep + level <= num_sep_this:
      del dirs[:]


def add_values_in_dict(dict, key, list_of_values):
  if key not in dict:
    dict[key] = list()
  dict[key].extend(list_of_values)
  # return dict


## Copy file src to the destination
def copy_contents(src, dest):
  step_dict = {}  # all steps
  dest_dict = {}  # steps to copy
  src_dirs = []
  src_files = []
  src_path_files = []

  # FOR LOOP FOR EVERY FILE AND DIRECTORY
  for entry, dirs, files in sorted(walklevel('lesson_snaps', level=1)):
    dirs[:] = [d for d in dirs if not "shared" in d]

    # Create step_dict
    for dir in sorted(dirs):
      # put begin,input,result in dictionary (key=step, value=dir array)
      step = dir.split("-")[0]
      add_values_in_dict(step_dict, step, [dir])

    # Create dest_dict
    temp = list(step_dict)
    for key in step_dict.keys():

      if key == src:
        # make source dir array
        src_dirs = step_dict[key]

        if temp[temp.index(key) + 1] == dest:
          dest_dict[dest] = step_dict[dest]
          break

        # create dest_dict
        next = temp[temp.index(key) + 1]
        dest_dict[next] = step_dict[next]
        while True:
          dest_dict[next] = step_dict[next]
          next = temp[temp.index(next) + 1]
          if next == dest:
            dest_dict[next] = step_dict[next]
            break

  # make src file with and without path
  result_dir = src_dirs[-1]
  source_path = os.path.join('lesson_snaps', result_dir)
  for entry, dirs, files in sorted(os.walk(source_path)):
    for file_dir in dirs:
      if file_dir == "editor":
        source_path_2 = os.path.join(source_path, file_dir)
        for file in os.listdir(source_path_2):
          file_path = os.path.join(source_path_2, file)
          src_path_files.append(file_path)
          src_files.append(file)

  # For loop through dest_dict
  for key, value in dest_dict.items():
    no_copy_file = ""
    # Go through each directory (step020-begin etc) in dest_dict
    for step_dir in value:
      # find NOT TO edit file
      step_path = os.path.join('lesson_snaps', step_dir)
      # FOR LOOP FOR EVERY FILE AND DIRECTORY
      for entry, dirs, files in sorted(os.walk(step_path)):
        #print(step_path)
        # for each file
        for file in sorted(files):
          if file == "test.js":
            pattern = re.compile("lesson_editor")

            # get NO edit file
            for line in open(os.path.join(entry, file), "r"):
              for match in re.finditer(pattern, line):
                file_pattern = "'(.*?)\'"
                no_copy_file = re.search(file_pattern, line).group(1)

    # COPY FILES
    for step_dir in value:
      step_path = os.path.join('lesson_snaps', step_dir)
      for entry, dirs, files in sorted(os.walk(step_path)):
        for dir in dirs:
          if dir == "editor":
            lesson_path = os.path.join(step_path, dir)
            lesson_entries = os.listdir(lesson_path)
            for entry in lesson_entries:
              if entry != no_copy_file:
                src_file = src_path_files[src_files.index(entry)]
                entry_path = os.path.join(lesson_path, entry)
                shutil.copyfile(src_file, entry_path)


# check if japanese method
def is_japanese(str):
  return True if re.search(r'[ぁ-んァ-ン]', str) else False


def check_japanese():
  for entry, dirs, files in sorted(os.walk('lesson_snaps')):
    dirs[:] = [d for d in dirs if not "shared" in d]

    for file in files:
      files[:] = [f for f in files if not "check-japanese.py" in f]
      path = os.path.join(entry, file)
      if file == "test.js" or file == "lesson_editor.css" or file == "lesson_editor.html" or file == "lesson_editor.js":
        for line in open(path):
          if is_japanese(line):
            print("Japanese in", os.path.join(entry, file))


def command(command_line_argument):
  if command_line_argument[1] == 'ls':
    list_file()
  elif command_line_argument[1] == 'japanese':
    check_japanese()
  elif command_line_argument[1] == 'copy':
    copy_contents(command_line_argument[2], command_line_argument[3])
  else:
    print("\nPlease pass in the appropriate command line argument.\n ls: lists out all the files that shouldn't be edited\n japanese: check if any files have japanese characters left in it\n copy <source step> <destination step> (e.g. copy step010 step040): copies the content of all the files except the edited ones in source to all the files in the step up to destination.\n")


command(sys.argv)
