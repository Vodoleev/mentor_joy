import argparse
import os
import subprocess

begin_doc = r'\begin{document}'
table_of_contents = r'''{
	\hypersetup{linkcolor=black}
	\tableofcontents
}'''
new_student = 'студент группы {group}\\\\\n\\rule{{2cm}}{{0.15mm}}/{name}/\\\\'
end_doc = r'\end{document}'
settings_templates = {
    'template_0': {'font_size': '12pt', 'paper_size': 'a4paper', 'left': '1.5cm', 'right': '1.5cm', 'top': '0.5cm',
                   'bottom': '1cm'},
    'template_1': {'font_size': '12pt', 'paper_size': 'a4paper', 'left': '2.5cm', 'right': '1cm', 'top': '2cm',
                   'bottom': '2cm'}}
template_1_newrules = r'\newgeometry{bottom=3.5cm, top=2cm, left=2.5cm, right=1cm}'


def make_pdf(type, information_list, result_dir):
    file_name = 'rules.tex'
    example_name = file_name
    add_info(f'latex_templates/report/{type}/{example_name}', list(settings_templates[type].values()),
             f'{result_dir}/{file_name}')
    build(result_dir, f'{result_dir}/{file_name}')
    writing_tool(f'{result_dir}/result.tex', begin_doc + '\n')

    title_count = 0
    section_count = 0
    subsection_count = 0
    pictures_count = 0
    counter = 0
    for info in information_list:
        students = ''
        if info[0] == 'title':
            counter = title_count
            title_count += 1
            for inf_l in information_list:
                if inf_l[0] == 'student':
                    students += new_student.format(group=inf_l[2], name=inf_l[1])
            info.append(students)
            if type == 'template_1':
                lu = info[11]
                lu = lu[:-3]
                info.append(lu)
        if info[0] == 'section':
            counter = section_count
            section_count += 1
        if info[0] == 'subsection':
            counter = subsection_count
            subsection_count += 1
        if info[0] == 'picture':
            counter = pictures_count
            pictures_count += 1
            info.append(f'latex_templates/report/images/picture_{counter}')
        if info[0] == 'student':
            continue
        template_file, new_file = generation_filename(result_dir, type, info[0], counter)
        add_info(template_file, info, new_file)
        build(result_dir, f'{result_dir}/{info[0]}_{counter}')
        if info[0] == 'title':
            writing_tool(f'{result_dir}/result.tex', template_1_newrules + '\n')
            writing_tool(f'{result_dir}/result.tex', table_of_contents + '\n' + r'\newpage' + '\n')

    writing_tool(f'{result_dir}/result.tex', end_doc + '\n')
    pdf_generatoin(result_dir)


def generation_filename(directory, type, name, counter):
    example_name = f'latex_templates/report/{type}/{name}.tex'
    new_filename = f'{directory}/{name}_{counter}.tex'
    return example_name, new_filename


def reading_tool(file_name):
    with open(file_name, 'r') as file:
        return file.read()


def writing_tool(file_name, information):
    with open(file_name, 'a') as file:
        file.write(information)


def build(result_dir, import_file):
    result_file = f'{result_dir}/result.tex'
    information = f'\input {import_file}\n'
    writing_tool(result_file, information)


def add_info(input_file, parameters, output_file):
    args = []
    parser = argparse.ArgumentParser()
    for i in range(len(parameters)):
        parser.add_argument(f'-input_{i}')
        args += [f'-input_{i}', parameters[i]]
    information = reading_tool(input_file)
    information = information % parser.parse_args(args).__dict__
    writing_tool(output_file, information)


def pdf_generatoin(result_dir):
    cmd = ['pdflatex', '-interaction', 'nonstopmode', '-output-directory', f'{result_dir}', f'{result_dir}/result.tex']
    proc = subprocess.Popen(cmd)
    proc.communicate()

    retcode = proc.returncode
    if not retcode == 0:
        os.unlink(f'{result_dir}/result.pdf')
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

    for file in os.listdir(f'{result_dir}'):
        if file != 'result.pdf' and file != 'images':
            os.unlink(f'{result_dir}/{file}')
