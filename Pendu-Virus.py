import tkinter as tk
from tkinter.ttk import Progressbar
import random

# === CONFIGURATION ===
mots = ["chien", "chat", "souris", "poisson", "montagne"]
CODE_SECRET = "libération"
mot_actuel = ""
mot_affiché = []
erreurs = []
score = 0
bombe_temps = 5000

# === FONCTIONS PRINCIPALES ===

def animation_bug_démarrage():
    fen = tk.Toplevel(root)
    fen.title("Chargement corrompu...")
    fen.geometry("400x300")
    fen.configure(bg="black")

    texte = tk.Label(fen, text="LOADING...", font=("Courier", 22), fg="lime", bg="black")
    texte.pack(expand=True)

    def bug_anim(état=[0]):
        glitched = ["LO@D1NG...", "LOA&ING...", "L0AD1NG...", "LOADING...", "😵🧨💾", "█▓▒░▒▓▒░▒▓▒░▒", "CRASH?"]
        texte.config(text=random.choice(glitched), fg=random.choice(["red", "cyan", "lime", "white"]))
        état[0] += 1
        if état[0] < 30:
            fen.after(100, lambda: bug_anim(état))
        else:
            fen.destroy()

    bug_anim()

def random_word():
    global mot_actuel, mot_affiché, erreurs, score, bombe_temps
    mot_actuel = random.choice(mots)
    mot_affiché = ["_" for _ in mot_actuel]
    erreurs = []
    score = 0
    bombe_temps = 5000
    label_result.config(text=" ".join(mot_affiché), fg="black", bg="white")
    label_erreurs.config(text="Erreurs : ")
    champ.config(state="normal")
    progression.config(value=0)

def envoyer_lettre():
    global score
    lettre = champ.get().lower()
    champ.delete(0, tk.END)

    if not lettre.isalpha() or len(lettre) != 1:
        return

    if lettre in mot_actuel and lettre not in mot_affiché:
        for i, char in enumerate(mot_actuel):
            if char == lettre:
                mot_affiché[i] = lettre
        label_result.config(text=" ".join(mot_affiché))
        if "_" not in mot_affiché:
            label_result.config(text=f"GAGNÉ ! Le mot était : {mot_actuel}", fg="green")
            champ.config(state="disabled")
    else:
        if lettre and lettre not in erreurs:
            erreurs.append(lettre)
            score += 1
            progression.config(value=score)
            label_erreurs.config(text=f"Erreurs : {', '.join(erreurs)} | Score : {score}")
            ouvrir_bombe()
        if score >= 11:
            label_result.config(text=f"💀 PERDU ! Le mot était : {mot_actuel}", fg="red")
            champ.config(state="disabled")
            bouton_envoyer.config(state="disabled")
            bouton_rejouer.config(state="disabled")
            button_mot.config(state="disabled")
            bombes_finales()

# === BOMBES & EFFETS ===
def ouvrir_bombe(n=1):
    for _ in range(n):
        fen = tk.Toplevel(root)
        fen.title("💣 BOMBE")
        fen.geometry("280x220")
        fen.protocol("WM_DELETE_WINDOW", lambda f=fen: duplication_fenetre(f))
        bombe_art = """
     _.-^^---....,,--
 _--                  --_
<        💣💥💣         >
 \\._                _./
    ```--. . , ; .--'''
          | |   |
       .-=||  | |=-.
       `-=#$%&%$#=-'
          | ;  :|
 _____.,-#%&$@%#&#~,._____
        """
        label = tk.Label(fen, text=bombe_art, font=("Courier", 10), justify="center", fg="white", bg="black")
        label.pack(expand=True)
        clignoter_bombe(fen, label)

def clignoter_bombe(fen, label, état=[True]):
    couleur = "red" if état[0] else "black"
    fen.configure(bg=couleur)
    label.configure(bg=couleur, fg="white" if état[0] else "red")
    état[0] = not état[0]
    fen.after(300, lambda: clignoter_bombe(fen, label, état))

def duplication_fenetre(fen):
    fen.destroy()
    ouvrir_bombe(5)
    
def écran_bleu_de_la_mort():
    fen = tk.Toplevel(root)
    fen.title("CRITICAL ERROR")
    fen.attributes("-fullscreen", True)
    fen.configure(bg="#0000AA")

    texte_bleu = (
        "💻 Un problème a été détecté et Windows a été arrêté pour éviter d'endommager votre ordinateur.\n\n"
        "IRQL_NOT_LESS_OR_EQUAL\n\n"
        "Si vous voyez cet écran pour la première fois, redémarrez votre ordinateur.\n"
        "Si cet écran apparaît encore, suivez les étapes suivantes :\n\n"
        "Assurez-vous que tous les nouveaux matériels ou logiciels sont correctement installés.\n"
        "Si vous avez besoin de désactiver des composants, redémarrez en mode sans échec.\n\n"
        "STOP: 0x0000000A (0x00000000, 0x00000002, 0x00000001, 0x804D9B61)"
    )

    label = tk.Label(fen, text=texte_bleu, fg="white", bg="#0000AA", font=("Courier", 12), justify="left")
    label.pack(padx=40, pady=40, anchor="nw")

    # Le bouton secret fonctionne même ici
    bouton_secret_bleu = tk.Button(fen, text="", command=lambda: root.destroy(), bg="#0000AA", bd=0)
    bouton_secret_bleu.place(relx=0.98, rely=0.98, width=2, height=2)

def bombes_finales():
    def série(i=0):
        if i >= 5:
            return
        ouvrir_bombe()
        root.after(bombe_temps, lambda: série(i + 5))
        root.after(bombe_temps * 6, écran_bleu_de_la_mort)
    série()

# === CODE SECRET & ARRÊT DU JEU ===
def bouton_invisible():
    bouton = tk.Button(root, text="", command=ouvrir_code_secret, bg="white", bd=0)
    bouton.place(relx=0.9, rely=0.95, width=5, height=5)

def ouvrir_code_secret():
    fen = tk.Toplevel(root)
    fen.title("Code secret")
    fen.geometry("300x100")
    tk.Label(fen, text="Entrez le code pour désactiver :", font=("Arial", 12)).pack()
    champ_code = tk.Entry(fen)
    champ_code.pack()

    def valider():
        global bombe_temps
        if champ_code.get() == CODE_SECRET:
            root.destroy()
        else:
            ouvrir_bombe(10)
            bombe_temps = max(1000, bombe_temps - 1000)
        fen.destroy()

    tk.Button(fen, text="Valider", command=valider).pack()

# === REJOUER ===
def rejouer():
    random_word()
    champ.config(state="normal")
    bouton_envoyer.config(state="normal")
    bouton_rejouer.config(state="normal")
    button_mot.config(state="normal")
    label_result.config(bg="white", fg="black")
    bouton_invisible()

# === INTERFACE PRINCIPALE ===

root = tk.Tk()
root.title("PENDU VIRUS 💀")
root.geometry("400x300")
animation_bug_démarrage()
root.protocol("WM_DELETE_WINDOW", lambda: ouvrir_bombe(5))  # Fermer = BOUM

champ = tk.Entry(root, width=5, font=("Arial", 14))
champ.pack(pady=10)

bouton_envoyer = tk.Button(root, text="Envoyer", command=envoyer_lettre)
bouton_envoyer.pack()

button_mot = tk.Button(root, text="Nouveau mot", command=random_word)
button_mot.pack(pady=10)

label_result = tk.Label(root, text="", font=("Arial", 18))
label_result.pack(pady=10)

label_erreurs = tk.Label(root, text="Erreurs : ", font=("Arial", 12))
label_erreurs.pack()

progression = Progressbar(root, orient='horizontal', length=200, mode='determinate', maximum=11)
progression.pack(pady=5)

bouton_rejouer = tk.Button(root, text="Rejouer", command=rejouer)
bouton_rejouer.pack(pady=5)

random_word()
bouton_invisible()
root.mainloop()


