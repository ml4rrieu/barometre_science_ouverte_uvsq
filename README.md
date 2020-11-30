# Baromètre de la science ouverte de l'UVSQ
En construction <br />
Maxence Larrieu -- 2020-11-30<br />


<br /><br /><br />

Reprise du code du baromètre de la science ouverte de l'Université de Lorraine afin de réaliser celui de l'UVSQ. Code original [partagé sur gitlab]( https://gitlab.com/Cthulhus_Queen/barometre_scienceouverte_universitedelorraine/-/blob/master/barometre_universite_lorraine.ipynb) par [@BraccoLaetitia](https://twitter.com/BraccoLaetitia) , merci ! 

### Table of Contents
* [Intégrer les publications de HAL sans DOI](#intégrer-les-publications-de-HAL-sans-DOI) <br/>
* [Pister les APC](#pister-les-APC) <br/>
* [Métadonnées extraites]() <br/>
* [Journaux suspects](#journaux-suspects) <br/>


### Intégrer les publications de HAL sans DOI
Les publications sans DOI dans HAL ont été intégrées. Cela impact la détection de l'accès ouvert et demande un alignement des référentiels des types de document et des domaines disciplinaires.
**Détection de l'accès ouvert **
Une publication de HAL sans DOI est considérée en accès ouvert si l'une des deux conditions est remplies
- la métadonnée `submitType_s` contient `file`
- la métadonnées `linkExtId_s` contient `arxiv` ou `pubmemdcentral`

**Alignement des référentiels**
Deux dictionnaires ont été réalisés afin d'aligner les types de document de HAL avec ceux de Crossref et les domaines disciplinaires de HAL avec ceux du baromètre français de la science ovuerte.
voir `data/match_referentials.json`

### Pister les APC
Le but est de savoir si la publication a nécessitée des APC( Article Processing Charges). <br/ > A moins que la publication soit référencée dans openapc, il n'est  pas possible de répondre avec certitude à cette question. Du fait des accords transformants un article peut en effet être publié dans une revue qui nécessite des APC sans que les auteurs en ait payé -- accord "publish & read" entre l'institution et l'éditeur. De plus, une revue peut changer de modèle économique ce qui limite la détection des APCs. Les informations recueillies sont donc données à titre indicatif.


L'algorithme réalisé à quatre étapes : 

+ Le DOI est-il dans [openapc](https://github.com/OpenAPC/openapc-de) ? 
    + oui, renseigner `doi_in_openapc` et extraire le prix
	+ non, la revue (ISSN) est-elle dans openapc et des frais de publications ont ils été payés _la même années_ ?
	
	    + oui, renseigner `journal_in_openapc`  et extraire le prix moyen sur l'année
		
		+ non, le document est-il en open access sur le site de l'éditeur chez une revue hybride ? (utilisation du champs `oa_status` de unpaywall)
			+ oui, renseigner `journal_is_hybrid`
			+ non, la revue (ISSN) est elle dans le [DOAJ](https://doaj.org/) et des informations sont elles présente ?
				+ oui, retourner `apc_journals_in_doaj` , le prix et la devise
	


### Journaux suspects

La liste [Stop Predatory Journals](https://github.com/stop-predatory-journals/stop-predatory-journals.github.io) a été utilisée. Informations à prendre avec circonspection.


 ### Nota 
  * sur les évolutions des APC voi aussi https://github.com/lmatthia/publisher-oa-portfolios/blob/master/README.md


