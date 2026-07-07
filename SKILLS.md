# Skills Catalog

## Core Capabilities (built into the `ambient` skill)

The `ambient` skill routes to these subskills. They're plain files read on
demand — always available, no manifest entry needed.

| Subskill | What it does | How to invoke |
|----------|-------------|---------------|
| **install** | Sets up ambient-library in a project | *"Set up ambient-library in this project"* |
| **select** | Scopes the project's domain skills via conversation | *"Configure my skills"* |
| **manage** | Adds/removes skills, points to `/plugin update` | *"Update my skills"*, *"Add X to this project"* |
| **review** | Code review for correctness, security, performance | *"Review this code"* |
| **load** | Reads a domain skill on demand when a request matches | Automatic — invoked by the router |

## Domain Skills (in `library/`, read on demand)

Domain skills live in the plugin at `library/<name>/instructions.md`.
They are plain files — **not** registered skills — so they add nothing to context
until the router reads one. Optionally scope which a project uses via
`skills-manifest.yaml`.

| Skill | What it does | How to invoke |
|-------|-------------|---------------|
| **project-brief** | Creates a one-page project overview anyone can read and share | *"Write a project brief"*, *"Summarize this project"* |
| **researcher** | Gathers sources into a structured research dossier | *"Research this topic"*, *"Find sources on X"* |
| **writer** | Drafts a piece from a brief and optional dossier (drafting only) | *"Draft this"*, *"Turn this brief into a post"* |
| **editor** | Surgically edits an existing draft for clarity, voice, structure | *"Edit this draft"*, *"Tighten this article"* |
| **writing-team** | Full research → draft → edit pipeline to a publish-ready piece | *"Write me an article on X end to end"* |
| **context-mgr** | Installs the multi-agent `.context/` continuity system into a project | *"Install context-mgr"*, *"Set up multi-agent context here"* |
| **session** | Session check-in/check-out against a project's `.context/` store | *"What should I work on"*, *"Checkpoint"* |
| **aimm-newsletter** | Sends a newsletter email to a named Google Contacts group | *"Send this to [group]"*, *"Send the newsletter"* |
| **aimm-writing-team** | Autonomous multi-role AIMM article team (Researcher → Publisher) | *"Use Strategist mode"*, full AIMM article run |
| **audit-fix** | Six-lens adversarial audit of a plan or change, then root-cause fixes | *"Audit this"*, *"Pressure test"*, *"Poke holes"* |
| **audit-mcp** | Security audit of a third-party MCP server repo before install | *"Audit this MCP"*, *"Is this MCP safe"* |
| **brand-writing-team** | Multi-role team for brand-building long-form content, end to end | *"Help me write a post about X"* (brand content) |
| **cognitive-operations** | Structured thinking via Lenses, Operations, and 40 Recipes | *"Think through"*, *"Run a pre-mortem"* |
| **conversation-consolidation-system** | Pipeline turning Claude chat history into a searchable Obsidian brain | *"Second brain for my AI work"* |
| **conversation-ip-extractor** | Extracts frameworks and publishable IP from a conversation transcript | *"What did I figure out here?"* |
| **deep-comprehension-assessment** | Rigorous text-comprehension assessments with feedback | *"Test my understanding of this text"* |
| **deep-field** | Eigenthinking + latent cartography + wisdom-of-crowds insight system | *"Run deep field"* |
| **eigenthinking** | Nine-step framework turning tacit expertise into branded IP | *"Package my methodology"* |
| **enrich-prompt** | Enriches a prompt to surface implicit constraints, then answers it | *"Make this prompt better"* |
| **extract-codify-patterns** | Packages a session into a look-over-my-shoulder artifact bundle | *"Codify this session"* |
| **fresh-eyes** | Zero-context agent walks docs/onboarding cold, fix-and-respawn | *"Fresh eyes"*, *"Test the docs"* |
| **geo-authority-architect** | GEO / AI-citation authority strategy and content architecture | *"GEO strategy"*, *"Get cited by AI"* |
| **grill** | One-question-at-a-time convergence with a decisions ledger | *"Grill me"*, *"Interview me"* |
| **ireport** | Styled, interactive HTML research reports | *"Interactive report on X"* |
| **irreplaceable-edge** | Live discovery of an irreplaceable competitive edge vs. AI competition | *"Find my edge"*, *"What's my moat"* |
| **knowledge-base-architect** | Designs and deploys a personal AI knowledge base from expertise assets | *"Talk to my own knowledge"* |
| **latent-cartographer** | Latent-space traversal mapping the probability landscape before answering | *"/lsc"*, *"Run the cartographer"* |
| **leaderize-storytelling-framework** | Storytelling frameworks for the Leaderize audience | Leaderize content or session design |
| **meeting-nuggets** | Meeting transcripts → newsletter-style topic recaps | *"Recap this meeting"* |
| **multi-model-debate-live** | Live human-steered Claude/Gemini/Codex debate on one shared file | *"Run the models against each other"* |
| **paradigm-collision-engine** | Collides 400+ disciplinary paradigms for non-obvious insight | *"Give me a non-obvious take"* |
| **polyglot-language-coach** | Coaches non-English writing mid-conversation, then returns to task | Automatic on code-switching |
| **transcript-to-content-pipeline** | Transcript → full content package (article, LinkedIn, summary) | *"Turn this into content"* |
| **voice-crm-pipeline** | Hands-free voice-to-database capture chain (Siri → Sheets) | *"Talk to my database"* |
| **voice-profile-trainer** | Builds a reusable voice profile from writing samples | *"Write in my voice"* |
| **wrap** | Full session close-out: commit, export, narrative, handoff, memories | *"Wrap up"*, *"Close out"* |
| **aimm-commands** | Index of 54 named AIMM prompt commands, loaded one at a time | *"/aimm:skeptic"*, *"Run the skeptic"* |
| **trello-pipeline** | Trello-board agentic pipeline from product idea to PRD | *"Run the Trello pipeline"* |
| **editorial-desk** | Senior-editor orchestrator: specialist contributors over a shared blackboard | *"Run the editorial desk"*, *"Write a sharp argument piece and have it critiqued"* |
| **to-issues** | Plan/spec/PRD → tracer-bullet vertical-slice issues on the tracker | *"Turn this plan into issues"* |
| **harness-prd** | Interview-driven design of a harness ProcessSpec (agent state machine) | *"Build an agent process for X"*, *"Spec out an agent pipeline"* |
| **graphify** | Any folder → persistent, queryable knowledge graph with community detection | *"Graphify this"*, codebase/architecture questions |
| **gmail-triage** | Two-phase inbox sweep: batch-archive junk, then one-at-a-time triage | *"Check my email"*, *"Clean up my inbox"* |
| **gmail-manager** | Cross-account Gmail management (search, read, send, label, drafts) | *"Send an email"*, *"Find that thread"* |

### In-context vs. spawned execution

Domain skills run in the current conversation by default. The **writing-team**
pipeline can also run in its own context — say *"...in the background"* or *"run
it separately"* and the router spawns a general-purpose subagent that follows the
same `library/writing-team/instructions.md`. No registered agent is shipped, so
the always-on context cost stays at the single `ambient` description.

---

## Adding a Domain Skill

Domain skills are project-specific tools that extend the core system — documentation generators, deployment workflows, custom review standards, etc.

To add one: see [docs/MANAGEMENT.md](docs/MANAGEMENT.md).

To activate one in your project, add it to `skills-manifest.yaml`:

```yaml
domain_skills:
  - your-skill-name
```
