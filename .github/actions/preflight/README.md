# Preflight Action

Trigger a [Preflight](https://github.com/YouLearn-AI/preflight) QA run from
your repo's GitHub Actions. Posts an HMAC-signed dispatch payload to the
Preflight dispatcher; the dispatcher creates a check_run on your PR and
streams progress + the final report back.

## Quick start

1. Get an HMAC secret from your Preflight onboarding contact and store it
   as a repo secret named `PREFLIGHT_HMAC_SECRET`
   (Settings → Secrets and variables → Actions → New repository secret).

2. Drop this file into `.github/workflows/preflight.yml`:

   ```yaml
   name: Preflight
   on:
     pull_request:
       types: [opened, synchronize, reopened]
     workflow_dispatch:
       inputs:
         pr_number:
           description: 'PR number to test (workflow_dispatch only)'
           required: false

   jobs:
     preflight:
       runs-on: ubuntu-latest
       steps:
         - uses: youlearn-ai/preflight-action@v1
           with:
             hmac_secret: ${{ secrets.PREFLIGHT_HMAC_SECRET }}
             # Override these only if you know what you're doing:
             # dispatcher_url: https://preflight.youlearn.ai/dispatch
             # workflow: voiceos/jonah-customer-video
             # force: 'true'  # bypass any server-side skip heuristic
   ```

3. Open a PR. A `Preflight` check appears on the PR and progresses to
   `passed` / `failed` with a link to the full report (video + repro).

## Inputs

| Name             | Required | Default                                       | Description                                                       |
|------------------|----------|-----------------------------------------------|-------------------------------------------------------------------|
| `dispatcher_url` | no       | `https://preflight.youlearn.ai/dispatch`      | Dispatcher endpoint to POST against.                              |
| `hmac_secret`    | yes      | —                                             | HMAC-SHA256 shared secret. Repo secret.                           |
| `workflow`       | no       | (tenant default)                              | Workflow id to run, e.g. `voiceos/jonah-customer-video`.          |
| `force`          | no       | `false`                                       | `true` to bypass any auto-trigger heuristic (e.g. docs-only PRs). |

## Outputs

| Name         | Description                                              |
|--------------|----------------------------------------------------------|
| `run_id`     | Preflight run id (UUID) assigned by the dispatcher.      |
| `status_url` | Where to track progress + view the final report.         |

## Manual trigger

Run a workflow against a specific PR or commit on demand:

```
Actions tab → Preflight → Run workflow
  branch: main
  pr_number: 123    (optional — populates head_sha if omitted)
```

`workflow_dispatch` triggers always set `force=true` server-side so a
manual run is never skipped by the auto-trigger heuristic.

## How it works

1. Action collects PR meta from the GitHub event.
2. JSON payload is HMAC-SHA256 signed with your repo secret.
3. POST to `dispatcher_url` with `X-Preflight-Signature-256` header.
4. Dispatcher verifies, creates a check_run, schedules a guest VM run,
   and 202-acks. Heavy work happens server-side.
5. As the run progresses, the check_run status updates from
   `queued` → `in_progress` → `passed`/`failed` with the report URL.

## Self-hosting the dispatcher

The dispatcher is in `apps/api/` of the
[`youlearn-ai/preflight`](https://github.com/YouLearn-AI/preflight) repo.
Deploy onto a Mac mini reachable from the public internet, set
`PREFLIGHT_GH_WEBHOOK_SECRET` to the HMAC secret you hand customers,
and point this Action at it via `dispatcher_url`.
