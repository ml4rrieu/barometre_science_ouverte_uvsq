# Baromètre de la science ouverte de l'UVSQ
En construction -- 2020-12-01<br />

<br /><br />

Reprise du code du baromètre de la science ouverte de l'Université de Lorraine afin de réaliser celui de l'UVSQ. Code original [partagé sur gitlab]( https://gitlab.com/Cthulhus_Queen/barometre_scienceouverte_universitedelorraine/-/blob/master/barometre_universite_lorraine.ipynb) par [@BraccoLaetitia](https://twitter.com/BraccoLaetitia) , merci ! 

<br /><br />

### Table des matières
* [Intégrer les publications de HAL sans DOI](#intégrer-les-publications-de-HAL-sans-DOI) <br/>
* [Pister les APC](#pister-les-APC) <br/>
* [Schéma de données](#Schéma-de-données) <br/>



### Intégrer les publications de HAL sans DOI
Les publications sans DOI dans HAL ont été intégrées. Cela impact la détection de l'accès ouvert et demande un alignement des référentiels des types de document et des domaines disciplinaires.

**Détection de l'accès ouvert **
Une publication dans HAL sans DOI est considérée en accès ouvert si l'une conditions suivante est remplie
- la métadonnée `submitType_s` contient `file`
- la métadonnées `linkExtId_s` contient `arxiv` ou `pubmemdcentral`

**Alignement des référentiels**
Deux dictionnaires ont été réalisés afin d'aligner les types de document de HAL avec ceux de Crossref et les domaines disciplinaires de HAL avec ceux du baromètre français de la science ovuerte.
voir `data/match_referentials.json`


### Pister les APC
Le but est de savoir si la publication a nécessitée des APC( Article Processing Charges). <br /> Du fait des accords transformants (publish & read), des changements possibles de modèle économique chez les revues et enfin des éventuels éxonérations (*waivers*) il n'est pas possible de répondre avec certitude à cette question. Les informations sont donc données à titre indicatif. Ces informations peuvent ensuite servir à pister les APC dans le cadre du projet openapc.


L'algorithme réalisé est fait de quatre étapes : 

+ Le DOI est-il dans [openapc](https://github.com/OpenAPC/openapc-de) ? 
    + oui, renseigner `doi_in_openapc` et extraire le montant payé
	+ non, la revue (ISSN) est-elle dans openapc et des frais de publications ont-ils été payés _la même année_ ?
	
	    + oui, renseigner `journal_in_openapc`  et extraire le prix moyen sur l'année
		
		+ non, le document est-il en open access sur le site de l'éditeur chez une revue hybride ? (utilisation du champs `oa_status` de unpaywall)
			+ oui, renseigner `journal_is_hybrid`
			+ non, la revue (ISSN) est elle dans le [DOAJ](https://doaj.org/) et des informations sont elles présente ?
				+ oui, retourner `apc_journals_in_doaj` , le prix et la devise
	

### Schéma de données
**en cours de réalisation**
| column             | description                                                                                   | source                   |
|--------------------|-----------------------------------------------------------------------------------------------|--------------------------|
| doi                |                                                                                               |                          |
| halId              | publication deposit id in HAL                                                                 | hal                      |
| hal_coverage       | hal coverage : in or missing                                                                  | hal                      |
| title              |                                                                                               | hal or unpaywall         |
| genre              | document type                                                                                 | hal or unpaywall         |
| author_count       | number of authors for curiosity                                                               | hal or unpaywall         |
| published_date     | date of publication                                                                           | hal or unpaywall         |
| published_year     | year of publication                                                                           | hal or unpaywall         |
| journal_name       |                                                                                               | hal or unpaywall         |
| journal_issns      |                                                                                               | hal or unpaywall         |
| publisher          |                                                                                               | hal or unpaywall         |
| upw_coverage       | unpaywall coverage (oa, missing, closed)                                                      | unpaywall                |
| oa_status          | status/type of open access (green, gold, hybrid, bronz)                                       | unpaywall                |
| upw_location       | where OA is founded (repository and/or publisher)                                             | unpaywall                |
| version            | publication version available (submitted, accepted, published)                                | unpaywall                |
| suspicious_journal | is the journal in "predatory" list                                                            | [Stop Predatory Journals](https://github.com/stop-predatory-journals/stop-predatory-journals.github.io)|
| hal_submittedDate  | when the publication has been submitted in HAL                                                | hal                      |
| hal_location       | where OA is founded (file, arxiv, pubmedcentral)                                              | hal                      |
| hal_licence        | licence in HAL deposit                                                                        | hal                      |
| hal_serlArchiving  | curiosity : is the deposit made by the author ?                                               | hal                      |
| hal_docType        | type of document                                                                              | hal                      |
| hal_domain         | domain / discipline                                                                           | hal                      |
| licence            | licence finded in unpaywall                                                                   | unpaywall                |
| apc_tracking       | APC information (doi_in_openapc, journal_in_openapc, journal_is_hybrid, apc_journals_in_doaj) | openapc, doaj, unpaywall |
| journal_is_in_doaj | does the journal inside doaj ?                                                                | unpaywall                |
| apc_amount         | rough approximation of APC cost                                                               | openapc, doaj            |
| apc_currency       |                                                                                               | openapc, doaj            |
| journal_is_oa      | is it an open access journal ?                                                                | unpaywall                |
| scientific_field   | scientific field from barometre-science-ouverte and hal                                       | barometre-so, hal        |
| is_oa              | is there an OA copy of this ressource                                                         | hal, unpaywall           |
| oa_type            | publisher and/repository                                                                      | hal, unpaywall           |



### Voir aussi
  * le baromètre français de la science ouverte https://ministeresuprecherche.github.io/bso/
  * sur les évolutions des APC chez qq grands éditeurs https://github.com/lmatthia/publisher-oa-portfolios/blob/master/README.md
  


