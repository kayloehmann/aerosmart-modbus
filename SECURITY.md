# Security Policy

## Kontext

Öffentliches Repo. Typisiertes, backend-neutrales Python-Modell der Modbus-
Register eines aerosmart Lüftungs-/Wärmepumpengeräts (137 Register über 16
Sub-Systeme, zwei Modbus-Units), aufgesetzt auf `modbus-connection`. Keine
eigene Netzwerk-Exponierung — die Bibliothek stellt nur das Register-Modell,
die eigentliche Verbindung baut der Consumer (z.B. `aerosmart-modbus-hass`)
auf.

## Was hier als Sicherheitsproblem zählt

- Ein Fehler im Register-Modell (falsche Adresse/Skalierung/`writable`-Flag),
  der dazu führt, dass ein Consumer auf das **falsche physische Register**
  schreibt. Bei diesem Gerät ist das kein abstraktes Datenrisiko, sondern
  kann eine reale Heizungs-/Lüftungsanlage in einen unerwarteten Zustand
  bringen — Korrektheit der `writable`/Scale-Metadaten ist hier
  sicherheitsrelevant, nicht nur funktional.
- Ein kompromittiertes Release/Tag auf PyPI, das nicht dem Source in diesem
  Repo entspricht (Supply-Chain).
- Eine Änderung, die stillschweigend ein bisher read-only Register auf
  `writable` setzt, ohne dass das aus einer echten Registermanual-Quelle
  (die es laut README nicht gibt — nur die Transkription einer Live-Anlage)
  belegt ist.

## Melden

Öffentliches Solo-Repo ohne Team — Issue hier öffnen. GitHub Private
Vulnerability Reporting ist aktiv, falls eine nicht-öffentliche Meldung
gewünscht ist.

## Reaktionszusage

Ein falsches `writable`/Scale-Feld wird als kritischer Fund behandelt (nicht
als normaler Bug) — Fix + Patch-Release vor der nächsten Nutzung in
`aerosmart-modbus-hass`. Die vendored Kopie dort wird danach explizit
nachgezogen (kein automatischer Sync).

## Automatisierte Härtung

Wöchentlicher `GitHub Security Sweep`: Vulnerability Alerts, Dependabot
Security Updates, Secret Scanning + Push Protection, Branch Protection auf
`main` (block force-push/deletion) und Private Vulnerability Reporting sind
aktiv (öffentliches Repo, alle vier Punkte verfügbar).
