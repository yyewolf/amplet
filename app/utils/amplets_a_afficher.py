from db import *
from models import *
from utils.timestamp import now, timestamp_to_date
from utils.recherche_par import distance
from utils.cast import conversion


def amplet_dict(amp_id) :

    amp = amplet.Amplets.query.get(amp_id)
    
    ampl = {'id' : amp.id}

    cours = users.User.query.add_entity(amplet.Amplets).join(amplet.Amplets).filter(amplet.Amplets.id == amp.id,amplet.Amplets.id_coursier==users.User.id).first()
    if cours is None :
        coursier = "NULL"
        id_cours = "Navette"
    else :
        coursier = cours[0].username
        id_cours = cours[0].id
        id_ad =  cours[0].id_adresse

        cp = adresses.Adresse.query.get(id_ad).codepostal

    ampl['coursier'] = coursier
    ampl['id_cours'] = id_cours
    ampl['dist_max'] = amp.dist_max

    participants = users.User.query.add_entity(participants_amp.Participants_amp).join(participants_amp.Participants_amp).filter(participants_amp.Participants_amp.id_amp == amp.id,participants_amp.Participants_amp.id_user==users.User.id,participants_amp.Participants_amp.valide==1)
    liste_p = []
    for p in participants :
        liste_p.append(p[0].username)
    ampl['participants'] = liste_p

    if amp.navette :
        navette = amp.id_coursier
        cp = amp.id_coursier
    else :
        navette = 'NULL'
        if cours is None :
            cp = 0
    ampl['navette'] = navette
    ampl['cp'] = int(cp)

    places = amp.places_dispo - len(liste_p)
    ampl['places'] = places

    magas = marchands.Marchands.query.add_entity(marchands_amp.Marchands_amp).join(marchands_amp.Marchands_amp).filter(marchands_amp.Marchands_amp.id_amp == amp.id,marchands_amp.Marchands_amp.id_marchand==marchands.Marchands.id)
    liste_m = []
    l_type = []
    l_type_m = []
    for m in magas :
        #print(m)
        liste_m.append(m[0].nom)
        if m[0].type not in l_type :
            l_type.append(m[0].type)
        l_type_m.append([m[0].nom,m[0].type])
    ampl['l_magasins'] = liste_m
    ampl['l_type'] = l_type
    ampl['l_type_m'] = l_type_m
    


    d = timestamp_to_date(amp.date_depart,True)
    ampl['debut'] = d
    ampl['date'] = amp.date_depart

    return ampl

def amplets_a_afficher(debut_stamp,fin_stamp,liste_typebis,current_user) :

    amps = amplet.Amplets.query.all()
    liste_amplet = []
    for amp in amps :
        
        ampl = amplet_dict(amp.id)

        ardesse_user = adresses.Adresse.query.get(current_user.id_adresse)
        
        id_adcours = users.User.query.get(ampl['id_cours']).id_adresse
        adresse_cours = adresses.Adresse.query.get(id_adcours)

        dist = distance(ardesse_user,adresse_cours)
        max_dist = conversion(ampl['dist_max'],int,40100)


        places = ampl['places']
        l_type = ampl['l_type']

        valide = True
        if amp.ferme or amp.date_depart < debut_stamp or amp.date_depart > fin_stamp or places <= 0 or amp.navette or dist > max_dist or amp.id_coursier == current_user.id:
            valide = False
            #print("date")
        for mag_typ in liste_typebis : 
            if mag_typ[1] :
                if mag_typ[0] not in l_type :
                    valide = False
                    #print("type")
        #if valide :
            #print(ampl)
        

        
        if valide :
            liste_amplet.append(ampl)
    return liste_amplet







