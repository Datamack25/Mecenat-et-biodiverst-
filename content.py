"""Contenus : territoires, encyclopédie (suite), lectures, emplois, réglementation, DPEF."""
import csv
GEO = {
"Guadeloupe": "Les Abymes;Anse-Bertrand;Baie-Mahault;Baillif;Basse-Terre;Bouillante;Capesterre-Belle-Eau;Capesterre-de-Marie-Galante;Deshaies;La Désirade;Le Gosier;Gourbeyre;Goyave;Grand-Bourg;Lamentin;Morne-à-l'Eau;Le Moule;Petit-Bourg;Petit-Canal;Pointe-à-Pitre;Pointe-Noire;Port-Louis;Saint-Claude;Saint-François;Saint-Louis;Sainte-Anne;Sainte-Rose;Terre-de-Bas;Terre-de-Haut;Trois-Rivières;Vieux-Fort;Vieux-Habitants",
"Martinique": "Ajoupa-Bouillon;Les Anses-d'Arlet;Basse-Pointe;Bellefontaine;Le Carbet;Case-Pilote;Le Diamant;Ducos;Fonds-Saint-Denis;Fort-de-France;Le François;Grand'Rivière;Gros-Morne;Le Lamentin;Le Lorrain;Macouba;Le Marigot;Le Marin;Morne-Rouge;Le Morne-Vert;Le Prêcheur;Rivière-Pilote;Rivière-Salée;Le Robert;Saint-Esprit;Saint-Joseph;Saint-Pierre;Sainte-Anne;Sainte-Luce;Sainte-Marie;Schœlcher;La Trinité;Les Trois-Îlets;Le Vauclin",
"Mayotte": "Acoua;Bandraboua;Bandrélé;Bouéni;Chiconi;Chirongui;Dembéni;Dzaoudzi;Kani-Kéli;Koungou;Mamoudzou;Mtsamboro;M'Tsangamouji;Ouangani;Pamandzi;Sada;Tsingoni",
"La Réunion": "Les Avirons;Bras-Panon;Cilaos;Entre-Deux;L'Étang-Salé;Petite-Île;La Plaine-des-Palmistes;Le Port;La Possession;Saint-André;Saint-Benoît;Saint-Denis;Saint-Joseph;Saint-Leu;Saint-Louis;Saint-Paul;Saint-Philippe;Saint-Pierre;Sainte-Marie;Sainte-Rose;Sainte-Suzanne;Salazie;Le Tampon;Les Trois-Bassins",
"Guyane": "Apatou;Awala-Yalimapo;Camopi;Cayenne;Grand-Santi;Iracoubo;Kourou;Macouria;Mana;Maripasoula;Matoury;Montsinéry-Tonnegrande;Ouanary;Papaïchton;Régina;Rémire-Montjoly;Roura;Saint-Élie;Saint-Georges;Saint-Laurent-du-Maroni;Saül;Sinnamary"}
PREF = {"Guadeloupe|Basse-Terre": "Préfecture", "Guadeloupe|Pointe-à-Pitre": "Sous-préfecture", "Martinique|Fort-de-France": "Préfecture",
 "Martinique|La Trinité": "Sous-préfecture", "Martinique|Le Marin": "Sous-préfecture", "Martinique|Saint-Pierre": "Sous-préfecture",
 "Mayotte|Mamoudzou": "Préfecture", "La Réunion|Saint-Denis": "Préfecture", "La Réunion|Saint-Benoît": "Sous-préfecture",
 "La Réunion|Saint-Paul": "Sous-préfecture", "La Réunion|Saint-Pierre": "Sous-préfecture", "Guyane|Cayenne": "Préfecture", "Guyane|Saint-Laurent-du-Maroni": "Sous-préfecture"}
def geo_rows():
    return [[t, c, "Commune", PREF.get(f"{t}|{c}", "")] for t, s in GEO.items() for c in s.split(";")]

ENC_NEW = [
("Endémisme", "Espèces", "Caractère d'une espèce qui n'existe naturellement que dans une zone géographique précise, comme une île ou un massif. Les espèces endémiques sont très vulnérables, car leur disparition locale équivaut à une extinction mondiale.", "Le tuit-tuit de La Réunion, oiseau présent uniquement sur l'île"),
("Trame verte et bleue", "Protection", "Réseau de réservoirs de biodiversité et de corridors écologiques, terrestres (verts) et aquatiques (bleus), qui permet aux espèces de se déplacer, de se nourrir et de se reproduire. Elle est intégrée aux documents d'aménagement du territoire.", "Préserver une ripisylve pour relier deux zones humides"),
("Blanchissement corallien", "Menaces", "Phénomène par lequel les coraux, stressés par une eau trop chaude ou polluée, expulsent les algues symbiotiques qui les nourrissent et les colorent. Prolongé, il entraîne la mort du récif et la perte des ressources et protections associées.", "Épisodes de blanchissement dans les lagons de Polynésie et de Mayotte"),
("Orpaillage illégal", "Menaces", "Extraction d'or sans autorisation, souvent en forêt, qui détruit les cours d'eau et les sols et rejette du mercure dans l'environnement. Il menace la biodiversité, la santé des populations riveraines et la sécurité dans les territoires concernés.", "Lutte contre les sites clandestins dans l'intérieur de la Guyane"),
("Sargasses", "Menaces", "Algues brunes flottantes dont les échouages massifs, fréquents aux Antilles et en Guyane depuis 2011, dégagent des gaz toxiques en se décomposant. Elles affectent la santé, le tourisme, la pêche et les écosystèmes côtiers.", "Barrages et ramassage sur le littoral de la Martinique"),
("Chlordécone", "Menaces", "Insecticide organochloré utilisé dans les bananeraies des Antilles jusqu'en 1993, très persistant dans les sols. Il contamine eaux, cultures, animaux et populations, et pose un enjeu sanitaire et de reconversion agricole durable.", "Analyses de sols avant mise en culture en Guadeloupe et Martinique"),
("Pêche illicite, non déclarée et non réglementée (INN)", "Économie", "Pêche pratiquée en violation des règles de gestion : sans licence, sans déclaration ou hors quotas. Elle épuise les stocks, fausse la concurrence et prive les territoires de ressources, d'où des dispositifs de surveillance maritime.", "Surveillance des navires étrangers dans la zone économique de Guyane"),
("Réserve de biosphère", "Protection", "Label de l'UNESCO attribué à un territoire qui concilie conservation de la biodiversité, développement économique et recherche. Elle comprend des zones de protection renforcée entourées de zones tampons et de transition.", "La réserve de biosphère de l'archipel de la Guadeloupe"),
("Site Ramsar", "Protection", "Zone humide d'importance internationale désignée dans le cadre de la convention de Ramsar de 1971. Les États s'engagent à en assurer l'utilisation rationnelle et la conservation, notamment pour les oiseaux d'eau et les mangroves.", "Le Grand Cul-de-sac marin en Guadeloupe"),
("Liste rouge UICN", "Politiques", "Inventaire de référence du risque d'extinction des espèces, qui les classe en catégories allant de « préoccupation mineure » à « éteinte », en passant par vulnérable, en danger et en danger critique. Il guide les priorités de conservation.", "Évaluation des espèces menacées de La Réunion"),
("Génie écologique", "Insertion", "Ensemble de techniques de restauration, de réhabilitation et de gestion des milieux naturels fondées sur les processus écologiques. Il crée des emplois locaux non délocalisables, souvent accessibles par des chantiers d'insertion.", "Replantation de mangrove, lutte contre les plantes invasives"),
("Écotourisme", "Économie", "Forme de tourisme qui valorise le patrimoine naturel et culturel en limitant son impact et en faisant bénéficier les populations locales. Il suppose une fréquentation encadrée, de l'éducation à l'environnement et des retombées économiques locales.", "Observation encadrée des tortues marines en Guyane"),
("Mécénat de compétences", "Mécénat", "Mise à disposition gratuite de salariés, sur leur temps de travail, au profit d'un organisme d'intérêt général. L'entreprise conserve la rémunération et valorise le coût de la mission, qui ouvre droit à la réduction d'impôt du mécénat.", "Techniciens d'usine formant les équipes d'un chantier d'insertion"),
("Fonds de dotation", "Mécénat", "Structure de droit privé à but non lucratif créée par la loi de modernisation de l'économie de 2008, qui reçoit des dons et les utilise ou les redistribue pour des missions d'intérêt général. Sa création est simple et rapide.", "Un fonds de dotation finançant des programmes de restauration d'habitats"),
("Fondation d'entreprise", "Mécénat", "Personne morale créée par une entreprise pour mener un programme d'action pluriannuel d'intérêt général, avec une dotation et une gouvernance propres. Elle structure le mécénat de long terme et son pilotage.", "Fondation soutenant la biodiversité et l'insertion dans les territoires où elle a des sites"),
("DPEF (déclaration de performance extra-financière)", "Politiques", "Document, intégré au rapport de gestion de certaines grandes entreprises, présentant leurs risques et politiques sociaux, environnementaux et éthiques, avec indicateurs de résultats. Il est progressivement remplacé par le rapport de durabilité de la directive CSRD.", "Section sur les émissions, les accidents du travail et la biodiversité"),
("CSRD (directive sur le reporting de durabilité)", "Politiques", "Directive européenne 2022/2464 qui impose un rapport de durabilité détaillé, selon les normes ESRS, audité par un tiers. Son calendrier d'application et son périmètre ont fait l'objet d'ajustements européens : à vérifier à la date de lecture.", "Rapport de durabilité d'un groupe industriel avec chapitre biodiversité"),
("Double matérialité", "Politiques", "Principe de la CSRD selon lequel une entreprise analyse à la fois ses impacts sur l'environnement et la société, et l'influence des enjeux de durabilité sur sa performance financière. C'est le point de départ de tout rapport.", "Un site industriel identifie son impact sur une rivière et sa dépendance à l'eau"),
("Taxonomie européenne", "Politiques", "Règlement (UE) 2020/852 qui définit les activités économiques durables selon six objectifs environnementaux, dont la protection de la biodiversité. Les entreprises concernées publient la part de leur activité alignée.", "Part du chiffre d'affaires alignée sur l'objectif d'économie circulaire"),
("Devoir de vigilance", "Politiques", "Obligation, issue de la loi française de 2017, pour les très grandes sociétés d'établir et mettre en œuvre un plan de vigilance qui prévient les atteintes graves aux droits humains et à l'environnement dans leur chaîne de valeur.", "Cartographie des risques chez les sous-traitants d'un groupe"),
]
def ensure(core):
    core.ensure_data()
    g = core.DATA / "geographie.csv"
    if not g.exists() or g.stat().st_size == 0:
        w = csv.writer(open(g, "w", encoding="utf-8", newline="")); w.writerow(["territoire", "commune", "type", "statut"]); w.writerows(geo_rows())
    have = {core.norm(r["terme"]) for r in csv.DictReader(open(core.CSV, encoding="utf-8"))}
    new = [[t, c, d, e, "Base enrichie", "2026-10-09"] for t, c, d, e in ENC_NEW if core.norm(t) not in have]
    try:  # vocabulaire complémentaire v3.2 (vocabulaire.py)
        from vocabulaire import VOCAB
        have |= {core.norm(r[0]) for r in new}
        for t, c, d, e in VOCAB:
            if core.norm(t) not in have:
                have.add(core.norm(t)); new.append([t, c, d, e, "Vocabulaire v3.2", "2026-10-17"])
    except Exception:
        pass
    if new:
        csv.writer(open(core.CSV, "a", encoding="utf-8", newline="")).writerows(new)

EXTRA_FEEDS = [{"theme": "rse", "territory": "France", "q": "RSE CSRD reporting durabilité"}, {"theme": "rse", "territory": "France", "q": "DPEF rapport de durabilité"},
 {"theme": "rse", "territory": "France", "q": "mécénat de compétences loi"}, {"theme": "emploi", "territory": "Outre-mer", "q": "recrutement biodiversité outre-mer"},
 {"theme": "emploi", "territory": "Outre-mer", "q": "offre emploi environnement Guadeloupe Martinique Réunion Guyane Mayotte"},
 {"theme": "associations", "territory": "Martinique", "q": "association environnement OR insertion Martinique"},
 {"theme": "associations", "territory": "Guadeloupe", "q": "association environnement OR insertion Guadeloupe"},
 {"theme": "associations", "territory": "Guyane", "q": "association environnement OR insertion Guyane"},
 {"theme": "associations", "territory": "La Réunion", "q": "association environnement OR insertion La Réunion"},
 {"theme": "associations", "territory": "Mayotte", "q": "association environnement OR insertion Mayotte"}]

READS = [
["Espèces envahissantes", "Débutant", "Centre de ressources sur les espèces exotiques envahissantes", "UICN France / OFB (site especes-exotiques-envahissantes.fr)", "Portail de référence : fiches espèces, retours d'expérience de gestion, réglementation et outils de prévention.", "Point d'entrée pratique pour identifier une espèce et savoir comment agir."],
["Espèces envahissantes", "Expert", "Évaluation thématique sur les espèces exotiques envahissantes", "IPBES (2023)", "Synthèse mondiale des causes, impacts et options de gestion des invasions biologiques, avec un focus sur les îles.", "Cadre scientifique pour justifier des projets de prévention et de contrôle."],
["Espèces envahissantes", "Intermédiaire", "Les espèces exotiques envahissantes en outre-mer", "UICN France (dossiers et rapports)", "Panorama des invasions dans les territoires ultramarins, de leurs conséquences et des priorités d'action.", "Utile pour cibler un appel à projets sur les îles."],
["Action biodiversité", "Expert", "Évaluation mondiale de la biodiversité et des services écosystémiques", "IPBES (2019)", "Bilan des pressions sur la nature et de leurs causes directes et indirectes, avec des leviers de transformation.", "Base commune pour comprendre les cinq pressions sur la biodiversité."],
["Action biodiversité", "Intermédiaire", "Stratégie nationale pour la biodiversité 2030", "Ministère de la Transition écologique", "Feuille de route française : restauration, protection, réduction des pressions et mobilisation des acteurs.", "Aligner un programme de mécénat sur les priorités publiques."],
["Action biodiversité", "Intermédiaire", "The Economics of Biodiversity (Dasgupta Review)", "Gouvernement du Royaume-Uni (2021)", "Analyse économique de la dépendance des sociétés à la nature et du coût de son érosion.", "Argumentaire utile pour convaincre des directions d'entreprise."],
["Cadre & politiques", "Débutant", "Cadre mondial de la biodiversité de Kunming-Montréal", "Convention sur la diversité biologique (2022)", "Vingt-trois cibles pour 2030, dont la protection de 30 % des terres et des mers et la restauration des écosystèmes dégradés.", "Référence des engagements internationaux de la France."],
["Cadre & politiques", "Intermédiaire", "Listes rouges des espèces menacées en France (outre-mer)", "UICN France / MNHN", "Évaluation du risque d'extinction des espèces, dont celles des territoires ultramarins.", "Prioriser les espèces et habitats à soutenir."],
]
JOBS = {"titres": [
["Chargé(e) de mission biodiversité", "Biodiversité", "OFB, DEAL, collectivités, parcs, associations"], ["Écogarde / garde du littoral", "Biodiversité", "Parcs nationaux, Conservatoire du littoral, réserves"],
["Technicien(ne) espaces naturels", "Biodiversité", "Collectivités, gestionnaires d'espaces naturels"], ["Ingénieur(e) écologue", "Biodiversité", "Bureaux d'études, CBN, organismes de recherche"],
["Chargé(e) de lutte contre les espèces invasives", "Biodiversité", "Associations, collectivités, OFB"], ["Animateur(trice) nature", "Éducation", "Associations, parcs, collectivités"],
["Chargé(e) d'insertion professionnelle", "Insertion", "Structures d'insertion, missions locales, SMA"], ["Encadrant(e) technique de chantier d'insertion", "Insertion", "Chantiers d'insertion, génie écologique"],
["Chargé(e) de mécénat / partenariats", "Mécénat", "Fondations, fonds de dotation, grandes entreprises"], ["Chargé(e) RSE / reporting extra-financier", "RSE", "Industriels, cabinets de conseil, banques"]],
"recruteurs": [["Office français de la biodiversité", "Public", "Tous territoires", "Agents, chargés de mission"], ["Parcs nationaux", "Public", "Guadeloupe, Guyane, Réunion", "Écogardes, animateurs"],
["Conservatoire du littoral", "Public", "Tous territoires", "Gardes, chargés de mission"], ["DEAL (services de l'État)", "Public", "Tous territoires", "Ingénieurs, techniciens"],
["Collectivités et intercommunalités", "Public", "Tous territoires", "Environnement, insertion"], ["Associations (WWF, LPO, UICN, locales)", "Associatif", "Tous territoires", "Chargés de projet, animateurs"],
["Structures d'insertion et missions locales", "Associatif", "Tous territoires", "Conseillers, encadrants"], ["Fondations et fonds de dotation", "Privé", "France entière", "Mécénat, partenariats"],
["Entreprises industrielles et cabinets RSE", "Privé", "Tous territoires", "RSE, reporting, conformité"]]}
REGS = [
["Mécénat", "Loi n° 2003-709 du 1er août 2003 (loi Aillagon)", "Cadre du mécénat. L'article 238 bis du CGI ouvre aux entreprises une réduction d'impôt de 60 % des dons, dans la limite de 20 000 € ou 5 ‰ du chiffre d'affaires, avec un taux de 40 % au-delà de 2 M€ de dons."],
["Mécénat de compétences", "Code du travail, art. L.8241-3 (prêt de main-d'œuvre à but non lucratif)", "Encadre la mise à disposition de salariés auprès d'un organisme d'intérêt général : convention tripartite et accord du salarié. Le coût de la mission est valorisé pour la réduction d'impôt."],
["Structures", "Loi n° 2008-776 (fonds de dotation) et régime des fondations d'entreprise", "Définit les véhicules du mécénat : fonds de dotation, fondation d'entreprise, fondation reconnue d'utilité publique."],
["RSE / reporting", "Directive (UE) 2022/2464 (CSRD) et ordonnance n° 2023-1142", "Rapport de durabilité selon les normes ESRS, qui remplace progressivement la DPEF. Le calendrier a été modifié au niveau européen : à vérifier."],
["RSE / reporting", "DPEF : Code de commerce, art. L.225-102-1", "Déclaration de performance extra-financière des grandes entreprises : modèle d'affaires, risques, politiques, indicateurs."],
["Finance durable", "Règlement (UE) 2020/852 (taxonomie)", "Classification des activités durables selon six objectifs, dont la biodiversité."],
["Vigilance", "Loi n° 2017-399 (devoir de vigilance) et directive (UE) 2024/1760 (CSDDD)", "Plan de vigilance sur les droits humains et l'environnement dans la chaîne de valeur."],
["Biodiversité", "Loi n° 2016-1087 (reconquête de la biodiversité)", "Consacre la séquence éviter-réduire-compenser, l'accès aux ressources génétiques et le partage des avantages."],
["Entreprise", "Loi PACTE n° 2019-486", "Raison d'être, société à mission et prise en compte des enjeux sociaux et environnementaux dans la gestion."]]
DPEF_MD = """# Trame DPEF / rapport de durabilité

1. Modèle d'affaires (activités, sites, chaîne de valeur, territoires)
2. Analyse des risques et double matérialité (impacts, dépendances, parties prenantes)
3. Politiques, diligences et résultats pour chaque enjeu
   - Social : emploi, santé-sécurité, formation, diversité, insertion
   - Environnement : climat, énergie, eau, déchets, biodiversité
   - Droits humains, lutte contre la corruption, achats responsables
   - Engagements sociétaux : mécénat, mécénat de compétences, ancrage territorial
4. Tableau d'indicateurs (définition, périmètre, unité, N, N-1, source)
5. Méthodologie et périmètre de reporting
6. Vérification par un organisme tiers indépendant
7. Table de concordance avec les ESRS (si CSRD)
"""
DPEF_STEPS = [["Cadrer le périmètre et l'assujettissement", "Note de cadrage", "RSE", "", "À faire"], ["Cartographier les parties prenantes", "Carte et consultations", "RSE", "", "À faire"],
["Réaliser l'analyse de matérialité", "Matrice de matérialité", "RSE", "", "À faire"], ["Collecter les données et indicateurs", "Tableau d'indicateurs", "Sites / RH / HSE", "", "À faire"],
["Rédiger les chapitres", "Projet de DPEF", "RSE", "", "À faire"], ["Relecture juridique et direction", "Version validée", "Juridique / DG", "", "À faire"],
["Vérification par l'OTI", "Avis de l'organisme tiers", "RSE / Finance", "", "À faire"], ["Publication et communication", "Rapport publié", "Communication", "", "À faire"]]

ENC_NEW += [
("Résilience écologique", "Concepts", "Capacité d'un écosystème à absorber une perturbation (cyclone, incendie, pollution) puis à retrouver sa structure et ses fonctions. Elle dépend de la diversité des espèces, de la connectivité des habitats et de l'intensité des pressions humaines.", "Récupération d'une forêt après le passage d'un cyclone"),
("Aire marine protégée", "Protection", "Espace maritime délimité où les activités humaines sont encadrées pour préserver les écosystèmes marins et les ressources halieutiques. Selon le niveau de protection, la pêche, la navigation ou l'extraction peuvent y être limitées ou interdites.", "Le parc naturel marin de Mayotte"),
("Herbier de phanérogames", "Écosystèmes", "Prairie sous-marine de plantes à fleurs adaptées à l'eau de mer, qui abrite de nombreuses espèces, fixe les sédiments et stocke du carbone. Les herbiers sont sensibles aux ancrages, à la pollution et à l'érosion des sols.", "Herbiers des Antilles fréquentés par les tortues vertes"),
("Forêt sèche tropicale", "Écosystèmes", "Forêt des zones à saison sèche marquée, très riche en espèces endémiques mais devenue rare après des siècles de défrichement et d'incendies. Sa restauration demande des plants locaux, une lutte contre les espèces invasives et un suivi à long terme.", "Restauration de forêt sèche à La Réunion"),
("Lagon", "Écosystèmes", "Étendue d'eau peu profonde séparée de la haute mer par une barrière corallienne ou un atoll. Il abrite herbiers, coraux et nurseries de poissons, et procure protection côtière, pêche et activités touristiques aux populations locales.", "Le lagon de Mayotte, entouré d'une double barrière corallienne"),
("Biopiraterie", "Politiques", "Appropriation de ressources biologiques ou de savoirs traditionnels sans autorisation ni partage équitable des avantages avec les communautés d'origine. Le protocole de Nagoya et le droit français encadrent l'accès et imposent des contrats de partage.", "Brevet sur une plante médicinale sans accord des communautés locales"),
("Bioindicateur", "Science", "Espèce ou groupe d'espèces dont la présence, l'abondance ou l'état de santé renseigne sur la qualité d'un milieu. Les suivis de bioindicateurs permettent de détecter précocement des pollutions ou des dégradations et d'évaluer des actions de restauration.", "Suivi de macro-invertébrés pour évaluer la qualité d'une rivière"),
("Pollinisation", "Concepts", "Transport du pollen d'une fleur à une autre, assuré par des insectes, des oiseaux ou des chauves-souris, qui permet la reproduction de nombreuses plantes sauvages et cultivées. Son déclin menace la production alimentaire et la diversité végétale.", "Abeilles et colibris pollinisant les cultures des Antilles"),
("Zone économique exclusive (ZEE)", "Outre-mer", "Espace maritime s'étendant jusqu'à 200 milles nautiques des côtes, où l'État côtier exerce des droits souverains sur les ressources. Grâce à ses territoires ultramarins, la France dispose de l'une des plus vastes ZEE du monde, ce qui accroît ses responsabilités.", "Surveillance des pêches dans la ZEE de la Guyane"),
("Région ultrapériphérique (RUP)", "Outre-mer", "Statut européen reconnu à des territoires éloignés du continent, intégrés à l'Union européenne mais bénéficiant de mesures d'adaptation. La Guadeloupe, la Martinique, la Guyane, La Réunion et Mayotte en font partie, avec accès à des fonds européens spécifiques.", "Fonds européens finançant des projets de biodiversité en Guyane"),
("Ripisylve", "Écosystèmes", "Végétation boisée qui borde un cours d'eau. Elle stabilise les berges, filtre les polluants, ombrage l'eau et sert de corridor aux espèces. Sa restauration est une action courante de génie écologique, souvent confiée à des chantiers d'insertion.", "Plantation d'espèces locales le long d'une rivière"),
("Sixième extinction", "Menaces", "Expression désignant l'accélération actuelle de la disparition des espèces, très supérieure au rythme naturel et attribuée surtout aux activités humaines. Les îles, riches en espèces endémiques, sont parmi les territoires les plus touchés.", "Disparition d'oiseaux et de reptiles endémiques sur des îles"),
("Capital naturel", "Économie", "Stock de ressources naturelles (sols, eau, forêts, espèces) qui fournit à l'économie des services indispensables. Le comptabiliser permet d'intégrer la dépendance des entreprises à la nature dans leurs décisions et leurs rapports de durabilité.", "Valoriser le rôle d'une mangrove dans la protection côtière"),
("Paiements pour services environnementaux", "Économie", "Mécanisme par lequel les bénéficiaires de services rendus par la nature rémunèrent ceux qui préservent ou restaurent les milieux qui les fournissent. Il valorise les pratiques favorables à la biodiversité chez les agriculteurs et propriétaires.", "Rémunération d'un agriculteur pour l'entretien de haies et de mares"),
("Agroécologie", "Économie", "Ensemble de pratiques agricoles qui s'appuient sur les processus naturels (diversité des cultures, couverture des sols, auxiliaires) pour réduire les intrants chimiques. Elle améliore la fertilité des sols, la biodiversité et la résilience des exploitations.", "Cultures associées et couverts végétaux en Martinique"),
("Agroforesterie", "Économie", "Association d'arbres et de cultures ou d'élevage sur une même parcelle, qui améliore la fertilité des sols, la gestion de l'eau et la biodiversité tout en diversifiant les revenus. Elle est bien adaptée aux milieux tropicaux et aux petites exploitations.", "Jardins créoles associant arbres fruitiers et cultures vivrières"),
("Sciences participatives", "Science", "Programmes associant citoyens et scientifiques à la collecte de données, par exemple l'observation d'espèces. Elles enrichissent les inventaires, sensibilisent le public et soutiennent la surveillance de la biodiversité, notamment des espèces invasives.", "Signalement d'espèces exotiques envahissantes par les habitants"),
("Contrat d'engagement jeune (CEJ)", "Insertion", "Dispositif d'accompagnement intensif des jeunes de 16 à 25 ans sans emploi ni formation, proposé par les missions locales et France Travail. Il combine un parcours personnalisé, des activités régulières et, selon la situation, une allocation.", "Un jeune accompagné vers un métier de l'environnement"),
("Clause d'insertion", "Insertion", "Disposition d'un marché public ou d'un chantier qui impose de réserver une part des heures de travail à des personnes éloignées de l'emploi. Elle fait du commanditaire un levier d'insertion et peut s'appliquer aux travaux de génie écologique.", "Heures d'insertion dans un marché de restauration d'espaces naturels"),
("Chantier d'insertion", "Insertion", "Structure de l'insertion par l'activité économique qui emploie, en contrat à durée déterminée d'insertion, des personnes éloignées de l'emploi sur des travaux utiles au territoire, avec un accompagnement social et professionnel préparant la suite du parcours.", "Nettoyage de plages et replantation de mangrove"),
("Économie sociale et solidaire (ESS)", "Société", "Ensemble des organisations (associations, coopératives, mutuelles, fondations, entreprises solidaires) dont l'objectif est l'utilité sociale plutôt que le profit, avec une gouvernance démocratique. L'ESS est un acteur clé de l'insertion et des projets locaux.", "Coopérative d'agriculteurs ou association d'insertion"),
("Entreprise à mission", "Mécénat", "Qualité, introduite par la loi PACTE de 2019, d'une société qui inscrit dans ses statuts une raison d'être et des objectifs sociaux et environnementaux, suivis par un comité de mission et vérifiés par un organisme tiers indépendant.", "Industriel intégrant la biodiversité dans ses objectifs statutaires"),
("Raison d'être", "Mécénat", "Ce qui constitue l'utilité d'une entreprise pour ses parties prenantes et la société, formulé dans ses statuts depuis la loi PACTE de 2019. Elle oriente la stratégie, la RSE ainsi que les choix de mécénat et d'engagement sociétal.", "Une entreprise s'engage à contribuer à la préservation des milieux naturels"),
("Parties prenantes", "Politiques", "Personnes et organisations affectées par l'activité d'une entreprise ou capables de l'influencer : salariés, clients, fournisseurs, riverains, associations, collectivités. Leur consultation nourrit l'analyse de matérialité et la légitimité des actions de mécénat.", "Consultation des riverains d'une usine avant un programme local"),
("Empreinte biodiversité", "Économie", "Mesure de l'impact d'une organisation, d'un produit ou d'un portefeuille sur la biodiversité, tout au long de sa chaîne de valeur. Plusieurs méthodes existent sans qu'aucune soit encore universelle : il faut documenter hypothèses et limites.", "Évaluation de l'impact des achats de matières premières"),
("TNFD", "Politiques", "Groupe de travail international (Taskforce on Nature-related Financial Disclosures) qui a publié en 2023 un cadre volontaire permettant aux entreprises et institutions financières d'identifier et de publier leurs risques, dépendances et impacts liés à la nature.", "Une entreprise cartographie ses sites proches de zones sensibles"),
("Greenwashing", "Politiques", "Pratique consistant à présenter de façon trompeuse une action ou un produit comme respectueux de l'environnement. Elle expose à des sanctions et à une perte de confiance, d'où l'importance de preuves chiffrées, vérifiables et de la transparence sur les limites.", "Allégation « neutre en biodiversité » sans méthode ni preuves"),
("Ancrage territorial", "Mécénat", "Capacité d'une entreprise ou d'une fondation à s'inscrire durablement dans un territoire, en nouant des liens avec les acteurs locaux, en recrutant sur place et en soutenant des projets utiles aux habitants. C'est un critère clé du mécénat de proximité.", "Une usine soutient une association de restauration écologique de sa commune"),
("Mesure d'impact social", "Mécénat", "Démarche qui évalue les changements produits par un projet sur les personnes et le territoire, à partir d'indicateurs définis dès le départ (emplois, formations, sorties positives). Elle aide à rendre compte aux financeurs et à améliorer les programmes.", "Taux d'accès à l'emploi des participants à un chantier d'insertion"),
("Rescrit mécénat", "Mécénat", "Procédure permettant à un organisme de demander à l'administration fiscale si les dons qu'il reçoit ouvrent droit à la réduction d'impôt. La réponse sécurise juridiquement l'organisme et ses donateurs et facilite la collecte de fonds.", "Une association vérifie son éligibilité avant de lancer une campagne"),
]

def _f(n, t, d, x, u="", c=""):
    return {"n": n, "t": t, "d": d, "x": x, "u": u, "c": c}
FOUND = [
_f("Fondation pour la recherche sur la biodiversité (FRB)", "Fondation de coopération scientifique", ["Biodiversité"], "Fait le lien entre chercheurs, entreprises, collectivités et associations autour de la biodiversité.", "https://www.fondationbiodiversite.fr"),
_f("Fondation de la Mer", "Fondation", ["Biodiversité"], "Soutient des projets de protection et de restauration de l'océan, de recherche et de sensibilisation.", "https://www.fondationdelamer.org"),
_f("Fondation Tara Océan", "Fondation reconnue d'utilité publique", ["Biodiversité"], "Expéditions scientifiques, éducation et plaidoyer pour l'océan.", "https://fondationtaraocean.org"),
_f("Fondation pour la Nature et l'Homme (FNH)", "Fondation reconnue d'utilité publique", ["Biodiversité"], "Transition écologique, plaidoyer et soutien à des projets de terrain.", "https://www.fnh.org"),
_f("Fondation GoodPlanet", "Fondation reconnue d'utilité publique", ["Biodiversité"], "Éducation à l'environnement, sensibilisation et soutien à des projets pour le climat et la biodiversité.", "https://www.goodplanet.org"),
_f("Fondation Prince Albert II de Monaco", "Fondation", ["Biodiversité"], "Soutient des projets de protection de la biodiversité, de l'eau et du climat, notamment océans et Méditerranée.", "https://www.fpa2.com"),
_f("Fondation Yves Rocher (Institut de France)", "Fondation abritée", ["Biodiversité"], "Engagée pour la biodiversité, la plantation d'arbres et l'éducation à la nature."),
_f("Fondation François Sommer", "Fondation", ["Biodiversité"], "Préservation de la nature et valorisation du lien entre l'homme et la nature."),
_f("Fondation BNP Paribas (Climate & Biodiversity Initiative)", "Fondation d'entreprise", ["Biodiversité"], "Soutient la recherche sur le climat et la biodiversité."),
_f("Fondation TotalEnergies", "Fondation d'entreprise", ["Biodiversité", "Insertion"], "Intervient notamment sur l'océan, la jeunesse et la solidarité.", "", "À vérifier"),
_f("Fondation Nature & Découvertes", "Fondation d'entreprise", ["Biodiversité"], "Soutient des actions de protection de la nature et d'éducation à l'environnement."),
_f("Fondation de France", "Fondation abritante", ["Biodiversité", "Insertion"], "Appels à projets en environnement, solidarité et emploi ; abrite de nombreux fonds.", "https://www.fondationdefrance.org"),
_f("Fondation VINCI pour la Cité", "Fondation d'entreprise", ["Insertion"], "Soutient l'insertion sociale et professionnelle ; des salariés du groupe parrainent des projets associatifs.", "", "Oui (parrainage de projets par les salariés)"),
_f("Fondation Safran pour l'Insertion", "Fondation d'entreprise", ["Insertion"], "Favorise l'insertion de personnes éloignées de l'emploi, notamment des jeunes et des personnes en situation de handicap.", "", "À vérifier"),
_f("Fondation Saint-Gobain Initiatives", "Fondation d'entreprise", ["Insertion"], "Soutient des projets d'insertion et d'habitat portés par des associations et parrainés par des salariés.", "", "Oui (parrainage par les salariés)"),
_f("Fondation SNCF", "Fondation d'entreprise", ["Insertion"], "Solidarité et insertion des jeunes, avec implication des collaborateurs.", "", "À vérifier"),
_f("Fondation ENGIE", "Fondation d'entreprise", ["Insertion"], "Solidarité, inclusion et transition énergétique, avec implication des collaborateurs.", "", "À vérifier"),
_f("Fondation de la 2e Chance", "Fondation", ["Insertion"], "Aide des personnes ayant traversé de grandes difficultés à construire un nouveau projet professionnel."),
_f("Apprentis d'Auteuil", "Fondation reconnue d'utilité publique", ["Insertion"], "Accompagne des jeunes en difficulté vers la formation et l'emploi ; présente en outre-mer (à vérifier par territoire).", "https://www.apprentis-auteuil.org"),
_f("Fondation Agir Contre l'Exclusion (FACE)", "Fondation reconnue d'utilité publique", ["Insertion"], "Réseau de clubs d'entreprises engagées contre l'exclusion : insertion et mécénat de compétences.", "", "Oui (réseau d'entreprises)"),
]
INTERMEDIARIES = [
_f("Admical", "Association", ["Mécénat"], "Promeut le mécénat d'entreprise ; ressources et guides, dont le mécénat de compétences.", "https://admical.org", "Oui"),
_f("Pro Bono Lab", "Association", ["Mécénat"], "Met en relation des professionnels et des associations pour des missions de compétences.", "https://probonolab.org", "Oui"),
_f("Passerelles & Compétences", "Association", ["Mécénat"], "Mobilise des professionnels volontaires pour des missions d'appui auprès d'associations.", "https://www.passerellesetcompetences.org", "Oui"),
_f("Centre français des Fonds et Fondations (CFF)", "Réseau", ["Mécénat"], "Réseau des fondations et fonds de dotation : ressources, formations et veille du secteur.", "", "Ressources"),
_f("France Générosités", "Syndicat professionnel", ["Mécénat"], "Représente les organisations faisant appel à la générosité du public.", "", "Ressources"),
]
PHIL_JOBS = {"titres": [
["Chargé(e) de mécénat", "Mécénat", "Fondations, associations, entreprises"], ["Responsable mécénat / fondation d'entreprise", "Mécénat", "Grandes entreprises, fondations d'entreprise"],
["Délégué(e) général(e) de fondation", "Direction", "Fondations, fonds de dotation"], ["Chargé(e) de collecte de fonds (fundraiser)", "Philanthropie", "Associations, ONG, fondations"],
["Responsable grands donateurs", "Philanthropie", "Fondations, universités, associations"], ["Chargé(e) de partenariats entreprises", "Partenariats", "Associations, fondations"],
["Responsable mécénat de compétences / engagement des collaborateurs", "Mécénat", "Entreprises, fondations d'entreprise"], ["Chargé(e) de programmes en fondation", "Programmes", "Fondations"],
["Conseiller(ère) en philanthropie", "Philanthropie", "Banques privées, fondations abritantes, cabinets de conseil"], ["Chargé(e) d'évaluation d'impact", "Impact", "Fondations, cabinets, associations"]],
"recruteurs": [["Fondations d'entreprise et fonds de dotation", "Privé", "France entière", "Mécénat, programmes"], ["Fondations abritantes et reconnues d'utilité publique", "Fondation", "France entière", "Programmes, philanthropie"],
["Associations et ONG", "Associatif", "Tous territoires", "Collecte, partenariats"], ["Réseaux : Admical, CFF, France Générosités", "Réseau", "France entière", "Offres et veille du secteur"],
["Grandes entreprises (directions RSE / engagement)", "Privé", "Tous territoires", "Mécénat, RSE"], ["Banques privées et cabinets de conseil en philanthropie", "Privé", "France entière", "Conseil aux donateurs"]]}
EXTRA_FEEDS += [{"theme": "fondations", "territory": "France", "q": "fondation biodiversité appel à projets"}, {"theme": "fondations", "territory": "France", "q": "fondation insertion professionnelle appel à projets"},
 {"theme": "competences", "territory": "France", "q": "mécénat de compétences fondation programme"}, {"theme": "philanthropie", "territory": "France", "q": "emploi mécénat philanthropie recrutement"},
 {"theme": "philanthropie", "territory": "France", "q": "chargé de mécénat offre emploi fondation"}]
