# Security Policy

## Supported Versions

We support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

**Please do not open public GitHub issues for security vulnerabilities.**

Instead, please report security vulnerabilities by emailing the maintainers directly. Include:

1. Description of the vulnerability
2. Steps to reproduce (if possible)
3. Impact assessment
4. Suggested fix (if you have one)

We will:
- Acknowledge receipt within 48 hours
- Provide a timeline for a fix
- Credit you in the security advisory (unless you prefer anonymity)
- Keep you updated on the fix progress

## Security Considerations

### Input Validation

- All HTML parsing uses BeautifulSoup4 which handles malformed HTML safely
- URLs are validated with `urllib.parse.urljoin`
- JSON schema validation prevents invalid data from being saved

### Network Security

- HTTPS is used for all CPPP connections
- Session handling respects server rate limits
- No credentials or sensitive data are stored locally

### Data Handling

- Collected data is stored in JSON format without encryption
- Sensitive fields (contact emails, phone numbers) are included as found in public procurement documents
- No user authentication data is transmitted or stored

## Dependencies

We regularly update dependencies to patch known vulnerabilities. Check:

```bash
pip list --outdated
poetry show --outdated  # if using poetry
```

## Best Practices for Users

1. **Run in sandboxed environment** - Use virtual environments
2. **Review collected data** - Verify tenders before using in production
3. **CAPTCHA handling** - eProcurement may have CAPTCHA; consider headless browser options
4. **Rate limiting** - The collector sleeps 1 second between sources; respect server load
5. **SSL verification** - Ensure `requests` library has latest CA certificates

## Security in CI/CD

- GitHub Actions runs on `ubuntu-latest` (regularly updated)
- All dependencies are pinned to specific versions in lockfiles
- No secrets are stored in repository (all environment-specific)
- Code is linted and tested before merge

## Responsible Disclosure

If you discover a security issue:

1. **Do not** disclose it publicly
2. **Do** contact maintainers directly
3. **Allow** reasonable time for a fix before disclosure
4. **Work with us** to verify the fix before release

## Security Updates

Security updates will be released as:
- Patch versions (0.1.x → 0.1.y) for urgent fixes
- Within 2 weeks of discovery when possible
- With detailed release notes explaining the issue and fix

## Legal

By reporting a vulnerability, you agree to:
- Allow us to fix and release publicly
- Not disclose the issue before our public release
- Not use the vulnerability for harm

We appreciate your responsible disclosure!
