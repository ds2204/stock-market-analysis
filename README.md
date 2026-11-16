# Stock Market Analysis and Email Reports

A Python report generator prepared for maintenance under **ds2204**, adapted from the supplied project credited in [ATTRIBUTION.md](ATTRIBUTION.md). It fetches Alpha Vantage daily prices, computes descriptive indicators, renders Matplotlib charts into HTML, and can send an attachment through AWS SES using recipient configuration in DynamoDB.

## Setup

Use Python 3.12:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest -v test_stock
```

Tests mock cloud services and do not email anyone. [`.env.example`](.env.example) lists configuration; Python does not automatically load `.env`. Export variables in your shell, or use the included VS Code env-file configuration. Keep keys outside Git.

`ALPHA_VANTAGE_API_KEY` defaults to the provider's demo value. Real symbols/full daily history may require an appropriate API subscription and rate-limit handling. `AWS_REGION` defaults to `us-east-1`; `EMAIL_TABLE` defaults to `EmailCredentials`. The table must contain one sender item (`emailID=sender`, `emailAddress`) and one or more `recipient...` items. SES identities and IAM permissions must be configured separately.

## Explicit execution

```sh
export ALPHA_VANTAGE_API_KEY=your-key
python stockMarketAnalysis.py
```

**This entry point attempts to email a report.** It is not an offline preview. The included Dockerfile runs this same command. The `lambda_handler` is a Python entry point, but the Dockerfile is a CLI container, not an AWS Lambda runtime image. No deployment infrastructure or schedule is supplied.

## Corrections and interpretation

- Cloud clients are created lazily, so importing analytics code makes no AWS calls.
- Price records are sorted before calculations/plots; HTTP requests have a timeout.
- RSI handles rising, falling and flat prices; it uses a simple rolling average, not Wilder smoothing.
- Missing long-window indicators are shown as unavailable, not zero or bearish signals.
- Volume bounds are actual minimum/maximum values.
- DynamoDB scans paginate, email errors propagate, empty reports are not sent, and a permanent `/tmp` lock no longer suppresses future invocations.
- External ticker descriptions are HTML-escaped. Personal email defaults and a personal email signature were removed.

The preserved HTML/PDF reports and architecture diagram are historical examples, not newly verified results or proof of deployed infrastructure. Financial summaries describe historical prices and do not establish investment performance. API and AWS integration, Docker execution, deployment, retries and production idempotency still require environment-specific testing. The current handler may make repeated API calls across time windows; respect provider limits.

No license was included. Confirm redistribution permission before public release. See [AUDIT.md](AUDIT.md).
