# Demonstration Coding Guidance (Synthetic Educational Content)

This file is synthetic educational guidance for a student prototype. It is not an official standard.

## Secrets and credentials
Do not hardcode real passwords, API keys, access tokens, or private credentials in source code. Use an approved secrets manager or environment variables. Do not print secrets to logs.

## Input validation
Validate input types, ranges, and expected formats. Reject invalid values with clear errors. Avoid trusting user-provided paths or commands.

## Error handling
Handle expected exceptions specifically. Avoid swallowing exceptions without logging useful non-sensitive context. Do not expose stack traces or secrets to end users.

## Resource management
Use context managers for files and other resources when available. Ensure resources are released even when errors occur.

## Secure subprocess use
Avoid building shell commands by concatenating untrusted input. Prefer argument lists and validate allowed values.

## Testing and review
A finding from a static analyzer is evidence to investigate, not proof of exploitability. Validate proposed changes with tests and human review.
