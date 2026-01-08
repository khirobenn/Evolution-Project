import random
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pygame

DEBUT_LECTURE = "ATG"
STOPS = ["TAA", "TAG", "TGA"]

ADN = "ATGTTAGAAATTTCATGGTGCCTTA"
CONST_POPULATION = 100

PROB_M=5
PROB_D=2
PROB_A=2

acide_amine = {
    "TTT" : "Phe",
    "TTC" : "Phe",

    "TTA" : "Leu",
    "TTG" : "Leu",
    "CTT" : "Leu",
    "CTC" : "Leu",
    "CTA" : "Leu",
    "CTG" : "Leu",

    "ATT" : "Ile",
    "ATC" : "Ile",
    "ATA" : "Ile",

    "ATG" : "Met",

    "GTT" : "Val",
    "GTC" : "Val",
    "GTA" : "Val",
    "GTG" : "Val",

    "TCT" : "Ser",
    "TCC" : "Ser",
    "TCA" : "Ser",
    "TCG" : "Ser",

    "CCT" : "Pro",
    "CCC" : "Pro",
    "CCG" : "Pro",
    "CCA" : "Pro",

    "ACT" : "Thr",
    "ACA" : "Thr",
    "ACG" : "Thr",
    "ACC" : "Thr",

    "GCT" : "Ala",
    "GCA" : "Ala",
    "GCC" : "Ala",
    "GCG" : "Ala",

    "TAT" : "Tyr",
    "TAC" : "Tyr",

    "CAT" : "His",
    "CAC" : "His",

    "CAA" : "Gln",
    "CAG" : "Gln",

    "AAT" : "Asn",
    "AAC" : "Asn",

    "AAA" : "Lys",
    "AAG" : "Lys",

    "GAT" : "Asp",
    "GAC" : "Asp",

    "GAA" : "Glu",
    "GAG" : "Glu",

    "TGT" : "Cys",
    "TGC" : "Cys",

    "TGG" : "Trp",

    "CGT" : "Arg",
    "CGA" : "Arg",
    "CGC" : "Arg",
    "CGG" : "Arg",
    "AGA" : "Arg",
    "AGG" : "Arg",

    "AGT" : "Ser",
    "AGC" : "Ser",

    "GGT" : "Gly",
    "GGC" : "Gly",
    "GGA" : "Gly",
    "GGG" : "Gly"

}

# Trouver le début de la séquence
def find_start(arn):
    if arn[0:3] == DEBUT_LECTURE:
        return arn[3:]
    return find_start(arn[1:])

# Supprimer les lettres à la fin de l'ARN qui ne servent pas au calcul
def delete_end(arn):
    if arn == "":
        return ""
    if arn[0:3] in STOPS:
        return ""
    return arn[0:3] + delete_end(arn[3:])

# ça retourne juste la séquence codante
def get_coding_sequence(arn):
    arn = find_start(arn)
    return delete_end(arn)


# Lire la séquence après avoir enlevé les éléments qu'on lit pas
def read_sequence(arn):
    if len(arn) <= 2 or arn[0:3] in STOPS:
        return ""
    return (acide_amine[arn[0:3]] + "-" + read_sequence(arn[3:]))

def compare_two_sequences(arn1, arn2):
    element1 = read_sequence(arn1)
    element2 = read_sequence(arn2)

    element1 = element1.split("-")
    element2 = element2.split("-")

    min_length = min(len(element1), len(element2))
    equal = 0

    for i in range(0, min_length):
        if element1[i] == element2[i]:
            equal = equal + 1

    return equal

# On lit notre ARN
def read_arn(arn):
    return read_sequence(find_start(arn))

def generate_letter():
    return random.choice(["A", "T", "G", "C"])

def generate_sequence(length=-1):
    if length == -1:
        length = random.choice(range(50, 80))
    s = ""
    for i in range(0, length):
        s = s+generate_letter()
    return s


def changement(arn, PROB_M=5, PROB_D=5, PROB_A=5):

    p = random.choice(range(0, 100))
    if p < PROB_M:
        arn = generate_letter()

    p = random.choice(range(0, 100))
    if p < PROB_A:
        arn = arn + generate_letter()

    p = random.choice(range(0,100))
    if p < PROB_D:
        arn = arn[1:]

    return arn

def sequence_changement(arn, PROB_M=5, PROB_D=5, PROB_A=5):
    if arn == '':
        return ''
    return changement(arn[0:1]) + sequence_changement(arn[1:], PROB_M, PROB_D, PROB_A)

def meilleur_personne(WIDTH, HEIGHT, RADIUS, screen=None, PROB_M=5, PROB_D=5, PROB_A=5):
    result =  []
    generated_adn = generate_sequence()
    g_adn = generated_adn
    print("ADN généré au départ :", generated_adn)
    find = False
    loop = 0
    adn_seq_length = len(read_sequence(ADN).split("-"))
    print(adn_seq_length)
    while not find:
        if screen != None:
            screen.fill("black")
            pygame.draw.line(screen, "red", [WIDTH, 0], [WIDTH, HEIGHT], 5)
    
        pop_sequences = [""]*CONST_POPULATION
        occurences = [None]*CONST_POPULATION
        for i in range(0, CONST_POPULATION):
            pop_sequences[i] = sequence_changement(generated_adn, PROB_M, PROB_D, PROB_A)
            occurences[i] = compare_two_sequences(ADN, pop_sequences[i])

            if screen != None:
                pos = pygame.Vector2(occurences[i]/adn_seq_length * WIDTH, i/CONST_POPULATION * HEIGHT)
                pygame.draw.circle(screen, "blue", pos, RADIUS)
                pygame.display.flip()
        
        max_index = occurences.index(max(occurences))
        result.append(pop_sequences[max_index])
        generated_adn = pop_sequences[max_index]

        if read_sequence(ADN) == read_sequence(generated_adn):
            if screen != None:
                l = occurences[max_index]
                pos = pygame.Vector2(l/adn_seq_length * WIDTH, max_index/CONST_POPULATION * HEIGHT)
                pygame.draw.circle(screen, "green", pos, RADIUS)
                pygame.display.flip()

            find = True
        loop = loop + 1

    return g_adn, result, loop


def moran_v1(WIDTH, HEIGHT, RADIUS, screen=None):
    alpha=50
    Poids=np.exp(-alpha*np.arange(CONST_POPULATION, 0, -1))
    Probas=Poids/np.sum(Poids)

    adn_seq_length = len(read_sequence(ADN).split("-"))

    result = []
    generated_adn = generate_sequence()
    g_adn = generated_adn
    print("ADN généré au départ :", generated_adn)
    find = False
    loop = 0
    pop_sequences = [""]*CONST_POPULATION
    occurences = [None]*CONST_POPULATION

    while not find:
        if screen != None:
            screen.fill("black")
            pygame.draw.line(screen, "red", [WIDTH, 0], [WIDTH, HEIGHT], 5)

        for i in range(0, CONST_POPULATION):
            if pop_sequences[i] == "":
                pop_sequences[i] = sequence_changement(generated_adn)
            else:
                pop_sequences[i] = sequence_changement(pop_sequences[i])
            occurences[i] = compare_two_sequences(ADN, pop_sequences[i])

            if screen != None:
                pos = pygame.Vector2(occurences[i]/adn_seq_length * WIDTH, i/CONST_POPULATION * HEIGHT)
                pygame.draw.circle(screen, "blue", pos, RADIUS)
                pygame.display.flip()


        population_triee = [val for _, val in sorted(zip(occurences, pop_sequences))]
        result.append(population_triee[-1])

        if read_sequence(population_triee[-1]) == read_sequence(ADN):
            if screen != None:
                l = max(occurences)
                pos = pygame.Vector2(l/adn_seq_length * WIDTH, l/CONST_POPULATION * HEIGHT)
                pygame.draw.circle(screen, "green", pos, RADIUS)
                pygame.display.flip()
                
            find = True
        loop = loop + 1

        pop_sequences = random.choices(population_triee, weights=Probas, k=CONST_POPULATION)


    return g_adn, result, loop


PROBA_MIN = 3
PROBA_MAX = 5
proba_mut = range(PROBA_MIN, PROBA_MAX+1)
proba_del = range(1, 4)
proba_add = range(1, 4)

mutation, deletion, addition = np.meshgrid(proba_mut, proba_del, proba_add)

generations = []

for i in range(len(proba_mut)):
    first_loop = []
    for j in range(len(proba_del)):
        second_loop = []
        for k in range(len(proba_add)):
            print("proba_mut =", mutation[i, j, k], ", proba_delete =", deletion[i, j, k], " proba_add =", addition[i, j, k])
            ADN_depart, result, loop = meilleur_personne(0, 0, 0, screen=None, PROB_M=mutation[i, j, k], PROB_D=deletion[i, j, k], PROB_A=addition[i, j, k])
            print("Nombre de générations :", loop)
            second_loop.append(loop)
        first_loop.append(second_loop)
    generations.append(first_loop)



generations = np.array(generations)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

img = ax.scatter(mutation, deletion, generations, c=addition, cmap=plt.plasma())
fig.colorbar(img)
plt.show()

ADN_depart, result, loop = meilleur_personne(proba_mut = 5, proba_delete = 3, proba_addition = 4)

print(loop)
