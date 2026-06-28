# TP — Gouvernance des agents IA

> **Durée estimée** : 3–4 heures (demi-journée)
> **Niveau** : Intermédiaire
> **Prérequis** : `fondamentaux/vocabulaire-essentiel.md`, `choix_entite.md`
> **Format** : Réflexion individuelle (15 min) → débat en groupe (15 min) par question
> **Aucun code à écrire**

---

## Contexte

Le **Groupe Hospitalier Régional Lumière** (5 cliniques, 2 400 employés) vient de recevoir
un budget pour déployer des agents IA dans ses services. Avant tout déploiement, la direction
et la DSI vous mandatent pour rédiger la **charte de gouvernance des agents**.

Vous n'êtes pas encore en train de configurer quoi que ce soit — vous définissez les **règles du jeu**.

---

## Partie 1 — Qu'est-ce qu'un agent ? (09h00)

> *Avant de gouverner quelque chose, on doit savoir ce que c'est.*

### Question 1
Un médecin utilise un logiciel qui complète automatiquement ses ordonnances selon un protocole figé. Un autre utilise Claude Code qui lit le dossier patient, pose des questions de clarification, et propose un plan de soin en plusieurs étapes.

Lequel est un **agent** ? Lequel est un **outil** ? Quelle est la distinction fondamentale entre les deux, et pourquoi cette distinction change-t-elle tout en termes de responsabilité ?

---

### Question 2
On parle souvent d'"autonomie" pour définir un agent. Mais l'autonomie est un spectre.

Proposez une **échelle de 4 niveaux d'autonomie** pour un agent IA déployé dans un hôpital, du plus supervisé au plus indépendant. Pour chaque niveau, donnez un exemple concret et identifiez qui valide l'action avant qu'elle soit exécutée.

> 💡 *Appuyez-vous sur la notion de blast radius (`vocabulaire-essentiel.md`) pour justifier le niveau de supervision.*

---

### Question 3
Un employé humain a un contrat de travail, une fiche de poste, un règlement intérieur, et une hiérarchie à qui rendre des comptes. Un agent IA déployé avec Claude Code a lui aussi plusieurs "documents constitutifs".

Faites la **correspondance** entre les éléments RH d'un employé et les composants d'un agent Claude Code (`CLAUDE.md`, `settings.json`, skills, hooks, permissions).

---

### Question 4 — Débat
Un agent peut accomplir en 10 minutes ce qu'un humain ferait en 2 heures. Mais un agent peut aussi commettre 1 000 erreurs en 10 minutes sans jamais ressentir de fatigue, de doute, ou de remords.

**Pour ou contre** : *"Un agent IA doit avoir un délai de réflexion obligatoire (confirmation humaine) pour toute action irréversible, même si cela annule le bénéfice de vitesse."*

Structurez votre argumentation en 3 points. Quelle position recommanderiez-vous à la direction du Groupe Lumière ?

---

## Partie 2 — Gouvernance et responsabilité (11h00)

> *Définir qui fait quoi, qui décide quoi, et qui répond de quoi.*

### Question 5
La DSI veut que certaines commandes soient **interdites pour tous les agents**, sans exception : pas d'accès à `/etc/`, pas de `curl` vers l'extérieur, pas de suppression de fichiers patients.

Dans quel fichier et avec quelle syntaxe configurez-vous ces interdictions ? Qui doit avoir le droit de modifier ce fichier, et faut-il versionner cette configuration ? Justifiez.

> 💡 *Voir `choix_entite.md` — dimension sécurité et blast radius.*

---

### Question 6
Un agent du service RH génère par erreur un document avec les données personnelles de 300 employés et l'envoie à une liste de diffusion interne avant qu'un humain puisse l'arrêter.

**Qui est responsable** : le développeur qui a configuré l'agent ? L'utilisateur qui a lancé l'action ? L'organisation qui a déployé sans garde-fou ? Anthropic qui a entraîné le modèle ?

Proposez un **cadre de responsabilité** en 3 niveaux pour le Groupe Lumière, en vous inspirant des pratiques de gouvernance IT existantes (RACI, etc.).

---

### Question 7
Pour être auditables, toutes les actions des agents doivent être tracées. Un agent a lu 12 fichiers, écrit 3 documents, et exécuté 2 commandes shell en une session.

Quel mécanisme de Claude Code permet de logger automatiquement ces actions **sans modifier le comportement de l'agent** ? Décrivez le flux complet : déclencheur, données capturées, destination du log.

---

### Question 8
Le Groupe Lumière envisage de donner aux chefs de service le droit de créer leurs propres agents, sans validation de la DSI.

Quels sont les **3 risques principaux** de cette décision ? Pour chacun, proposez une mesure de mitigation qui préserve l'autonomie des services tout en maintenant un niveau de contrôle minimal.

---

## Partie 3 — Cycle de vie d'un agent (14h00)

> *Un agent qui n'est pas maintenu devient un risque.*

### Question 9
Le Groupe Lumière veut déployer son premier agent : un assistant de rédaction de comptes-rendus médicaux pour le service de cardiologie.

Décrivez les **5 étapes obligatoires** entre "l'idée" et "la mise en production" de cet agent. Qui intervient à chaque étape ? Quel est le critère de passage à l'étape suivante ?

---

### Question 10
Six mois après le déploiement, le modèle Claude sous-jacent est mis à jour par Anthropic. L'agent de cardiologie commence à produire des comptes-rendus dans un style légèrement différent, avec des tournures que les médecins ne reconnaissent pas.

Est-ce une régression ? Comment le détecter avant que les médecins s'en plaignent ? Qui décide si le comportement est acceptable ou non ?

> 💡 *Référez-vous à `skills/guide-tests-et-regression.md` pour les niveaux de test.*

---

### Question 11
Un agent déployé depuis 8 mois n'est plus utilisé — son créateur a quitté l'hôpital, personne ne sait exactement ce qu'il fait, et il tourne encore en arrière-plan avec des permissions larges.

Décrivez la procédure de **mise hors service propre** de cet agent. Quelles informations récolter ? Dans quel ordre agir ? Faut-il l'archiver ou le supprimer ?

---

### Question 12 — Débat final
Dans le droit du travail, un employé bénéficie de protections : il ne peut pas être licencié sans motif, sans préavis, sans procédure. Un agent IA peut être éteint en une commande.

**Faut-il des "droits de l'agent" ?** Non pas pour protéger l'agent (qui n'a pas de conscience), mais pour protéger les utilisateurs qui en dépendent, les données qu'il manipule, et les processus qu'il supporte.

Proposez 3 règles concrètes qui définiraient un "préavis minimal" avant la désactivation d'un agent en production.

---

## Livrable attendu

À la fin de la session, chaque groupe remet une **fiche de gouvernance d'une page** :

```
Groupe Hospitalier Lumière — Charte agents IA (v0.1)

1. Définition d'un agent (notre définition opérationnelle)
2. Niveaux d'autonomie autorisés par type de service
3. Matrice de responsabilité (qui crée / qui valide / qui répond)
4. 5 règles non négociables (permissions, audit, dépréciation...)
5. Processus de mise en production en 5 étapes
```

---

## Ressources du projet

| Question | Fichier utile |
|---|---|
| Q1, Q2 | `fondamentaux/vocabulaire-essentiel.md` (sections Agent, Tool Use, Blast Radius) |
| Q3 | `choix_entite.md` |
| Q5 | `choix_entite.md` (dimension sécurité) |
| Q7 | `choix_entite.md` (Hooks) |
| Q9, Q10 | `skills/guide-creation.md`, `skills/guide-tests-et-regression.md` |
| Q11 | `skills/cycle-de-vie.md` |
