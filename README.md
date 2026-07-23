# HIE Calculator — iOS (Capacitor)

Therapeutic hypothermia (cooling) eligibility calculator for neonatal hypoxic-ischemic
encephalopathy. This repo wraps the web calculator as a native iOS app using Capacitor
and builds/signs/uploads it via Codemagic — no Mac required.

## What's here

- `www/index.html` — the calculator (source of truth for the UI and logic).
- `capacitor.config.json` — Capacitor config (app id, app name, `webDir: www`).
- `package.json` — Capacitor dependencies.
- `codemagic.yaml` — Codemagic CI workflow: generates `ios/`, signs, builds, and
  uploads to App Store Connect / TestFlight.

The `ios/` folder is generated in CI (`npx cap add ios`), so it is intentionally not
committed.

## Build (Codemagic)

1. Connect this repo in Codemagic.
2. Add an **App Store Connect API key** in Codemagic integrations named
   **`AppStoreConnectKey`** (must match `codemagic.yaml`).
3. Register bundle id `com.HIE-Calc` and create the app record in
   App Store Connect.
4. Start the `ios-capacitor` workflow. The signed build lands in TestFlight.

## Clinical basis

Based on the AAP clinical report: Zanelli SA, Wusthoff CJ, Lucke AM, Kaufman DA;
Committee on Fetus and Newborn; Section on Neurology. Therapeutic Hypothermia for
Neonatal Hypoxic-Ischemic Encephalopathy: Clinical Report. Pediatrics.
2026;157(2):e2025073627.

The aEEG pattern reference is Fig. 16.2 from El-Dib M, de Vries LS (2024),
Neurophysiological Monitoring, in Meijler G, Mohammad K (eds), Neonatal Brain Injury,
Springer (CC BY 4.0).

This tool supports, and does not replace, clinical judgement and assessment.
