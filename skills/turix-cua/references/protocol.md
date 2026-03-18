# TuriX Protocol

## Local state resolution

The binary resolves credentials and runtime context in this order:

1. `TURIX_TOKEN`, `TURIX_API_HOST`, `TURIX_WS_URL`, `TURIX_DEVICE_ID`, `TURIX_STATE_FILE`, `TURIX_APP`
2. `~/Library/Application Support/TuriX/user_info_v4.json`
3. `~/Library/Application Support/TuriXDev/user_info_v4.json`
4. Built-in prod defaults:
   `https://api.cloud.turix.ai`
   `wss://api.cloud.turix.ai/api/v1/ws/global`

`TURIX_APP` may be `TuriX`, `TuriXDev`, or a full `.app` path. `TURIX_STATE_FILE` overrides automatic state file selection.

## HTTP endpoints

- `GET /api/v1/auth/users`
- `GET /api/v1/devices`
- `GET /api/v1/devices/{id}`
- `POST /api/v1/tasks/meta`
- `GET /api/v1/history/{historyId}`

The client always sends:

- `Authorization: Bearer <token>`
- `User-Agent: TuriX-Client`
- `X-Request-Id: turix-cua-<timestamp>`

## WebSocket flow

Connect to:

- `/api/v1/ws/global?clientType=web&token=<token>`

Planner messages:

1. Send `PLAN_TASK`
2. Read `TASK_PLAN_UPDATE`
3. Ack messages with `ACK`
4. In `ultra`, send `CONFIRM_PLAN` with the received `plan` as soon as the plan payload arrives
5. If `TASK_STATUS_UPDATE(confirming)` arrives before the plan payload, fall back to sending `CONFIRM_PLAN` there

`ultra` waits for planner flow. `execute` and `process` only trigger `PLAN_TASK`.

Stop messages:

1. Send `STOP_TASK` with the target `task_id`
2. Accept the server `ACK` when it arrives
3. Continue polling `/api/v1/history/{historyId}` until the task reaches a terminal state

## Device resolution

Resolution order:

1. Explicit `--device-id`
2. Current device id from local TuriX state
3. First online device from `/api/v1/devices`

If no device is online and the configured app bundle exists, the binary attempts:

- `open -a /Applications/TuriX.app`
- or the resolved app bundle path

Then it waits up to 30 seconds for a device to appear online.

## Task semantics

The binary creates tasks with:

- `source=web`
- `mode=ultra|process|execute`
- `enable_plan=false` only for `execute`

The binary preserves existing device plan settings. Server-side behavior depends on the device:

- `use_plan=off`: task may move through `prepared` instead of planner confirmation states
- `plan_confirmation=off`: server can move directly from `planning` to `planned`
- `plan_confirmation=on`: `ultra` auto-confirms the generated plan by sending `CONFIRM_PLAN`

## Status handling

In-flight statuses:

- `queued`
- `pending`
- `planning`
- `confirming`
- `planned`
- `prepared`
- `running`

Success statuses:

- `success`
- `completed`

Any terminal status outside the success list is returned as a failure.

## JSON-only command outputs

All commands print JSON to stdout.

Default mode prints one final JSON object.

`run`, `watch`, and `stop` also support `--stream` and `--progress` (same behavior). In stream mode, stdout becomes NDJSON: one compact JSON object per line, emitted as progress happens.

Stream event types:

- `task_created`: emitted after `/api/v1/tasks/meta` succeeds
- `plan_update`: emitted when the websocket sends `TASK_PLAN_UPDATE`
- `ws_status`: emitted when the websocket sends a new `TASK_STATUS_UPDATE`
- `history_status`: emitted when `/api/v1/history/{historyId}` changes status
- `warning`: emitted for non-fatal planner issues such as websocket timeout
- `result`: final line containing the same `run`, `watch`, or `stop` result payload

Successful `run`/`watch` example:

```json
{
  "ok": true,
  "taskId": "task-1",
  "historyId": "history-1",
  "deviceId": "device-1",
  "status": "success"
}
```

Successful `stop` example:

```json
{
  "ok": true,
  "taskId": "task-1",
  "historyId": "history-1",
  "status": "stopped"
}
```

Stream mode example:

```json
{"type":"task_created","goal":"Open Safari and search for OpenAI","taskId":"task-1","historyId":"history-1","deviceId":"device-1"}
{"type":"plan_update","taskId":"task-1","payload":{"task_id":"task-1","plan":[{"step_id":"step-1","description":"do something"}]}}
{"type":"history_status","taskId":"task-1","historyId":"history-1","deviceId":"device-1","status":"running"}
{"type":"result","result":{"ok":true,"goal":"Open Safari and search for OpenAI","taskId":"task-1","historyId":"history-1","deviceId":"device-1","status":"success"}}
```

Timeout example:

```json
{
  "ok": false,
  "taskId": "task-1",
  "historyId": "history-1",
  "deviceId": "device-1",
  "lastStatus": "running",
  "timedOut": true,
  "error": "timeout waiting for terminal history status"
}
```
