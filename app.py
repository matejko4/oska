from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tajneheslo123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fotbalisti.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Uzivatel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uzivatelske_jmeno = db.Column(db.String(80), unique=True, nullable=False)
    heslo = db.Column(db.String(200), nullable=False)


class Fotbalista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(100), nullable=False)
    prijmeni = db.Column(db.String(100), nullable=False)
    vek = db.Column(db.Integer)
    pozice = db.Column(db.String(50))
    klub = db.Column(db.String(100))
    cislo_dresu = db.Column(db.Integer)
    narodnost = db.Column(db.String(50))
    uzivatel_id = db.Column(db.Integer, db.ForeignKey('uzivatel.id'), nullable=False)


def prihlaseni_nutne(view_func):
    @wraps(view_func)
    def obalena_funkce(*args, **kwargs):
        if 'uzivatel_id' not in session:
            flash('Přihlaste se, prosím.', 'warning')
            return redirect(url_for('prihlaseni'))
        return view_func(*args, **kwargs)
    return obalena_funkce


@app.route('/')
def index():
    if 'uzivatel_id' in session:
        return redirect(url_for('prehled'))
    return redirect(url_for('prihlaseni'))


@app.route('/registrace', methods=['GET', 'POST'])
def registrace():
    if request.method == 'POST':
        jmeno = request.form.get('uzivatelske_jmeno')
        heslo = request.form.get('heslo')
        potvrzeni = request.form.get('heslo_potvrzeni')

        if not jmeno or not heslo or heslo != potvrzeni:
            flash('Vyplňte všechna pole a ověřte heslo.', 'danger')
            return redirect(url_for('registrace'))

        if Uzivatel.query.filter_by(uzivatelske_jmeno=jmeno).first():
            flash('Uživatelské jméno už existuje.', 'danger')
            return redirect(url_for('registrace'))

        uzivatel = Uzivatel(
            uzivatelske_jmeno=jmeno,
            heslo=generate_password_hash(heslo)
        )
        db.session.add(uzivatel)
        db.session.commit()

        flash('Registrace hotová, přihlaste se.', 'success')
        return redirect(url_for('prihlaseni'))

    return render_template('registrace.html')


@app.route('/prihlaseni', methods=['GET', 'POST'])
def prihlaseni():
    if request.method == 'POST':
        jmeno = request.form.get('uzivatelske_jmeno')
        heslo = request.form.get('heslo')

        uzivatel = Uzivatel.query.filter_by(uzivatelske_jmeno=jmeno).first()
        if uzivatel and check_password_hash(uzivatel.heslo, heslo):
            session['uzivatel_id'] = uzivatel.id
            session['uzivatelske_jmeno'] = uzivatel.uzivatelske_jmeno
            flash('Jste přihlášeni.', 'success')
            return redirect(url_for('prehled'))

        flash('Špatné jméno nebo heslo.', 'danger')

    return render_template('prihlaseni.html')


@app.route('/odhlaseni')
def odhlaseni():
    session.clear()
    flash('Byli jste odhlášeni.', 'info')
    return redirect(url_for('prihlaseni'))


@app.route('/prehled')
@prihlaseni_nutne
def prehled():
    fotbalisti = Fotbalista.query.filter_by(uzivatel_id=session['uzivatel_id']).all()
    return render_template('prehled.html', fotbalisti=fotbalisti)


@app.route('/pridat-fotbalistu', methods=['GET', 'POST'])
@prihlaseni_nutne
def pridat_fotbalistu():
    if request.method == 'POST':
        jmeno = request.form.get('jmeno')
        prijmeni = request.form.get('prijmeni')
        vek = request.form.get('vek')
        cislo_dresu = request.form.get('cislo_dresu')

        if not jmeno or not prijmeni:
            flash('Jméno i příjmení jsou povinná.', 'danger')
            return redirect(url_for('pridat_fotbalistu'))

        fotbalista = Fotbalista(
            jmeno=jmeno,
            prijmeni=prijmeni,
            vek=int(vek) if vek else None,
            pozice=request.form.get('pozice'),
            klub=request.form.get('klub'),
            cislo_dresu=int(cislo_dresu) if cislo_dresu else None,
            narodnost=request.form.get('narodnost'),
            uzivatel_id=session['uzivatel_id']
        )
        db.session.add(fotbalista)
        db.session.commit()

        flash('Fotbalista přidán.', 'success')
        return redirect(url_for('prehled'))

    return render_template('pridat_fotbalistu.html')


@app.route('/smazat-fotbalistu/<int:id>')
@prihlaseni_nutne
def smazat_fotbalistu(id):
    fotbalista = Fotbalista.query.get_or_404(id)
    if fotbalista.uzivatel_id != session['uzivatel_id']:
        flash('Tohoto hráče nemůžete mazat.', 'danger')
        return redirect(url_for('prehled'))

    db.session.delete(fotbalista)
    db.session.commit()
    flash('Fotbalista smazán.', 'info')
    return redirect(url_for('prehled'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
