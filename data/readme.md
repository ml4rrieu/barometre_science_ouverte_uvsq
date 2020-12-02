## Données à charger/actualiser dans ce dossier

* Les données bibliographiques de votre institution depuis les bases HAL, PUBMED, LENS etc. <br />

* le dump en `.csv` du barometre français de la science ouverte

https://data.enseignementsup-recherche.gouv.fr/explore/dataset/open-access-monitor-france/

* les issns des journaux suspects

https://github.com/ml4rrieu/open_science_tools/blob/main/questionnable_journals/suspiciousIssns.json



<br /><br />
## Données à charger/actualiser dans le dossier `APC_tracking` charger 

* le fichier openapc_dois.csv à récupérer en ligne

https://github.com/OpenAPC/openapc-de/blob/master/data/apc_de.csv

* doaj_apc_journals.csv

https://doaj.org/docs/public-data-dump/

`2020-11-30 utilisation du csv disponible sur doaj.org/csv`


* openapc_journals.csv

https://github.com/ml4rrieu/open_science_tools/blob/main/apc_journal_tables/openapc_journals.csv



<br /><br />
## Requêtes utilisées pour extraire les données des bases bibliographiques
**WOS**

`OG=(Universite de Versailles Saint-Quentin-En-Yvelines)
Timespan: 2015-2019. Indexes: SCI-EXPANDED, SSCI, A&HCI, CPCI-S, CPCI-SSH, ESCI, CCR-EXPANDED, IC. `

limit 5k


**SCOPUS**

`AF-ID ( "Universite de Versailles Saint-Quentin-en-Yvelines"   60029937 )  AND  ( LIMIT-TO ( PUBYEAR ,  YYYY ) ) `

limite 2k


**HAL**

`https://api.archives-ouvertes.fr/search?rows=10000&q=structId_i:81173&fq=publicationDateY_i:[2015%20TO%202019]&fq=( (docType_s:(ART OR COMM) AND popularLevel_s:0 AND peerReviewing_s:1) OR (docType_s:(OUV OR COUV OR DOUV) AND popularLevel_s:0) OR (docType_s:UNDEFINED))
&fl=doiId_s,%20title_s,%20halId_s 
&wt=csv`

UVSQ & 2015-19 
ART + COMM if peer reviewed and not popular level
OUV + COUV  + DOUV  if not popular level
+ UNDEFINIED


**PUBMED**

`(("université versailles"[Affiliation] OR "université de Versailles"[Affiliation] OR "universite Versailles"[Affiliation] OR UVSQ[Affiliation] OR "versailles university"[Affiliation] OR "university of versailles"[Affiliation])) AND (("2015"[Date - Publication] : "2019"[Date - Publication]))`


**lens.org**

`Filters: Year Published = ( 2015 - 2019  ) Institution Name = ( LM-Versailles  , Versailles Saint-Quentin-en-Yvelines University  , Institut Lavoisier de Versailles  , Universite de Versailles  , Université Versailles Saint-Quentin-en-Yvelines  , Université de Versailles Saint-Quentin-en-Yvelines  , Université de Versailles  , University of Versailles  , Université de Versailles Saint-Quentin  , Laboratoire de Mathématiques de Versailles  , Laboratoire d'Ingénierie des Systèmes de Versailles  Show less filters... )`

