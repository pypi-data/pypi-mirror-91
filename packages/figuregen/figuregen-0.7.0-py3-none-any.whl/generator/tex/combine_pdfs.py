import glob
import os
from . import compile_tex

def documentclass():
    return "\\documentclass[varwidth=500cm, border=0pt]{standalone}\n"

def use_packages(list_packages):
    packages = ["{graphicx}", "[utf8]{inputenc}", "{newverbs}"]
    packages.extend(list_packages)
    usepackages = [r"\usepackage" + p + "\n" for p in packages]
    return ''.join(usepackages)

def begin_document():
    return '\\begin{document}\n'

def include_graphics(path, files):
    code = [r'\Verbdef\filename{' + f.replace('\\', '/') + '}' + r'\includegraphics[]{\filename}%' for f in files]
    code.append('')
    body_content = '\n'.join(code)
    return body_content

def end_document():
    return '\end{document}'

def create_tex_content(path, files, list_packages):
    header = documentclass() + use_packages(list_packages)
    beginning = begin_document()
    body = include_graphics(path, files)
    ending = end_document()
    return header + beginning + body + ending

def get_files(path, search_for_filenames):
    pattern = os.path.join(path, search_for_filenames)
    files = glob.glob(pattern)
    return files

def create_tex_file(content, path, filename):
    f = open(os.path.join(path, filename), 'w')
    f.write(content)
    f.close()

def delete_files(path, files):
    for f in files:
        os.remove(f)

def make_pdf(path, search_for_filenames='gen_pdf*.pdf', list_packages=[], delete_gen_files=True):
    files = get_files(path, search_for_filenames)
    content = create_tex_content(path, files, list_packages)

    tex_filename = 'gen_tex.tex'
    create_tex_file(content, path, filename=tex_filename)
    compile_tex.compile(path, tex_filename, pdf_filename='gen_figure.pdf')

    if delete_gen_files:
        os.remove(os.path.join(path, tex_filename)) # delete .tex file after compiling to .pdf
        delete_files(path, files)

