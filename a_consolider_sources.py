import pandas as pd, unidecode
'''
Concaténation des données venant des différentes sources (HAL, WOS, Scopus, PUBMED, LENS) et dédoublonnage.
Sont conservés les documents avec DOI et ceux sans DOI présents dans HAL.

Etapes
	___0___Charger les fichiers CSV_______
	___1___Dedoublonner les documents sur les DOI ou bien les titres_______
	___X___CODE OPTIONNEL POUR ENRICHIR et NETTOYER HAL
	
 
fichiers produits
	data/uvsq_dois_halId_2015_19 : liste des documents conservés avec une colonne DOI et une autre halID
 	misc/sources_statistiques.csv : statistiques volumétriques sur les sources
 	misc/hal_verif_doi_manquants : documents dans HAL sans DOI dont le titre correspond à un doc avec DOI 
 	misc/hal_verif_doublons_titres.csv : documents dans HAL avec titre identifique

'''

def analyse_df(src_name, df) : 
	"""analyse nb de doi dans la base et export de statistique  """
	no_doi = df["doi"].isna().sum()
	w_doi = df["doi"].str.match("10.").sum()
	if no_doi + w_doi == len(df.index) : 
		print(f"\n\n{src_name} imported ok\n\tdois {w_doi}\n\tno dois {no_doi}")
		return [src_name, len(df.index), w_doi, no_doi]
	else :
		print(f"{src_name} not imported")
		return [src_name, 'problem']
	

#___0___Charger les fichiers CSV_______
df_buffer = []
row_buffer = []


# HAL 
hal_r = pd.read_csv("./data/hal_2015-19.csv", encoding='utf8')
hal = pd.DataFrame({"doi": hal_r["doiId_s"], 'halId':hal_r['halId_s'], 'title':hal_r['title_s']})
row_buffer.append (analyse_df("hal", hal))


# WOS
files = ["wos_2015-16","wos_2017-18", "wos_2019"]
for f in files : 
	df = pd.read_csv(f"./data/{f}.txt", sep="\t", index_col=False, encoding='utf8')
	df_buffer.append(df)
wos_r = pd.concat(df_buffer)
wos = pd.DataFrame( {"doi":  wos_r["DI"], 'title': wos_r['TI']} )
row_buffer.append( analyse_df('wos', wos) )


# SCOPUS
df_buffer.clear()
for y in range(2015, 2020): #2020 is exclude
	df_buffer.append( pd.read_csv(f"./data/scopus_{str(y)}.csv", encoding='utf8'))
scopus_r = pd.concat(df_buffer)
scopus = pd.DataFrame( {"doi" : scopus_r["DOI"], 'title': scopus_r['Title']})
row_buffer.append (analyse_df("scopus", scopus))


# PUBMED
pubmed_r = pd.read_csv("./data/pubmed_2015-19.csv", encoding='utf8')
pubmed = pd.DataFrame({"doi": pubmed_r["DOI"], 'title':pubmed_r['Title']})
row_buffer.append(analyse_df('pubmed', pubmed))


# LENS
lens_r = pd.read_csv("./data/lens_2015-19.csv", encoding='utf8')
lens = pd.DataFrame({'doi': lens_r["DOI"], 'title':lens_r['Title']})
row_buffer.append( analyse_df("lens", lens))



#___1___Dedoublonner les documents sur les DOI ou bien les titres_______
rawdf = pd.concat([wos, scopus, hal, pubmed, lens]) 
# trie des documents par DOI puis par halId 
rawdf.sort_values(by=['doi', 'halId'], inplace = True)
print("\n\nnombre item trouvés (sans dédoublonnage)", len(rawdf[ rawdf['doi'].notna()]) )

# doi en miniscule et normalisze le titre une colonne title_norm
rawdf['doi'] = rawdf['doi'].str.lower()
def normalize(title) : 
	"""retirer les espaces, des accents, sans majuscules"""
	temp = title.split()
	temp = "".join(temp).lower()
	return unidecode.unidecode(temp)

rawdf['title_norm'] = rawdf["title"].apply(lambda row : normalize(row))


# __a Dedoublonnage sur les DOI
# retirer les docs dont le DOI est en double (et conserver les docs sans DOI)
# (dans le mask il faut que la valeur boolean soit False pour qu'elle soit retirée, d'où le ~ )
clean_doi = rawdf[ (~rawdf['doi'].duplicated()) | (rawdf['doi'].isna()) ].copy()
print('\nnombre publi apres dedoublonnage sur DOI', len(clean_doi.index))

# __b dedoublonnage sur les titres normés
#Sélectionner les documents  avec DOI, et ceux sans DOI dont les titres ne sont pas des doublons
mask = (clean_doi['doi'].notna()) | ( (clean_doi['doi'].isna()) & (~clean_doi['title_norm'].duplicated()) )
clean_doi_title = clean_doi[mask].copy()
print('nombre publi arpes dedoublonnage (des publi sans DOI) sur le titre', len(clean_doi_title.index))

#retrait des docs sans doi ni halId
final = clean_doi_title[ (clean_doi_title['doi'].notna()) | (clean_doi_title['halId'].notna()) ].copy()
print('nombre publi apres retrait docs sans DOI ni halId' , len(final.index))

toprint = {
'doc à traiter': len(final.index),
'doc avec doi': len(final[ final['doi'].notna() ]),
'doc sans doi' : len(final[ final['doi'].isna() ]),
#les docs non pris en compte sont les docs sans DOI et sans idHAL
'docs echappes' : len( clean_doi_title[  (clean_doi_title['doi'].isna()) & (clean_doi_title['halId'].isna()) ] ),
'pertinence %' : round(
	len(final.index)/len(clean_doi_title.index)*100, 1)
}

print('\n')
[print(k, '\t\t', v) for k, v in toprint.items()]

# Extraire des statistiques pour comarer les sources
stat_table = pd.DataFrame(row_buffer, columns=['name', 'all', 'doi', 'no_doi'])
stat_table.to_csv("./data/out/sources_statistiques.csv", index = False)

final.drop(["title", "title_norm"], axis = 1, inplace = True)
final.to_csv("./data/uvsq_dois_halId_2015_19.csv", index = False, encoding = 'utf8')



#___X___CODE OPTIONNEL POUR ENRICHIR et NETTOYER HAL

# __a Identifier les documents HAL sans DOI et dont le titre correspond à un document avec DOI 
doionly = rawdf[(
	 rawdf['doi'].notna() & rawdf['halId'].isna() )].copy()
doionly['doi'] = doionly['doi'].str.lower()
doionly.drop_duplicates('doi', inplace = True)
del doionly['halId']

halonly = rawdf[(
	rawdf['doi'].isna() & rawdf['halId'].notna()) ].copy()
del halonly['doi']

hal_verify_doi = pd.merge(doionly, halonly, on='title_norm')
hal_verify_doi.sort_values("title_x", inplace = True)
hal_verify_doi.drop( ["title_y", "title_norm"], axis = 1, inplace = True)
hal_verify_doi.to_csv("./data/out/hal_verif_doi_manquants.csv", index= False, encoding = 'utf8')


# __b identifier les doublons de titre sur les notices HAL sans DOI
halonly = rawdf[(
	rawdf['doi'].isna() & rawdf['halId'].notna() )].copy()
# identification des doublons de titre
halonly['duplicated'] = halonly.duplicated('title_norm', keep = False)
halonly_doubl = halonly[ halonly['duplicated']].copy()
halonly_doubl.sort_values("title", inplace = True)
halonly_doubl.drop(["title_norm", "duplicated"], axis = 1, inplace = True)

halonly_doubl.to_csv("./data/out/hal_verif_doublons_titres.csv", index= False, encoding = 'utf8')








#___NOT NECESSARY____Venn diagramm
'''
pubset = set(pubmed["doi"].values)
scopusset = set(scopus["doi"].values)
print("pmonly", len(pubset - scopusset) )
print("scopus only", len( scopusset - pubset) )
print("pmInter	scopus", len(pubset.intersection(scopusset)))
'''


'''
dois.reset_index(drop = True, inplace = True) # re index
print("dois no duplicates", len(dois))
print(dois.head())
dois.to_csv("./data/valid_dois.csv", index = False, encoding = 'utf8')

'''