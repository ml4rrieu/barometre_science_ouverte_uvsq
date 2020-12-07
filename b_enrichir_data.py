import requests, json, pandas as pd
"""
Pour toutes les publications idenitifiées à l'étape précédente récupérer et ajouter les métadonnées

Etapes
	______0______ Charger les données
	______1______ Ajouter les principales métadonnées : HAL, unpaywall et détection des APC
	______2______ Ajouter métadonnées de domaine et déduire le statut d'accès ouvert
	______3______ Effectuer les alignements entre HAL et Crossref
	______4______ Complétion des cellules vides pour la couverture des bases

fichiers chargés
	./data/uvsq_dois_halId_2015_19.csv : les identifiants des publications de l'université
	./data/apc_tracking/openapc_dois.csv : les DOI des documents dans openapc
	./data/apc_tracking/openapc_journals.csv : les journaux dans openapc avec pour chaque années le prix moyen payé
	./data/apc_tracking/doaj_apc_journals.csv : le dump du DOAJ
	./data/suspiciousIssns.json : une liste de journaux suspects extraite de https://github.com/stop-predatory-journals/stop-predatory-journals.github.io
	./data/match_referentials.json : correspondance entre les référentiels HAL type de document et domaine, vers ceux respectivement de crossref et du barometre fr science ouverte 
	./data/open-access-monitor-france.csv : le dump du barometre fr science ovuerte 
	
fichers produits
	./data/out_uvsq_publications_2015_19__avant_alignement.csv : export des données avant d'effectuer les aligments HAL-Unpaywall-BSO 
	./data/out_uvsq_publications_2015_19.csv : ficher finalisé 
"""

def req_to_json(url):
	"""S'assuer que la réponse de l'API est en JSON"""
	found = False
	while not found : 
		req = requests.get(url)
		try : 
			res = req.json()
			found = True
		except : 
			pass
	return res

def get_hal_data(doi, halId):
	""" Récupérer les métadonnées de HAL.
	Si le DOI est présent dans unpaywall les métadonnées de HAL communes seront écrasées """
	
	if doi and not halId : 
		query = "doiId_s:"+str(doi)
	if not doi and halId : 
		query = "halId_s:"+str(halId)
	if doi and halId : 
		query = f"(doiId_s:{str(doi)} OR halId_s:{str(halId)})"
		
	res = req_to_json("https://api.archives-ouvertes.fr/search/?q="+ query+\
		"&fl=halId_s,title_s,authFullName_s,publicationDate_s,publicationDateY_i,docType_s,journalTitle_s,journalIssn_s,"\
		"journalEissn_s,journalPublisher_s,domain_s,submittedDate_s,submitType_s,linkExtId_s,license_s,selfArchiving_bool"
		)

	# Si l'API renvoi une erreur ou bien si aucun document n'est trouvé
	if res.get("error") or res['response']['numFound'] == 0 : 
		return {
		'hal_coverage':'missing'
		}

	res = res['response']['docs'][0]
	#print(json.dumps(res, indent = 2))

	#déduire le champs hal_location
	if res['submitType_s'] == 'file' : 
		hal_location = 'file' #on favorise les fichiers des HAL sur arxiv et pubmedcentral
	elif res['submitType_s'] == 'notice' and (res.get('linkExtId_s') == 'arxiv'  or res.get('linkExtId_s') == 'pubmedcentral') : 
		hal_location = res['linkExtId_s']
	else : 
		hal_location = 'notice'

	#déduire les ISSNs
	issn = [ res.get("journalIssn_s"), res.get("journalEissn_s")]
	issn = [item for item in issn if item]
	issn = ";".join(issn) if issn else False

	# Vérifier la présence de domaine disciplinaire (qq notices peuvent ne pas avoir de domaine)
	domain = False
	if res.get('domain_s') : 
		domain = res["domain_s"][0]
	if not domain : 
		print("pb domain in hal", res.get("halId_s"))

	return{
	#métadonnées partagées avec unpaywall
	'title': res['title_s'][0],
	'author_count': len(res['authFullName_s']),
	'published_date': res.get('publicationDate_s'),
	'published_year': res.get('publicationDateY_i'),
	'journal_name': res.get('journalTitle_s'),
	'journal_issns': issn,
	'publisher': res.get('journalPublisher_s'),
	#métadonnées propre à HAL
	'halId': res.get('halId_s'),
	'hal_coverage' : 'in',
	'hal_submittedDate' : res.get('submittedDate_s'),
	'hal_location' : hal_location, 
	'hal_licence': res.get('license_s'),
	'hal_serlArchiving' : res.get("selfArchiving_bool"),
	'hal_docType': res.get('docType_s'),
	'hal_domain': domain,
	}
	


def get_upw_data(doi):
	"""Récupérer les métadonnées de Unpaywall """
	
	res = req_to_json(f"https://api.unpaywall.org/v2/{doi}?email=m@larri.eu")
	
	# déduire upw_coverage
	if res.get("message") and "isn't in Unpaywall" in res.get("message") : 
		upw_coverage = "missing"
	elif res.get("is_oa") :
		upw_coverage = "oa"
	else : 
		upw_coverage = "closed"

	# facultif : déduire nombre auteurs 
	author_count = len(res['z_authors']) if res.get('z_authors') else False

	#déduire upw_location
	location = licence = version = None
	if res.get('oa_locations') : 

		oa_loc = res.get('oa_locations')
		location = list(set(
			[loc["host_type"] for loc in oa_loc]))
		location = ";".join(location)
		
		licence = list(set(
			[loc["license"] for loc in oa_loc if loc["license"] ]))
		licence = ";".join(licence) if licence else None
		
		version = list(set(
			[loc["version"] for loc in oa_loc if loc["version"] ]))
		version = ";".join(version) if version else None

	return {
	#métadonnées partagées avec HAL
	"title": res.get("title"), 
	"author_count": author_count,
	"published_date": res.get("published_date"),
	"published_year": res.get("year"),
	"journal_name": res.get("journal_name"),
	"journal_issns": res.get("journal_issns"),
	"publisher": res.get("publisher"),
	# métadonnées propre à unpaywall
	"genre": res.get("genre"),
	"journal_is_in_doaj": res.get("journal_is_in_doaj"),
	"upw_coverage": upw_coverage,
	"is_paratext": res.get("is_paratext"),
	"journal_issn_l": res.get("journal_issn_l"),
	"journal_is_oa": res.get("journal_is_oa"),
	"oa_status" : res.get("oa_status"),
	"upw_location": location, 
	"licence": licence, 
	"version": version
	}


def track_apc(doi, md) :
	"""Récupérer des informations sur les APC""" 
	
	#__a Vérifier si le DOI est dans openapc
	if doi and openapc_dois["doi"].str.contains(doi, regex = False).any() :
		try : 
			apc_amount = openapc_dois.loc[ openapc_dois["doi"] == doi, "apc_amount_euros"].item()
		except : 
			apc_amount = "unknow"
		return{
		"apc_tracking" : "doi_in_openapc",
		"apc_amount" :  apc_amount,
		"apc_currency" : "EUR"
		}

	# Si le document n'a pas d'ISSN ne rien remplir
	if not md.get("journal_issns") : 
		return {}
	
	issns = md["journal_issns"].split(";")

	#__b si l'ISSN est dans openapc et que des APC ont été payés la même années
	cols = ["issn", "issn_print", "issn_electronic"]
	openapc_mean = False
	if md.get("published_year") and int(md["published_year"]) > 2014 : 
		for item in issns : 
			for col in cols : 
				if openapc_journals[col].str.contains(item).any() :
					openapc_mean = openapc_journals.loc[ openapc_journals[col] == item, str(md["published_year"])].item()
					break

	if openapc_mean :
		return{
		"apc_tracking" : "journal_in_openapc",
		"apc_amount" :  openapc_mean,
		"apc_currency" : "EUR"
		}


	#__c si le type d'accès ouvert du document dans unpaywall est hybride
	if md.get("oa_status") == "hybrid": 
		return { "apc_tracking" : "journal_is_hybrid"}

	
	#__d si le journal est dans le DOAJ extraire les données d' APC du DOAJ
	cols = ["Journal ISSN (print version)",	"Journal EISSN (online version)"] 
	for item in issns : 
		for col in cols : 
			if doaj_apc_journals[col].str.contains(item).any() : 
				return {
				"apc_tracking" : "apc_journals_in_doaj",
				"apc_amount" :  doaj_apc_journals.loc[ doaj_apc_journals[col] == item, "APC amount" ].item(),
				"apc_currency" : doaj_apc_journals.loc[ doaj_apc_journals[col] == item, "Currency" ].item()
				}
	#__si aucun cas ne s'est présenté ne rien remplir
	return {}


def check_suspicious_j(md) :
	"""Vérifier si le journal est dans la liste de ceux suspects"""
	if not md.get("journal_issns") :
		return {}

	is_suspicious = False
	issns = md["journal_issns"].split(";")
	for item in issns : 
		if item in suspiciousIssns["print"] or item in suspiciousIssns["electronic"] : 
			is_suspicious = True
	
	return {"suspicious_journal" : is_suspicious }

	

def enrich_df(df, count):
	"""pour chaque document lancer les requêtes et ajouter les métadonnées"""

	nb = 0 
	for row in df.itertuples():
		# % de progression
		if row.Index > 0 and row.Index % 10 == 0 : 
			print( round(row.Index/ len(df.index) * 100), "%")
		
		#print(row.doi, row.halId) 
			
		# __a récupérer les métadonnées de HAL
		md = get_hal_data(row.doi, row.halId)
	
		# __b si le doc a un DOI récupérer les données de unpaywall 
		# (Les métadonnées de HAL commune avec unpaywall seront écrasées)
		if row.doi  : 
			add = get_upw_data(row.doi)
			# ajout des métadonnées qui ne sont pas False
			md.update( (k, v) for k, v in add.items() if v ) 

		# __c chercher la présence d'APC
		md.update(track_apc(row.doi, md))

		# __d vérifier si le journal est dans la liste des journaux suspects
		md.update(check_suspicious_j(md)) 

		#__e ajouter les métadonnées au document
		for field in md : 
			df.loc[row.Index, field] = md[field]

		
		nb+=1
		if nb  > count : break

	return df



# ______0______ Charger les données
openapc_dois = pd.read_csv("./data/apc_tracking/openapc_dois.csv", na_filter= False)
openapc_journals = pd.read_csv("./data/apc_tracking/openapc_journals.csv", na_filter= False)
doaj_apc_journals = pd.read_csv("./data/apc_tracking/doaj_apc_journals.csv", na_filter= False)
fhjson = open('./data/suspiciousIssns.json') 
suspiciousIssns = json.load(fhjson)

#df = pd.read_csv("./data/test__alone.csv", converters={'doi' : str}, na_filter= False, encoding='utf8')
df = pd.read_csv("./data/uvsq_dois_halId_2015_19.csv", converters={'doi' : str}, na_filter= False, encoding='utf8')



# ______1______ Ajouter les principales métadonnées : HAL, unpaywall et détection des APC
print("nb of publis to treat", len(df))
#en 2e argument préciser le nb de publication
df = enrich_df(df, 18000) 



# ______2______ Ajouter métadonnées de domaine et déduire le statut d'accès ouvert
# add scientific field from bso Lorrain
scifield = pd.read_csv("./data/open-access-monitor-france.csv", usecols= ["doi", "scientific_field"],  sep=";", )
df = pd.merge(df, scifield, how= "left", on = "doi")
df['scientific_field'].fillna('unknown', inplace = True) 

# déduire is_oa
def deduce_oa(row) : 
	if row["hal_location"] == "file" or \
	row["hal_location"] == "arxiv" or \
	row["hal_location"] == "pubmedcentral" or \
	row["upw_coverage"] == "oa" : 
		return True
	else : 
		return False
df["is_oa"] = df.apply(lambda row : deduce_oa(row) , axis = 1)

# déduire oa_type
def deduce_oa_type(row) : 
	loc = []
	if pd.notna( row["upw_location"] ) : 
		loc.extend( row["upw_location"].split(";") )

	# si unpaywall n'a pas trouvé de "repository" mais que c'est bien le cas dans HAL alors l'ajouter
	if "repository" not in loc and\
	(row["hal_location"] == "file" or
	row["hal_location"] == "arxiv" or 
	row["hal_location"] == "pubmedcentral") : 
			loc.append(0, "repository")

	return ";".join(loc) if loc else "closed"

df["oa_type"] = df.apply(lambda row : deduce_oa_type(row) , axis = 1)

#un export avant les alignements
df.to_csv("./data/out/uvsq_publications_2015_19__avant_alignement.csv", index = False)



# ______3______ Effectuer les alignements entre HAL et BSO
# Aligner les types de documents
def align_doctype(row) : 
	if pd.notna(row["genre"]) : 
		return row["genre"]
	# si pas de genre chez unpaywall mais présence chez HAL
	if pd.isna(row["genre"]) and pd.notna(row["hal_docType"]) : 
		if row["hal_docType"] in match_ref["docType"] : 
			return match_ref["docType"][row["hal_docType"]] 
		else : print("cannot align doctype", row["halId"])

match_ref = json.load(open("./data/match_referentials.json"))		
df["genre"] = df.apply(lambda row : align_doctype(row) , axis = 1)


# Aligner les domaines scientifiques
def align_domain(row):
	if row["scientific_field"] == "unknown" and pd.notna(row["hal_domain"]) :
		if row["hal_domain"] in match_ref["domain"] : 
			return match_ref["domain"][row["hal_domain"]]
		else : 
			print("cannot align domain", row["halId"])

	else : 
		return row["scientific_field"]

df["scientific_field"] = df.apply(lambda row : align_domain(row), axis = 1)



# ______4______ Complétion des cellules vides pour la couverture des bases
df['hal_coverage'].fillna('missing', inplace = True) 
df['upw_coverage'].fillna('missing', inplace = True) 


# Exporter les données
df.to_csv("./data/out/uvsq_publications_2015_19.csv", index = False)