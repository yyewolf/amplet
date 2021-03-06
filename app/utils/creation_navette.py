import threading
from time import sleep
from models import *
from utils.vote_marchand import vote
from utils.update_multiplicateur import update_multiplicateur
from utils.timestamp import until
from models.amplet import Amplets
from db import *

def ferme_navette(id):
    amp = Amplets.query.get(id)
    if not amp:
        return
    liste_marchand, dic_marchand = vote(id)
    for key in dic_marchand.keys():
        marchand = marchands_amp.Marchands_amp.query.filter_by(id_amp=id,id_marchand=key).first()
        print(key)
        marchand.votes = dic_marchand[key]
    update_multiplicateur(liste_marchand, dic_marchand)
    amp.ferme = True
    db.session.commit()

def attend_vote_automatique(id):
    amp = Amplets.query.get(id)
    sleep(until(amp.date_arrivee-amp.delai_fermeture_depart))
    ferme_navette(id)


def lance_vote_automatique(id):
    x = threading.Thread(target=attend_vote_automatique, args=(id,))
    x.start()