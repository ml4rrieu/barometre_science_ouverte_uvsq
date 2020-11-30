# Baromètre de la science ouverte de l'UVSQ
En construction <br />

<br /><br />

Reprise du code du baromètre de la science ouverte de l'Université de Lorraine afin de réaliser celui de l'UVSQ. Code original [partagé sur gitlab]( https://gitlab.com/Cthulhus_Queen/barometre_scienceouverte_universitedelorraine/-/blob/master/barometre_universite_lorraine.ipynb) par [@BraccoLaetitia](https://twitter.com/BraccoLaetitia) , merci ! 

<br /><br />

### Table des matières
* [Intégrer les publications de HAL sans DOI](#intégrer-les-publications-de-HAL-sans-DOI) <br/>
* [Pister les APC](#pister-les-APC) <br/>
* [Métadonnées extraites]() <br/>
* [Journaux suspects](#journaux-suspects) <br/>


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
    + oui, renseigner `doi_in_openapc` et extraire le prix
	+ non, la revue (ISSN) est-elle dans openapc et des frais de publications ont ils été payés _la même années_ ?
	
	    + oui, renseigner `journal_in_openapc`  et extraire le prix moyen sur l'année
		
		+ non, le document est-il en open access sur le site de l'éditeur chez une revue hybride ? (utilisation du champs `oa_status` de unpaywall)
			+ oui, renseigner `journal_is_hybrid`
			+ non, la revue (ISSN) est elle dans le [DOAJ](https://doaj.org/) et des informations sont elles présente ?
				+ oui, retourner `apc_journals_in_doaj` , le prix et la devise
	



### Journaux suspects

La liste [Stop Predatory Journals](https://github.com/stop-predatory-journals/stop-predatory-journals.github.io) a été utilisée. Informations à prendre avec circonspection.


### Voir aussi
  * le baromètre français de la science ouverte https://ministeresuprecherche.github.io/bso/
  * sur les évolutions des APC chez qq grands éditeurs https://github.com/lmatthia/publisher-oa-portfolios/blob/master/README.md
  


