# Security Policy

## Scope

This repository is an **educational demonstration** of the Padding Oracle Attack on AES-128 CBC mode. It is intentionally vulnerable by design and should never be used in production or security-sensitive environments.

## Supported Versions

No versions of this project are supported for security fixes, as the vulnerable behavior is the point of the demonstration.

## Reporting a Vulnerability

If you discover an unintentional security issue (for example, a dependency vulnerability, unsafe code execution, or anything outside the scope of the demonstrated attack), please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, use GitHub's private vulnerability reporting:
1. Go to the **Security** tab of this repository
2. Click **"Report a vulnerability"**
3. Fill in the details

See [GitHub's documentation](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability) for more on private vulnerability reporting.

You can expect an acknowledgment within 7 days.

## Disclaimer

The techniques demonstrated in this project (padding oracle attacks, CBC bit-flipping) are well-documented cryptographic attacks intended for learning purposes only. Use of these techniques against systems you do not own or have explicit permission to test is illegal and unethical.
