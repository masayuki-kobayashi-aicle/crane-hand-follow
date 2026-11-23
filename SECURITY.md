# Security policy

## Reporting a vulnerability

Please **do not** open a public issue for a security problem.

Use GitHub's private vulnerability reporting: open the repository's **Security**
tab and choose **Report a vulnerability**. If that option is not available, open
a public issue that says only that you have a security report, without details,
and a maintainer will arrange a private channel.

We aim to acknowledge a report within 7 days. This is a small project run in
spare time, so there is no guaranteed fix time.

## Scope and known limits

crane-hand-follow can command a physical robot arm. Treat it as a tool for your
own machine, not as a service.

Known and documented properties (see the "Security model" section of the README):

- The server listens on `127.0.0.1` only. There is no option to open it on
  another interface, and nothing here is meant to be exposed to a network.
- Plain HTTP, no TLS, no login. Anything that can reach `127.0.0.1` on your machine
  (another local user or process) can use the page.
- `POST` requests are accepted only when the `Host` and `Origin` headers match
  the local address, and the content type is as expected. This is a guard against
  other web pages in your browser, not an authentication.
- The following-session token that the server issues is for detecting a stale
  page; it is not a secret that protects against a local attacker.
- The software stop (lost hand, lost input, stop button) is not a certified safety
  function. Keep the power switch of the arm within reach.

Reports about these documented properties are welcome as improvement ideas, but
are not treated as vulnerabilities by themselves. Reports we especially want:

- a way for a remote web page to make the server move the arm (Host/Origin
  check bypass, DNS rebinding, CSRF),
- a way to send a command that the server-side limits and clamps should refuse,
- path traversal, request smuggling, or unbounded resource use in the server,
- the download in `app/prepare.py` accepting a file whose SHA-256 does not match.

## Supported versions

Only the latest release (or `main` before the first release) is supported.
