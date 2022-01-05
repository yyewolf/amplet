from flask_login.utils import login_required
from db import *
from models import *
from flask_login import current_user
from flask import render_template
from routes.commande import commande

@app.route('/f/<string:id_ampl>/')
@login_required
def fermerAmplet(id_ampl):
    amp = amplet.Amplets.query.filter_by(id = id_ampl).first()
    if amp and current_user.id==amp.id_coursier:
        amp.ferme=1
        db.session.commit()
        return commande()
    else:
        return render_template('info.html', user=current_user, msg="Vous n'avez pas l'autorisation de fermer cette Amplet ou elle n'existe pas", retour="/commande")