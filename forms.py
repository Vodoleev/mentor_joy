from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import StringField, FormField, FieldList, FileField
from wtforms.widgets import TextArea
from flask import session, request, flash, render_template


class LoginForm(FlaskForm):
    email = StringField("Email: ", default="Книгоман", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100,
                                                       message="Пароль должен быть от 4 до 100 символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100,
                                                       message="Пароль должен быть от 4 до 100 символов")])

    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


class InitialForm(FlaskForm):
    add_title = SubmitField("Добавить титульный лист")
    add_section = SubmitField("Добавить секцию")
    add_picture = SubmitField("Добавить фотографию")
    clear_all = SubmitField("Очистить форму")
    save = SubmitField("Сохранить изменения")
    end = SubmitField("Скачать файл")
    new_template = SubmitField("Выбрать новый шаблон")


class TitleForm1(FlaskForm):
    label = 'Титульный лист'
    full_name = StringField("Ф.И.О.", default="")
    university = StringField("Университет", default="")
    faculty = StringField("Факультет", default="")
    ed_program = StringField("Образовательная программа", default="")
    group_number = StringField("Номер группы", default="")
    topic = StringField("Название работы", default="")
    full_professor_name = StringField("Ф.И.О. научного руководителя", default="")
    post = StringField("Должность научного руководителя", default="")
    workplace = StringField("Местро работы научного руководителя", default="")
    add_student = SubmitField("Добавить студента")
    delete = SubmitField("Удалить блок")

    def set_block(self, block_num):
        for field_name in vars(self).get('_fields'):
            if field_name not in ['csrf_token', 'delete', 'add_student']:
                vars(self).get('_fields').get(field_name).name = str(block_num)
        self.delete.name = f'delete_{block_num}'
        self.add_student.name = f'add_student_{block_num}'


class TitleForm2(FlaskForm):
    label = 'Титульный лист'
    university = StringField("Университет", default="")
    faculty = StringField("Факультет", default="")
    ed_program = StringField("Образовательная программа", default="")
    scientific_supervisor_name = StringField("Ф.И.О. научного руководителя", default="")
    scientific_supervisor_post = StringField("Должность научного руководителя", default="")
    scientific_supervisor_data = StringField("Дата согласования с научным руководителем", default="")
    director_name = StringField("Ф.И.О. руководителя ОП", default="")
    director_post = StringField("Должность руководителя ОП", default="")
    director_data = StringField("Дата утверждения", default="")
    title = StringField("Название работы", default="")
    approval_sheet = StringField("Лист утвержения", default="")
    full_name = StringField("Ф.И.О. студента", default="")
    group_number = StringField("Группа студента", default="")
    student_data = StringField("Дата составления документа", default="")
    footer = StringField("Введите город и год", default="")

    add_student = SubmitField("Добавить студента")
    delete = SubmitField("Удалить блок")

    def set_block(self, block_num):
        for field_name in vars(self).get('_fields'):
            if field_name not in ['csrf_token', 'delete', 'add_student']:
                vars(self).get('_fields').get(field_name).name = str(block_num)
        self.delete.name = f'delete_{block_num}'
        self.add_student.name = f'add_student_{block_num}'


class StudentForm(FlaskForm):
    label = 'Студент'
    name = StringField("ФИО", default="")
    group = StringField("Группа", default="")
    delete = SubmitField("Удалить блок")

    def set_block(self, block_num):
        for field_name in vars(self).get('_fields'):
            if field_name not in ['csrf_token', 'delete']:
                vars(self).get('_fields').get(field_name).name = str(block_num)
        self.delete.name = f'delete_{block_num}'


class SectionForm(FlaskForm):
    label = 'Секция'
    name = StringField("Название", default="")
    content = StringField("Содержание", default="")
    add_subsection = SubmitField("Добавить субсекцию")
    delete = SubmitField("Удалить блок")

    def set_block(self, block_num):
        for field_name in vars(self).get('_fields'):
            if field_name not in ['csrf_token', 'delete', 'add_subsection']:
                vars(self).get('_fields').get(field_name).name = str(block_num)

        self.add_subsection.name = f'add_subsection_{block_num}'
        self.delete.name = f'delete_{block_num}'


class SubsectionForm(FlaskForm):
    label = 'Субсекция'
    name = StringField("Название", default="")
    content = StringField("Содержание", default="")
    add_subsection_below = SubmitField("Добавить субсекцию ниже")
    delete = SubmitField("Удалить блок")

    def set_block(self, block_num):
        for field_name in vars(self).get('_fields'):
            if field_name not in ['csrf_token', 'delete', 'add_subsection_below']:
                vars(self).get('_fields').get(field_name).name = str(block_num)
        self.add_subsection_below.name = f'add_subsection_below_{block_num}'
        self.delete.name = f'delete_{block_num}'


class PicturesForm(FlaskForm):
    label = 'Изображение'
    uploaded_filename = ''
    name = StringField("Подпись к изображению", default="")
    picture = FileField("Выбрать изображение")
    upload = SubmitField("Загрузить")
    delete = SubmitField("Удалить блок")

    def set_block(self, block_num):
        for field_name in vars(self).get('_fields'):
            if field_name not in ['csrf_token', 'delete', 'upload', 'file']:
                vars(self).get('_fields').get(field_name).name = str(block_num)
        self.picture.name = f'file_{block_num}'
        self.upload.name = f'upload_picture_{block_num}'
        self.delete.name = f'delete_{block_num}'

    def set_uploaded_filename(self, filename):
        self.uploaded_filename = filename.split('/')[-1]


def get_forms(type, forms):
    array = []
    for block_num, form in enumerate(forms):
        if form[0] == 'title':
            if type == 0:
                array.append(TitleForm1(full_name=form[1], university=form[2], faculty=form[3], ed_program=form[4],
                                        group_number=form[5], topic=form[6], full_professor_name=form[7], post=form[8],
                                        workplace=form[9]))
            if type == 1:
                array.append(TitleForm2(university=form[1], faculty=form[2], ed_program=form[3],
                                        scientific_supervisor_name=form[4],
                                        scientific_supervisor_post=form[5], scientific_supervisor_data=form[6],
                                        director_name=form[7], director_post=form[8],
                                        director_data=form[9], title=form[10], approval_sheet=form[11],
                                        full_name=form[12], group_number=form[13], student_data=form[14],
                                        footer=form[15]))

            array[-1].set_block(block_num)
        if form[0] == 'section':
            array.append(SectionForm(name=form[1], content=form[2]))
            array[-1].set_block(block_num)
        if form[0] == 'subsection':
            array.append(SubsectionForm(name=form[1], content=form[2]))
            array[-1].set_block(block_num)
        if form[0] == 'picture':
            array.append(PicturesForm(name=form[1]))
            array[-1].set_block(block_num)
            array[-1].set_uploaded_filename(form[2])
        if form[0] == 'student':
            array.append(StudentForm(name=form[1], group=form[2]))
            array[-1].set_block(block_num)

    return array


def read_form():
    for i in range(len(session['form'])):
        if session['form'][i][0] == 'picture':
            session['form'][i] = [session['form'][i][0]] + request.form.getlist(str(i)) + [session['form'][i][2]]
        else:
            session['form'][i] = [session['form'][i][0]] + request.form.getlist(str(i))
    print(session['form'])


def add_form(name, count):
    session['form'].append([name] + [''] * count)


def set_validator_data_required(form, validators):
    for field_name in validators:
        vars(form).get('_fields').get(field_name).validators = [DataRequired(message='Заполните поле')]
    return form


def validate_forms(template_num):
    forms = get_forms(template_num, session['form'])
    flag = True
    for form in forms:
        if isinstance(form, TitleForm1):
            form = set_validator_data_required(form,
                                               ['full_name', 'university', 'faculty', 'ed_program', 'group_number',
                                                'topic', 'full_professor_name', 'post', 'workplace'])
        if isinstance(form, TitleForm2):
            form = set_validator_data_required(form,
                                               ['university', 'faculty', 'ed_program', 'scientific_supervisor_name',
                                                'scientific_supervisor_post', 'scientific_supervisor_data',
                                                'director_name', 'director_post', 'director_data', 'title',
                                                'approval_sheet', 'full_name', 'group_number', 'student_data',
                                                'footer'])
        if isinstance(form, StudentForm):
            form = set_validator_data_required(form, ['name', 'group'])
        if isinstance(form, SectionForm):
            form = set_validator_data_required(form, ['name', 'content'])
        if isinstance(form, SubsectionForm):
            form = set_validator_data_required(form, ['name', 'content'])
        if isinstance(form, PicturesForm):
            form = set_validator_data_required(form, ['name'])
            if form.uploaded_filename == '':
                flag = False
                form.picture.errors = ['Вставьте изображение']
        flag = flag and form.validate_on_submit()
    return [flag, forms]
