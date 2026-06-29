# Choisir la bonne entité Claude Code

> Schéma de décision complet pour l'ingénierie de l'écosystème Claude Code.
> Trois niveaux : vue globale → arbre de décision → matrice comparative.

---

## Niveau 1 — Vue d'ensemble de l'écosystème

```mermaid
graph TD
    subgraph HARNESS["🔧 Harness (environnement hôte)"]
        S[settings.json<br/>permissions · hooks · MCP]
        CI[.claudeignore<br/>filtrage du contexte]
    end

    subgraph MEMOIRE["🧠 Mémoire permanente"]
        CM[CLAUDE.md<br/>règles · conventions · commandes]
    end

    subgraph DECLENCHABLE["⚡ Entités déclenchables"]
        SK[Skill<br/>capacité à la demande]
        HK[Hook<br/>réaction aux événements]
    end

    subgraph EXTERNE["🌐 Intégrations externes"]
        MCP[MCP Server<br/>outils · ressources · prompts]
    end

    subgraph AGENT["🤖 Agents autonomes"]
        AG[Agent SDK<br/>boucle autonome]
        SAG[Subagent<br/>délégation isolée]
    end

    USER((Utilisateur)) -->|session démarre| CM
    USER -->|demande explicite| SK
    USER -->|commande shell| HK

    CM -->|system prompt| LLM((Claude LLM))
    SK -->|chargé si pertinent| LLM
    HK -->|exécuté par le harness| HARNESS
    MCP -->|outils disponibles| LLM
    AG -->|orchestre| SAG
    AG -->|appelle| LLM
    S -->|configure| HK
    S -->|déclare| MCP
    CI -->|réduit le contexte| LLM
```

---

## Niveau 2 — Arbre de décision

Posez les questions **dans l'ordre**. La première réponse OUI détermine l'entité.

```mermaid
flowchart TD
    START([🚀 J'ai un besoin à satisfaire]) --> Q1

    Q1{"Est-ce une RÈGLE, une CONVENTION\nou un CONTEXTE permanent\nque Claude doit toujours connaître ?"}
    Q1 -->|OUI| Q1a{"Concerne-t-il\nun projet spécifique ?"}
    Q1 -->|NON| Q2

    Q1a -->|OUI — règle projet| CM_P["📄 CLAUDE.md\nà la racine du projet\n(commité dans le repo)"]
    Q1a -->|NON — règle personnelle| CM_U["📄 CLAUDE.md\ndans ~/.claude/\n(global utilisateur)"]
    Q1a -->|OUI — règle d'un module| CM_S["📄 CLAUDE.md\nimbriqué dans le sous-dossier"]

    Q2{"Est-ce un FICHIER ou DOSSIER\nque Claude NE doit PAS\nindexer automatiquement ?"}
    Q2 -->|OUI| IGNORE["🙈 .claudeignore\npatterns gitignore\nsecrets · binaires · node_modules"]
    Q2 -->|NON| Q3

    Q3{"Est-ce une RÉACTION AUTOMATIQUE\nà un événement du harness\n(avant/après un outil, au démarrage...) ?"}
    Q3 -->|OUI| Q3a{"Quel type d'événement ?"}
    Q3 -->|NON| Q4

    Q3a -->|Avant un appel d'outil| HK_PRE["🪝 Hook PreToolUse\npeut bloquer l'action"]
    Q3a -->|Après un appel d'outil| HK_POST["🪝 Hook PostToolUse\nlint · format · tests auto"]
    Q3a -->|Démarrage de session| HK_START["🪝 Hook SessionStart\nsetup · vérifications initiales"]
    Q3a -->|Fin de session| HK_STOP["🪝 Hook Stop\nnotification · nettoyage · rapport"]
    Q3a -->|Notification Claude| HK_NOTIF["🪝 Hook Notification\nalerte · log · webhook"]

    Q4{"Est-ce une CAPACITÉ que l'utilisateur\ndemandera explicitement\nou que Claude détectera comme utile ?"}
    Q4 -->|OUI| Q4a{"La capacité nécessite-t-elle\ndes OUTILS SENSIBLES\nou des ACTIONS IRRÉVERSIBLES ?"}
    Q4 -->|NON| Q5

    Q4a -->|NON — lecture seule| SK_R["🎯 Skill\nallowed-tools: Read, Grep, Glob\nex: revue de code, analyse"]
    Q4a -->|OUI — écriture locale| SK_W["🎯 Skill\nallowed-tools: Read, Write, Edit\nex: génération de fichiers"]
    Q4a -->|OUI — exécution shell| SK_B["🎯 Skill\nallowed-tools: Bash\n⚠️ justifier dans le SKILL.md"]
    Q4a -->|OUI — systèmes externes| Q5

    Q5{"Est-ce une INTÉGRATION avec\nun SYSTÈME EXTERNE\n(API, BDD, service tiers) ?"}
    Q5 -->|OUI| Q5a{"Ce système est-il\nun service STANDARD\navec un serveur MCP existant ?"}
    Q5 -->|NON| Q6

    Q5a -->|OUI — GitHub, Slack, DB...| MCP_USE["🔌 MCP Server existant\nconfigurer dans settings.json\nex: @modelcontextprotocol/server-github"]
    Q5a -->|NON — système propriétaire| Q5b{"La logique est-elle\nsimple et déterministe ?"}

    Q5b -->|OUI — script bash/python| MCP_SCRIPT["🔌 MCP Server custom\nscript stdio exposant des tools\nex: scripts/mcp_server.py"]
    Q5b -->|NON — logique complexe| Q6

    Q6{"Est-ce un PROCESSUS AUTONOME\nmulti-étapes qui doit décider\nde ses propres actions ?"}
    Q6 -->|OUI| Q6a{"Est-il déclenché\nde façon PROGRAMMATIQUE\n(pas par l'utilisateur) ?"}
    Q6 -->|NON| Q7

    Q6a -->|OUI — pipeline automatisé| AG_PROG["🤖 Agent SDK\nclient Python/TS\nboucle ReAct autonome"]
    Q6a -->|NON — lancé par Claude| Q6b{"Peut-on isoler\nla tâche en sous-problème\nindépendant ?"}

    Q6b -->|OUI| SAG["🤖 Subagent\ndélégué par l'orchestrateur\ncontexte isolé · parallélisable"]
    Q6b -->|NON| AG_CODE["🤖 Agent dans Claude Code\nvia l'outil Agent tool\norchestration native"]

    Q7{"Est-ce une CONFIGURATION\ndu comportement global\n(permissions, modèle, UI) ?"}
    Q7 -->|OUI| Q7a{"Partagée avec l'équipe\nou personnelle ?"}
    Q7 -->|NON| UNCLEAR["❓ Besoin mal défini\n→ Reposer les questions\ndepuis le début"]

    Q7a -->|Partagée — commiter| SET_P["⚙️ .claude/settings.json\n(dans le repo du projet)"]
    Q7a -->|Personnelle — locale| SET_U["⚙️ .claude/settings.local.json\n(gitignorée)\nou ~/.claude/settings.json"]
```

---

## Niveau 3 — Matrice comparative

### Dimension 1 : Caractéristiques fondamentales


| Entité           | Qui déclenche         | Quand                        | Persiste entre sessions | Coûte des tokens        |
| ----------------- | ---------------------- | ---------------------------- | ----------------------- | ------------------------ |
| **CLAUDE.md**     | Automatique            | Toujours, dès le démarrage | ✅ Oui (fichier)        | ✅ Oui (system prompt)   |
| **.claudeignore** | Automatique            | Indexation initiale          | ✅ Oui (fichier)        | ✅ Réduit les tokens    |
| **Skill**         | Claude ou`/slash-cmd`  | À la demande, si pertinent  | ✅ Oui (fichier)        | ⚡ Seulement si activée |
| **Hook**          | Le harness             | Événement d'outil          | ✅ Oui (settings.json)  | ❌ Non (code, pas LLM)   |
| **MCP Server**    | Claude (via tool call) | Quand Claude appelle l'outil | ✅ Oui (settings.json)  | ⚡ Résultat injecté    |
| **Agent SDK**     | Code applicatif        | Programmatique               | ❌ Non (éphémère)    | ✅ Oui (chaque appel)    |
| **Subagent**      | Agent parent           | Délégation                 | ❌ Non (éphémère)    | ✅ Oui (isolé)          |
| **settings.json** | — (config)            | Au démarrage                | ✅ Oui (fichier)        | ❌ Non                   |

---

### Dimension 2 : Quoi mettre où ?


| Je veux…                                                    | Entité                         | Exemple concret                                                                  |
| ------------------------------------------------------------ | ------------------------------- | -------------------------------------------------------------------------------- |
| Que Claude connaisse toujours les conventions de mon projet  | **CLAUDE.md**                   | Format de branches, stack technique, commandes build                             |
| Que Claude ignore les gros dossiers inutiles                 | **.claudeignore**               | `node_modules/`, `data/raw/`, `*.log`                                            |
| Que Claude sache faire une revue de code structurée         | **Skill**                       | `reviewing-code-changes/SKILL.md`                                                |
| Lancer`eslint` automatiquement après chaque `Write`         | **Hook PostToolUse**            | `"matcher": "Write", "command": "eslint $CLAUDE_FILE_PATH"`                      |
| Que Claude puisse créer des PRs GitHub                      | **MCP Server**                  | `@modelcontextprotocol/server-github`                                            |
| Que Claude puisse interroger ma BDD PostgreSQL               | **MCP Server**                  | `@modelcontextprotocol/server-postgres`                                          |
| Exposer mon API interne à Claude                            | **MCP Server custom**           | `scripts/mcp_api.py` en stdio                                                    |
| Analyser 200 fichiers en parallèle sans saturer le contexte | **Subagents**                   | Orchestrateur → N subagents par module                                          |
| Déclencher une analyse de code dans un pipeline CI          | **Agent SDK**                   | Script Python avec`anthropic.Anthropic()`                                        |
| Interdire à Claude d'appeler`rm` sans confirmation          | **settings.json** (permissions) | `"deny": ["Bash(rm*)"]`                                                          |
| Recevoir une notif Slack quand Claude finit                  | **Hook Stop**                   | `"command": "curl -X POST $SLACK_WEBHOOK -d '{\"text\":\"Claude a terminé\"}'"` |
| Garder mes préférences perso (pas dans le repo)            | **settings.local.json**         | Modèle favori, couleurs, aliases                                                |

---

### Dimension 3 : Portée et visibilité

```
Portée croissante →

  Fichier          Projet            Utilisateur         Organisation
  ──────────────   ────────────────  ──────────────────  ────────────────────
  .claudeignore    .claude/          ~/.claude/          Banque de skills
  (à la racine)    settings.json     settings.json       (repo partagé)
                   commands/skill/   commands/skill/
                   CLAUDE.md         CLAUDE.md
                   (racine)          (global)
```

---

### Dimension 4 : Sécurité et blast radius


| Entité               | Peut modifier des fichiers | Peut exécuter du shell | Peut accéder au réseau | Blast radius                 |
| --------------------- | :------------------------: | :---------------------: | :----------------------: | ---------------------------- |
| **CLAUDE.md**         |             ❌             |           ❌           |            ❌            | Zéro (lecture seule)        |
| **.claudeignore**     |             ❌             |           ❌           |            ❌            | Zéro                        |
| **Skill (Read only)** |             ❌             |           ❌           |            ❌            | Zéro                        |
| **Skill (Write)**     |             ✅             |           ❌           |            ❌            | Fichiers locaux              |
| **Skill (Bash)**      |             ✅             |           ✅           |      ⚠️ Selon cmd      | Local + réseau              |
| **Hook**              |             ✅             |           ✅           |            ✅            | Illimité —**audit requis** |
| **MCP Server**        |        Selon outils        |      Selon outils      |            ✅            | Selon le serveur             |
| **Agent SDK**         |        Selon outils        |      Selon outils      |            ✅            | **Maximum** — sandboxer     |
| **Subagent**          |        Selon outils        |      Selon outils      |            ✅            | Isolé mais réel            |

> **Règle d'or** : blast radius doit être proportionnel au niveau de validation humaine.
> Hook qui supprime des fichiers → confirmation obligatoire dans le `settings.json`.

---

### Dimension 5 : Anti-patterns fréquents


| Anti-pattern                                       | Symptôme                                                                | Correction                           |
| -------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------ |
| Mettre une règle de style dans une Skill          | La skill se déclenche pour styler alors que ça devrait être permanent | → CLAUDE.md                         |
| Mettre une logique d'intégration dans CLAUDE.md   | Claude essaie d'appeler une API sans outil dédié, hallucine les URLs   | → MCP Server                        |
| Utiliser un Agent SDK pour une tâche simple       | Sur-ingénierie, complexité inutile                                     | → Skill ou Bash direct              |
| Skill avec`allowed-tools: Bash` sans justification | Risque de sécurité non justifié                                       | → Audit + restriction               |
| Hook trop large (`matcher: ".*"`)                  | Ralentit toutes les actions, faux positifs                               | → Matcher précis (`Write`, `Bash`) |
| Un seul CLAUDE.md de 500 lignes                    | Tout est chargé à chaque requête = tokens gaspillés                  | → Déplacer dans`references/`       |
| Skill "fourre-tout" qui fait tout                  | Ne se déclenche jamais bien                                             | → Décomposer en skills focalisées |
| MCP custom pour quelque chose de natif             | `Bash` ou `Read` suffisent                                               | → Utiliser les outils natifs        |

---

## Règles mnémotechniques

```
PERMANENT   → CLAUDE.md
ÉVÉNEMENT   → Hook
DEMANDE     → Skill
EXTERNE     → MCP
AUTONOME    → Agent SDK
DÉLÉGATION  → Subagent
CONFIG      → settings.json
BRUIT       → .claudeignore
```

```
Si ça doit TOUJOURS être vrai         → CLAUDE.md
Si ça se passe QUAND quelque chose    → Hook
Si l'utilisateur le DEMANDE           → Skill
Si ça parle à un SYSTÈME TIERS        → MCP
Si ça décide TOUT SEUL en boucle      → Agent
```

---

## Cheatsheet — Questions à poser à chaque nouveau besoin

```
1. Est-ce PERMANENT ou PONCTUEL ?
   Permanent → CLAUDE.md / .claudeignore / settings.json
   Ponctuel  → Skill / Hook / MCP / Agent

2. Qui DÉCLENCHE ?
   Toujours automatique  → CLAUDE.md ou Hook
   L'utilisateur         → Skill
   Un événement d'outil  → Hook
   Claude lui-même       → MCP tool
   Du code applicatif    → Agent SDK

3. Y a-t-il un SYSTÈME EXTERNE impliqué ?
   Oui → MCP Server (existant ou custom)
   Non → Skill ou Hook suffisent

4. Est-ce AUTONOME et MULTI-ÉTAPES ?
   Oui → Agent SDK ou Subagent
   Non → Skill avec workflow

5. Quel est le BLAST RADIUS acceptable ?
   Zéro      → Skill read-only ou CLAUDE.md
   Local     → Skill avec Write/Edit
   Élevé     → Hook ou Agent SDK → validation humaine obligatoire

6. Doit-on le PARTAGER avec l'équipe ?
   Oui → .claude/commands/ ou .claude/settings.json (commité)
   Non → ~/.claude/ ou settings.local.json (ignoré)
```
