# TP Claude Code — Parcours Développeur Débutant

> Deux TP pratiques pour prendre en main Claude Code : des exercices guidés pas à pas,
> avec des prompts exacts à taper et des sorties de référence à comparer.

---

## À qui s'adresse ce dossier ?

Développeurs qui connaissent déjà Git et Python mais qui découvrent Claude Code.
Aucune expérience préalable avec les LLM n'est requise.

---

## Prérequis techniques

- Claude Code installé (`npm install -g @anthropic-ai/claude-code` ou équivalent)
- Python 3.10+ avec pip
- Un éditeur de texte
- Accès internet (pour wttr.in dans le TP2)

```bash
# Installer la dépendance MCP pour le TP2
pip install mcp httpx
```

---

## Structure du dossier

```
tp_claude_debutant_dev/
├── README.md                          ← vous êtes ici
├── TP02_dev-bases.md                  ← TP02 : modèles, contexte, entités, tokens
├── TP02_solutions_dev-bases.md        ← Corrigé TP02 avec exemples de sorties
├── TP03_dev-mcp-skills.md             ← TP03 : MCP météo, skills, subagents, hooks
├── TP03_solutions_dev-mcp-skills.md   ← Corrigé TP03 avec code complet
└── support/
    ├── CLAUDE.md                      ← CLAUDE.md de référence pour le projet météo
    ├── settings.json                  ← Configuration MCP + hooks pour le TP2
    ├── scripts/
    │   └── mcp_meteo.py               ← Serveur MCP météo (wttr.in, sans clé API)
    └── skills/
        ├── fetching-weather.md        ← Skill complète : récupérer la météo
        └── recommending-activities.md ← Skill complète : suggérer des activités
```

---

## Parcours recommandé

| Étape | Durée | Fichier |
|---|---|---|
| 1. TP02 — Modèles et entités | 2h30 | `TP02_dev-bases.md` |
| 2. Vérification TP02 | 30 min | `TP02_solutions_dev-bases.md` |
| 3. TP03 — Météo, skills, subagents | 3h30 | `TP03_dev-mcp-skills.md` |
| 4. Vérification TP03 | 30 min | `TP03_solutions_dev-mcp-skills.md` |

---

## Ressources du projet principal

| Besoin | Fichier |
|---|---|
| Comprendre les modèles | `../fondamentaux/guide-modeles-claude.md` |
| Choisir entre Skill/Hook/MCP/Agent | `../choix_entite.md` |
| Créer une skill | `../skills/guide-creation.md` |
| Économiser des tokens | `../optimisation/guide-tokens.md` |
| Tester une skill | `../skills/guide-tests-et-regression.md` |
