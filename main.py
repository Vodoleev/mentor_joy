from app import app
from flask import Blueprint, render_template, redirect, url_for, request, session, current_app, send_from_directory, \
    flash
from forms import *
import os
import random
import string
import datetime
from generator import make_pdf

main = Blueprint('main', __name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)


def handling_button():
    for i in range(len(session['form'])):
        if request.form.get(f'delete_{i}'):
            if session['form'][i][0] == 'title':
                last_section = i + 1
                while last_section < len(session['form']) and session['form'][last_section][0] == 'student':
                    last_section += 1
                for del_section in range(last_section - 1, i, -1):
                    session['form'].pop(del_section)
            elif session['form'][i][0] == 'section':
                last_section = i + 1
                while last_section < len(session['form']) and session['form'][last_section][0] == 'subsection':
                    last_section += 1
                for del_section in range(last_section - 1, i, -1):
                    session['form'].pop(del_section)
            session['form'].pop(i)
        if request.form.get(f'add_subsection_below_{i}'):
            print("Section below")
            session['form'].insert(i + 1, ['subsection', '', ''])
        if request.form.get(f'add_subsection_{i}'):
            last_section = i + 1
            while last_section < len(session['form']) and session['form'][last_section][0] == 'subsection':
                last_section += 1
            session['form'].insert(last_section, ['subsection', '', ''])
        if request.form.get(f'add_student_{i}'):
            session['form'].insert(i + 1, ['student', '', ''])
        if request.form.get(f'upload_picture_{i}'):
            file = request.files[f'file_{i}']
            if file:
                update_dir()
                add_images_dir()
                file.save(os.path.join(current_app.root_path,
                                       f'results/{str(session["dir"])}/images/{file.filename}'))
                session['form'][i][2] = f'results/{str(session["dir"])}/images/{file.filename}'


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def update_dir():
    if 'dir' not in session:
        session['dir'] = generate_random_string(15)
    if not os.path.isdir(os.path.join(current_app.root_path, f'results/{str(session["dir"])}')):
        os.mkdir(os.path.join(current_app.root_path, f'results/{str(session["dir"])}'))


def add_images_dir():
    print(os.path.join(current_app.root_path, f'results/{str(session["dir"])}/images'))
    if not os.path.isdir(os.path.join(current_app.root_path, f'results/{str(session["dir"])}/images')):
        os.mkdir(os.path.join(current_app.root_path, f'results/{str(session["dir"])}/images'))


@main.route('/create_report/template_<int:template_num>', methods=['POST', 'GET'])
def create_report(template_num):
    session['template_type'] = template_num
    session.modified = True
    # print(session['form'])
    # session.pop('form')
    if 'form' not in session:
        session['form'] = []
    initial_form = InitialForm()
    if initial_form.validate_on_submit():
        read_form()
        handling_button()
        if initial_form.new_template.data:
            session.pop('form')
            session.pop('template_type')
            return redirect(url_for('main.templates'))
        if initial_form.end.data:
            flag, forms = validate_forms(template_num)
            if flag:
                update_dir()
                print('-' * 100)
                print(session['form'])
                print('-' * 100)
                make_pdf(f'template_{template_num}', session['form'], os.path.join(current_app.root_path, f'results/{str(session["dir"])}'))
                return redirect(url_for('main.download', filename='result.pdf'))
            else:
                return render_template('index.html', initial_form=initial_form, test_forms=forms,
                                       list_size=len(forms))
        if initial_form.clear_all.data:
            session['form'] = []
        if initial_form.add_title.data:
            if template_num == 0:
                add_form('title', count=9)
            if template_num == 1:
                add_form('title', count=15)
        if initial_form.add_section.data:
            add_form('section', count=2)
        if initial_form.add_picture.data:
            add_form('picture', count=2)

    print(session['form'], get_forms(template_num, session['form']))
    return render_template('index.html', initial_form=initial_form, test_forms=get_forms(template_num, session['form']),
                           list_size=len(get_forms(template_num, session['form'])))


@main.route('/manual', methods=['POST', 'GET'])
@main.route('/', methods=['POST', 'GET'])
def manual():
    return render_template('manual.html')


class Template:
    def __init__(self, name, content):
        self.name = name
        self.content = os.path.join(app.config['UPLOAD_FOLDER'], content)


@main.route('/templates', methods=['POST', 'GET'])
def templates():
    if 'template_type' in session:
        return redirect(f'/create_report/template_{session["template_type"]}')
    session['form'] = []
    templates_list = [Template('Первый шаблон', 'template_0.png'),
                      Template('Второй шаблон', 'template_1.png')]
    return render_template('templates.html', templates_list=templates_list, list_size=len(templates_list))


@main.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, f'results/{str(session["dir"])}')
    return send_from_directory(directory=uploads, path=filename, as_attachment=True)
