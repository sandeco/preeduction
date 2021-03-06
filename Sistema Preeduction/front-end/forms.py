
from flask_wtf import Form
from werkzeug.datastructures import MultiDict
from wtforms import StringField, BooleanField, RadioField, PasswordField,SelectField,SubmitField,IntegerField
from wtforms.validators import DataRequired,InputRequired,Length

class AlunoForm(Form):
    matricula = StringField('matricula', validators=[InputRequired("Please enter your name.")])
    sit_matricula = SelectField('sit_matricula',
                                choices=[('0', "Matriculado"), ('2', "Trancado"),('3', "Transferido Interno"),
                                ('4', "Concludente"),('5', "Concluído"),('6', "Falecido"),('7', "Afastado"),
                                ('8', "Evasão"),('9', "Cancelado"),('10', "Transferido Externo"),
                                ('11', "Estagiário(concludente)"),('12', "Aguardando Colação"),('13', "Intercâmbio"),
                                ('14', "Certificado Enem"),('15', "Aguardando seminário"),('16', "Egresso"),
                                ('17', "Formado"),('18', "Aguardando ENADE"),('19', "Cancelamento Compulsório"),
                                ('20', "Matricula vinculo institucional"),('21', "Não concluído")],
                                validators=[DataRequired()])

    curso = RadioField('curso', choices=[('si','S.I'),('eca','E.C.A')],validators=[DataRequired()])

    renda_familiar = SelectField('renda_familiar',
                                choices=[('1', "Até 1 salário"), ('2', "1 a 2 salários"),('3', "2 a 3 salários"),
                                ('4', "3 a 5 salários"),('5', "5 a 10 salários"),('6', "10 a 20 salários"),('7', "Mais de 20 salários")],
                                validators=[DataRequired()])

    tipo_escola = SelectField('tipo_escola', choices=[('0', "Conveniada"), ('1', "Estadual"),('2', "Federal"),('3', "Filantrópico"),
                              ('4', "Municipal"),('5', "Outros"),('6', "Privada")],validators=[DataRequired()])
    ano_conclusao_2_grau = StringField('ano_conclusao_2_grau', validators=[DataRequired()])
    ano_ingresso = StringField('ano_ingresso', validators=[DataRequired()])
    renda_per_capita = SelectField('renda_per_capita)',
                                choices=[('0', "Menos de 1 salário"), ('1', "1 salário mínimo"),('2', "2 salários mínimos"),
                                ('3', "3 salários mínimos"),('4', "4 salários mínimos"),('5', "5 a 6 salários mínimos"),
                                ('6', "7 a 10 salários mínimos"), ('7', "11 a 15 salários mínimos"), ('8', "16 a 20 salários mínimos"),
                                ('9', "Mais de 20 salários mínimos"), ('10', "Não informado")],
                                validators=[DataRequired()])
    estado_civil = RadioField('estado_civil', choices=[('0', "Solteiro"), ('1', "Casado"),('2', "Divorciado")],validators=[DataRequired()])
    numero_filhos = StringField('numero_filhos',validators=[DataRequired()])
    sexo = RadioField('sexo', choices=[('1', 'Feminino'), ('0', 'Masculino')],validators=[DataRequired()])
    dt_nascimento = StringField('dt_nascimento',validators=[DataRequired()])
    profissao = RadioField('profissao', choices=[('1', "Sim"), ('0', "Nao")],validators=[DataRequired()])
    cidade = SelectField('cidade',
                                choices=[('0', "Capital"), ('1', "Grande Goiânia"),('2', "Interior de Goiás")],
                                validators=[DataRequired()])
    nivel_fala = StringField('nivel_fala',validators=[DataRequired()])
    nivel_compreensao = StringField('nivel_compreensao',validators=[DataRequired()])
    nivel_escrita = StringField('nivel_escrita',validators=[DataRequired()])
    nivel_leitura = StringField('nivel_leitura',validators=[DataRequired()])
    submit = SubmitField("Salvar")



class LoginForm(Form):
    matricula = StringField('matricula', validators=[DataRequired()])

    senha = PasswordField('senha', validators=[DataRequired()])

class AlunoPesquisa(Form):
    matricula =StringField('matricula', validators=[DataRequired(),Length(min=14,max=14)])
