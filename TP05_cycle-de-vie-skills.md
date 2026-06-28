# TP — Cycle de vie des skills Claude Code

> **Durée estimée** : 3–4 heures (demi-journée)
> **Niveau** : Intermédiaire
> **Prérequis** : `skills/guide-creation.md`, `skills/cycle-de-vie.md`, idéalement avoir fait `TP04_hopital-maternite.md`
> **Format** : Réflexion individuelle (15 min) → mise en commun (15 min) par question
> **Aucun code à écrire — des extraits de configuration et de processus sont attendus**

---

## Contexte

Vous reprenez le scénario de l'**Hôpital Sainte-Claire**. Six mois ont passé depuis le déploiement des premières skills dans le service de maternité.

L'équipe a maintenant **8 skills actives** :

| Skill | Utilisateurs | Créée par | Dernière MàJ |
|---|---|---|---|
| `summarizing-patient-record` | Amina, Dr. Mercier | DSI | il y a 6 mois |
| `generating-birth-report` | Amina | Amina | il y a 4 mois |
| `escalating-to-on-call` | Toute l'équipe | DSI | il y a 6 mois |
| `drafting-admin-letter` | Léa | Léa | il y a 3 mois |
| `checking-appointment-conflicts` | Léa | Léa | il y a 1 mois |
| `summarizing-neonatal-exam` | Dr. Mercier | Dr. Mercier | il y a 5 mois |
| `generating-discharge-summary` | Amina, Léa | DSI | il y a 6 mois |
| `formatting-hl7-export` | DSI uniquement | DSI | il y a 2 mois |

Trois événements viennent de survenir simultanément :
- Anthropic vient de publier une mise à jour du modèle Claude
- La HAS (Haute Autorité de Santé) a publié de nouveaux critères pour les comptes-rendus de naissance
- Léa quitte l'hôpital dans 3 semaines — elle est la seule à savoir comment fonctionnent ses skills

La DSI vous mandate pour **structurer le cycle de vie des skills** du service.

---

## Partie 1 — Naissance et propriété d'une skill (matin)

> *Avant de gérer le cycle de vie, on définit qui possède quoi et selon quelles règles.*

### Question 1
Regardez le tableau des 8 skills. Trois ont été créées par des utilisateurs métier (Amina, Léa, Dr. Mercier), pas par la DSI.

Est-ce une bonne pratique, un risque, ou les deux ? Quelles règles mettre en place pour encadrer la création de skills par des non-techniciens, sans décourager l'initiative ?

Proposez un **processus de création en 4 étapes** qui équilibre autonomie des équipes et contrôle qualité.

---

### Question 2
`drafting-admin-letter` et `checking-appointment-conflicts` ont été créées par Léa, qui part dans 3 semaines. Personne d'autre ne sait exactement ce qu'elles font, quelles permissions elles utilisent, ni pourquoi certaines règles ont été ajoutées.

C'est le problème de la **skill orpheline avant qu'elle le soit**.

Quelles informations minimales doit contenir toute skill pour être reprise par quelqu'un d'autre ? Où les documenter ? Proposez un **format de métadonnées standard** que l'hôpital pourrait imposer à toutes les skills.

---

### Question 3
Deux nouvelles demandes arrivent en même temps :
- Amina veut une skill qui génère automatiquement les transmissions de fin de garde
- Le Dr. Mercier veut améliorer `summarizing-neonatal-exam` pour inclure les scores APGAR

**Doit-on créer une nouvelle skill ou mettre à jour l'existante ?**

Définissez les critères qui font pencher vers l'un ou l'autre choix. Dans quels cas une nouvelle skill est-elle préférable même si une mise à jour semblerait plus simple ?

---

### Question 4 — Débat
Actuellement, n'importe quel membre de l'équipe peut modifier une skill dans `.claude/commands/` si elle a accès au repo.

**Faut-il un processus de validation avant tout merge d'une modification de skill ?** Qui doit valider : la DSI ? Un pair technique ? Un utilisateur métier ? Les trois ?

Argumentez votre position en tenant compte de la réalité du terrain hospitalier : les urgences ne peuvent pas attendre 3 jours de review.

---

## Partie 2 — Mise à jour et déploiement (milieu de journée)

> *Comment faire évoluer une skill sans perturber les utilisateurs qui en dépendent.*

### Question 5
La HAS vient de publier de nouveaux critères pour les comptes-rendus de naissance. La skill `generating-birth-report` doit être mise à jour — mais elle est utilisée par Amina tous les jours, y compris la nuit.

Proposez une **stratégie de mise à jour sans coupure** : comment tester la nouvelle version en parallèle ? Comment basculer en douceur ? Comment revenir en arrière si la nouvelle version pose problème le lendemain matin à 3h ?

---

### Question 6
Le modèle Claude vient d'être mis à jour par Anthropic. Vous ne savez pas encore si ce changement affecte vos skills — mais vous savez qu'il *pourrait* les affecter.

Décrivez le **processus de vérification que vous lancez immédiatement**, avant que les utilisateurs ne se plaignent. Quelles skills testez-vous en priorité et pourquoi ? Quel outil vous permettrait d'automatiser cette vérification à chaque mise à jour du modèle ?

> 💡 *Voir `skills/guide-tests-et-regression.md` pour les 4 couches de test.*

---

### Question 7
L'hôpital veut maintenant partager certaines skills avec d'autres services (cardiologie, urgences) voire d'autres établissements du groupe hospitalier.

Comment **packager et distribuer** des skills conçues pour la maternité de façon à ce qu'elles soient réutilisables ailleurs, sans imposer le contexte spécifique de Sainte-Claire ?

Qu'est-ce qui doit rester spécifique au service ? Qu'est-ce qui peut être généralisé ?

> 💡 *Voir `skills/banques-de-skills.md` pour les modes de distribution.*

---

### Question 8
La skill `escalating-to-on-call` est critique : elle prévient le médecin de garde en cas d'alerte. Si elle est cassée, personne ne s'en aperçoit immédiatement — jusqu'à ce qu'une alerte réelle ne soit pas transmise.

Proposez un **mécanisme de surveillance en production** pour cette skill. Comment savoir qu'elle fonctionne encore correctement, sans attendre qu'un incident révèle le problème ?

---

## Partie 3 — Dépréciation et fin de vie (après-midi)

> *Savoir arrêter proprement est aussi important que savoir créer.*

### Question 9
`formatting-hl7-export` n'est utilisée que par la DSI, une fois par semaine. Le SIH va être remplacé dans 6 mois — cette skill sera inutile.

Quel est le **bon moment pour déclencher la dépréciation** ? Faut-il attendre le remplacement effectif du SIH, ou commencer le processus de retrait maintenant ? Décrivez les étapes concrètes de la mise hors service propre de cette skill.

---

### Question 10
Deux skills font des choses très proches : `summarizing-patient-record` (résumé général) et `summarizing-neonatal-exam` (résumé néonatal). Des utilisateurs confondent les deux et utilisent parfois la mauvaise.

**Fusionner ou déprécier ?** Présentez les critères de décision, et si vous choisissez de fusionner, décrivez comment gérer la transition sans perdre les utilisateurs qui ont des habitudes avec l'ancienne skill.

---

### Question 11
L'hôpital passe à l'échelle : le groupe hospitalier veut déployer les skills de maternité dans 12 établissements. Vous avez maintenant potentiellement **150 utilisateurs** sur 8 skills.

En quoi la gouvernance du cycle de vie change-t-elle à cette échelle ? Quelles pratiques qui fonctionnaient à 10 personnes deviennent des problèmes à 150 ? Proposez 3 adaptations concrètes.

---

### Question 12 — Débat final
Une skill déployée en production dans un hôpital est-elle comparable à un **médicament mis sur le marché** ?

Un médicament a : une notice (documentation), des essais cliniques (tests), une AMM (validation réglementaire), une pharmacovigilance (surveillance en production), un processus de retrait (dépréciation).

Quels éléments de ce cadre sont applicables aux skills IA ? Lesquels sont excessifs ? Lesquels manquent encore dans les pratiques actuelles de Claude Code ?

---

## Livrable attendu

Chaque groupe produit un **registre de skills sur une page** :

```
Service Maternité — Hôpital Sainte-Claire
Registre des skills (version actuelle)

| Skill | Version | Statut | Propriétaire | Prochaine action | Échéance |
|---|---|---|---|---|---|
| summarizing-patient-record | 1.2.0 | ✅ Active | DSI | Vérifier après MàJ modèle | Immédiat |
| generating-birth-report | 1.0.0 | ⚠️ À mettre à jour | Amina | Intégrer critères HAS | 2 semaines |
| ... | ... | ... | ... | ... | ... |

Processus de création : [5 étapes]
Processus de mise à jour : [déclencheurs + étapes]
Processus de dépréciation : [critères + étapes]
Outils de test utilisés : [liste]
```

---

## Ressources du projet

| Question | Fichier utile |
|---|---|
| Q1, Q2, Q3 | `skills/guide-creation.md` |
| Q4 | `skills/banques-de-skills.md` (section gouvernance) |
| Q5, Q6 | `skills/cycle-de-vie.md`, `skills/guide-tests-et-regression.md` |
| Q7 | `skills/banques-de-skills.md` (modes de distribution) |
| Q9, Q10, Q11 | `skills/cycle-de-vie.md` |
| Q12 | `fondamentaux/vocabulaire-essentiel.md` + `expert/presentation-avancee-claude.md` |
