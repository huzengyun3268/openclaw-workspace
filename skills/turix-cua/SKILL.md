---
name: turix-cua
description: Submit CUA goals to a locally installed TuriX client and track task execution through TuriX HTTP and WebSocket APIs. Use when Codex needs to hand off desktop automation to TuriX instead of driving the UI directly, especially for goal-based CUA execution, checking available TuriX devices, inspecting local TuriX login state, or following a TuriX task until it reaches a terminal status.
---

# TuriX CUA

## Overview

Use the packaged Go binary in this skill to submit a natural-language CUA goal to TuriX and wait for the remote task result. Prefer this skill over raw HTTP or WebSocket calls because it already knows how to read local TuriX state, resolve devices, trigger planner flow, and return JSON-only results.

## Quick Start

Run the packaged binary for your platform:

```bash
TURIX_CUA_BIN="{baseDir}/scripts/bin/turix-cua-darwin-arm64"
"${TURIX_CUA_BIN}" status
"${TURIX_CUA_BIN}" devices
"${TURIX_CUA_BIN}" run --goal "Open Safari and search for OpenAI"
"${TURIX_CUA_BIN}" run --goal "Open Safari and search for OpenAI" --stream
"${TURIX_CUA_BIN}" stop --history-id history-123 --stream
```

```powershell
$TURIX_CUA_BIN = "{baseDir}\scripts\bin\turix-cua-windows-amd64.exe"
& $TURIX_CUA_BIN status
& $TURIX_CUA_BIN devices
& $TURIX_CUA_BIN run --goal "Open Safari and search for OpenAI"
& $TURIX_CUA_BIN run --goal "Open Safari and search for OpenAI" --stream
& $TURIX_CUA_BIN stop --history-id history-123 --stream
```

Read [references/protocol.md](references/protocol.md) only when you need endpoint details, state precedence, or status semantics.

## Commands

### `status`

Inspect local TuriX state and currently online devices.

```bash
TURIX_CUA_BIN="{baseDir}/scripts/bin/turix-cua-darwin-arm64"
"${TURIX_CUA_BIN}" status
```

### `devices`

List all devices visible to the resolved TuriX token.

```bash
TURIX_CUA_BIN="{baseDir}/scripts/bin/turix-cua-darwin-arm64"
"${TURIX_CUA_BIN}" devices
```

### `run`

Submit a goal and track it to a terminal status.

```bash
TURIX_CUA_BIN="{baseDir}/scripts/bin/turix-cua-darwin-arm64"
"${TURIX_CUA_BIN}" run \
  --goal "Open Safari and search for OpenAI" \
  --mode ultra \
  --stream \
  --timeout 10m \
  --plan-timeout 30s
```

Flags:

- `--goal`: required CUA target
- `--device-id`: optional explicit device code
- `--mode`: `ultra`, `process`, `execute`, or `quick`
- `--stream`: print line-oriented JSON progress events plus a final `result` event
- `--progress`: alias for `--stream`
- `--timeout`: overall wait budget
- `--plan-timeout`: planner wait budget for `ultra`

`quick` is a CLI alias for `execute`.

### `watch`

Resume tracking an existing TuriX history id.

```bash
TURIX_CUA_BIN="{baseDir}/scripts/bin/turix-cua-darwin-arm64"
"${TURIX_CUA_BIN}" watch --history-id history-123 --timeout 10m
"${TURIX_CUA_BIN}" watch --history-id history-123 --progress --timeout 10m
```

### `stop`

Stop an existing TuriX task through the websocket `STOP_TASK` flow and wait for the history to reach a terminal state.

```bash
TURIX_CUA_BIN="{baseDir}/scripts/bin/turix-cua-darwin-arm64"
"${TURIX_CUA_BIN}" stop --history-id history-123 --timeout 2m
"${TURIX_CUA_BIN}" stop --history-id history-123 --progress --timeout 2m
```

Flags:

- `--history-id`: required history id from a previous `run` or `watch`
- `--task-id`: optional sanity-check for the latest task inside that history
- `--timeout`: overall wait budget while stopping
- `--stream`: print line-oriented JSON progress events plus a final `result` event
- `--progress`: alias for `--stream`

## Workflow

1. Prefer `status` when you need to confirm the local TuriX app, token, and online runner before execution.
2. Use `run` for new CUA goals. Let the binary resolve local TuriX state instead of hand-building tokens and endpoints.
3. Use `watch` when you already have a `historyId` from a previous run or partial failure.
4. Use `stop` when you need to halt an existing task; prefer this over hand-written REST stop requests so TuriX keeps the normal stop semantics.
5. By default stdout is a single JSON object. With `--stream` or `--progress`, stdout becomes line-oriented JSON events that can be tailed and forwarded to chat while the task is running.
6. Stream mode emits `task_created`, `plan_update`, `ws_status`, `history_status`, `warning`, and a final `result` event.
7. On `timedOut=true`, preserve the returned `taskId`, `historyId`, and `lastStatus`, then use `watch` to continue tracking.

## Environment Overrides

Use env vars only when you need to override the local TuriX client state:

- `TURIX_TOKEN`
- `TURIX_API_HOST`
- `TURIX_WS_URL`
- `TURIX_DEVICE_ID`
- `TURIX_STATE_FILE`
- `TURIX_APP`

If these are absent, the binary prefers the production client state under `~/Library/Application Support/TuriX`.

## Resources

- `scripts/bin/turix-cua-darwin-arm64`: Packaged Go executable.
- `scripts/bin/turix-cua-windows-amd64.exe`: Packaged Go executable for Windows.
- `references/protocol.md`: Endpoint list, planner flow, state precedence, and JSON output contract.
