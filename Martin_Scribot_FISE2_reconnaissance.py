from image import Image

def lecture_modeles(chemin_dossier):
    fichiers= ['_0.png','_1.png','_2.png','_3.png','_4.png','_5.png','_6.png', 
            '_7.png','_8.png','_9.png']
    liste_modeles = []
    for fichier in fichiers:
        model = Image()
        model.load(chemin_dossier + fichier)
        liste_modeles.append(model)
    return liste_modeles


def reconnaissance_chiffre(image, liste_modeles, S):
    
    n=0
    m=0
    rx1=image.binarisation(S)

    rx2=rx1.localisation()
    
    for i in range(len(liste_modeles)):
        
        image_resized = rx2.resize(liste_modeles[i].H, liste_modeles[i].W)
        
        if image_resized.similitude(liste_modeles[i])>m:
            n=i
            m=image_resized.similitude(liste_modeles[i])
    return n