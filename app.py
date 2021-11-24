from flask import Flask,render_template,request,url_for,redirect, session,flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-UU8JNB2/DB_Ptolomeu?driver=SQL+Server+Native+Client+11.0&trusted_connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key ='vrraaau'

db = SQLAlchemy(app)


class INFO(db.Model):
    __tablename__ = "Tabela_site"
    UF = db.Column(db.String(50),primary_key = True)
    Capital = db.Column(db.String(50))
    PIB_medio = db.Column(db.String(50))
    PIB_percapita = db.Column(db.String(50))
    def __str__(self):
        return self.name


class INFO2(db.Model):
    __tablename__= "Tabela_site2"
    UF2 = db.Column(db.String(50),primary_key = True)
    Capital2 = db.Column(db.String(50))
    PIB_medio2 = db.Column(db.String(50))
    PIB_percapita2 = db.Column(db.String(50))
    def __str__(self):
        return self.name  





class Usuario:  
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
usuario1 = Usuario('Ptolomeu', 'Grande Ptolomeu', 'macacomatador')
usuarios = {usuario1.id: usuario1,}
    



@app.route('/')
def index():
    infos= db.session.query(INFO.UF,INFO.Capital,INFO.PIB_medio,INFO.PIB_percapita).order_by(INFO.PIB_percapita.desc())
    infos2= db.session.query(INFO2.UF2,INFO2.Capital2,INFO2.PIB_medio2,INFO2.PIB_percapita2).order_by(INFO2.PIB_medio2.asc())    
    return render_template('lista.html',info=infos,titulo='Estados com maiores PIBs',infos2=infos2)

@app.route('/login')
def login():
    proxima = request.args.get('proxima') 
    return render_template('login.html', proxima=proxima)



@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


if __name__ =='__main__':
    db.create_all()
    app.run(debug=True)
