---

## CI/CD Pipeline (GitHub Actions)

The pipeline is triggered on every push to the `main` branch.

### Workflow Steps

1. Checkout repository
2. Set up Python runtime
3. Install AWS SAM CLI
4. Authenticate to AWS using OIDC
5. Build the application (`sam build`)
6. Deploy the stack (`sam deploy`)

### Key Benefit

- Uses **OIDC-based authentication** instead of AWS access keys
- Provides secure, short-lived credentials
- Follows modern DevOps best practices

---

## Deployment

### Local Deployment

```bash
sam build
sam deploy