import re, sys

contenu_corpus = open(sys.argv[1], 'r', encoding='utf-8').readlines()
dic = open('subst.dic', 'r', encoding='utf-16-le').readlines()
dic_enrichi = open("subst_corpus.dic", 'w', encoding='utf-16-le')
dic_enrichi.write('\ufeff \n')
prov = [] ##cette liste contiendra les elements du corpus medical  et du  dossier vidal
print("Medicament  apres enrichissement sont : \n")
for i in contenu_corpus:
    lol= re.search(r"^-? ?(\w+) :? ?(\d+|,)+ (mg|ml).+", i, re.I)
    if lol:
        dic_enrichi.write(str(lol.group(1)) + ",.N+subst \n")
        print(str(lol.group(1).lower()) + ",.N+subst ")

        t = str(lol.group(1)).lower()
        ## match inside the subst dic teh current element
        y = re.search(t, str(dic), re.I)
        if y == None:
            if t != "puis" and not t.startswith("ø") and t != "intraveineuse":
                prov.append(t)

        if t != "puis" and not t.startswith("ø") and t != "intraveineuse":
            dic.append(t + ",.N+subst\n")
dic_enrichi.close()

## on elimine les doubles avec le dic
list_trie = dict.fromkeys(sorted(dic))

## on genere le fichier info3 sans doublant 
first = ord('A')
last = ord('Z')

info3 = open("info3.txt", 'w', encoding='utf-8')
j = 0
for i in range(first, last + 1):
    car_actuel = chr(i)
    cpt_car = 0
    for r in prov:
        if (r[0].lower() == car_actuel.lower()):
            cpt_car = cpt_car + 1 
    info3.write("le nombre de medocs issus de l enrichissement  commencant par la lettre " + car_actuel+
                " est : " + str(cpt_car) + "\n")
    j= j + cpt_car
info3.write("le nombre total des medocs issus de l enrichissement est de : " + str(j) + "\n")
info3.close()

w = open("subst.dic", "w", encoding="utf-16-le")
w.write('\ufeff \n')

list_trie = list(dict.fromkeys(sorted(list_trie)))

w.write(list_trie[-1])
## on trie le 'é' manuellment et on le positionne  apres le 'e'
for i in list_trie:
    if i[0] <= 'e':
        w.write(i)

for i in list_trie:
    if i[0] == 'é':
        w.write(i)

for i in list_trie:
    if i[0] > 'e' and i[0] <= 'z':
        w.write(i)
w.close()

## generation de fichier info2
test = open("infos2.txt", "w")
fichier = open("subst_corpus.dic", "r",
               encoding="utf-16-le").read().lower().split()
list_enrichir = list(dict.fromkeys(sorted(fichier[1:-1])))
prem_car = list_enrichir[0][0].lower()

cmpt = 0
for token in list_enrichir:
    if token.lower().startswith(prem_car) and token.lower(
    ) != "puis" and token.lower() != "intraveineuse " and prem_car != "ø":
        cmpt += 1
    else:
        if token != "puis" and not token.startswith(
                "ø") and token != "intraveineuse":
            #Si notre script rencontre un mot qui ne commencent pas le terme courant , alors il affiche le nombre de medicament commencant par la lettre dite
            test.write(
                "Le nombre de médicaments provenant de l'enrichissement qui commencent par la lettre "
                + prem_car + " sont: " + str(cmpt) + "\n")
            prem_car = token[0]
            cmpt = 1
# ici la boucle n'a pas d"effet donc on le fais d'une maniere manuelle 
test.write(
    "Le nombre de médicaments provenant de l'enrichissement qui commencent par la lettre "
    + prem_car + " sont: " + str(cmpt) + "\n")
test.write(
    "Le nombre total de médicament provenant de l'enrichissement est: " +
    str(len(list_enrichir)) + " \n")
test.close()
