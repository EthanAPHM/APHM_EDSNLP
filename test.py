
import sys #Permet d’accéder aux arguments passés au script
import os
import edsnlp
import time

def pseudonymise_file(path, nlp, suffix="_pseudo.txt"):
    with open(path, "r", encoding="utf-8") as f: #Lecture du doc
        texte = f.read()

    t_start = time.time()  # Début chronométrage pour ce fichier
    doc = nlp(texte) # Applique le modèle

    #Pseudonymise le texte 
    pseudo_texte = texte
    # Changer l'entité par son  [label]
    for ent in reversed(doc.ents):  # On va de la fin au début pour ne pas décaler les index
        pseudo_texte = (pseudo_texte[:ent.start_char] + f"[{ent.label_}]" + pseudo_texte[ent.end_char:])
    # Nouveau nom de fichier
    out_path = (path[:-4] + suffix if path.lower().endswith(".txt") else path + suffix)
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write(pseudo_texte)
    t_end = time.time()  # Fin chronométrage pour ce fichier
    print(f"{out_path} fichier pseudonymisé. Temps de traitement : {t_end - t_start:.2f} secondes.")




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(" python test.py fichier1.txt fichier2.txt //  python test.py dossier/")
        sys.exit(1)

    # Charge le modèle
    nlp = edsnlp.load("AP-HP/eds-pseudo-public", auto_update=True)

    # Si argument = dossier, traite tous les .txt du dossier
    if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        dossier = sys.argv[1]
        fichiers = [os.path.join(dossier, f) for f in os.listdir(dossier) if f.endswith(".txt")]
    else:
        # Sinon, traite tous les fichiers listés
        fichiers = sys.argv[1:]
	
    t_global_start = time.time()  # début chrono global

    for path in fichiers:
        pseudonymise_file(path, nlp)

    t_global_end = time.time()  # fin chrono global
    print(f"Temps total pour {len(fichiers)} fichier(s) : {t_global_end - t_global_start:.2f} secondes.")
