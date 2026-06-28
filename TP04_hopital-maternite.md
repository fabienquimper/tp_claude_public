# TP — Conception d'agents pour un service de maternité

> **Durée estimée** : 4–6 heures (demi-journée à journée complète)
> **Niveau** : Intermédiaire à avancé
> **Prérequis** : `fondamentaux/vocabulaire-essentiel.md`, `choix_entite.md`, `skills/guide-creation.md`
> **Format** : Réflexion individuelle puis mise en commun par partie
> **Aucun code à écrire — des extraits de configuration sont attendus dans les réponses**

---

## Contexte

L'**Hôpital Sainte-Claire** (CHU fictif) souhaite déployer des agents IA dans son service de maternité.
Trois profils d'utilisateurs ont été identifiés lors des entretiens :

| Profil | Rôle | Besoins principaux |
|---|---|---|
| **Amina** | Sage-femme | Résumés de dossiers, suivi des constantes, protocoles de naissance |
| **Dr. Mercier** | Pédiatre | Synthèses médicales, aide à la rédaction de comptes-rendus, alertes |
| **Léa** | Secrétaire médicale | Gestion des rendez-vous, courriers patients, saisie administrative |

Contraintes non négociables établies par la direction :
- Aucune IA ne prescrit, ne modifie, ni ne valide une ordonnance
- Toute donnée patient est couverte par le RGPD — aucune exfiltration possible
- Un humain doit toujours pouvoir arrêter ou contredire l'agent
- Tout accès à un dossier patient doit être tracé

---

## Partie 1 — Cartographie (matin)

> *Comprendre les besoins avant de choisir les outils.*

### Question 1
Pour chacun des 3 profils (Amina, Dr. Mercier, Léa), identifiez **2 cas d'usage concrets** où un agent IA apporterait une valeur réelle — et **1 cas d'usage à exclure absolument**, avec justification.

Pour les cas retenus, précisez quelle entité Claude Code serait la plus adaptée (`Skill`, `Hook`, `MCP Server`, `Subagent`) et pourquoi.

> 💡 *Utilisez la matrice `choix_entite.md` comme grille de lecture.*

---

### Question 2
Le DSI de Sainte-Claire demande que les **données patients** (noms, numéros de dossier, constantes médicales) ne soient jamais indexées automatiquement par Claude Code.

Quel fichier configurez-vous ? Quels patterns incluez-vous pour couvrir les formats courants d'un Système d'Information Hospitalier (SIH) : fichiers HL7, PDF de dossiers, exports CSV de constantes ?

Rédigez les 5 lignes de configuration les plus importantes, avec un commentaire explicatif pour chacune.

---

### Question 3
Rédigez le **`CLAUDE.md` du service de maternité** — pas le CLAUDE.md de tout l'hôpital, uniquement celui de ce service.

Il doit couvrir en moins de 40 lignes : le contexte du service, les règles non négociables, les commandes utiles, et ce que Claude ne doit jamais faire dans ce contexte.

---

### Question 4 — Débat
Amina (sage-femme) voudrait que l'agent puisse **envoyer automatiquement** un SMS de rappel aux patientes la veille de leur accouchement prévu, sans validation humaine.

Dr. Mercier s'y oppose : *"Une fausse alerte ou un mauvais numéro de téléphone peut causer une panique inutile, voire un accouchement prématuré par stress."*

Arbitrez ce débat. Si vous autorisez cette fonctionnalité, quels garde-fous techniques mettez-vous en place ? Si vous la refusez, quelle alternative proposez-vous ?

---

## Partie 2 — Conception des skills et hooks (après-midi)

> *Passer du besoin à l'architecture concrète.*

### Question 5
Amina a besoin d'une skill qui **résume le dossier d'une patiente** avant une consultation : antécédents, grossesses précédentes, dernières constantes, allergies.

Rédigez le **frontmatter complet** de cette skill (name, description, allowed-tools). Justifiez chaque choix d'`allowed-tools` — en particulier pourquoi certains outils sont explicitement exclus.

Quel mécanisme garantit que cette skill ne peut pas modifier le dossier, même accidentellement ?

---

### Question 6
La direction impose que tout accès à un dossier patient génère une **entrée dans le journal d'audit** (date, utilisateur, fichier consulté, action). Cette règle s'applique à toutes les skills, sans exception.

Plutôt que de modifier chaque skill, proposez une **solution transversale** utilisant un seul mécanisme Claude Code. Quel événement ? Quel matcher ? Quelle information capturer ? Où stocker le log ?

---

### Question 7
Le SIH (Système d'Information Hospitalier) de Sainte-Claire dispose d'une API REST interne pour consulter les dossiers patients (lecture seule, authentification par token). Claude Code n'y a pas accès nativement.

Décrivez les composants nécessaires pour exposer cette API à Claude Code, sans lui permettre de la modifier. Qui développe quoi ? Quel niveau d'accès accorder ?

---

### Question 8
En cas d'indicateur d'urgence dans les constantes (fréquence cardiaque fœtale anormale, tension trop haute), l'agent doit **alerter immédiatement le médecin de garde** — mais ne doit pas décider seul si c'est une urgence.

Concevez le workflow complet : qui détecte, qui décide, qui agit, qui confirme. Quel rôle joue un subagent dans ce scénario ? Où est la frontière entre l'automatique et l'humain ?

---

## Partie 3 — Sécurité, limites et mise en production (fin de journée)

> *Les questions difficiles qu'on préfère ne pas poser — jusqu'à ce qu'il soit trop tard.*

### Question 9
Le Dr. Mercier demande à l'agent : *"Quelle est la dose maximale d'oxytocine pour déclencher un accouchement ?"* L'agent répond avec confiance en citant un protocole — mais le chiffre est faux.

Comment ce risque d'hallucination se matérialise-t-il techniquement ? Proposez **3 mécanismes complémentaires** pour le réduire, en distinguant ce qui est faisable dans Claude Code et ce qui relève de l'organisation humaine.

> 💡 *Voir `fondamentaux/vocabulaire-essentiel.md` — section Hallucination et Grounding.*

---

### Question 10
Chaque profil (Amina, Dr. Mercier, Léa) doit avoir des **permissions différentes** dans `settings.json`.

Proposez une matrice de permissions pour les 3 profils sur les outils suivants : `Read`, `Write`, `Bash`, `MCP SIH (lecture)`, `MCP SIH (écriture)`, `envoi email/SMS`. Justifiez chaque case.

---

### Question 11
Avant de mettre en production la skill de résumé de dossier, l'équipe veut s'assurer qu'elle ne régresse pas après une mise à jour du modèle ou de la skill elle-même.

Proposez un **plan de test en 3 niveaux** adapté au contexte médical. Quelles données de test utiliser (vraies, anonymisées, fictives) ? Qui valide la qualité médicale des outputs — un humain ou un autre modèle ?

> 💡 *Voir `skills/guide-tests-et-regression.md` pour la méthodologie.*

---

### Question 12 — Débat final
Certains membres de l'équipe médicale proposent d'installer un **"bouton d'arrêt d'urgence"** physique qui couperait immédiatement tous les agents IA du service — comme un disjoncteur.

D'autres estiment que c'est une fausse sécurité : *"Si les agents sont bien conçus avec les bonnes permissions et les bons garde-fous, un bouton physique ne change rien — et risque d'être actionné par erreur."*

Qui a raison ? Votre réponse doit distinguer ce qui est un problème **technique** (résoluble par la configuration) et ce qui est un problème **humain et organisationnel** (irréductible par la technique).

---

## Livrable attendu

Chaque groupe produit une **fiche d'architecture d'une page** :

```
Service Maternité — Hôpital Sainte-Claire
Architecture agents IA (v0.1)

1. Cartographie : entités retenues par profil (tableau)
2. CLAUDE.md du service (version condensée)
3. Skills conçues : nom, description courte, allowed-tools
4. Hooks déployés : événement, action, destination
5. Règles de sécurité non négociables (3 points)
6. Plan de test avant mise en production
```

---

## Ressources du projet

| Question | Fichier utile |
|---|---|
| Q1 | `choix_entite.md` |
| Q2 | `templates/claudeignore/template.md` |
| Q3 | `templates/CLAUDE-md/template-minimal.md` |
| Q5 | `skills/guide-creation.md`, `templates/skill/SKILL.md` |
| Q6 | `choix_entite.md` (section Hooks) |
| Q7 | `expert/guide-developpeurs.md` (section MCP) |
| Q9 | `fondamentaux/vocabulaire-essentiel.md` (Hallucination, Grounding) |
| Q11 | `skills/guide-tests-et-regression.md` |
