## Données à charger dans ce dossier

* Les données bibliographiques de votre institution depuis les bases HAL, PUBMED, LENS etc. <br />

* le jeu de données en `.csv` du barometre français de la science ouverte

https://data.enseignementsup-recherche.gouv.fr/explore/dataset/open-access-monitor-france/

* les issns des journaux suspects

https://github.com/ml4rrieu/open_science_tools/blob/main/questionnable_journals/suspiciousIssns.json



<br /><br />
## Données à charger dans le dossier `APC_tracking` 

* `openapc_dois.csv` à récupérer en ligne

https://github.com/OpenAPC/openapc-de/blob/master/data/apc_de.csv

* `doaj_apc_journals.csv` à récupérer en ligne

https://doaj.org/docs/public-data-dump/

`2020-11-30 utilisation du csv disponible sur doaj.org/csv`


* `openapc_journals.csv` à récupérer en ligne

https://github.com/ml4rrieu/open_science_tools/blob/main/apc_journal_tables/openapc_journals.csv



<br /><br />
## Requêtes utilisées pour extraire les données des bases bibliographiques
Sont inclus les publications directement affiliées à l'université et les publications des unités de recherche dont l'université est tutelle.

**WOS**

`OG=(Universite de Versailles Saint-Quentin-En-Yvelines)
Timespan: 2015-2019. Indexes: SCI-EXPANDED, SSCI, A&HCI, CPCI-S, CPCI-SSH, ESCI, CCR-EXPANDED, IC. `

<!--nota : Le WOS fonctionne avec une logique de variantes d'affiliation. le champs `Organization-Enhanced : OG` inclut ces différentes variantes.
-->
limit 5k

**SCOPUS**

`AF-ID("Universite de Versailles Saint-Quentin-en-Yvelines" 60029937) OR AF-ID("Biomarqueurs en Cancérologie et Onco-Hématologie" 60106042) OR AF-ID("Biostatistique Biomathématique, Pharmacoépidémiologie et Maladies Infectieuses" 60106096) OR AF-ID("Centre d'Études sur la Mondialisation Les Conflits, Les Territoires et Les Vulnérabilités" 60106072) OR AF-ID("Centre d'Histoire Culturelle Des Sociétés Contemporaines" 60106071) OR AF-ID("Centre de recherche en épidémiologie et santé des populations" 60106085) OR AF-ID("Centre de Recherche Versailles Saint-Quentin Institutions Publiques" 60106070) OR AF-ID("Centre de Recherches en économie-écologique éco-innovation et ingénierie du Développement Soutenable" 60106206) OR AF-ID("Centre de Recherches Sociologiques sur le Droit et les Institutions Pénales" 60106097) OR AF-ID("Cohortes épidémiologiques en population" 60106188) OR AF-ID("Cultures Environnements, Arctique, Représentations, Climat" 60106069) OR AF-ID("Données et Algorithmes pour une Ville Intelligente et Durable" 60109215) OR AF-ID("Dynamiques Patrimoniales et Culturelles" 60106099) OR AF-ID("Fédération Conflits Vulnérabilités, Espaces" 60106104) OR AF-ID("Gamètes Implantation, Gestation" 60106302) OR AF-ID("Groupe d'Etude de la Matière Condensée CNRS-Université de Versailles" 60101347) OR AF-ID("Handicap Neuromusculaire : Physiopathologie Biothérapie et Pharmacologie Appliquées" 60106116) OR AF-ID("Infection et inflammation Chronique" 60106125) OR AF-ID("Institut Lavoisier de Versailles" 60106152) OR AF-ID("Laboratoire Atmosphères Milieux, Observations Spatiales" 60106194) OR AF-ID("Service d'Aéronomie" 60032611) OR AF-ID("Laboratoire des Sciences du Climat et de l'Environnement" 60045588) OR AF-ID("Laboratoire Anthropologie Archéologie, Biologie" 60172670) OR AF-ID("Laboratoire d'Étude de la Réponse Neuroendocrine au Sepsis" 60106308) OR AF-ID("Laboratoire d'Ingénierie des Systèmes de Versailles" 60106176) OR AF-ID("Laboratoire de Droit des Affaires et Nouvelles Technologies" 60106177) OR AF-ID("Laboratoire de Génétique et Biologie Cellulaire" 60106178) OR AF-ID("Laboratoire de Mathématiques de Versailles" 60106179) OR AF-ID("Laboratoire de Recherche en Management" 60106180) OR AF-ID("Laboratoire de recherche sur les mécanismes moléculaires et pharmacologiques de lobstruction bronchique" 60106181) OR AF-ID("Laboratoire de Recherches cliniques et en santé publique sur les handicaps psychiques cognitifs et moteurs" 60106205) OR AF-ID("Laboratoire d’informatique Parallélisme Réseaux Algorithmes Distribués" 60111070) OR AF-ID("Laboratoire Études Cliniques et Innovations Thérapeutiques en Psychiatrie" 60106309) OR AF-ID("Laboratoire Parallélisme Réseaux, Systèmes, Modélisation" 60106200) OR AF-ID("Laboratoire physiopathologie et diagnostic des infections microbiennes" 60106204) OR AF-ID("Laboratoire Professions Institutions, Temporalités" 60106150) OR AF-ID("Laboratoire Universitaire Santé-Environnement-Vieillissement" 60106301) OR AF-ID("Observatoire de Versailles Saint-Quentin-en-Yvelines" 60106237) OR AF-ID("Pharmacoépidémiologie et Maladies Infectieuses" 60106203) OR AF-ID("Physiopathologie et Pharmacologie Clinique de la Douleur" 60106202) OR AF-ID("Risques Cliniques et Sécurité en Santé des Femmes et en Santé Périnatale" 60106112) OR AF-ID("Vieillissement et Maladies Chroniques. Approches Épidémiologiques et de Santé Publique" 60106201) AND ( LIMIT-TO ( PUBYEAR,2018) )` 

limite 2k 

utilsation du filtre boolean openaccess pour faire des extractions de moins de 2k  (ex. `AND ( LIMIT-TO ( openaccess,0) )` )

<!--nota : Inclusion des publications directement affiliées à l'université et des publications des unités dont l'université est tutelle.-->
mémo : pour avoir la requête avec toutes des unités faire une recherche par affiliation de l'université puis sélectionner *whole instition*. Attention néanmoins : cela peut inclure, du fait des fédérations de recherche, des unités dont l'université n'est pas tutelle : penser à les retirer. 


**HAL**

`https://api.archives-ouvertes.fr/search?rows=10000&q=structId_i:81173&fq=publicationDateY_i:[2015%20TO%202019]&fq=( (docType_s:(ART OR COMM) AND popularLevel_s:0 AND peerReviewing_s:1) OR (docType_s:(OUV OR COUV OR DOUV) AND popularLevel_s:0) OR (docType_s:UNDEFINED)) &fl=doiId_s,%20title_s,%20halId_s &wt=csv`

UVSQ

ART ou COMM, si peer review et pas de vulgarisation

OUV ou COUV ou DOUV, si ce n'est pas de la vulgarisation

UNDEFINIED (inlusion des preprints !)


**PUBMED**

`(("université versailles"[Affiliation] OR "université de Versailles"[Affiliation] OR "universite Versailles"[Affiliation] OR UVSQ[Affiliation] OR "versailles university"[Affiliation] OR "university of versailles"[Affiliation])) AND (("2015"[Date - Publication] : "2019"[Date - Publication]))`


**lens.org**

`Filters: Year Published = ( 2015 - 2019  ) Institution Name = ( LM-Versailles  , Versailles Saint-Quentin-en-Yvelines University  , Institut Lavoisier de Versailles  , Universite de Versailles  , Université Versailles Saint-Quentin-en-Yvelines  , Université de Versailles Saint-Quentin-en-Yvelines  , Université de Versailles  , University of Versailles  , Université de Versailles Saint-Quentin  , Laboratoire de Mathématiques de Versailles  , Laboratoire d'Ingénierie des Systèmes de Versailles  Show less filters... )`

