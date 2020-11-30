## Ajouter à la racine

- vos extractions HAL, PUBMED, LENS etc. <br />
- le dump en csv du barometre français de la science ouverte <br />
https://data.enseignementsup-recherche.gouv.fr/explore/dataset/open-access-monitor-france/
- les issns des journaux suspects
--> donner lien

## dans APC_tracking
- openapc_dois.csv
https://github.com/OpenAPC/openapc-de/blob/master/data/apc_de.csv
- doaj_apc_journals.csv
https://doaj.org/docs/public-data-dump/
- openapc_journals.csv



## Requêtes pour l'UVSQ
**WOS**

`OG=(Universite de Versailles Saint-Quentin-En-Yvelines)
Timespan: 2015-2019. Indexes: SCI-EXPANDED, SSCI, A&HCI, CPCI-S, CPCI-SSH, ESCI, CCR-EXPANDED, IC. `

limit 5k
2020-11-06

**SCOPUS**

`AF-ID ( "Universite de Versailles Saint-Quentin-en-Yvelines"   60029937 )  AND  ( LIMIT-TO ( PUBYEAR ,  2019 ) ) `
limite 2k

2020-11-06

**HAL**

UVSQ & 2015-19 & ART COMM OUV COUV  PREPRINT
`https://api.archives-ouvertes.fr/search?rows=10000&q=structId_i:81173&fq=publicationDateY_i:[2015%20TO%202019]&fq=docType_s:(ART OR COMM OR OUV OR DOUV OR COUV OR UNDEFINED )&fl=doiId_s,%20title_s,%20halId_s`
`&wt=csv`
&fq=docType_s

2020-11-06

on ne filtre pas sur popularLevel_s et peerReviewing_s car ces métadonnées ne sont pas dispo sur les preprint

**PUBMED**

`(("université versailles"[Affiliation] OR "université de Versailles"[Affiliation] OR "universite Versailles"[Affiliation] OR UVSQ[Affiliation] OR "versailles university"[Affiliation] OR "university of versailles"[Affiliation])) AND (("2015"[Date - Publication] : "2019"[Date - Publication]))`

**lens.org**

`Filters: Year Published = ( 2015 - 2019  ) Institution Name = ( LM-Versailles  , Versailles Saint-Quentin-en-Yvelines University  , Institut Lavoisier de Versailles  , Universite de Versailles  , Université Versailles Saint-Quentin-en-Yvelines  , Université de Versailles Saint-Quentin-en-Yvelines  , Université de Versailles  , University of Versailles  , Université de Versailles Saint-Quentin  , Laboratoire de Mathématiques de Versailles  , Laboratoire d'Ingénierie des Systèmes de Versailles  Show less filters... )`

2020-11-06