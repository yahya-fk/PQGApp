Chapitre 3 : Contexte général du projet PQG CONTROLLER


1. # <a name="_toc148123400"></a>**PQG CONTROLLER VERSION DEMO**
Cette version n'exécute aucune action réelle, mais elle vous permettra d'explorer les interfaces et certaines fonctionnalités de l'application.

Lien :    [PQG Controller (yahya-fk.github.io)](https://yahya-fk.github.io/PQG-APP/)

![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.022.png)

<a name="_toc148122997"></a>**Figure 58 Code QR PQG Controller DEMO**





# <a name="_toc148123372"></a>**INTRODUCTION**
L'avènement de la technologie a engendré une transformation fondamentale dans la manière dont les entreprises abordent l'amélioration de la qualité de leur production. Au cœur de cette révolution, la digitalisation des Plans de Qualité Générale (PQG) s'est affirmée comme un pilier essentiel d'un projet d'envergure dirigé par le Responsable général du montage M. **Mohammed BOUHAOUI**, au sein de **STELLANTIS** Kenitra. L'objectif de ce projet ambitieux est double : d'une part, il vise à numériser les PQG pour les rendre plus accessibles et plus efficaces, et d'autre part, il vise à améliorer la qualité de la production en filtrant les points de vérification moins pertinents.

Dans ce contexte de transformation, ce chapitre se consacre à l'aspect central du projet que j'ai personnellement développé : la création d'une application innovante conçue pour mesurer et suivre l'efficacité du PQG au sein de l'atelier de montage de **STELLANTIS** Kenitra. Cette application représente la pierre angulaire de notre démarche visant à améliorer la qualité de production. En effet, elle s'attaque à un défi majeur : comment garantir que le PQG, en tant qu'outil de référence pour la qualité, soit à la fois fiable, pertinent, et évolutif.

Au cours de ce chapitre, je vais vous guider à travers les étapes cruciales de conception, de développement et de déploiement de cette application, en mettant en lumière les défis que j'ai relevés et les solutions que j'ai apportées pour assurer son succès. En particulier, je vais me focaliser sur la troisième et dernière étape du projet, à savoir le déploiement de l'outil de suivi et de mesure de l'efficacité du PQG. Nous explorerons en détail son architecture, ses fonctionnalités clés, et les avantages tangibles qu'il offre à l'atelier de montage.
1. # <a name="_toc148123373"></a>**CAHIER DES CHARGES** 
la mise en œuvre d'un projet visant à développer un système de suivi en temps réel de l'efficacité du Plan de Qualité Générale (PQG) au sein de l'atelier de montage de STELLANTIS Kenitra. L'objectif principal de ce projet est de digitaliser et d'améliorer la gestion de la qualité en fournissant des données chiffrées en temps réel sur l'efficacité du PQG.
1. ## <a name="_toc148123374"></a>**Objectifs du Projet**
- Concevoir et développer une application informatique permettant de collecter, analyser et visualiser en temps réel les données liées à l'efficacité du PQG.
- Fournir des valeurs de performance clés pertinents pour évaluer la qualité de la production et l'efficacité du PQG.
- Améliorer la réactivité de l'atelier de montage en identifiant rapidement les déviations par rapport au PQG et en permettant des actions correctives immédiates
- Assurer la confidentialité et la sécurité des données collectées, conformément aux normes de protection des données en vigueur.
  1. ## <a name="_toc148123375"></a>**Fonctionnalités Clés**
     1. ### <a name="_toc148123376"></a>**Collecte de Données en Temps Réel :**
- Suivi en temps réel des points de vérification du PQG.
- Collecte automatique de données depuis les postes de travail.
- Intégration de capteurs et de dispositifs de mesure pour la collecte de données.
  1. ### <a name="_toc148123377"></a>**Analyse des Données :**
- Calcul des valeurs liés à l'efficacité du PQG.
- Comparaison des données en temps réel avec les normes du PQG.
  1. ### <a name="_toc148123378"></a>**Visualisation :**
- Tableaux de bord pour afficher les données en temps réel.
- Graphiques et diagrammes permettant une analyse visuelle.
  1. ## <a name="_toc148123379"></a>**Sécurité et Confidentialité des Données**
- Mise en place de mesures de sécurité robustes pour protéger les données collectées.
- Respect des réglementations locales et internationales en matière de protection des données personnelles.
  1. ## <a name="_toc148123380"></a>**Évolutivité**
L'architecture du système doit être conçue pour permettre une évolutivité facile afin de prendre en charge de nouveaux postes de travail ou de nouvelles fonctionnalités au fur et à mesure que les besoins évoluent.
1. ## <a name="_toc148123381"></a>**Contraintes Techniques**
- Le système doit être compatible avec les équipements existants de l'atelier de montage.
- L'application doit être accessible à partir de divers dispositifs, y compris les ordinateurs de bureau et les appareils mobiles.
1. # <a name="_toc148123382"></a>**CONCEPTION**
Pour répondre à ces besoins, nous avons envisagé de réaliser les diagrammes suivants, en utilisant UML.
1. ## <a name="_toc148123383"></a>**Diagramme de classe**
![Une image contenant texte, diagramme, Parallèle, ligne

Description générée automatiquement](Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.001.png)

<a name="_toc148122988"></a>**Figure 49 Diagramme de classe PQG Controller**
1. ## **<a name="_toc148123384"></a>DIAGRAMME DE CAS D’UTILISATION**
![Une image contenant texte, diagramme, ligne, dessin

Description générée automatiquement](Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.002.png)

<a name="_toc148122989"></a>**Figure 50 Diagramme de cas D'utilisation de PQG Controller**
1. ## <a name="_toc148123385"></a>**DIAGRAMMES DE SEQUENCE**
   1. ### <a name="_toc148123386"></a>**DS  AUJOURD’HUI / HIER** 
![Une image contenant texte, capture d’écran, nombre, Parallèle

Description générée automatiquement](Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.003.png)

<a name="_toc148122990"></a>**Figure 51 DS Aujourd’hui / Hier PQG Controller**
1. ### <a name="_toc148123387"></a>**DS  Paramètre**
![Une image contenant texte, Parallèle, reçu, document

Description générée automatiquement](Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.004.jpeg)

<a name="_toc148122991"></a>**Figure 52 DS paramètre PQG Controller**
### <a name="_toc148123388"></a>**N.B**
Outre les fonctionnalités principales décrites précédemment, d'autres fonctions ont été mises en place pour compléter l'application. Celles-ci partagent des étapes similaires avec les fonctions déjà discutées ou présentent des processus qui ne nécessitent pas d'explication détaillée. Ces fonctions incluent (Log in, Log out, Statistiques Personnalisées, page DATA).
1. # <a name="_toc148123389"></a>**REALISATION**
Après avoir finalisé la phase de conception, nous sommes passés à la réalisation de l'application en suivant les spécifications et les maquettes établies dans la phase précédente. Cette étape consiste à transformer les concepts abstraits en une application fonctionnelle en utilisant les technologies et les outils appropriés.
1. ## <a name="_toc148123390"></a>**Environnement de Développement**
L'environnement de développement choisi pour la réalisation de l'application était le suivant:

- Langages de programmation : JavaScript ,HTML,CSS
- FrameWorks : BOOSTRAP,DJANGO
- Web Scraping : SELENIUM
- Analyse et traitement des données : Pandas, xlrd, OS, PYSQL
- Outils de développement : Visual Studio Code, Git, Laragon

![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.005.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.006.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.007.jpeg)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.008.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.009.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.010.jpeg)
1. ## <a name="_toc148123391"></a>**Développement**
   1. ### <a name="_toc148123392"></a>**Création du  compte et Log  in** 
      1. #### **Développement du Front-end**
Pour le développement de l'interface utilisateur (front-end) de notre application, nous avons opté pour l'utilisation d'une Template Bootstrap qui offre une disposition spécifique. Cette disposition comprend un formulaire positionné à gauche de la page, tandis qu'à droite, un espace est réservé pour décrire l'application, son rôle et son objectif.
1. #### **Développement du Back-end**
Le développement du back-end de l'application revêt une importance cruciale pour garantir la sécurité et la fiabilité des données. Voici les principales fonctionnalités que nous avons mises en place dans cette phase :

- **Vérification des Données Utilisateur :** Le back-end, basé sur le framework Django, se charge de vérifier les données saisies par l'utilisateur conformément aux normes prédéfinies. Cela inclut également la vérification de la confirmation du mot de passe.
- **Sauvegarde des Données :** En cas de succès de la validation des données, celles-ci sont sauvegardées de manière sécurisée dans la base de données associée. Ceci assure la préservation des informations essentielles.
- **Gestion des Erreurs :** En cas d'erreur, le back-end génère un message d'erreur approprié. L'utilisateur est ensuite redirigé vers la page de menu pour maintenir une expérience fluide.
  1. #### **Captures d’écran des interfaces** 
![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.011.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.012.png)

<a name="_toc148122992"></a>**Figure 53 Captures d'écran des interfaces Log in Création du compte PQG Controller**
1. ### <a name="_toc148123393"></a>**Page MENU**
   1. #### **Front-end**
La page Menu de notre application présente une interface utilisateur soigneusement conçue pour offrir une expérience utilisateur conviviale et intuitive. Voici les principales caractéristiques de la partie front-end :

- **Cartes**  : La page est organisée en six cartes, chacune représentant une interface distincte de l'application. 
- **Barre de Navigation (Navbar)** : En haut de la page, une barre de navigation bien structurée offre une navigation fluide. Elle contient des liens vers les différentes interfaces de l'application, ainsi qu'un logo **Stellantis** à droite.
- **Menu de l'Utilisateur** : Un bouton avec le logo de l'utilisateur est également présent dans la barre de navigation. En cliquant sur ce bouton, un menu latéral s'affiche, proposant des liens vers d'autres pages de l'application. En dessous du menu se trouve un bouton de déconnexion pour une expérience utilisateur complète.
  1. #### **Back-end**
Du côté du back-end, la logique est relativement simple, car la page Menu est principalement axée sur l'interface utilisateur et la navigation. Voici ce que nous gérons du côté du back-end:

- **Vérification de l'Authentification** : Avant de permettre l'accès à la page Menu, le back-end utilise la fonction "is\_authenticated" fournie par Django pour vérifier si l'utilisateur est authentifié. Cette vérification garantit que seuls les utilisateurs autorisés accèdent à cette section de l'application.
- **Redirection** : Si l'utilisateur n'est pas authentifié, il est automatiquement redirigé vers la page d'authentification. Cette mesure de sécurité garantit que seuls les utilisateurs autorisés peuvent accéder au menu de l'application.
  1. #### **Capture d’écran de l’interface**
![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.013.png)

<a name="_toc148122993"></a>**Figure 54 Capture de page Menu PQG Controller**
1. ### <a name="_toc148123394"></a>**Page Aujourd’hui /Hier** 
   1. #### **Front-end**
Pour La page "Aujourd'hui/Hier" de notre application offre une interface utilisateur riche en informations, conçue pour fournir une vue détaillée des données pertinentes. Voici les principales caractéristiques de la partie front-end :

- **Barre de Navigation (Navbar)** : Tout comme sur la page Menu, en haut de la page, une barre de navigation bien organisée facilite la navigation. Elle contient des liens vers différentes parties de l'application, ainsi qu'un menu latéral affiché au clic sur le bouton de l'utilisateur.
- **Menu de l'Utilisateur** : Le bouton de l'utilisateur déclenche un menu latéral qui permet à l'utilisateur de naviguer vers d'autres sections de l'application. De plus, un bouton de déconnexion est disponible pour une expérience utilisateur complète.

- **Tableau des Top 8 Défauts** : Au centre de la page, un tableau présente les huit défauts les plus fréquemment détectés. Ce tableau fournit des informations essentielles sur ces défauts.
- **Cartes d'Informations** : À droite du tableau des défauts, quatre cartes affichent des statistiques essentielles, telles que le nombre de véhicules produits, le nombre de défauts détectés par DVX, le nombre de défauts détectés par PQG, et le nombre de défauts détectés par à la fois PQG et DVX.
- **Graphes en Barres** : En bas de la page, deux graphiques en barres, créés à l'aide de Chart.js, présentent des données cruciales. Le premier graphe montre le pourcentage d'efficacité pour chaque PQG, tandis que le deuxième répartit cette efficacité entre les équipes A, B et N.
- **Sélecteur de Méthode de Données** : En haut de la page, un sélecteur permet de choisir la méthode de collecte de données. Étant donné une contrainte concernant les données brutes du système, nous avons ajouté cette méthode basée sur l'heure d'entrée des véhicules dans notre atelier de montage.
  1. #### **Back-end**
Du côté du back-end, la page "Aujourd'hui/Hier" s'appuie sur une logique robuste pour collecter, calculer et afficher les données pertinentes. Voici ce que nous gérons du côté du back-end :

- **Calcul des Données** : Le back-end effectue des calculs complexes pour recueillir les données nécessaires à l'affichage des défauts, des statistiques et des graphiques.
- **Affichage des Graphiques** : Les graphiques en barres sont générés à l'aide de la bibliothèque Chart.js pour présenter les données sous une forme visuellement compréhensible. 


1. #### **Capture d’écran de l’interface**

![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.014.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.015.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.016.png)



1. ### <a name="_toc148122994"></a><a name="_toc148123395"></a>**Page DATA** 
   1. #### **Front-end**
La page "DATA" de notre application présente une interface utilisateur similaire à celle des autres pages , avec une barre de navigation (Navbar) et un menu latéral (Sidebar). Cependant, son contenu diffère pour fournir des informations spécifiques. Voici les principales caractéristiques de la partie front-end :

- **Barre de Navigation (Navbar)** : La barre de navigation en haut de la page offre des options de navigation, tout comme sur la page Menu.
- **Menu Latéral (Sidebar)** : Le menu latéral contient deux boutons d'action :
- **"Nombre de Défauts par Poste PQG et Équipe"** : Lorsque l'utilisateur clique sur ce bouton, l'application affiche un tableau présentant les données sur le nombre de défauts par poste PQG et par équipe.
- **"Défauts les Plus Détectables"** : En cliquant sur ce bouton, l'application affiche un tableau fournissant des informations sur les défauts les plus fréquemment détectés.
  1. #### **Back-end**
Du côté du back-end, la page "Aujourd'hui/Hier" suit une logique similaire à celle décrite précédemment, car elle implique la collecte, le calcul et la présentation des données pertinentes. Voici ce que nous gérons du côté du back-end :

- **Calcul des Données** : Le back-end effectue des calculs pour recueillir les données nécessaires pour les deux tableaux mentionnés.
- **Affichage des Tableaux** : En fonction du bouton sélectionné par l'utilisateur, le back-end génère et affiche le tableau correspondant avec les données calculées. 
  1. #### **Captures d’écran des interfaces**
![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.017.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.018.png)

<a name="_toc148122995"></a>**Figure 56 captures du page DATA PQG Controller**
1. ### <a name="_toc148123396"></a>**Page  STATISTIQUES**
   1. #### **Front-End**
- **Barre de Navigation (Navbar) et Menu Latéral (Sidebar) :**Tout comme sur les autres pages de l'application, la page Front-End dispose d'une barre de navigation en haut (Navbar) pour la navigation générale et d'un menu latéral (Sidebar) pour les options spécifiques. Cela garantit une cohérence dans l'interface utilisateur.
- **Sélecteurs pour Personnalisation** : La page Front-End propose trois sélecteurs pour personnaliser l'affichage des données :
  - **Sélecteur de Période (7 jours, 14 jours, 30 jours)** : L'utilisateur peut choisir la période de 7 jours à 30 jours pour laquelle il souhaite voir les données.
  - **Sélecteur de PQG** : L'utilisateur peut sélectionner l'un des PQG (Postes de Contrôle Qualité) disponibles pour lesquels il souhaite afficher les données.
  - **Sélecteur de Méthode d'Extraction des Données** : L'utilisateur peut choisir entre deux méthodes d'extraction de données : basées sur les données brutes ou basées sur l'heure d'entrée (EMON).
- **Bouton de Soumission :** Une fois que l'utilisateur a fait ses sélections, il peut cliquer sur un bouton "Soumettre" pour générer les graphiques et le tableau correspondants.
- **Graphiques Line Chart :** Suite à la soumission, l'application génère deux graphiques Line Chart :
- **Changement d'Efficacité du PQG par Jours** : Ce graphique montre comment le pourcentage d'efficacité du PQG sélectionné a évolué au fil des jours dans la période choisie.
- **Changement de l'Efficacité des Équipes A, B, N par Jours** : Ce graphique illustre comment l'efficacité des équipes A, B et N a varié au cours des jours dans la période spécifiée.
- **Tableau des Défauts Détectés :** En plus des graphiques, l'application génère un tableau qui présente un Pareto des défauts détectés au cours de la période choisie par le PQG sélectionné. Ce tableau offre une vue détaillée des types de défauts et de leur fréquence relative. 
  1. #### **Back-End**
La partie Back-End de la page Front-End joue un rôle crucial dans la collecte, le calcul et la présentation des données. Voici comment ces opérations sont gérées :

- **Collecte des Données :** Le Back-End commence par collecter les données nécessaires à partir de diverses sources de données, telles que des bases de données internes, des fichiers de logs, ou des services d'API externes. Ces données incluent les informations sur l'efficacité des PQG, les performances des équipes A, B et N, ainsi que les détails sur les défauts détectés.
- **Traitement des Données :** Une fois les données collectées, elles sont traitées pour les préparer à la visualisation. Cela peut inclure le nettoyage des données, le calcul des statistiques et la structuration en vue de la génération de graphiques et de tableaux.
- **Génération des Graphiques :** Pour générer les graphiques Line Chart, le Back-End utilise une bibliothèque de graphiques telle que Chart.js. Les données sont formatées de manière appropriée, puis utilisées pour créer les graphiques montrant l'évolution de l'efficacité du PQG et des équipes au fil des jours.
- **Génération du Tableau des Défauts :** Le Back-End génère également un tableau présentant un Pareto des défauts détectés. Les données sont triées et résumées pour montrer les types de défauts les plus fréquents, offrant ainsi une vue détaillée de la qualité des produits.
  1. #### **Capture d’écran de l’interface**

![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.019.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.020.png)![](Readme/Aspose.Words.8b2f661c-4da3-49d0-b99e-c638213380cd.021.png)






1. ### <a name="_toc148122996"></a><a name="_toc148123397"></a>**Page  Paramètre**
   1. #### **Front-End**
La page "Paramètres" de notre application offre aux utilisateurs la possibilité de personnaliser divers aspects de leur expérience, avec plusieurs formulaires disponibles. Voici les principaux éléments de la partie front-end :

- **Formulaire "Paramètres PQG"** : Ce formulaire permet aux utilisateurs administrateurs de configurer des paramètres spécifiques aux PQG (Postes de Contrôle Qualité).
- **Formulaire "Ajouter PQG"** : Les administrateurs peuvent utiliser ce formulaire pour ajouter de nouveaux PQG à l'application.
- **Formulaire "Rendre un Utilisateur Admin"** : Ce formulaire est accessible uniquement aux administrateurs et leur permet de promouvoir un utilisateur standard au statut d'administrateur.
- **Formulaire "Changer l'Objectif"** : Les utilisateurs administrateurs ont la possibilité de modifier les objectifs à l'aide de ce formulaire.
- **Formulaire "Paramètre du Compte"** : Ce formulaire est visible pour tous les utilisateurs, quel que soit leur statut, et leur permet de changer leur mot de passe .
  1. #### **Back-End**
Du côté du back-end, la page "Paramètres" gère le traitement des données et la vérification du mot de passe pour les champs nécessitant une confirmation. Voici comment cela est géré:

- **Vérification du Mot de Passe** : Chaque fois qu'un utilisateur souhaite effectuer une modification qui nécessite la confirmation du mot de passe (par exemple, changer l'objectif ou promouvoir un utilisateur en administrateur), le back-end vérifie que le mot de passe saisi est correct avant d'autoriser la modification.
- **Traitement des Données de Paramètres PQG** : Les données entrées dans le formulaire "Paramètres PQG" sont traitées par le back-end pour mettre à jour les paramètres spécifiques aux PQG.
- **Ajout de Nouveaux PQG** : Le back-end gère l'ajout de nouveaux PQG à l'application à partir du formulaire "Ajouter PQG".
- **Promotion en Administrateur** : Lorsqu'un administrateur souhaite promouvoir un utilisateur standard en administrateur, le back-end effectue les modifications nécessaires dans la base de données.
- **Modification des Objectifs** : Les modifications de l’objectif de l'application sont prises en charge par le back-end.
- **Gestion des Paramètres de Compte** : Le back-end traite également les modifications des mots de passe de compte utilisateur.
1. # <a name="_toc148123398"></a>**WEB SCRAPING**
Pour accéder aux données de NEO qui est responsable des bases de données dans l'usine, nous avons mis en place un processus d'extraction automatisée en utilisant le web scraping. Cette approche était nécessaire car l'accès direct aux données n'était pas disponible pour l'équipe en charge de la transformation numérique. Voici comment nous avons réalisé cette tâche complexe :

- **Utilisation de Selenium et WebDriver** : Nous avons utilisé la bibliothèque Selenium en conjonction avec un WebDriver adapté à notre navigateur web pour automatiser l'interaction avec l'interface de l'application responsable des bases de données. Cela nous a permis de naviguer dans l'application, de saisir des requêtes et d'extraire les données nécessaires.

DRIVER\_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable\_path=DRIVER\_PATH)
driver.get('https://username:psswd@neo.inetpsa.com/qualite/init-vehicles-search.do')

- **Traitement des Fichiers Excel avec Pandas et xlrd** : Une fois les données extraites, elles étaient généralement dans un format Excel. Pour les traiter efficacement, nous avons utilisé la bibliothèque Pandas pour la manipulation des données tabulaires. La bibliothèque xlrd nous a permis de lire les fichiers Excel.
- **Déplacement et Renommage des Fichiers avec OS** : Après avoir extrait et traité les données, nous avons automatisé leur déplacement vers l'emplacement souhaité en utilisant la bibliothèque OS. Nous avons également géré le renommage des fichiers si nécessaire pour assurer une organisation cohérente des données.

downloads\_folder = os.path.expanduser('~') + '\\Downloads\\'
new\_filename = 'PQGAPP.xls'
if os.path.exists(downloads\_folder + new\_filename):
`    `os.remove(downloads\_folder + new\_filename)
os.rename(downloads\_folder + 'SE39040\*', "./" + new\_filename)

- **Insertion des Données dans la Base de Données avec PySQL** : Enfin, nous avons inséré les données extraites et traitées dans la base de données de l'application en utilisant la bibliothèque PySQL, en veillant à respecter la structure de la base de données et à suivre les procédures d'insertion appropriées.

file\_path="PQGAPP.xls"
sheet='NEO'
workbook = xlrd.open\_workbook(file\_path, encoding\_override='utf-8')
df = pd.read\_excel(workbook,sheet\_name=sheet,usecols=['VIS', 'Date/heure de passage (porte physique)'])
df.columns = ['VIS', 'EMON']
df.to\_sql('VIS', con=engine, if\_exists='append', index=True)

Ce processus automatisé de web scraping et de gestion des données a permis à l'équipe de la transformation numérique d'accéder aux informations cruciales de l'application responsable des bases de données, garantissant ainsi une utilisation efficace de ces données pour le besoins de PQG Controller et opérationnels de l'usine **STELLANTIS**.
1. # <a name="_toc148123399"></a>**CONCLUSION**
En conclusion, ce projet a abouti à la création d'une application de contrôle de la qualité des véhicules qui allie une interface utilisateur conviviale, des fonctionnalités de back-end solides et une gestion efficace des données. Le front-end offre des formulaires interactifs, des graphiques et des tableaux pour une visualisation claire des données, tandis que le back-end assure la sécurité des données avec des vérifications de mots de passe et une manipulation de données efficace. Cette application vise à améliorer le contrôle de la qualité des véhicules en offrant des outils flexibles pour le suivi, l'analyse et la personnalisation, contribuant ainsi à l'amélioration continue de la qualité des produits dans l'industrie automobile.

