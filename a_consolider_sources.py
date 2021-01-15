import pandas as pd, unidecode
import re
'''
Consolidations des données venant des différentes sources (HAL, WOS, Scopus, PUBMED, LENS) et dédoublonnage.
Sont conservés les documents avec DOI et ceux sans DOI présents dans HAL.

Etapes
	___0___Charger les fichiers CSV_______
	___1___Dedoublonner les documents sur les DOI ou bien les titres_______
	___X___CODE OPTIONNEL POUR ENRICHIR et NETTOYER HAL
	
 
fichiers produits
	data/uvsq_dois_halId_2015_19 : liste des documents conservés avec une colonne DOI et une autre halId
 	data/out/sources_statistiques.csv : statistiques volumétriques sur les sources
 	data/out/hal_verif_doi_manquants : documents dans HAL sans DOI dont le titre correspond à un doc avec DOI 
 	data/out/hal_verif_doublons_titres.csv : documents dans HAL avec titre identifique

'''
def normalize_txt(title) : 
	"""retirer les espaces, des accents, sans majuscules"""
	cut = re.split("\W+", title)
	join_cut = "".join(cut).lower()
	return unidecode.unidecode(join_cut)


def conforme_df(df, col_name):
	"""garde les colonnes de col_name, les renommes et passe en miniscule doi et titre """
	df = df[ list(col_name.keys()) ].copy()  
	df.rename(columns = col_name, inplace = True) 

	df["doi"] = df["doi"].str.lower() # doi en minuscule
	df["title_norm"] = df["title"].apply(lambda row:  normalize_txt(row))
	df.drop(columns=["title"], inplace = True)
	return df

def extract_stats_from_base(src_name, df) : 
	"""de la base extraire les données total publi, doi only, no doi"""
	no_doi = df["doi"].isna().sum()
	w_doi = df["doi"].str.match("10.").sum()
	if no_doi + w_doi == len(df.index) : 
		print(f"\n\n{src_name} imported ok\n\tdois {w_doi}\n\tno dois {no_doi}")
		stats_buffer.append([src_name, len(df.index), w_doi, no_doi] )
	else :
		print(f"{src_name} not imported")
	

#___0___Charger les fichiers CSV_______
stats_buffer, df_buffer = [], []

# HAL 
hal = pd.read_csv("./data/hal_2015-19.csv")
hal = conforme_df( hal, {"doiId_s": "doi", 'halId_s': 'halId', 'title_s': 'title'})
extract_stats_from_base("hal", hal)


# WOS
files = ["wos_2015-16","wos_2017-18", "wos_2019"]
for f in files : 
	df = pd.read_csv(f"./data/{f}.txt", sep="\t", index_col=False)
	df_buffer.append(df)

wos = pd.concat(df_buffer)
wos = conforme_df( wos, {"DI":"doi", "TI": "title"})
extract_stats_from_base('wos', wos)



# SCOPUS
df_buffer.clear()
for y in range(2015, 2020): #2020 is exclude
	for suff in ["oa", "other"] : 
		df_buffer.append( pd.read_csv(f"./data/scopus_{str(y)+suff}.csv"))

scopus = pd.concat(df_buffer)
scopus = conforme_df(scopus, {"DOI" : "doi", "Title" : "title"})
extract_stats_from_base("scopus", scopus)

# PUBMED
pubmed = pd.read_csv("./data/pubmed_2015-19.csv")
pubmed = conforme_df( pubmed, {"DOI" : "doi" , "Title" : "title" })
extract_stats_from_base('pubmed', pubmed)

# LENS
lens = pd.read_csv("./data/lens_2015-19.csv")
lens = conforme_df(lens, {"DOI" : "doi", "Title" : "title"})
extract_stats_from_base("lens", lens)



#___1___Dedoublonner les documents sur les DOI ou bien les titres_______
rawdf = pd.concat([wos, scopus, hal, pubmed, lens]) 
# trie des documents par DOI puis par halId 
rawdf.sort_values(by=['doi', 'halId'], inplace = True)
print("\n\nAvant dédoublonnage nombre item", len(rawdf[ rawdf['doi'].notna()]) )


# __a Dedoublonnage sur les DOI
# retirer les docs dont le DOI est en double (et conserver les docs sans DOI)
# (dans le mask il faut que la valeur boolean soit False pour qu'elle soit retirée, d'où le ~ )
clean_doi = rawdf[ (~rawdf['doi'].duplicated()) | (rawdf['doi'].isna()) ].copy()
print('Apres dedoublonnage sur DOI, nb publi', len(clean_doi.index))

# __b dedoublonnage sur les titres normés
#sélectionner les documents  avec DOI, et ceux sans DOI dont les titres ne sont pas des doublons
mask = (clean_doi['doi'].notna()) | ( (clean_doi['doi'].isna()) & (~clean_doi['title_norm'].duplicated()) )
clean_doi_title = clean_doi[mask].copy()
print("Apres dedoublonnage DOI et (pour les sans DOI) sur titre , nb publi", len(clean_doi_title.index))

# retenir uniquement les publis  avec DOI ou idHAL
final = clean_doi_title[ (clean_doi_title['doi'].notna()) | (clean_doi_title['halId'].notna()) ].copy()

#ajout des données retenues dans les stats
stats_buffer.append([
	"retenu", 
	len(final), 
	len(final[ final['doi'].notna()]), 
	len(final[ final['doi'].isna()]) ])

toprint = {
"\n\ndoc total apres dedoublonnage" : len(clean_doi_title),
'docs exclus (no doi no halId) ' : len( clean_doi_title[  (clean_doi_title['doi'].isna()) & (clean_doi_title['halId'].isna()) ] ),
'doc inclus (doi ou halId)\t': len(final),
'pertinence %\t\t\t\t' : round(
	len(final.index)/len(clean_doi_title.index)*100, 1),
'\ndoc à traiter avec doi': len(final[ final['doi'].notna() ]),
'doc à traiter sans doi' : len(final[ final['doi'].isna() ]),
}

[print(k, '\t\t', v) for k, v in toprint.items()]



# Extraire des statistiques pour comarer les sources
stat_table = pd.DataFrame(stats_buffer, columns=['name', 'all', 'doi', 'no_doi'])
stat_table.to_csv("./data/out/statistiques_sur_les_bases.csv", index = False)

#extraire le jeu de données final
final.drop(["title_norm"], axis = 1, inplace = True)
final.to_csv("./data/uvsq_dois_halId_2015_19.csv", index = False, encoding = 'utf8')



#______________VENN DIAGRAMM sur les bases
def deduce_set_from_df(df) :
	"""dans un set mettre les dois et, pour les publis sans dois, les titres normés""" 
	publis = df["doi"].tolist()
	titleonly = df[ df["doi"].isna()]
	titles = titleonly["title_norm"].tolist()
	publis.extend(titles)
	return set(publis)

venn_data = {
"Hal" : deduce_set_from_df(hal),
"Scopus" : deduce_set_from_df(scopus),
"Wos" : deduce_set_from_df(wos)
#"Pubmed" : set(pubmed["doi"].values),
#"Lens" : set(lens["doi"].values)
}


from matplotlib_venn import venn2, venn2_circles, venn2_unweighted
from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt

plt.figure(figsize=(14,8))

v = venn3(subsets = 
	(venn_data["Hal"], venn_data["Scopus"], venn_data["Wos"]),
	#set_colors=("#f2a191", "#f0c165", "#64bac3" ),
	 set_labels = tuple(venn_data.keys()), alpha = 0.3  )
	  

#change label size
for label in v.set_labels : 
	label.set_fontsize(13)
	label.set_fontweight("bold")
#[label.set_fontsize(13) for label in v.set_labels]
 
plt.title("Recouvrement entre les 3 principales bases", fontsize=16, fontweight = 'bold', alpha = 0.6)
plt.savefig('./img/recouvrement_entre_bases.png', dpi=130, bbox_inches='tight', pad_inches=0.1)

exit()

#print("pmonly", len(pubmedset - scopusset) )
#print("scopus only", len( scopusset - pubmedset) )
#print("pmInter	scopus", len(pubmedset.intersection(scopusset)))


"""
venn_data = {
"HAL" : set(hal["doi"].values),
"Scopus" : set(scopus["doi"].values),
"Wos" : set(wos["doi"].values),
"Pubmed" : set(pubmed["doi"].values),
"Lens" : set(lens["doi"].values)
}

import matplotlib
from matplotlib import pyplot as plt
import venn
from venn import venn

"""

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








