# Introduction

[![PyPi](https://img.shields.io/pypi/v/iparapheur-utils.svg)](https://pypi.org/project/iparapheur-utils)

C'est principalement une librairie écrite en Python permettant la communication avec le i-Parapheur en version 4.2+, au travers de l'API REST ou via webservice SOAP.

Elle offre des commandes accessibles depuis un shell standard, pour faciliter certaines opérations d'exploitation.

# Installation

Sur une distribution Ubuntu 18.04 LTS :

* une instance i-Parapheur accessible en v4.4.0 ou plus
* un environnement Python fonctionnel !
* ajout de l'outil ` pip ` depuis un terminal BASH :

```bash
sudo bash
curl https://bootstrap.pypa.io/get-pip.py | python
```

* installation du paquet python `iparapheur-utils`, depuis un terminal BASH :

```bash
sudo pip install iparapheur-utils
```

## Problèmes connus et solutions

### python2 et python3 coexistent sur la machine

Lancer les commandes pour python2, spécifiquement (partant du principe que `python2` pointe sur l'exécutable python 2)

```bash
curl https://bootstrap.pypa.io/get-pip.py | python2
sudo python2 -m pip install iparapheur-utils
```

### Erreur urllib3 : "No module named ordered_dict"

Une dépendance de iparapheur-utils est installée dans une mauvaise version, non supportée (eg urllib3 v 1.24).
Il faut la désinstaller et la réinstaller dans la bonne version (v 1.23).

```bash
sudo pip uninstall urllib3
sudo pip install urllib3==1.23
```

## Cas d'environnement avec MitM

Certains environnements réseau bloquent l'accès à pypi.org, avec un message "SSL Error: Certificate_Verify_Failed".

> Could not fetch URL https://pypi.org/…/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host=’pypi.org’, port=443): Max retries exceeded with url: /…/ (Caused by SSLError(SSLCertVerificationError(1, ‘[ SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: …

Il est possible de passer outre, au prix d'une réduction de la confiance, avec l'argument `--trusted-host`

```bash
sudo pip install --trusted-host pypi.org  iparapheur-utils
```


## Support CentOS / RHEL :

* Version 6 : Cette version n'est plus supportée, en cause une version de python trop ancienne (2.6)
* Version 7 : Cette version requiert l'installation de paquets supplémentaires :  
  `yum install libffi-devel gcc openssl-devel`

# Usage

Ces commandes sont actuellement disponibles :

- [`ph-init`](#ph-init)
- [`ph-check`](#ph-check)
- [`ph-echo`](#ph-echo)
- [`ph-recupArchives`](#ph-recuparchives)
- [`ph-export`](#ph-export)
- [`ph-import`](#ph-import)
- [`ph-rename`](#ph-rename)
- [`ph-removeldap`](#ph-removeldap)
- [`ph-pushdoc`](#ph-pushdoc)
- [`ph-ipclean`](#ph-ipclean)
- [`ph-ldapsearch`](#ph-ldapsearch)
- [`ph-count_files`](#ph-count_files)
- [`ph-reset_admin_password`](#ph-reset_admin_password)
- [`ph-patch`](#ph-patch)

> Remarques : Elles sont conçues pour être exécutées en environnement bash standard: ligne de commande, ou script BASH.  
Aucune qualification à ce stade pour l'usage de ces commandes dans un interpréteur Python.

## `ph-init`

Cette commande permet la génération d'un fichier de configuration "par défaut", qu'il faut bien sûr adapter au serveur.

Exemple d'utilisation :
```bash
usage: ph-init [-h] [-p P] [-c {recuparchives,export,import}]

Génère un fichier de configuration par défaut dans le répertoire courant

Arguments:
  -h, --help            Affiche ce message et quitte
  -p P                  Chemin du fichier de configuration
  -c {recuparchives,export,import}
                        Commande pour laquelle générer le fichier de
                        configuration
```

Le lancement de la commande génère un fichier `iparapheur-utils.cfg`, lu par défaut lors de l'appel des autres fonctions

## `ph-check`

Lance le script de check d'installation. Pas de pré-requis particulier.

## `ph-echo`

Lance la fonction `echo` vers le i-Parapheur désigné dans le fichier de configuration.

Exemple d'utilisation :
```bash
ph-echo -h
---
usage: ph-echo [-h] [-s S] [-c C] [-u U] [-p P]

Lance un echo via webservice sur un iParapheur

Arguments:
  -h, --help  Affiche ce message et quitte
  -s S        URL du serveur iParapheur
  -c C        Fichier de configuration
  -u U        Utilisateur
  -p P        Mot de passe
```

## `ph-recupArchives`

Lance la fonction de récupération ou/et de purge des archives.
Il est vivement conseillé d'utiliser la commande `ph-init -c recuparchives` afin de générer un squelette de fichier de configuration complet.

Exemple d'utilisation :
```bash
ph-recupArchives -h
---
usage: ph-recupArchives [-h] [-s S] [-c C] [-u U] [-p P] [-f F] [-ps PS]
                        [-r {true,false}] [-pu {true,false}] [-d {true,false}]
                        [-t T] [-st ST] [-w W]

Lance une récupération / purge des archives

Arguments:
  -h, --help        Affiche ce message et quitte
  -s S              URL du serveur iParapheur
  -c C              Fichier de configuration
  -u U              Utilisateur
  -p P              Mot de passe
  -f F              Répertoire de destination
  -ps PS            Taille des pages à récupérer
  -r {true,false}   Chemins réduis des téléchargements
  -pu {true,false}  Active la purge les données
  -d {true,false}   Télécharge les données
  -t T              Filtre sur type
  -st ST            Filtre sur sous-type
  -w W              Délai de conservation des données
```

## `ph-export`

Lance la fonction d'exporation de la configuration du parapheur vers un dossier.
Il est vivement conseillé d'utiliser la commande `ph-init -c export` afin de générer un squelette de fichier de configuration complet.
La liste des éléments à exporter peut être modifiée dans ce fichier.

**ATTENTION** : Seule la **configuration** du parapheur est exportée. Comprendre qu'aucun dossier, archive, statistique ou historique n'est conservé.

Exemple d'utilisation :
```bash
usage: ph-export [-h] [-s S] [-c C] [-u U] [-p P] [-i I] [-dh DH] [-dp DP]
                 [-du DU] [-dpw DPW] [-dd DD] [-ou OU] [-og OG] [-ob OB] [-oc OC] [-ot OT] [-om OM] [-oq OQ] [-oa OA]

Exporte la configuration du parapheur ciblé vers un dossier

Arguments:
  -h, --help  Affiche ce message et quitte
  -s S        URL du serveur iParapheur
  -c C        Fichier de configuration
  -u U        Utilisateur administrateur
  -p P        Mot de passe
  -i I        Répertoire de destination
  -dh DH      IP du serveur mysql
  -dp DP      Port du serveur mysql
  -du DU      Utilisateur alfresco de mysql
  -dpw DPW    Mot de passe utilisateur alfresco de mysql
  -dd DD      Nom de la base mysql
  -ou {true,false}      Boolean importe les utilisateurs
  -og {true,false}      Boolean importe les groupes
  -ob {true,false}      Boolean importe les bureaux
  -oc {true,false}      Boolean importe les circuits
  -ot {true,false}      Boolean importe les types et sous-types
  -om {true,false}      Boolean importe les metadatas
  -oq {true,false}      Boolean importe les calques
  -oa {true,false}      Boolean importe les advanced

```

## `ph-import`

Lance la fonction d'importation de la configuration du parapheur à partir d'un dossier.
Il est vivement conseillé d'utiliser la commande `ph-init -c import` afin de générer un squelette de fichier de configuration complet.

**ATTENTION** : Seule la **configuration** du parapheur est importée. Comprendre qu'aucun dossier, archive, statistique ou historique n'est conservé.

Exemple d'utilisation :
```bash
usage: ph-import [-h] [-s S] [-c C] [-u U] [-p P] [-i I] [-dh DH] [-dp DP]
                 [-du DU] [-dpw DPW] [-dd DD]

Importe la configuration ciblée dans un parapheur vierge

Arguments:
  -h, --help  Affiche ce message et quitte
  -s S        URL du serveur iParapheur
  -c C        Fichier de configuration
  -u U        Utilisateur administrateur
  -p P        Mot de passe
  -i I        Répertoire à importer
  -dh DH      IP du serveur mysql
  -dp DP      Port du serveur mysql
  -du DU      Utilisateur alfresco de mysql
  -dpw DPW    Mot de passe utilisateur alfresco de mysql
  -dd DD      Nom de la base mysql
```

## `ph-rename`

Cette commande permet de changer l'URL d'accès au i-Parapheur

Exemple d'utilisation :
```bash
usage: ph-rename [-h] -n N

Change l'URL d'accès du i-Parapheur

Arguments:
  -h, --help  Affiche ce message et quitte
  -n N        Nouvelle URL du serveur iParapheur

```

Le lancement de la commande modifie l'URL d'accès au i-Parapheur mais ne change pas la configuration du certificat serveur.

Il est important de suivre la procédure de changement de certificat serveur donnée après le lancement de la commande.

```bash
ATTENTION ! Le certificat configuré dans le fichier /etc/nginx/conf.d/parapheur_ssl.conf
ne correspond potentiellement plus avec le nouveau nom du parapheur.
Il convient de remplacer ce certificat (localisé dans le dossier /etc/nginx/ssl/)
pour que le parapheur soit totalement fonctionnel.

Propriétés à modifier dans le fichier de configuration /etc/nginx/conf.d/parapheur_ssl.conf :
- ssl_certficiate /etc/nginx/ssl/test.pem;     # Partie publique
- ssl_certficiate_key /etc/nginx/ssl/test.key; # Partie privée

Une fois les modifications de certificat effectuées, relancer le service NginX :
service nginx restart
```

## `ph-removeldap`

Cette commande permet de supprimer les utilisateurs synchronisés avec un LDAP n'ayant aucun bureau liés.

Exemple d'utilisation :
```bash
usage: ph-removeldap [-h]

Supprime les utilisateurs synchronisés LDAP n'ayant aucune liaison avec un bureau

Arguments:
  -h, --help  Affiche ce message et quitte

```

## `ph-pushdoc`

Lance la fonction d'importation de dossier via le connecteur générique Pushdoc.
Il est vivement conseillé d'utiliser la commande ` ph-init -c pushdoc ` afin de générer un squelette de fichier de configuration complet.

**ATTENTION** : Des pré-requis sont nécéssaires avant l'utilisation de cette commande :
- Un jar pushdoc en dernière version dans le même dossier que ce script
- Tout le nécéssaire pour faire fonctionner pushdoc (wsdl, conf.cf, keystore, truststore)
- Le fichier par défaut pour le visuel pdf des flux PES (template-visuelPDF.pdf)

Exemple d'utilisation :
```bash
usage: ph-pushdoc [-h] [-c C] [-j J] [-i I] [-e E] [-x X] [-v V]

Importe la configuration ciblée dans un parapheur vierge

Arguments:
  -h, --help  Affiche ce message et quitte
  -c C        Fichier de configuration
  -j J        Fichier JAR du pushdoc
  -i I        Répertoire à traiter
  -e E        Courriel de l'utilisateur webservice
  -x X        xPath par défaut dans le cas d'un envoi de flux PES
  -v V        Visuel PDF à utiliser dans le cas d'un envoi de flux PES
```

## `ph-ipclean`

Cette commande permet de générer les index automatiquement en supprimant les noeuds dans la base de données, en lançant
la procédure doIPcleantransaction.sql, en supprimant les dossiers ald_data/lucene-indexes et
alf_data/backup-lucene-indexes et en coupant et relançant l'application.

Exemple d'utilisation :
```bash
usage: ph-ipclean [-h]

Génère les index

Arguments:
  -h, --help  Affiche ce message et quitte

```

## `ph-ldapsearch`

Cette commande vérifie que le fichier de conf LDAP est bien présent, que la synchronisation est bien demandée, que le serveur est accessible.
Puis affiche la requête LDAP complète et enfin retourne la liste des utilisateurs correspondants.
Il est vivement conseillé d'utiliser la commande `ph-init -c ldapsearch` afin de générer un squelette de fichier de configuration complet.


Exemple d'utilisation :
```bash
usage: ph-ldapsearch [-h]

Génère des vérifications de propriétés du fichier conf, la requête LDAP, la liste des utilisateurs retournés par celle-ci.

Arguments:
  -h, --help  Affiche ce message et quitte

```


## `ph-count_files`

Cette commande affiche un tableau récapitulatif du nombre de dossier et d'archives par tenant. Les dossiers sont classés par bureau et banette.

Exemple d'utilisation :
```bash
usage: ph-count_files [-h]

Arguments:
  -h, --help  Affiche ce message et quitte

```


## `ph-reset_admin_password`

Cette commande passe le mot de passe de l'utilisateur à "admin".
Il est vivement conseillé d'utiliser la commande `ph-init -c reset_admin_password` afin de générer un squelette de fichier de configuration complet.

Exemple d'utilisation :
```bash
usage: ph-reset_admin_password [-h] [-c C] [-dh DH] [-dp DP] [-du DU] [-dpw DPW] [-dd DD]

Arguments:
  -h, --help  Affiche ce message et quitte
  -c C        Fichier de configuration
  -dh DH      IP du serveur mysql
  -dp DP      Port du serveur mysql
  -du DU      Utilisateur alfresco de mysql
  -dpw DPW    Mot de passe utilisateur alfresco de mysql
  -dd DD      Nom de la base mysql

```

## `ph-patch`

Cette commande déploie le patch.

Il faut au préalable créer un dossier contenant l'archive tar.gz du patch,
et compléter le iparapheur-utils.cfg (en lançant la commande `ph-init -c patch`)

Exemple d'utilisation :
```bash
usage: ph-patch [-h] [-c C] [-u U] [-d D]

Arguments:
  -h, --help  Affiche ce message et quitte
  -c C        Fichier de configuration
  -u U        URL webservice sans le "secure-"
  -d D        dossier du parapheur (par défaut /opt/iParapheur)
```

# Utilisation en librairie

Définir un fichier de configuration `script.cfg` dans le répertoire racine via la commande `ph-init`, qui aura la forme suivante :

```ini
[Parapheur]
username = admin
password = admin
server = secure-iparapheur.dom.local
```

Puis, créer un script python avec utilisation de l'API REST :

```python
#!/usr/bin/env python
# coding=utf-8

import parapheur

# Init REST API client
client = parapheur.getrestclient()

if client.islogged:
    # Do a lot of things...
```

Ou, pour une utilisation avec l'API SOAP :

```python
#!/usr/bin/env python
# coding=utf-8

import parapheur

# Init SOAP API client
webservice = parapheur.getsoapclient()

webservice.call().echo('Coucou, ici python !')
```

Le rendre éxecutable, puis le lancer depuis une console bash :

```bash
chmod +x ./script.py
./script.py
```

# Cas spécifiques

## Proxy

Il est possible de contourner l'usage d'un proxy pour les appels Webservices ou API REST,
si le script à lancer doit communiquer directement avec le serveur i-Parapheur
sans passer par un éventuel proxy défini sur le système.

Pour cela, il suffit d'ajouter la variable **NO_PROXY** avant l'appel d'une fonction ou d'un script.
Par exemple, pour un appel de `ph-echo` vers `secure-iparapheur.dom.local`, la commande sera :

```bash
NO_PROXY="secure-iparapheur.dom.local" ph-echo
```
