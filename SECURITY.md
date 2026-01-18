# Security Guidelines for SmartAllot

## Immediate Actions Required

⚠️ **URGENT**: If you have previously committed the `.env` file to this repository:

1. **Rotate all secrets immediately**:
   - Generate a new Django `SECRET_KEY`
   - Change database passwords
   - Update email credentials
   - Regenerate any API keys or tokens

2. **Remove secrets from git history**:
   The `.env` file has been removed from the current commit, but it may still exist in git history. You must purge it completely.

### Method 1: Using git-filter-repo (Recommended)

```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove .env from entire history
git filter-repo --path .env --invert-paths

# Force push to remote (WARNING: This rewrites history)
git push origin --force --all
git push origin --force --tags
```

### Method 2: Using BFG Repo-Cleaner

```bash
# Download BFG from https://rtyley.github.io/bfg-repo-cleaner/
# Then run:
bfg --delete-files .env

# Clean up and force push
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

## Environment Configuration Best Practices

### For Development

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Fill in your local values**:
   - Use strong, unique values for all secrets
   - Never use production credentials in development
   - Keep `.env` in your `.gitignore` (already configured)

3. **Generate a secure Django SECRET_KEY**:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

### For Production

1. **Never store secrets in code or config files**:
   - Use environment variables set directly on the server
   - Or use a secret management service (AWS Secrets Manager, HashiCorp Vault, etc.)

2. **Set `DEBUG=False`**:
   - Always disable debug mode in production
   - This prevents sensitive information leaks in error pages

3. **Use strong database passwords**:
   - Minimum 16 characters
   - Mix of letters, numbers, and special characters

4. **Secure email credentials**:
   - Use app-specific passwords for Gmail
   - Consider using a dedicated SMTP service (SendGrid, Mailgun, etc.)

## Checking for Exposed Secrets

If you're unsure whether secrets were exposed:

1. **Check git history**:
   ```bash
   git log --all --full-history -- .env
   ```

2. **Search for the .env file in all commits**:
   ```bash
   git rev-list --all | xargs git grep -l "DJANGO_SECRET_KEY"
   ```

3. **Use online tools** (with caution):
   - GitHub secret scanning will alert you if common secret patterns are detected
   - Consider using tools like `truffleHog` to scan your repository

## Reporting Security Issues

If you discover a security vulnerability in SmartAllot:

- **Do NOT** open a public issue
- Contact the repository maintainers privately
- Provide details about the vulnerability and potential impact

## Additional Resources

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
