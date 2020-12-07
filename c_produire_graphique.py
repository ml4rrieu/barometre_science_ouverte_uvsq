import pandas as pd, matplotlib, matplotlib.pyplot  as plt
import numpy as np

"""

Réalisation des 4 graphiques
  2018 : bilan open access
  2018 : type d'accès ouvert par éditeurs
  2018 : type d'accès ouvert par discipline
  Evolution taux open access par an et type oa
    

"""
df = pd.read_csv("./data/out/uvsq_publications_2015_19.csv", na_filter= False)
print("nb of publications", len(df.index))



"""
#===========================================================
##___________________Evolution taux open access par années et par type
#===========================================================
dfyears = df.loc[ (df["published_year"] == "2015.0") | (df["published_year"] == "2016.0") | (df["published_year"] == "2017.0") | (df["published_year"] == "2018.0") | (df["published_year"] == "2019.0"), :]
print("nb publis entre 2015 et 2019", len(dfyears.index))
pd.set_option('mode.chained_assignment', None)
dfyears.is_oa = dfyears.is_oa.astype(bool)

#uniquement pour un retour dans la consol
halnodoi = dfyears.loc[ (dfyears["doi"] == "") , :]
print(f"nb publis hal uniquement {len(halnodoi.index)}")
print(f"soit en % de plus {round(len(halnodoi.index)/len(dfyears.index) * 100, 1)}")

haloa = dfyears.loc[ (dfyears["doi"] == "") & (dfyears["is_oa"] == True) , :]
print("nombre de publi oa dans hal", len(haloa))

#retrouver les types d'AO
dfyears["oa_publisher_repository"] = dfyears.oa_type == "repository;publisher"
dfyears["oa_repository"] = dfyears.oa_type == "repository"
dfyears["oa_publisher"] = dfyears.oa_type == "publisher"
dfyears["oa_unk"] = dfyears.oa_type == "unknow"


#definition du taux AO par années
dfoa = pd.DataFrame(dfyears.groupby(["published_year"])
  [["is_oa", "oa_repository", "oa_publisher", "oa_unk", "oa_publisher_repository"]].agg(
    ["count", np.mean])).reset_index()

dfoa.columns = ["published_year", "nb_doi", "oa_mean", "nbdoi1", "oa_repository_mean", "nb_doi2",
"oa_publisher_mean", "nb_doi3", "oa_unk_mean", "nb_doi4", "oa_publisher_repository_mean"]

#print(dfoa.info())

dfoa["year_label"] = dfoa.apply(
  lambda x: "{}\n({} publications)".format(x.published_year[:x.published_year.index(".")]
  , int(x.nb_doi)), axis = 1)
dfoa = dfoa.sort_values(by = "published_year", ascending = True)


fig, (ax) = plt.subplots(figsize=(15, 10), dpi=100, facecolor='w', edgecolor='k')

years = dfoa.year_label.tolist()
y_pos = np.arange(len(years))

oa_publisher_repository_mean = dfoa.oa_publisher_repository_mean.tolist() 
oa_repository_mean = dfoa.oa_repository_mean.tolist() 
oa_publisher_mean = dfoa.oa_publisher_mean.tolist() 
oa_unk_mean = dfoa.oa_unk_mean.tolist()

oa_total_mean = list( map(lambda x,y: x+y, oa_publisher_repository_mean, oa_repository_mean))
oa_total_mean = list( map(lambda x,y: x+y, oa_total_mean, oa_publisher_mean)  )
oa_total_mean = list( map(lambda x,y: x+y, oa_total_mean, oa_unk_mean)  )     


rect1 = ax.bar(y_pos, oa_publisher_mean, align='center', alpha = 1.0, color='gold',
        ecolor='black', label="Éditeur")

ax.bar(y_pos, oa_publisher_repository_mean, align='center', alpha = 1.0, color='greenyellow',
        bottom = oa_publisher_mean,
        ecolor='black', label="Éditeur et Archive ouverte")

ax.bar(y_pos, oa_repository_mean, align='center',alpha = 1.0, color='seagreen',
       bottom = [oa_publisher_mean[i] + oa_publisher_repository_mean[i] for i in range(0, len(oa_publisher_mean))], 
         ecolor='black', label="Archive ouverte")


w = rect1[0].get_width()
# Lors de l'ajout (ou du retrait) d'une nouvelle année pendant la génération de ce graphique, penser à changer l'intervalle.
# Pour observer la période 2016-2020, il faudra remplacer range(0, 4) par range (O,5)
for year_ix in range(0, 5):
    ax.annotate("{:,.1%}".format(oa_total_mean[year_ix]),
                        xy=(year_ix , oa_total_mean[year_ix]),
                        xytext=(0, 20),  
                        size=20,
                        textcoords="offset points",
                        ha='center', va='bottom')


ax.set_xticks(y_pos)
ax.set_xticklabels(years, fontsize = 15)
#ax.invert_xaxis()  # labels read top-to-bottom
ax.set_ylim([0,1])
ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()], fontsize = 20)

# reordonner la legende pour avoir en haut l'éditeur
handles, labels = ax.get_legend_handles_labels()
order = [2,1,0]
ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order], fontsize = 15)
#ax.legend( fontsize=15)

ax.yaxis.grid(ls='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.title("Évolution du taux d'accès ouvert aux publications", fontsize = 20, x = 0.5, y = 1, fontweight = 'bold', alpha = 0.6)
plt.savefig('./img/evolution_oa.png', dpi=100, bbox_inches='tight', pad_inches=0.1)
exit()



#===========================================================
##___________________2018 : bilan open access
#===========================================================
dfpie = df[ df["published_year"] == "2018.0"]
oa_bool = dfpie["is_oa"].value_counts().sort_index()
oa_bool = oa_bool.rename( {True : "Accès ouvert global", False : "Accès fermé global"})
print(oa_bool)

oa_type = dfpie["oa_type"].value_counts().sort_index()
oa_type = oa_type.rename({"closed" : "Accès fermé", "publisher" : "Éditeur", 
  "repository" : "Archive ouverte", "repository;publisher" : "Éditeur et Archive ouverte"})
print(oa_type)


fig, ax = plt.subplots(dpi=100)
ax.set_aspect('equal')
ax.pie(oa_bool, labels=oa_bool.index, radius=3, labeldistance = None, 
  colors=['tomato', 'springgreen'], autopct=lambda x: str(round(x, 1)) + '%', pctdistance = 0.9, shadow = True);
ax.pie(oa_type, labels=oa_type.index, radius=2.3, labeldistance = None, 
  colors=['firebrick','gold','greenyellow','seagreen'], autopct=lambda x: str(round(x, 1)) + '%', pctdistance = 0.9);
    
ax.pie([1], radius=1.3, colors='white');
ax.legend(loc="center", fontsize = 12)
plt.title('Proportion des publications 2018 en accès ouvert (mesuré en 2020)', fontsize = 20, x = 0.55, y = 1.8, fontweight = 'bold', alpha = 0.6)
plt.savefig('./img/type_oa_2018.png', dpi=150, bbox_inches='tight', pad_inches=0.9)

exit()

"""

#===========================================================
##___________________2018 : type d'accès ouvert par éditeurs
#===========================================================
publications_2018 = df.loc[df['published_year'] == "2018.0",:]
publications_par_editeur = publications_2018['publisher'].value_counts().iloc[0:30]
sel_editors = ["Elsevier BV", "Springer Science and Business Media LLC", "Wiley", "Copernicus GmbH", "Oxford University Press (OUP)", 
"American Geophysical Union (AGU)", "Ovid Technologies (Wolters Kluwer Health)", "IEEE", "EDP Sciences", "Springer International Publishing",
"Informa UK Limited", "BMJ", "IOP Publishing", "American Chemical Society (ACS)", "Public Library of Science (PLoS)", "MDPI AG", 
"American Meteorological Society", "CAIRN", "Dalloz", "Frontiers Media SA"]
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
df_oa_editeur = df_oa_editeur.sort_values(by='closed', ascending=False)

## __2__ Générer le graphique
import matplotlib.ticker as mtick
ax = df_oa_editeur.drop(["Total", "y_label"], axis=1).plot(kind="barh", stacked=True, figsize=(15, 13), 
  color=['tomato','gold','greenyellow','seagreen'])
ax.xaxis.set_major_formatter(mtick.PercentFormatter())

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
        ax.text(x + width/2., y + height/2., label, ha='center', va='center', fontsize=15)
        
plt.gca().invert_yaxis()
plt.tick_params(axis = 'both', labelsize = 20)
plt.xlabel("proportions des type d'accès ouvert", fontsize=20)  
plt.ylabel(None, fontsize = 15)

# Les légendes sont nativement en anglais. Elles ont été renommées ici, mais attention, pour une réutilisation avec d'autres
# données, il est conseillé d'enlever cette liste ["Accès fermé", "Editeur"...] et de générer le graphique une 1ère
# fois pour voir quels types de documents ressortent et dans quel ordre. On peut toujours renommer la légende dans un 2ème 
# temps.

plt.legend(['Accès fermé', 'Éditeur', 'Éditeur et Archive ouverte', 'Archive ouverte'],
              loc = 'best', ncol = 4,
              frameon = True, markerscale = 1, title = None, fontsize = 17,
              borderpad = 0.2, labelspacing = 0.3, bbox_to_anchor=(0.011, 0.985), framealpha= 1)

plt.title("Taux d'accès ouvert aux publications 2018 par éditeur", fontsize = 25, x = 0.49, y = 1.05,
          fontweight = 'bold', alpha = 0.6)
plt.savefig('./img/taux_type_oa_editeur.png', dpi=100, bbox_inches='tight', pad_inches=0.9)

exit()


#===========================================================
##___________________2018 : type d'accès ouvert par discipline
#===========================================================

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
df_oa_discipline["y_label"] = df_oa_discipline.index + "\n" + df_oa_discipline["Total"].apply(str) \
                                     + " publications"
df_oa_discipline.index = df_oa_discipline["y_label"]

import matplotlib.ticker as mtick
ax = df_oa_discipline.drop(["Total", "y_label"], axis=1).plot(kind="barh", stacked=True, figsize=(14, 10), 
    color=['tomato','gold','greenyellow','seagreen'])
ax.xaxis.set_major_formatter(mtick.PercentFormatter())

labels = []
for j in df_oa_discipline.columns:
    for i in df_oa_discipline.index:
        label = df_oa_discipline.loc[i][j]
        if type(label) != str : 
          #si ce n'est pas la discipline on arrondi pour un meilleur affichage
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

plt.xlabel("proportion des types d'accès ouvert", fontsize=15)  
plt.ylabel(None, fontsize = 15)

# Les légendes sont nativement en anglais. Elles ont été renommées ici, mais attention, pour une réutilisation avec d'autres
# données, il est conseillé d'enlever cette liste ["Accès fermé", "Editeur"...] et de générer le graphique une 1ère
# fois pour voir quels types de documents ressortent et dans quel ordre. On peut toujours renommer la légende dans un 2ème 
# temps.
plt.legend(['Accès fermé', 'Éditeur', 'Éditeur et Archive ouverte', 'Archive ouverte'],
              loc = 'best', ncol = 4,
              frameon = True, markerscale = 1, title = None, fontsize = 15,
              borderpad = 0.2, labelspacing = 0.3, bbox_to_anchor=(0.02, 0.985), framealpha= 1)

plt.title("Taux d'accès ouvert des publications 2018 par discipline", fontsize = 25, x = 0.49, y = 1.1,
          fontweight = 'bold', alpha = 0.6)

#plt.show()
plt.savefig('./img/taux_type_oa_discipline.png', dpi=100, bbox_inches='tight', pad_inches=0.1)


exit()




## simple bar chart example
"""
years = [y for y in range(2015, 2020)]
repo = [40, 10, 30, 45, 55]
editors = [10, 15, 12, 17, 20 ]
plt.bar(years, repo, label = "repo")
plt.bar(years, editors, bottom = repo, label = "editors")
plt.legend(loc = "upper right")
plt.show()
"""
