import os
import shutil
import tempfile

from . import tikz
from . import calculate
from . import compile_tex
from . import combine_pdfs
from ..mplot import make_plot

def gen_content(data, str_appendix=''):
    ''' TODO Describe me please

    A str_appendix is recommended if this script is used to combine the generated tikz code with another set of generated tikz code:
    Allowing to merge two or multiple generated tikz is somewhat in progress and I am not sure if and when this will be completely supported.
    '''
    # img/element blocks
    # Usually an img/block consists only of an image node (with or without frames) and some paddings between other image nodes.
    # However, it can also contain a complex subset of nodes (caption titles on each side) - if so desired.
    content = tikz.gen_all_image_blocks(data, str_appendix)

    # titles that have content for each row or column
    content += tikz.add_col_and_row_titles(data, str_appendix)

    # figure title (positions around the figure facing: north, south, east, west)
    content += tikz.add_big_titles(data, str_appendix)

    # outer spacing
    content += tikz.add_all_outer_paddings(data, str_appendix)

    # write into json height and width. # CAREFUL: NOT frames included if frame line width > paddings
    data['total_height'] = calculate.get_total_height(data)
    data['total_width'] = calculate.get_total_width(data)
    print('total width of generated tikz module: ', data['total_width'])
    print('total height of generated tikz module: ', data['total_height'])

    return content

def begin_tikz_document(background_color):
    beginnig = '\\usetikzlibrary{backgrounds} \n'
    beginnig += '\\begin{document}\n'
    beginnig += '\\tikzstyle{background rectangle}=[fill='+ tikz.gen_tikZ_rgb255(background_color) + '] \n'
    beginnig += '\\begin{tikzpicture}[show background rectangle,inner frame sep=0pt]\n\n'
    return beginnig

def create_header(background_color):
    header = combine_pdfs.documentclass()
    # used package 'libertine', but maybe let the user decide which font-family he wants
    header += combine_pdfs.use_packages(["{comment}", "{amsmath}", "{tikz}", "[T1]{fontenc}", "{libertine}"])
    header += begin_tikz_document(background_color)
    return header

def write_into_tex_file(path, body_content, file_name, background_color=[255,255,255]):
    header = create_header(background_color)
    ending = '\n\\end{tikzpicture}\n\\end{document}'
    whole_content = header + body_content + ending

    f = open(os.path.join(path, file_name), 'w')
    f.write(whole_content)
    f.close()

def delete_gen_images(data):
    for row in data['elements_content']:
        for elem in row:
            os.remove(os.path.join(elem['filename']))


def generate(module_data, to_path, index, temp_folder, delete_gen_files=True):
    tex_filename = 'gen_tex'+str(index)+'.tex'
    pdf_filename = tex_filename.replace('tex', 'pdf')

    if module_data['type'] == 'grid':
        content = gen_content(module_data)
        write_into_tex_file(temp_folder, content, tex_filename, background_color=module_data['background_color'])
        compile_tex.compile(temp_folder, tex_filename, pdf_filename)
    elif module_data['type'] == 'plot':
        make_plot.generate(module_data, temp_folder, pdf_filename)
    else:
        raise "unsupported module type '" + module_data['type'] + "'"

    if delete_gen_files:
        try:
            os.remove(os.path.join(to_path, tex_filename))
            delete_gen_images(module_data)
        except:
            pass

    return pdf_filename

def combine(data, filename, temp_folder, delete_gen_files=True):
    combine_pdfs.make_pdf(temp_folder, delete_gen_files=delete_gen_files)
    gen = os.path.join(temp_folder, "gen_figure.pdf")
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    shutil.copy(gen, filename)
    print('Tikz/LaTeX file was generated.')