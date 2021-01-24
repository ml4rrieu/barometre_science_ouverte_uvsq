import pandas as pd, matplotlib, matplotlib.pyplot  as plt
import numpy as np

"""

Réalisation des graphiques
  2018 : bilan open access
  2018 : type d'accès ouvert par éditeurs
  2018 : type d'accès ouvert par discipline
  Evolution taux open access par an et type oa
    

"""



#===========================================================
##___________________2018 : type d'accès ouvert par éditeurs
#===========================================================
df = pd.read_csv("./data/out/uvsq_publications_2015_19.csv", dtype={"published_year":"string"}, na_filter=False, low_memory=False)
publications_2018 = df.loc[df['published_year'] == "2018.0",:]
publications_par_editeur = publications_2018['publisher'].value_counts().iloc[0:30]
print(publications_par_editeur)
sel_editors = ["Elsevier BV", "Springer Science and Business Media LLC", "Wiley", "Copernicus GmbH", "Oxford University Press (OUP)", 
"American Geophysical Union (AGU)", "Ovid Technologies (Wolters Kluwer Health)", "IEEE", "EDP Sciences", "Springer International Publishing",
"BMJ", "Informa UK Limited", "Public Library of Science (PLoS)", "IOP Publishing", "American Chemical Society (ACS)", "MDPI AG", 
"American Meteorological Society", "Dalloz", "CAIRN", "Frontiers Media SA"]
editeurs_2018 = publications_2018[publications_2018['publisher'].isin(sel_editors)]
#Quelle est la proportion d'accès ouvert, par type d'accès, des publications par éditeur dans l'année ?
df_oa_editeur_global = pd.crosstab([editeurs_2018['publisher']],editeurs_2018['oa_type'])
df_oa_editeur_global["Total"] = publications_par_editeur
df_oa_editeur_global["y_label"] = df_oa_editeur_global.index + " - " + df_oa_editeur_global["Total"].apply(str) + " publications"
                                     
df_oa_editeur_global.index = df_oa_editeur_global["y_label"]
df_oa_editeur_global.sort_values(by='closed', ascending=False)


#Convertir le résultat en pourcentages
df_oa_editeur = pd.crosstab([editeurs_2018['publisher']],editeurs_2018['oa_type'])
df_oa_editeur = (df_oa_editeur.T / df_oa_editeur.T.sum()).mul(100).round(1)
df_oa_editeur = df_oa_editeur.T
df_oa_editeur["Total"] = publications_par_editeur
df_oa_editeur["y_label"] = df_oa_editeur.index + " - " + df_oa_editeur["Total"].apply(str) \
                                     + " publications"
df_oa_editeur.index = df_oa_editeur["y_label"]
df_oa_editeur = df_oa_editeur.sort_values(by=['closed', "publisher"], ascending=False)

## __2__ Générer le graphique
import matplotlib.ticker as mtick
ax = df_oa_editeur.drop(["Total", "y_label"], axis=1).plot(kind="barh", stacked=True, figsize=(15, 13), 
  color=['tomato','gold','greenyellow','seagreen'])


## ___3____ configurer l'afichage
# remove axis
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
# remove xticks
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    labelbottom=False) # labels along the bottom edge are off

# ajotuer le pourcentage pour chaque types
labels = []
for j in df_oa_editeur.columns:
    for i in df_oa_editeur.index:
      label = df_oa_editeur.loc[i][j]
      #label = str(df_oa_editeur.loc[i][j]) + "%"
      if type(label) != str : 
        label = round(label)
        label = str(label) 
        label = label[ : label.find(".")] + "%"
        labels.append(label)

patches = ax.patches
for label, rect in zip(labels, patches):
    width = rect.get_width()
    if width > 0:
        x = rect.get_x()
        y = rect.get_y()
        height = rect.get_height()
        ax.text(x + width/2., y + height/2., label, ha='center', va='center', fontsize=12)
        
plt.gca().invert_yaxis()
plt.tick_params(axis = 'both', labelsize = 18)
plt.ylabel(None)

# Les légendes sont nativement en anglais. Elles ont été renommées ici, mais attention, pour une réutilisation avec d'autres
# données, il est conseillé d'enlever cette liste ["Accès fermé", "Editeur"...] et de générer le graphique une 1ère
# fois pour voir quels types de documents ressortent et dans quel ordre. On peut toujours renommer la légende dans un 2ème 
# temps.

plt.legend(['Accès fermé', 'Éditeur', 'Éditeur et Archive ouverte', 'Archive ouverte'],
              loc = 'best', ncol = 4, markerscale = 1, title = None, fontsize = 18,
              borderpad = 0.2, labelspacing = 0.3, bbox_to_anchor=(0.011, 0.985), framealpha= False)

plt.title("Taux d'accès ouvert aux publications 2018 par éditeur", fontsize = 34, x = 0.49, y = 1.08,  alpha = 0.6)
plt.savefig('./img/taux_type_oa_editeur.png', dpi=100, bbox_inches='tight', pad_inches=0.9)




#===========================================================
##___________________2018 : type d'accès ouvert par discipline
#===========================================================
df = pd.read_csv("./data/out/uvsq_publications_2015_19.csv", dtype={"published_year":"string"}, na_filter=False, low_memory=False)
publications_2018 = df.loc[df['published_year'] == "2018.0",:]
print("2018 nb of publi", len(publications_2018))
publications_par_domaine = publications_2018['scientific_field'].value_counts().sort_index()
#print(publications_par_domaine)

df_oa_discipline_global = pd.crosstab([publications_2018['scientific_field']],publications_2018['oa_type'])
# Ajout d'une colonne avec le total par discipline
df_oa_discipline_global["Total"] = publications_par_domaine
# Ajout d'une colonne qui concatène le nom de la discipline et le total
df_oa_discipline_global["y_label"] = df_oa_discipline_global.index + "\n" + df_oa_discipline_global["Total"].apply(str) + " publications"

# Réindexation de l'index pour que les bonnes informations s'affichent dans le graphique final
df_oa_discipline_global.index = df_oa_discipline_global["y_label"]


df_oa_discipline = pd.crosstab([publications_2018['scientific_field']],publications_2018['oa_type'])
df_oa_discipline = (df_oa_discipline.T / df_oa_discipline.T.sum()).mul(100).round(1)
df_oa_discipline = df_oa_discipline.T
df_oa_discipline["Total"] = publications_par_domaine
df_oa_discipline["y_label"] = df_oa_discipline.index + "\n" + df_oa_discipline["Total"].apply(str) + " publications"
                                     
df_oa_discipline.index = df_oa_discipline["y_label"]

import matplotlib.ticker as mtick
ax = df_oa_discipline.drop(["Total", "y_label"], axis=1).plot(kind="barh", stacked=True, figsize=(14, 10), 
    color=['tomato','gold','greenyellow','seagreen'])
#ax.xaxis.set_major_formatter(mtick.PercentFormatter())

## _______ configurer l'afichage
# remove axis
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
# remove xticks
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    labelbottom=False) # labels along the bottom edge are off


labels = []
for j in df_oa_discipline.columns:
    for i in df_oa_discipline.index:
        label = df_oa_discipline.loc[i][j]
        if type(label) != str : 
          #pour un meilleur affichage : si ce n'est pas la discipline on arrondi 
          label = str(round(label))
          label = label[:label.find(".")] + "%"     
          labels.append(label)
        

patches = ax.patches
for label, rect in zip(labels, patches):
    width = rect.get_width()
    if width > 0:
        x = rect.get_x()
        y = rect.get_y()
        height = rect.get_height()
        ax.text(x + width/2., y + height/2., label, ha='center', va='center', fontsize=12)

# Trier les disciplines par ordre alphabétique
plt.gca().invert_yaxis()
plt.tick_params(axis = 'both', labelsize = 13)

#plt.xlabel("proportion des types d'accès ouvert", fontsize=15)  
plt.ylabel(None, fontsize = 15)

# Les légendes sont nativement en anglais. Elles ont été renommées ici, mais attention, pour une réutilisation avec d'autres
# données, il est conseillé d'enlever cette liste ["Accès fermé", "Editeur"...] et de générer le graphique une 1ère
# fois pour voir quels types de documents ressortent et dans quel ordre. On peut toujours renommer la légende dans un 2ème 
# temps.
plt.legend(['Accès fermé', 'Éditeur', 'Éditeur et Archive ouverte', 'Archive ouverte'],
              loc = 'best', ncol = 4,
              frameon = True, markerscale = 1, title = None, fontsize = 15,
              borderpad = 0.2, labelspacing = 0.3, bbox_to_anchor=(0.02, 0.985), framealpha= False)

plt.title("Taux d'accès ouvert des publications 2018 par discipline", fontsize = 25, x = 0.49, y = 1.07,  alpha = 0.6)

#plt.show()
plt.savefig('./img/taux_type_oa_discipline.png', dpi=100, bbox_inches='tight', pad_inches=0.1)


#exit()



#===========================================================
##___________________Evolution taux open access par années et par type
#===========================================================
df = pd.read_csv("./data/out/uvsq_publications_2015_19.csv", dtype={"published_year":"string"}, na_filter=False, low_memory=False)
# ____0____ recupérer les données
dfyears = df.loc[ df["published_year"].isin(["2015.0", "2016.0", "2017.0", "2018.0", "2019.0"]), :]
print("nb publis a traiter", len(dfyears))
pd.set_option('mode.chained_assignment', None)
dfyears.is_oa = dfyears.is_oa.astype(bool)

#comparer les valeurs avec ou sans DOI : retour consol uniquement
halnodoi = dfyears[ dfyears["doi"] == ""]
print(f"nb publis hal uniquement {len(halnodoi.index)}")
print(f"soit en % de plus {round(len(halnodoi.index)/len(dfyears.index) * 100, 1)}")

haloa = dfyears.loc[ (dfyears["doi"]== "") & (dfyears["is_oa"] == True) , :]
print("nombre de publi oa dans hal", len(haloa))

#retrouver les types d'AO
dfyears["oa_publisher_repository"] = dfyears.oa_type == "publisher;repository"
dfyears["oa_repository"] = dfyears.oa_type == "repository"
dfyears["oa_publisher"] = dfyears.oa_type == "publisher"
dfyears["oa_unk"] = dfyears.oa_type == "unknow"

#definition du taux AO par années
dfoa = pd.DataFrame(dfyears.groupby(["published_year"])
  [["is_oa", "oa_repository", "oa_publisher", "oa_unk", "oa_publisher_repository"]].agg(
    ["count", np.mean])).reset_index()

dfoa.columns = ["published_year", "nb_doi", "oa_mean", "nbdoi1", "oa_repository_mean", "nb_doi2",
"oa_publisher_mean", "nb_doi3", "oa_unk_mean", "nb_doi4", "oa_publisher_repository_mean"]

dfoa["year_label"] = dfoa.apply(
  lambda x: "{}\n({} publications)".format(x.published_year[:x.published_year.index(".")]
  , int(x.nb_doi)), axis = 1)
dfoa = dfoa.sort_values(by = "published_year", ascending = True)


# ____1____ passer les données dans le modele de representation graphique
fig, (ax) = plt.subplots(figsize=(15, 10), dpi=100, facecolor='w', edgecolor='k')

ax.bar(dfoa.year_label, dfoa.oa_repository_mean.tolist() , align='center', alpha = 1.0, color='seagreen',
        ecolor='black', label="Archive ouverte")

ax.bar(dfoa.year_label, dfoa.oa_publisher_repository_mean.tolist(), align='center', alpha = 1.0, color='greenyellow',
        bottom = dfoa.oa_repository_mean.tolist(),
        ecolor='black', label="Éditeur et Archive ouverte")

ax.bar(dfoa.year_label, dfoa.oa_publisher_mean.tolist() , align='center',alpha = 1.0, color='gold',
       bottom = [sum(x) for x in zip(dfoa.oa_repository_mean.tolist(), dfoa.oa_publisher_repository_mean.tolist())], ecolor='black', label="Éditeur")


# ____2____ configurer l'affichage
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
# retirer l'origine sur Y
yticks = ax.yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)

# tracer les grilles 
ax.yaxis.grid(ls='--', alpha=0.4)
#ax.set_xticks(y_pos)
ax.set_xticklabels(dfoa.year_label, fontsize = 12)
ax.set_ylim([0,1])
ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()], fontsize = 10)
# reordonner la legende pour avoir en haut l'éditeur
handles, labels = ax.get_legend_handles_labels()
order = [2,1,0]
ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order], fontsize = 15, loc="upper center", borderaxespad =1.7)

oa_total_mean = [sum(x) for x in zip(dfoa.oa_repository_mean.tolist(), dfoa.oa_publisher_repository_mean.tolist(), dfoa.oa_publisher_mean.tolist())]

#ajout le taux d'accès ouvert global
for year_ix in range(len(dfoa.year_label)):
    ax.annotate("{:,.1%}".format(oa_total_mean[year_ix]),
                        xy=(year_ix , oa_total_mean[year_ix]),
                        xytext=(0, 20),  
                        size=16,
                        textcoords="offset points",
                        ha='center', va='bottom')


## Ajouter les taux par type, difficulté : il faut prendre en compte les taux précédents
colname = ["oa_repository_mean", "oa_publisher_repository_mean", "oa_publisher_mean"]
for col in  colname : 
  for year_ix in range(len(dfoa.year_label)) : 

    ypos_bottom = 0 
    for col_before_ix in range(colname.index(col)) :
      col_before = colname[col_before_ix]
      ypos_bottom += dfoa[col_before][year_ix]

    ax.annotate( f"{int(round( dfoa[col][year_ix] * 100 ))} %",
      xy = (year_ix, ypos_bottom + dfoa[col][year_ix] * 0.40), 
      xytext= (0,0), 
      size = 8, 
      textcoords="offset points",
      ha='center', va='bottom', color = "black")


plt.title("Évolution du taux d'accès ouvert aux publications", fontsize = 25, x = 0.5, y = 1.05, alpha = 0.6)
plt.savefig('./img/evolution_oa.png', dpi=100, bbox_inches='tight', pad_inches=0.1)

#exit()




#===========================================================
##___________________Répartition des publications entre les bases
#===========================================================

# ____0____ recupérer les données
df = pd.read_csv("./data/out/statistiques_sur_les_bases.csv")
data = df.to_dict("list")

x = np.arange(len(data["name"]))  # the label locations
width = 0.2


# ____1____ passer les données dans le modele de representation graphique
fig, ax = plt.subplots(figsize=(7,4))

ax.bar(x - width, data["all"], width, label='toutes publications', color = "orchid")
ax.bar(x , data["doi"], width, label='publications avec DOI',color = "gold")
ax.bar(x + width, data["no_doi"], width, label='publications sans DOI', color = "skyblue")


# ____2____ configurer l'affichage
ax.yaxis.grid(ls='--', alpha=0.4)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
# retirer l'origine sur Y
yticks = ax.yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)


plt.yticks([i for i in range(0, 18000, 5000)], fontsize = 10)
ax.set_ylabel('Nombre de publications', fontsize = 8)
ax.set_xticks(x)
ax.set_xticklabels([n.capitalize() for n in data["name"] ], fontsize = 11)
plt.legend(loc="upper center", fontsize = 8)

ax.set_title("Quantité de publications dans les bases", fontsize=16, alpha = 0.6, y = 1.05)
plt.savefig('./img/comparaisons_entre_les_bases.png', dpi=150, bbox_inches='tight', pad_inches=0.05)
#plt.show()

#exit()





#===========================================================
##___________________2018 : bilan open access
#===========================================================
df = pd.read_csv("./data/out/uvsq_publications_2015_19.csv", dtype={"published_year":"string"}, na_filter=False, low_memory=False)
dfpie = df[ df["published_year"] == "2018.0"]
oa_bool = dfpie["is_oa"].value_counts().sort_index()
oa_bool = oa_bool.rename( {True : "Accès ouvert global", False : "Accès fermé global"})
print(oa_bool)

oa_type = dfpie["oa_type"].value_counts().sort_index()
oa_type = oa_type.rename({"closed" : "Accès fermé", "publisher" : "Éditeur", 
  "repository" : "Archive ouverte", "publisher;repository" : "Éditeur et Archive ouverte"})
print(oa_type)


fig, ax = plt.subplots(dpi=100)
ax.set_aspect('equal')
ax.pie(oa_bool, labels=oa_bool.index, radius=3, labeldistance = None, 
  colors=['tomato', 'springgreen'], autopct=lambda x: str(round(x, 1)) + '%', pctdistance = 0.9, shadow = True);
ax.pie(oa_type, labels=oa_type.index, radius=2.3, labeldistance = None, 
  colors=['firebrick','gold','greenyellow','seagreen'], autopct=lambda x: str(round(x, 1)) + '%', pctdistance = 0.9);
    
ax.pie([1], radius=1.3, colors='white');
ax.legend(loc="center", fontsize = 12)
plt.title('Proportion des publications 2018 en accès ouvert (mesuré en 2020)', fontsize = 23, x = 0.55, y = 1.8, alpha = 0.6)
#plt.show()
plt.savefig('./img/type_oa_2018.png', dpi=150, bbox_inches='tight', pad_inches=0.9)


#exit()



