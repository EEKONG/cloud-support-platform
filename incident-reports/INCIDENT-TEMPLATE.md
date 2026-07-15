# INC-XXX — Incident Title

## Incident Metadata

| Field | Value |
|---|---|
| Severity | SEV-X |
| Status | Investigating / Monitoring / Resolved |
| Start time | YYYY-MM-DD HH:MM UTC |
| End time | YYYY-MM-DD HH:MM UTC |
| Duration | |
| Affected component | |
| Failure domain | |
| Detection method | |
| Owner | |

## Executive Summary

Describe what failed, who was affected, the confirmed root cause, and how service was restored.

## Customer Impact

- Number or type of users affected:
- Features unavailable:
- Geographic or account scope:
- Data loss:
- SLA impact:

## Detection

How was the incident detected?

- Customer report
- Monitoring alarm
- Log alert
- Health check
- Manual test

## Initial Symptoms

```text
Paste sanitized symptom or response.
```

## Timeline

| Time UTC | Event |
|---|---|
| HH:MM | Incident detected |
| HH:MM | Initial triage |
| HH:MM | Failure domain isolated |
| HH:MM | Root cause confirmed |
| HH:MM | Fix applied |
| HH:MM | Recovery validated |
| HH:MM | Incident closed |

## Investigation

### Hypothesis 1

**Reason for testing:**

**Commands:**

```bash
command
```

**Evidence:**

```text
sanitized output
```

**Conclusion:** Confirmed / rejected.

### Hypothesis 2

Repeat as needed.

## Root Cause

State only what the evidence proves.

## Contributing Factors

-
-

## Resolution

```bash
commands used
```

## Recovery Validation

```bash
validation commands
```

Expected evidence:

```text
HTTP 200
service active
port listening
alarm returned to OK
```

## Corrective and Preventive Actions

| Action | Owner | Priority | Status | Due date |
|---|---|---|---|---|
| | | | | |

## Customer-Facing Update

> Provide a clear, non-technical update covering impact, restoration, and next steps.

## Engineering Escalation Notes

**Expected behavior:**

**Actual behavior:**

**Reproduction steps:**

**Logs and request IDs:**

**Workaround:**

**Required engineering action:**

## Security and Privacy Review

- [ ] Secrets removed
- [ ] IPs and identifiers redacted
- [ ] Customer data removed
- [ ] Logs sanitized
- [ ] No Terraform state included
- [ ] No private keys included

## Lessons Learned

-
-
