import os
import scripts
import zipfile
import urllib.request
import glob2
from distutils.dir_util import copy_tree
import shutil
import click

data_directory = '.sleepy_files/'
datapath = os.path.expanduser('~') + "/" + data_directory


def get_gitignores():
    files_hash = {}
    if not os.path.exists(datapath):
        return files_hash

    datapath_for_search = datapath + '**/*.gitignore'
    for filename in glob2.glob(datapath_for_search):
        if filename.endswith('.gitignore'):
            files_hash[(filename.split('/')[-1]).split('.')
                       [0].lower()] = filename

    return files_hash


@click.group()
def main():
    pass


@main.command(name='generate')
@click.argument('gitignore_files', nargs=1, required=True)
@click.pass_context
def generate(ctx, gitignore_files): #enerate gitignore files
    gitignores_to_generate = gitignore_files.split(',')
    gitignores_to_generate = [string.lower()
                              for string in gitignores_to_generate]

    goofy_data = get_gitignores()
    not_found = []
    output_string = ""

    if len(goofy_data.keys()):
        for file_name in gitignores_to_generate:
            if file_name.lower() in goofy_data:
                output_string += "\n\n### " + file_name + "\n"

                with open(goofy_data[file_name.lower()], 'r') as gitignore_file:
                    content = gitignore_file.read()

                output_string += str(content)
            else:
                not_found.append(file_name)

        if not_found:
            not_found_files = ', '.join(not_found)
            print("\nUnsupported files:", not_found_files)
            print('Run `sleepy ls` to see list of available gitignore files.\n\n')

        if len(output_string) > 0:
            output_string = "Generated by Sleepy (https://github.com/benmshapiro/sleepy)" + \
                output_string
            print(output_string)

    else:
        print(
            "\ngitignore files are not found. Run `sleepy update` to update the files\n")


@main.command(name='update')
@click.pass_context

def update(ctx): #Update all gitignore files
    print("Downloading gitignore files...")
    gitignore_url = "https://github.com/github/gitignore/archive/master.zip"
    zip_path = urllib.request.urlretrieve(gitignore_url, '/tmp/master.zip')

    zip_ref = zipfile.ZipFile('/tmp/master.zip', 'r')
    zip_ref.extractall('/tmp')
    copy_tree("/tmp/gitignore-master/", datapath)

    print("\ngitignore files are stored in " + datapath)
    zip_ref.close()

@main.command(name='ls')
@click.pass_context

def list(ctx): #list all gitignore files
    files = get_gitignores()
    file_name_list = []
    if len(files.keys()):
        print("Total gitignore files: " + str(len(files)))
        print()
        for file_name in sorted(files.keys()):
            file_name_list.append(file_name)
        all_gitignores = ', '.join(file_name_list)
        print(all_gitignores)

    else:
        print(
            "\ngitignore files are not found. Run `sleepy update` to update the files\n")