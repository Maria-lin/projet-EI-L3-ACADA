import sqlite3, re


concord = open('corpus-medical_snt/concord.html','r')
res = re.findall(r'<a href=\"[0-9 ]+\">.+</a>',concord.read())

for i in range(len(res)):
    res[i] = re.findall(r'>.+<',res[i])[0][1:-1]

connection= sqlite3.connect("extraction.db") #on se connect 
connection.execute("CREATE TABLE POSOLOGIE(id INTEGER , posologie TEXT)") 
#connection.execute('SELECT * FROM POSOLOGIE')#on utillise cette instruction apres avoir crée la table sql l'istruction creat marche qu'une seule fois 
## select consiste a afficher la table posologie 
#on peut aussi faire un DROP 
i=1

for line in res:
     print(str(i)+'\t'+line)
     connection.execute("INSERT INTO POSOLOGIE VALUES (?,?)",(str(i),line))
     i=i+1



 
connection.commit()