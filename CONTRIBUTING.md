# Contributing

Thanks for wanting to improve the Opik skills.

**This repository is generated.** The skills, the README and the manifest are built from
[`comet-ml/opik-mcp`](https://github.com/comet-ml/opik-mcp) under `src/opik_mcp/skills/`
and synchronised here automatically. A change made directly in this repository is
overwritten by the next sync, so please make it upstream instead — it will reach here on
its own once merged.

## Where to make each kind of change

| You want to | Where |
|---|---|
| Fix or extend a skill's guidance | `src/opik_mcp/skills/<skill>/` in `opik-mcp` |
| Add a reference document | `src/opik_mcp/skills/<skill>/references/` in `opik-mcp` |
| Add a new skill | `src/opik_mcp/skills/` in `opik-mcp` — it appears here, and in this README, automatically |
| Change the README's wording or branding | the pack README template in `opik-mcp` |
| Report a problem with a skill's advice | an issue on either repository |

## What is maintained here

`LICENSE`, this file, and the workflows under `.github/`. Nothing else — everything else
is replaced on each sync.

## How a change reaches users

1. Your pull request merges in `opik-mcp`.
2. That build publishes a new pack artifact.
3. Within a day, a sync pull request opens here with the diff.
4. A maintainer merges it, and `npx skills add comet-ml/opik-skills` serves it.
