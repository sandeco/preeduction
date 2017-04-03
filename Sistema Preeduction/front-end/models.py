import csv
import os

from flask import json
from flask_login import UserMixin
import pandas as pd

from manager import db, login_manager

@login_manager.user_loader
def get_user(ident):
  return Usuario.query.get(ident)


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id_user = db.Column(db.Integer, primary_key=True, nullable=False)
    login = db.Column(db.String(64), index=True, nullable=False,
                         unique=True)
    nome = db.Column(db.String(64), index=True, nullable=False,
                         unique=True)
    senha = db.Column(db.String(128), nullable=False)

    def __init__(self, login,nome, senha):
        self.login = login
        self.senha = senha
        self.nome = nome

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id_user

    def __repr__(self):
        return '<User %r>' % (self.nome)


class Aluno(db.Model):
    __tablename__ = 'aluno'
    MATRICULA = db.Column(db.String(64), index=True, nullable=False, unique=True, primary_key=True)
    SIT_MATRICULA = db.Column(db.Integer, nullable=False)
    RENDA_FAMILIAR = db.Column(db.Float,nullable=False)
    RENDA_PER_CAPITA = db.Column(db.Float, nullable=False)
    ANO_CONCLUSAO_2_GRAU = db.Column(db.Integer,nullable=False)
    ANO_INGRESSO = db.Column(db.Integer, nullable=False)
    TIPO_ESCOLA_ORIGEM = db.Column(db.Integer, nullable=False)
    COD_ESTADO_CIVIL = db.Column(db.Integer, nullable=False)
    N_FILHOS = db.Column(db.Integer, nullable=False)
    SEXO = db.Column(db.Integer, nullable=False)
    PROFISSAO = db.Column(db.Integer, nullable=False)
    DESC_CIDADE = db.Column(db.Integer, nullable=False)
    DT_NASCIMENTO = db.Column(db.String(64), nullable=False)
    NIVEL_FALA_INGLES = db.Column(db.Integer, nullable=False)
    NIVEL_COMPREENSAO_INGLES = db.Column(db.Integer, nullable=False)
    NIVEL_ESCRITA_INGLES = db.Column(db.Integer, nullable=False)
    NIVEL_LEITURA_INGLES = db.Column(db.Integer, nullable=False)
    CURSO = db.Column(db.String(64), nullable=False)
    IDADE_INGRESSO = db.Column(db.Integer, nullable=False)



    def __init__(self, matricula,sit_matricula,renda_familiar,tipo_escola,ano_conclusao_2_grau,ano_ingresso,renda_per_capita,
                 estado_civil,numero_filhos,sexo,profissao,cidade,dt_nascimento,nivel_fala,nivel_compreensao,
                 nivel_escrita,nivel_leitura,curso,idade_ingresso):
        self.MATRICULA = matricula
        self.SIT_MATRICULA = sit_matricula
        self.RENDA_FAMILIAR = renda_familiar
        self.TIPO_ESCOLA_ORIGEM = tipo_escola
        self.ANO_CONCLUSAO_2_GRAU = ano_conclusao_2_grau
        self.ANO_INGRESSO = ano_ingresso
        self.RENDA_PER_CAPITA = renda_per_capita
        self.COD_ESTADO_CIVIL = estado_civil
        self.N_FILHOS = numero_filhos
        self.SEXO = sexo
        self.PROFISSAO = profissao
        self.DESC_CIDADE = cidade
        self.DT_NASCIMENTO = dt_nascimento
        self.NIVEL_FALA_INGLES = nivel_fala
        self.NIVEL_COMPREENSAO_INGLES = nivel_compreensao
        self.NIVEL_ESCRITA_INGLES = nivel_escrita
        self.NIVEL_LEITURA_INGLES = nivel_leitura
        self.CURSO = curso
        self.IDADE_INGRESSO = idade_ingresso



    def saveAluno(aluno):
        db.session.add(aluno)
        db.session.commit()

    def removeAluno(aluno):
        db.session.delete(aluno)
        db.session.commit()

    def listAlunos(self):
        return self.query.all()

    def saveAlunoCSV(self):

        if (self.CURSO == 'si'):
            writer = csv.writer(open("../back-end/dados/si_clean_com_matricula.csv", 'a'))
            writer.writerow(self.toCSV())

        else:
            writer = csv.writer(open("../back-end/dados/eca_clean_com_matricula.csv", 'a'))
            writer.writerow(self.toCSV())

    def editAlunoCSV(self):

        if self.CURSO == 'si':
            dados = pd.read_csv('../back-end/dados/si_clean_com_matricula.csv')
            dados.loc[dados['MATRICULA'] == int(self.MATRICULA), dados.columns.values] = self.toCSV()
            dados.to_csv('../back-end/dados/si_clean_com_matricula.csv', index=False)
        elif self.CURSO == 'eca':
            dados = pd.read_csv('../back-end/dados/eca_clean_com_matricula.csv')
            dados.loc[dados['MATRICULA'] == int(self.MATRICULA), dados.columns.values] = self.toCSV()
            dados.to_csv('../back-end/dados/eca_clean_com_matricula.csv', index=False)


    def removeAlunoCSV(self):

        if self.CURSO == 'si':
            print('aq')
            dados = pd.read_csv('../back-end/dados/si_clean_com_matricula.csv')
            new = dados[dados['MATRICULA'] != int(self.MATRICULA)]
            new.to_csv('../back-end/dados/si_clean_com_matricula.csv', index=False)

        elif self.CURSO == 'eca':
            dados = pd.read_csv('../back-end/dados/eca_clean_com_matricula.csv')
            new = dados[dados['MATRICULA'] != int(self.MATRICULA)]
            new.to_csv('../back-end/dados/eca_clean_com_matricula.csv', index=False)

    def __repr__(self):
        return self


    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'matricula': self.MATRICULA,
            'sit_matricula': self.SIT_MATRICULA ,
            'renda_familiar': self.RENDA_FAMILIAR,
            'renda_per_capita': self.RENDA_PER_CAPITA ,
            'ano_2_grau': self.ANO_CONCLUSAO_2_GRAU ,
            'ano_ingresso': self.ANO_INGRESSO,
            'tipo_escola': self.TIPO_ESCOLA_ORIGEM ,
            'estado_civil': self.COD_ESTADO_CIVIL ,
            'n_filhos': self.N_FILHOS ,
            'sexo': self. SEXO ,
            'profissao': self.PROFISSAO ,
            'cidade': self.DESC_CIDADE ,
            'nascimento': self.DT_NASCIMENTO ,
            'fala': self.NIVEL_FALA_INGLES,
            'compreensao': self.NIVEL_COMPREENSAO_INGLES ,
            'escrita': self.NIVEL_ESCRITA_INGLES ,
            'leitura': self.NIVEL_LEITURA_INGLES ,
            'curso': self.CURSO

        }

    def toCSV(self):
        """Return object data in easily serializeable format"""
        return [self.MATRICULA,self.SIT_MATRICULA ,float(self.RENDA_FAMILIAR),float(self.TIPO_ESCOLA_ORIGEM) ,
            self.ANO_CONCLUSAO_2_GRAU ,float(self.RENDA_PER_CAPITA), float(self.COD_ESTADO_CIVIL) ,
            float(self.N_FILHOS ),float(self. SEXO) ,float(self.PROFISSAO) ,float(self.DESC_CIDADE) ,float(self.NIVEL_FALA_INGLES),
            float(self.NIVEL_COMPREENSAO_INGLES) ,float(self.NIVEL_ESCRITA_INGLES) ,float(self.NIVEL_LEITURA_INGLES) ,
            '0.0','0.0','0',self.ANO_INGRESSO,'',self.IDADE_INGRESSO]


