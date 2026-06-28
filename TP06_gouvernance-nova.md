# TP — Gouvernance et déploiement de Claude Code en entreprise

> **Durée estimée** : 6–7 heures (journée complète)
> **Niveau** : Intermédiaire à avancé
> **Prérequis** : Avoir lu `fondamentaux/vocabulaire-essentiel.md` et `choix_entite.md`
> **Format** : Réflexion individuelle puis débat en groupe — aucun code à écrire

---

## Contexte du TP — Le Centre NOVA

Le **Centre de Formation Professionnelle NOVA** est un organisme de formation continue
qui emploie 120 personnes et forme 3 000 apprenants par an. La direction vient de valider
le déploiement de Claude Code dans toute l'organisation.

NOVA est structuré en **4 équipes** :


| Équipe            | Taille       | Mission principale                              |
| ------------------ | ------------ | ----------------------------------------------- |
| **Pédagogie**     | 35 personnes | Concevoir et animer les formations              |
| **Contenu**        | 20 personnes | Produire supports de cours, vidéos, ressources |
| **Marketing**      | 15 personnes | Acquisition, communication, landing pages       |
| **Administration** | 50 personnes | RH, finance, logistique, relation apprenants    |

Chaque équipe a désigné un **référent IA** qui participera au comité de gouvernance.
Vous êtes consultant·e mandaté·e pour les aider à concevoir leur architecture Claude Code.

---

## Structure de la journée


| Temps | Partie       | Thème                                                  |
| ----- | ------------ | ------------------------------------------------------- |
| 1h30  | **Partie 1** | Cartographier les besoins — quelle entité pour quoi ? |
| 1h30  | **Partie 2** | Gouvernance et structure des settings                   |
| 1h30  | **Partie 3** | Concevoir et organiser les skills par équipe           |
| 1h15  | **Partie 4** | Cycle de vie, mises à jour, dépréciation             |
| 45m   | **Partie 5** | Synthèse — présenter votre plan de déploiement      |

---

## Partie 1 — Cartographier les besoins

> *Avant de déployer quoi que ce soit, on comprend ce que chaque équipe attend.*

### Contexte de la partie

Lors des entretiens préliminaires, les 4 référents IA ont exprimé ces besoins :

- **Pédagogie** : *"On veut que Claude génère des quiz à partir de nos supports de cours, révise nos plans de formation, et nous aide à donner du feedback sur les travaux des apprenants."*
- **Contenu** : *"On a besoin d'aide pour rédiger des scripts vidéo, reformuler des textes selon notre charte éditoriale, et vérifier la cohérence des supports avant publication."*
- **Marketing** : *"On veut automatiser la rédaction de newsletters, générer des variantes d'emails selon les segments d'apprenants, et analyser les performances de nos campagnes."*
- **Administration** : *"On a besoin de résumer les dossiers d'inscription, générer des conventions de formation conformes au droit, et répondre aux emails courants des apprenants."*

---

### Question 1

Pour chacune des 4 équipes, identifiez **quelles entités Claude Code** seraient les plus adaptées parmi : `CLAUDE.md`, `Skill`, `Hook`, `MCP Server`, `Agent SDK`.

Justifiez chaque choix en une phrase. Appuyez-vous sur la matrice `choix_entite.md`.

> 💡 *Indice : certains besoins semblent similaires mais n'impliquent pas les mêmes entités selon le niveau d'automatisation souhaité.*

---

### Question 2

L'équipe Administration mentionne la génération de **"conventions de formation conformes au droit"**. Ce document a une valeur légale.

Quel mécanisme de Claude Code pourrait garantir qu'un humain valide toujours le document avant envoi ? Décrivez le workflow complet, de la demande à la signature.

> 💡 *Pensez aux hooks, aux permissions, et à la notion de blast radius.*

---

### Question 3

Le directeur technique soulève un point : *"Chaque équipe a des besoins différents, mais on ne veut pas que chaque équipe fasse n'importe quoi de son côté. Il faut un socle commun."*

Proposez une **architecture de fichiers** (`CLAUDE.md`, `settings.json`, dossiers) qui permette à la fois :

- Un socle de règles communes à toute l'organisation NOVA
- Des règles spécifiques par équipe
- Une indépendance des équipes pour leurs propres skills

Dessinez ou décrivez la structure de dossiers.

---

**Pause — 10h30 à 10h45**

---

## Partie 2 — Gouvernance et structure des settings

> *Qui a le droit de faire quoi ? Comment le harness fait respecter les règles ?*

### Contexte de la partie

Après votre cartographie, le comité de gouvernance NOVA se réunit. Voici les tensions qui émergent :

- La **DRH** : *"Je ne veux pas que Claude puisse envoyer des emails au nom de l'organisation sans supervision."*
- Le **référent IA Contenu** : *"Si on doit demander une autorisation à chaque fois qu'on veut utiliser une skill, ça va être inutilisable."*
- Le **RSSI** (Responsable Sécurité) : *"Les skills créées par les équipes doivent être auditées avant déploiement. Et certaines commandes shell sont hors de question."*
- Le **référent IA Pédagogie** : *"On voudrait que nos skills soient automatiquement testées à chaque mise à jour."*

---

### Question 4

Le RSSI veut **interdire certaines commandes** dans toute l'organisation, quel que soit l'utilisateur ou l'équipe.

Dans quel fichier cette règle doit-elle être écrite ? Comment la syntaxe `deny` dans `settings.json` permet-elle de bloquer, par exemple, toute commande `curl` ou tout accès à `/etc/` via Bash ?

Écrivez la configuration `settings.json` correspondante (pas de code d'exécution — juste la configuration JSON).

---

### Question 5

Le référent IA Contenu a raison : demander une confirmation à chaque appel d'outil rendrait le système inutilisable. Mais la DRH a aussi raison sur les emails.

Proposez une **stratégie de permissions graduées** pour l'équipe Contenu :

- Quels outils peuvent être approuvés automatiquement (sans confirmation) ?
- Quels outils nécessitent une confirmation ?
- Quels outils sont interdits ?

Justifiez chaque décision par le niveau de réversibilité de l'action.

---

### Question 6

Le référent IA Pédagogie veut un **hook qui lance automatiquement les tests** d'une skill à chaque fois qu'elle est modifiée.

Quel événement de hook utiliser ? Sur quel `matcher` ? Quel serait le risque si ce hook bloque (exit code non-zéro) et comment le gérer sans bloquer le travail de l'équipe ?

---

### Question 7

NOVA envisage de **centraliser toutes les skills** dans un repo GitHub interne, accessible à toutes les équipes. Mais les équipes veulent aussi pouvoir créer leurs propres skills localement.

Décrivez la **politique de gouvernance** des skills que vous recommandez : qui peut créer une skill ? Qui valide ? Comment distinguer une "skill officielle NOVA" d'une "skill expérimentale d'équipe" ?

> 💡 *Référez-vous à `skills/banques-de-skills.md` — section gouvernance.*

---

**Déjeuner — 12h15 à 13h30**

---

## Partie 3 — Concevoir les skills par équipe

> *On passe du concept à la conception — sans coder, mais en détaillant précisément.*

### Contexte de la partie

Le comité valide votre architecture. Maintenant, chaque équipe doit concevoir ses premières skills. Vous accompagnez l'équipe **Pédagogie** en priorité, car c'est la plus grande et son usage est le plus sensible (feedback sur les travaux d'apprenants).

---

### Question 8

L'équipe Pédagogie veut une skill `generating-quiz-from-content`.

Rédigez le **frontmatter complet** de cette skill (`name`, `description`, `allowed-tools`) en respectant toutes les contraintes de nommage vues dans `skills/guide-creation.md`.

Puis justifiez votre choix d'`allowed-tools` : pourquoi ces outils et pas d'autres ?

---

### Question 9

Une formatrice soulève un problème : *"Quand Claude génère un quiz, parfois les questions sont trop faciles, parfois hors sujet. Comment s'assurer que la skill produit toujours un résultat pédagogiquement valide ?"*

Sans modifier le SKILL.md, proposez **deux mécanismes complémentaires** qui permettent de contrôler la qualité des outputs de cette skill, en vous appuyant sur le vocabulaire et les outils vus dans ce projet.

---

### Question 10

L'équipe Administration a un besoin particulier : générer des **conventions de formation** à partir d'un modèle Word interne stocké sur leur serveur SharePoint.

Claude Code ne peut pas accéder à SharePoint nativement. Quelle solution proposez-vous ? Décrivez les composants nécessaires, qui les crée, et comment ils s'articulent.

---

### Question 11 — Débat de groupe

*(20 minutes — à discuter en équipe)*

L'équipe Marketing veut créer une skill qui **publie automatiquement** des posts LinkedIn depuis Claude, sans confirmation humaine, dès qu'une campagne est validée en interne.

Arguments **pour** et **contre** cette automatisation totale. Quelle position recommandez-vous à NOVA, et quelles garde-fous proposez-vous si vous autorisez ce cas ?

---

**Pause — 15h00 à 15h15**

---

## Partie 4 — Cycle de vie : maintenir un écosystème de skills

> *Un déploiement réussi, c'est aussi savoir faire évoluer et retirer ce qu'on a créé.*

### Contexte de la partie

Six mois après le déploiement, NOVA a 23 skills actives. Voici la situation :

- La skill `reviewing-training-content` (Pédagogie) a été créée par une formatrice qui a quitté l'organisation. Personne ne sait exactement ce qu'elle fait.
- La skill `generating-newsletters` (Marketing) produit des emails avec la mauvaise charte graphique depuis la refonte du site il y a 3 semaines.
- Deux skills de l'équipe Contenu font quasiment la même chose : `reformulating-text` et `rewriting-for-clarity`. Les utilisateurs ne savent pas laquelle choisir.
- Une nouvelle réglementation impose que toute communication vers des apprenants soit archivée. Aucune skill actuelle ne respecte cette règle.

---

### Question 12

Pour la skill orpheline `reviewing-training-content`, décrivez le **processus de reprise en main** que vous recommandez avant de décider de la maintenir ou de la déprécier.

Quelles informations minimales chercher ? Où les chercher dans le projet ? Qui impliquer ?

---

### Question 13

La skill `generating-newsletters` est en production et utilisée quotidiennement. Sa mise à jour est urgente mais risquée.

Proposez une **stratégie de mise à jour sans coupure de service** : comment tester la nouvelle version en parallèle de l'ancienne, comment basculer, et comment revenir en arrière si nécessaire ?

---

### Question 14

Pour les deux skills redondantes, vous devez décider : les fusionner ou en déprécier une ?

Listez les **critères de décision** que vous utiliseriez, et décrivez le processus de dépréciation propre en vous appuyant sur `skills/cycle-de-vie.md`.

---

### Question 15

La nouvelle obligation d'archivage doit s'appliquer à **toutes** les skills qui génèrent des communications vers des apprenants, sans modifier chaque skill une par une.

Proposez une solution architecturale. Quel mécanisme de Claude Code permet d'ajouter un comportement transversal à plusieurs skills sans les modifier individuellement ?

---

**Pause — 16h30 à 16h45**

---

## Partie 5 — Synthèse et présentation

> *Vous présentez votre plan au comité de direction de NOVA.*

### Question 16 — Livrable final *(travail de groupe, 45 minutes)*

Chaque groupe produit un **document de gouvernance Claude Code pour NOVA** d'une page maximum, structuré ainsi :

```
1. Architecture retenue (3 points clés)
2. Matrice des permissions par équipe (tableau)
3. Processus de création d'une skill officielle (5 étapes max)
4. 3 règles non négociables de sécurité
5. Plan de montée en compétence des équipes (3 phases)
```

Ce document sera présenté oralement en 5 minutes par groupe, suivi de 5 minutes de questions.

---

## Grille d'évaluation


| Critère                        | Indicateurs                                                     | Points |
| ------------------------------- | --------------------------------------------------------------- | ------ |
| **Maîtrise des concepts**      | Utilisation correcte du vocabulaire, entités bien choisies     | /20    |
| **Pertinence architecturale**   | Cohérence de la structure proposée, pas de sur-ingénierie    | /20    |
| **Sens de la gouvernance**      | Équilibre entre contrôle et autonomie, justifications solides | /20    |
| **Gestion des risques**         | Blast radius pris en compte, mécanismes de contrôle           | /20    |
| **Clarté de la communication** | Document lisible, présentation convaincante                    | /20    |

---

## Ressources à disposition pendant le TP


| Question      | Ressource utile                                                      |
| ------------- | -------------------------------------------------------------------- |
| Q1, Q2, Q3    | `choix_entite.md`                                                    |
| Q4, Q5, Q6    | `fondamentaux/vocabulaire-essentiel.md` (section Permissions, Hooks) |
| Q7            | `skills/banques-de-skills.md`                                        |
| Q8, Q9        | `skills/guide-creation.md` + `templates/skill/SKILL.md`              |
| Q10           | `expert/guide-developpeurs.md` (section MCP)                         |
| Q12, Q13, Q14 | `skills/cycle-de-vie.md`                                             |
| Q15           | `choix_entite.md` (section Hooks)                                    |
| Q16           | Tout le projet                                                       |
