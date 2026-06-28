# Cycle de vie des skills — Versioning, mise à jour, dépréciation

> Une skill non maintenue devient un boulet : elle se déclenche mal, produit des résultats
> obsolètes, et personne ne sait si elle est encore d'actualité. Ce guide couvre tout le
> cycle, de la création à la retraite.

---

## Vue d'ensemble du cycle

```
[Idée] → [Brouillon] → [Active] → [Révisée] → [Dépréciée] → [Archivée]
             │               │           │
          Pas encore      Version     Version
          déployée        1.0.0       2.0.0
```

---

## Phase 1 — Brouillon (Draft)

Une skill est en brouillon tant qu'elle n'a pas passé les tests de déclenchement.

**Convention de nommage en draft :**
```
.claude/commands/
└── _draft-reviewing-code-changes/   ← préfixe _ pour signaler le statut
    └── SKILL.md
```
Le préfixe `_` empêche le déclenchement automatique tout en gardant le fichier visible.

**Critères de sortie du brouillon :**
```
- [ ] Testée sur 3 prompts directs → se déclenche
- [ ] Testée sur 3 prompts indirects → se déclenche
- [ ] Testée sur 3 hors-sujet → ne se déclenche PAS
- [ ] Format de sortie validé par un humain
- [ ] Revue par au moins un autre membre de l'équipe
```

---

## Phase 2 — Versioning

### Stratégie de version

Les skills n'ont pas de mécanisme de version natif dans Claude Code.
Utilisez l'une de ces approches selon votre contexte :

#### Option A — Version dans le nom du fichier (simple, lisible)
```
.claude/commands/
├── reviewing-code-changes/        ← version courante (toujours ce nom)
│   └── SKILL.md
└── _archive/
    └── reviewing-code-changes-v1/ ← archive
        └── SKILL.md
```

#### Option B — Version dans un commentaire en tête de SKILL.md
```yaml
---
name: reviewing-code-changes
description: >-
  ...
# version: 2.1.0
# last-updated: 2026-03-15
# changelog: Ajout de la checklist Go, amélioration du format de sortie
---
```

#### Option C — Git tags sur le repo de skills
```bash
git tag skills/reviewing-code-changes/v2.1.0
git push origin skills/reviewing-code-changes/v2.1.0
```

### Quand incrémenter

| Type de changement | Incrément |
|---|---|
| Correction d'une règle ❌/✅ | Patch (2.0.**1**) |
| Ajout d'une section ou d'exemples | Mineur (2.**1**.0) |
| Refonte du workflow ou du format de sortie | Majeur (**3**.0.0) |
| Changement du nom ou des allowed-tools | Majeur + communication d'équipe |

---

## Phase 3 — Mise à jour d'une skill active

### Processus recommandé

1. **Ouvrir une issue** (ou note interne) décrivant le problème constaté
2. **Créer une branche** : `update/skill-reviewing-code-changes`
3. **Modifier `SKILL.md`** en preservant le format existant
4. **Tester** : relancer la grille de 6 prompts
5. **PR avec diff visible** pour que l'équipe valide
6. **Mettre à jour le changelog** dans l'en-tête ou dans `SKILL-CHANGELOG.md`
7. **Communiquer** si le format de sortie change (les utilisateurs s'y habituent)

### Triggers typiques de mise à jour

- Le modèle a changé de comportement (après une mise à jour d'Anthropic)
- Les conventions du projet ont évolué
- Une règle ❌/✅ s'avère incomplète ou incorrecte
- Le format de sortie ne répond plus aux besoins de l'équipe
- La skill se déclenche trop souvent ou pas assez

### Mise à jour de la description — le cas le plus fréquent

La description est la pièce la plus fragile. Elle peut nécessiter un ajustement si :
- La skill se déclenche trop souvent (description trop large) → restreindre les mots-clés
- La skill ne se déclenche pas assez (description trop vague) → ajouter des formulations

```yaml
# Avant (trop vague → ne se déclenche pas)
description: >-
  Aide avec le code.

# Après (précis → se déclenche au bon moment)
description: >-
  Relit du code modifié (diff, PR, fichiers ciblés) pour bugs et sécurité.
  À utiliser quand l'utilisateur demande une revue, un code review, ou
  "est-ce correct avant merge ?", même sans le mot "revue".
```

---

## Phase 4 — Dépréciation

### Quand déprécier ?

- La skill a été remplacée par une meilleure
- Le cas d'usage a disparu (outil abandonné, processus changé)
- La skill n'a pas été utilisée depuis > 3 mois

### Procédure de dépréciation

**Étape 1 — Ajouter un avertissement dans la description**
```yaml
description: >-
  [DÉPRÉCIÉE — utiliser reviewing-code-v2 à la place]
  Ancienne skill de revue de code...
```

**Étape 2 — Mettre à jour le registre de skills**
Si votre équipe tient un registre (voir `skills/banques-de-skills.md`), marquer la skill comme dépréciée.

**Étape 3 — Période de grâce (2–4 semaines)**
Laisser la skill en place avec l'avertissement pour que les utilisateurs migrent leurs habitudes.

**Étape 4 — Archivage**
```bash
# Déplacer dans le dossier archive plutôt que supprimer
mv .claude/commands/reviewing-code-changes .claude/commands/_archive/reviewing-code-changes-v1
```

---

## Phase 5 — Archivage

### Structure d'archive recommandée

```
.claude/
├── commands/           ← skills actives uniquement
│   └── ...
└── _archive/           ← skills dépréciées (ne se déclenchent pas)
    └── reviewing-code-changes-v1/
        ├── SKILL.md
        └── ARCHIVE-NOTE.md   ← pourquoi archivée, par quoi remplacée
```

### Contenu d'ARCHIVE-NOTE.md

```markdown
# Archive — reviewing-code-changes v1

- **Date d'archivage** : 2026-03-01
- **Raison** : Remplacée par `reviewing-code-changes` v2 (meilleur support Go)
- **Remplacée par** : `reviewing-code-changes` (version courante)
- **Référence** : PR #142 — "Refonte skill revue de code"
```

---

## Registre d'équipe (SKILLS-REGISTRY.md)

Pour les équipes avec plusieurs skills, tenir un registre central évite les doublons et facilite la découverte.

```markdown
# Registre des skills

| Skill | Version | Statut | Propriétaire | Dernière MàJ |
|---|---|---|---|---|
| reviewing-code-changes | 2.1.0 | ✅ Active | @alice | 2026-03-15 |
| generating-release-notes | 1.0.0 | ✅ Active | @bob | 2026-01-20 |
| analyzing-performance | 1.2.0 | ⚠️ Dépréciée | @charlie | 2025-11-01 |
| old-code-helper | — | 🗄️ Archivée | — | 2025-06-01 |

## Skills en développement
| Skill | Auteur | ETA |
|---|---|---|
| _draft-security-audit | @alice | 2026-04-01 |
```

---

## Tests de régression

Après chaque mise à jour d'une skill, rejouer l'ensemble de la grille de test :

```bash
# Si vous automatisez les tests (voir skills/banques-de-skills.md)
./scripts/test-skill.sh reviewing-code-changes

# Grille manuelle minimale
- [ ] 3 prompts directs → déclenchement
- [ ] 3 prompts indirects → déclenchement
- [ ] 3 hors-sujet → pas de déclenchement
- [ ] Format de sortie identique à la version précédente (ou changement documenté)
- [ ] Aucun outil non autorisé utilisé
```

---

## Ressources liées

- Guide de création : `skills/guide-creation.md`
- Organisation en banques : `skills/banques-de-skills.md`
- Template vierge : `templates/skill/SKILL.md`
