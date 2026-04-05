# Infra Automation

This repository hosts infrastructure automation assets for the MBrunk homelab. The initial bundle deploys a prompt-optimizer processing pipeline that can run as a Docker Compose workload, can be deployed with Ansible, can batch-process chat transcripts into reusable prompt artifacts, and can be extended with logging, notifications, and GitHub commit workflows.

## Scope

This bundle is designed around the following operating model:

- Primary deployment host: `vUbtDoc-Infra-Crt-Prod-N01.mbrunk.net`
- Persistent data root: `/mnt/docker_nfs/docker/vUbtDoc-Infra-Crt-Prod-N01/prompt-optimizer`
- Source toolkit repo: `Mikebru10/Export_Prompt`
- Default processing profile: `technical-only`
- Local AI backend: Ollama-compatible API endpoint

## What this repo provides

- Ansible inventory and group variables for prompt-optimizer deployment
- A Docker Compose stack for the prompt-optimizer runtime
- Bootstrap and batch-processing shell scripts
- systemd service and timer units for scheduled processing
- Environment templates for Ollama endpoint, model selection, paths, and optional notifications
- A sane starting structure for adding Loki logging, ntfy alerts, and future GitHub auto-commit workflows

## Repository layout

```text
infra-automation/
├── README.md
├── ansible/
│   ├── inventory.ini
│   ├── group_vars/
│   │   └── prompt_optimizer_hosts.yml
│   ├── deploy-prompt-optimizer.yml
│   └── roles/
│       └── prompt_optimizer_stack/
│           ├── tasks/
│           │   └── main.yml
│           ├── templates/
│           │   ├── prompt-optimizer.env.j2
│           │   ├── docker-compose.yml.j2
│           │   ├── run-mbrunk-batch.sh.j2
│           │   ├── prompt-optimizer-batch.service.j2
│           │   └── prompt-optimizer-batch.timer.j2
│           └── files/
├── scripts/
│   ├── bootstrap-export-prompt.sh
│   └── process-transcript-once.sh
└── docs/
    └── deployment-notes.md
```

## Deployment flow

The Ansible role creates the required directory tree under the NFS-backed storage path, clones or updates the `Export_Prompt` toolkit into the repo workspace, writes the runtime environment file, renders the Docker Compose stack, installs a batch wrapper script, and enables a systemd timer to periodically process new transcripts from the input directory.

## Required manual edits before production use

Replace the placeholder Ollama URL in the inventory or group variables with the actual host serving your local model endpoint.

Review the `inventory.ini` file and confirm the SSH target, Ansible user, and privilege escalation model for your environment.

If you want notifications, set the optional ntfy variables in `group_vars/prompt_optimizer_hosts.yml` and update the batch script behavior as needed.

## Quick start

```bash
cd ansible
ansible-playbook -i inventory.ini deploy-prompt-optimizer.yml
```

After deployment, place Markdown, text, or JSON transcripts in:

```text
/mnt/docker_nfs/docker/vUbtDoc-Infra-Crt-Prod-N01/prompt-optimizer/input
```

The timer will process them automatically. You can also run a one-off execution manually on the host.

## Next extension points

- GitHub auto-commit of generated artifacts
- ntfy push notifications for success or failure
- log shipping into Loki via Docker logging driver or Promtail scraping
- a small internal web UI for upload-and-generate workflows
