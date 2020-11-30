# Baromètre de la science ouverte de l'UVSQ
En construction -- 2020-12-01<br />

<br /><br />

<!--repris et adaptaté

<br /><br />
### Table des matières
* [Intégrer les publications de HAL sans DOI](#intégrer-les-publications-de-HAL-sans-DOI) <br/>
* [Pister les APC](#pister-les-APC) <br/>
* [Schéma de données](#Schéma-de-données) <br/>



### Présentation -->
le Baromètre de la science ouverte de l'UVSQ reprend celui de l'université de Lorraine (mars 2020), [partagé sur gitlab]( https://gitlab.com/Cthulhus_Queen/barometre_scienceouverte_universitedelorraine/-/blob/master/barometre_universite_lorraine.ipynb) et réalisé par [@BraccoLaetitia](https://twitter.com/BraccoLaetitia), (merci !). Deux "modules" ont été ajoutés : le premier permet d'intégrer les publications venant de HAL ne possédant pas de DOI et le second apporte des informations sur les frais de publication (APC : Article Processing Charges)

### Intégrer les publications de HAL sans DOI
Les publications sans DOI dans HAL ont été intégrées. Cela impact la détection de l'accès ouvert et demande un alignement des référentiels des types de document et des domaines disciplinaires.

**Détection de l'accès ouvert**

Une publication dans HAL sans DOI est considérée en accès ouvert si l'une conditions suivante est remplie
- la métadonnée `submitType_s` contient `file`
- la métadonnées `linkExtId_s` contient `arxiv` ou `pubmemdcentral`

**Alignement des référentiels**

Deux dictionnaires ont été réalisés afin d'aligner les types de document de HAL avec ceux de Crossref et les domaines disciplinaires de HAL avec ceux du baromètre français de la science ovuerte.
voir `data/match_referentials.json`
<br />

### Pister les APC
Le but est d'obtenir des informations sur d'éventuels APC (Article Processing Charges) afin d'alimenter [openapc](https://github.com/OpenAPC/). <br /> En considérant au moins les "accords transformants" (publish & read) ; les changements possibles des modèles économique des revues et enfin les possibles éxonérations (*waivers*) il reste difficle de répondre à cette question. Les informations sont donc données à titre indicatif.


L'algorithme réalisé est fait de quatre étapes : 

+ Le DOI est-il dans [openapc](https://github.com/OpenAPC/openapc-de) ? 
    + oui, renseigner `doi_in_openapc` et extraire le montant payé
	+ non, la revue (ISSN) est-elle dans openapc et des frais de publications ont-ils été payés _la même année_ ?
	
	    + oui, renseigner `journal_in_openapc`  et extraire le prix moyen sur l'année
		
		+ non, le document est-il en open access sur le site de l'éditeur chez une revue hybride ? (utilisation du champs `oa_status` de unpaywall)
			+ oui, renseigner `journal_is_hybrid`
			+ non, la revue (ISSN) est elle dans le [DOAJ](https://doaj.org/) et des informations sont elles présente ?
				+ oui, retourner `apc_journals_in_doaj` , le prix et la devise
<br />

### Schéma de données
**en cours ...**
| column             | description (if needed)                                                                       | source                   |
|--------------------|-----------------------------------------------------------------------------------------------|--------------------------|
| doi                |                                                                                               |                          |
| halId              | Publication deposit id in HAL                                                                 | hal                      |
| hal_coverage       | Hal coverage (in or missing )                                                                 | hal                      |
| title              |                                                                                               | hal or unpaywall         |
| genre              | Document type                                                                                 | hal or unpaywall         |
| author_count       | Curiosity : number of authors                                                                 | hal or unpaywall         |
| published_date     |                                                                                               | hal or unpaywall         |
| published_year     |                                                                                               | hal or unpaywall         |
| journal_name       |                                                                                               | hal or unpaywall         |
| journal_issns      |                                                                                               | hal or unpaywall         |
| publisher          |                                                                                               | hal or unpaywall         |
| upw_coverage       | Unpaywall coverage (oa, missing, closed)                                                      | unpaywall                |
| oa_status          | Status/type of open access (green, gold, hybrid, bronze)                                      | unpaywall                |
| upw_location       | Where OA is founded (repository and/or publisher)                                             | unpaywall                |
| version            | Publication version available (submitted, accepted, published)                                | unpaywall                |
| suspicious_journal | Is the journal in "predatory" list                                                            | [Stop Predatory Journals](https://github.com/stop-predatory-journals/stop-predatory-journals.github.io)|
| hal_submittedDate  | When the publication has been submitted in HAL                                                | hal                      |
| hal_location       | Where OA is founded (file, arxiv, pubmedcentral)                                              | hal                      |
| hal_licence        | Licence in HAL deposit                                                                        | hal                      |
| hal_serlArchiving  | Curiosity : is the deposit made by the author                                                 | hal                      |
| hal_docType        | Type of document                                                                              | hal                      |
| hal_domain         | Domain, scientific field from hal                                                             | hal                      |
| licence            | licence finded in unpaywall                                                                   | unpaywall                |
| apc_tracking       | APC information (doi_in_openapc, journal_in_openapc, journal_is_hybrid, apc_journals_in_doaj) | openapc, doaj, unpaywall |
| journal_is_in_doaj | Is this resource published in a DOAJ-indexed journal                                          | unpaywall                |
| journal_is_oa      | Is this resource published in a completely OA journal                                         | unpaywall                |
| is_paratext        | Is the item an ancillary part of a journal (column disappear if everything is False )         | unpaywall                |
| apc_amount         | Rough approximation of APC cost                                                               | openapc, doaj            |
| apc_currency       |                                                                                               | openapc, doaj            |
| scientific_field   | Scientific field from barometre-science-ouverte and hal                                       | barometre-so, hal        |
| is_oa              | Is there an OA copy of this ressource                                                         | hal, unpaywall           |
| oa_type            | Publisher and/repository                                                                      | hal, unpaywall           |



### Voir aussi
  * le baromètre français de la science ouverte https://ministeresuprecherche.github.io/bso/
  * sur les évolutions des APC chez qq grands éditeurs https://github.com/lmatthia/publisher-oa-portfolios/blob/master/README.md
  


