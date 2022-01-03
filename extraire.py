import urllib.request
import re
import codecs
import string
import sys

arg_valable=True

if len(sys.argv)!=3: #3 argument (le nom du fichier +le domaine d'aspiration +le port )
	print("devez entrez le domaine d'aspiration et le port du serveur en arguments svp")
	arg_valable=False
# creation des deux argument 
else:	#1- l'intervalle d'extraction 
	if (not re.match("[A-Za-z]-[A-Za-z]",sys.argv[1])) or (sys.argv[1][2].upper()< sys.argv[1][0].upper()):
		print("Le premier argument est faux veulliez le changer svp")
		arg_valable=False
	#le port http format chiffre 
	if re.search(r"\D",sys.argv[2]):
		print("Le port est incorrect veulliez le changer svp (le port contient que des chiffres)")
		arg_valable=False

if arg_valable:
	
	infoD={}
	s=0 #initialissation
	
	dic=open("subst.dic",'w',encoding='utf-16-le')
	dic.write('\ufeff')
	
	alfa=string.ascii_uppercase
	
	for j in range(alfa.index(sys.argv[1].upper()[0]),alfa.index(sys.argv[1].upper()[2])+1):
		
		url= urllib.request.urlopen('http://localhost:'+sys.argv[2]+'/vidal/vidal-Sommaires-Substances-'+alfa[j]+'.htm')
		html=url.read().decode('utf8')
		
		medoc=re.findall("(<a href=\"Substance.+?>)(.+?)(</a>)",html)
		infoD[alfa[j]]=len(medoc)
		s=s+len(medoc)
		

		for i in medoc:
			dic.write(i[1]+",.N+subst\n")
		
		
	dic.close()
		
	infos1=open("infos1.txt",'w') #generer le fichier infos1
	
	for i in infoD:
		infos1.write(i+": "+str(infoD.get(i))+"\n")
	infos1.write("\nTotal: "+str(s))