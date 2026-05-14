# WATCHER_CONTROL_V1

repo: JayDEmily/nvda10
issue: 2
watcher_control_hash: sha256:2a9626937a131a7ff4472a8644664aa8f0b22eb240b8ea510b101cb6d6385ba1
allowed_actions: on, off, status, dashboard, tail

## Purpose

This file is the local watcher control contract for this repository.

It is not an internet security boundary. It is a project-local guard that lets the Makefile and watcher control script confirm they are operating the intended watcher for the intended repository.

## Human commands

Run these from the repository root:

```bash
make bridge-on
make bridge-off
make bridge-status
make bridge-dashboard
```

Two-word compatibility commands are also supported:

```bash
make bridge on
make bridge off
make watch status
make watch dashboard
```
