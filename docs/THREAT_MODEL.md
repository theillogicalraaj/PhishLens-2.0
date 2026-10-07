# Threat Model

## Assets

- Campaign configuration
- Recipient metadata
- Simulation event history
- Analyst accounts
- Risk analytics
- Reports

## Threats

- Unauthorized access to campaign data
- Credential theft from compromised analyst accounts
- Data leakage through logs
- Malicious HTML/content injection into campaign previews
- Abuse of simulation endpoints

## Mitigations

- JWT authentication
- scrypt password hashing
- Role checks for administrative audit data
- Rate-limited API surface in the architecture
- No credential forms in simulation pages
- No real email delivery in the default product
- Bounded text fields
- IP hashing before event persistence
- Secrets via environment variables

## Residual risk

Production deployments should add enterprise SSO, stronger rate limiting, CSRF protections where applicable, centralized secrets management, structured security logging, database encryption, reverse-proxy controls, and privacy review.
