# PHP-Investment GmbH Website

Kleine, statische Unternehmenswebsite für die PHP-Investment GmbH. Die Website benötigt keinen Build-Schritt, kein JavaScript, keine Datenbank und keine externen Ressourcen. Sie ist für die direkte Bereitstellung auf Hetzner Webhosting M ausgelegt.

Die gelb markierten Angaben auf der Website sind absichtliche Platzhalter. Sie müssen vor der Veröffentlichung ersetzt oder – sofern als optional gekennzeichnet – entfernt werden.

## Technische Entscheidungen

- Reines HTML5 und CSS; kein Produktions-Runtime und kein Paketmanager
- Keine Cookies, Analyse, Tracker, externen Schriftarten, CDNs oder Einbettungen
- Kein Kontaktformular; Kontakt erfolgt nach Ergänzung der Daten über E-Mail bzw. Telefon
- Restriktive Sicherheitsheader über `.htaccess`
- Systemschriften und eine rein in CSS aufgebaute grafische Gestaltung
- Kleine, dependency-freie Prüfungen für HTML-Grundstruktur und interne Links

Diese bewusst einfache Architektur ist für den Umfang robuster und wartungsärmer als ein Framework, CMS oder PHP-Anwendung.

## Projektstruktur

```text
.
├── .github/
│   └── workflows/
│       └── checks.yml
├── assets/
│   └── css/
│       └── styles.css
├── scripts/
│   └── check_site.py
├── .gitignore
├── .htaccess
├── README.md
├── datenschutz.html
├── favicon.svg
├── impressum.html
├── index.html
├── robots.txt
└── sitemap.xml
```

## Local development

Im Projektverzeichnis einen dependency-freien lokalen Webserver starten:

```bash
python3 -m http.server 8080
```

Anschließend `http://localhost:8080` im Browser öffnen. Die automatisierten Struktur- und Linkprüfungen laufen mit:

```bash
python3 scripts/check_site.py
```

## Deployment to Hetzner Webhosting M

1. Finale Domain in der Hetzner-Verwaltung dem Webhosting-Paket zuordnen.
2. HTTPS-Zertifikat (Let's Encrypt, soweit im gebuchten Produkt verfügbar) aktivieren und die HTTPS-Weiterleitung in den Hosting-Einstellungen einschalten.
3. Prüfen, dass `php-investment.de` in `index.html`, `impressum.html`, `datenschutz.html`, `robots.txt` und `sitemap.xml` als Produktionsdomain eingetragen ist.
4. Firmen- und Rechtsangaben vervollständigen; alle gelb markierten Platzhalter und `TODO`-Kommentare prüfen.
5. Die Produktionsdateien per SFTP/FTP in den konfigurierten Document Root hochladen: `index.html`, `impressum.html`, `datenschutz.html`, `assets/`, `favicon.svg`, `robots.txt`, `sitemap.xml` und `.htaccess`.
6. Auf dem Zielsystem Startseite, interne Links, Impressum, Datenschutz und Darstellung auf Mobilgeräten testen.
7. Mit den Browser-Entwicklerwerkzeugen prüfen, ob HTTPS aktiv ist, keine Mixed-Content-Fehler auftreten und die Security-Header ausgeliefert werden.

`README.md`, `.github/`, `scripts/` und `.git/` werden für den Betrieb nicht benötigt und sollten nicht in den öffentlichen Document Root geladen werden.

Hinweis: Die `.htaccess` setzt HSTS ohne `includeSubDomains`. HSTS wirkt nur über HTTPS, sollte aber dennoch erst zusammen mit einem korrekt eingerichteten und dauerhaft verfügbaren Zertifikat veröffentlicht werden. Falls eine Direktive im gewählten Hetzner-Tarif nicht erlaubt ist und einen HTTP-500-Fehler verursacht, den betroffenen optionalen Block nach Rücksprache mit dem Hosting-Support entfernen.

## Hetzner- und GitHub-Actions-Setup

Webhosting M unterstützt SFTP/FTPS, aber keinen interaktiven SSH-Login. Das Deployment verwendet deshalb SFTP auf Port 22. Der Workflow ist zunächst ausschließlich manuell startbar und löscht keine bereits vorhandenen Dateien auf dem Server.

### 1. Hetzner vorbereiten

Auf diesem Webhosting liegen zwei unabhängige Websites. Die Verzeichnisstruktur soll deshalb so aussehen:

```text
public_html/
├── php-investment.de/
└── steinpilot.de/
```

1. In konsoleH das Webhosting-Paket auswählen und beide Domains dem Paket hinzufügen.
2. Unter `Services` → `WebFTP` die Verzeichnisse `public_html/php-investment.de` und `public_html/steinpilot.de` anlegen.
3. Für `php-investment.de` als Document Root `public_html/php-investment.de` auswählen.
4. Für `steinpilot.de` als Document Root `public_html/steinpilot.de` auswählen.
5. Unter `Einstellungen` → `Zugangsdaten` zwei **zusätzliche FTP-Benutzer** anlegen:
   - Benutzer A erhält ausschließlich Zugriff auf `public_html/php-investment.de`.
   - Benutzer B erhält ausschließlich Zugriff auf `public_html/steinpilot.de`.
6. Für beide Benutzer unterschiedliche, lange Zufallspasswörter verwenden und sicher verwahren. Nicht im Repository oder in lokalen Projektdateien speichern.
7. Servername, Benutzernamen und SFTP-Port 22 notieren.
8. Beide SFTP-Verbindungen separat testen. Jeder Benutzer darf nach dem Login nur den Inhalt seiner eigenen Website sehen.
9. Den angezeigten Host-Fingerprint prüfen und anschließend den bestätigten `known_hosts`-Eintrag für GitHub bereithalten.
10. Für beide Domains jeweils Let's Encrypt aktivieren und die HTTPS-Weiterleitung einschalten.

Da der zusätzliche Benutzer für dieses Repository bereits auf `public_html/php-investment.de` begrenzt wird, lautet `HETZNER_REMOTE_DIR` in GitHub `/`. Für Steinpilot werden in dessen eigenem Repository separate Secrets mit dem zweiten Benutzernamen und Passwort hinterlegt. Die Zugangsdaten dürfen nicht zwischen den Repositories wiederverwendet werden.

### 2. GitHub-Zugangsdaten anlegen

Im GitHub-Repository unter `Settings` → `Secrets and variables` → `Actions` folgende **Repository Secrets** anlegen. Repository Secrets funktionieren auch bei privaten Repositories, bei denen Environment Secrets je nach GitHub-Tarif nicht verfügbar sind:

| Name | Inhalt |
| --- | --- |
| `HETZNER_SFTP_HOST` | Hetzner-Server, z. B. `www123.your-server.de` |
| `HETZNER_SFTP_USER` | zusätzlicher FTP-Benutzer |
| `HETZNER_SFTP_PASSWORD` | Passwort dieses Benutzers |
| `HETZNER_SFTP_KNOWN_HOSTS` | zuvor geprüfte vollständige `known_hosts`-Zeile für Port 22 |

Unter `Variables` zusätzlich folgende Repository-Variablen anlegen:

| Name | Inhalt |
| --- | --- |
| `HETZNER_REMOTE_DIR` | normalerweise `/` beim eingeschränkten zusätzlichen Benutzer |
| `PRODUCTION_URL` | `https://php-investment.de/` |

Optional kann unter `Settings` → `Environments` zusätzlich ein Environment namens `production` mit erlaubten Deployment-Branches oder manueller Freigabe eingerichtet werden. Welche Schutzregeln verfügbar sind, hängt vom GitHub-Tarif und der Sichtbarkeit des Repositories ab.

### 3. Erstes Deployment

Vor dem Deployment müssen alle sichtbaren Firmen-/Rechtsplatzhalter sowie `example.invalid` ersetzt sein. `scripts/check_deploy_ready.py` blockiert die Veröffentlichung andernfalls absichtlich.

Danach auf GitHub unter `Actions` → `Deploy to Hetzner` → `Run workflow` starten. Der Workflow:

1. prüft HTML-Struktur, interne Links und Veröffentlichungsbereitschaft,
2. stellt ausschließlich die Produktionsdateien zusammen,
3. prüft den hinterlegten SFTP-Hostschlüssel,
4. lädt die Dateien verschlüsselt per SFTP hoch und
5. prüft anschließend die konfigurierte Produktions-URL.

Erst nach einem erfolgreichen manuellen Deployment sollte der Workflow optional um einen automatischen Trigger für Pushes auf `main` erweitert werden.

## Noch zu ersetzende Platzhalter

- `[STRASSE UND HAUSNUMMER]`
- `[PLZ ORT]`
- `[E-MAIL-ADRESSE]`
- `[TELEFONNUMMER]` bzw. `[TELEFONNUMMER, FALLS VERÖFFENTLICHT]`; danach `tel:`-Link ergänzen oder optionalen Eintrag entfernen
- `[VOLLSTÄNDIGER NAME DES GESCHÄFTSFÜHRERS]`
- `[REGISTERGERICHT]`
- `HRB [NUMMER]`
- `[KONFIGURIERTE SPEICHERDAUER UND LOG-EINSTELLUNGEN IN KONSOLEH PRÜFEN UND HIER EINTRAGEN]`
- `[NACH FESTSTEHEN DES FIRMENSITZES ZUSTÄNDIGE DATENSCHUTZ-AUFSICHTSBEHÖRDE EINTRAGEN]`
- `[ANGABE NACH § 36 VSBG: ...]` nach Prüfung von Beschäftigtenzahl, Teilnahmebereitschaft und einer möglichen gesetzlichen Verpflichtung

Zusätzlich in den Quelltext-Kommentaren zu prüfen:

- Umsatzsteuer-Identifikationsnummer und/oder Wirtschafts-Identifikationsnummer, falls vorhanden
- Datenschutzbeauftragter, falls bestellt oder gesetzlich erforderlich
- Status als Gesellschaft in Abwicklung/Liquidation, falls zutreffend
- zuständige Aufsichtsbehörde nur dann, wenn die konkret ausgeübte Tätigkeit einer behördlichen Zulassung unterliegt
- `mailto:`- und `tel:`-Links nach Einsetzen echter Kontaktdaten
- Auftragsverarbeitungsvereinbarung und tatsächliche Log-Konfiguration des Hetzner-Vertrags

## Rechtliche Annahmen und berücksichtigte Vorschriften

Die Texte sind auf eine rein informative Website einer deutschen GmbH zugeschnitten. Angenommen wurde:

- Die GmbH ist eine Beteiligungs- und Holdinggesellschaft und bietet keine erlaubnispflichtigen Finanz-, Anlageberatungs-, Vermittlungs- oder Vermögensverwaltungsleistungen über diese Website an.
- Es werden keine Finanzprodukte angeboten, keine Verbraucher-Verträge online geschlossen und keine journalistisch-redaktionellen Inhalte veröffentlicht.
- Es gibt keine Formulare, Nutzerkonten, Cookies, Analyse-, Marketing- oder Drittdienste.
- Hetzner Webhosting M ist der einzige Hosting-Dienstleister. Die tatsächliche Vertrags- und Log-Konfiguration ist noch zu verifizieren.

Berücksichtigt wurden insbesondere:

- [§ 5 Digitale-Dienste-Gesetz (DDG)](https://www.gesetze-im-internet.de/ddg/__5.html) für die Anbieterkennzeichnung
- [§ 36 Verbraucherstreitbeilegungsgesetz (VSBG)](https://www.gesetze-im-internet.de/vsbg/__36.html); die Pflicht hängt unter anderem von Beschäftigtenzahl sowie Teilnahmebereitschaft/-verpflichtung ab und bleibt deshalb als sichtbarer Prüfpunkt offen
- [Datenschutz-Grundverordnung (DSGVO)](https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=de), insbesondere Art. 6, 12–21 und 77
- [Verordnung (EU) 2024/3228](https://eur-lex.europa.eu/eli/reg/2024/3228/oj?locale=de), durch die die frühere EU-ODR-Verordnung zum 20. Juli 2025 aufgehoben und die OS-Plattform eingestellt wurde; daher enthält das Impressum keinen alten OS-Link
- [Hetzner-Dokumentation zu Logfiles bei Webhosting](https://docs.hetzner.com/de/general/company-and-policy/data-protection-at-hetzner/), laut der Apache-Logs standardmäßig sieben Tage vorgehalten werden können, die Dauer konfigurierbar ist und IP-Adressen anonymisiert werden; die konkrete Account-Einstellung muss geprüft werden

Eine Verantwortlichenangabe nach § 18 Abs. 2 MStV wurde nicht ergänzt, weil für diese reine Unternehmenspräsenz keine journalistisch-redaktionellen Inhalte vorgesehen sind. Eine Aufsichtsbehörde wurde im Impressum nicht genannt, weil keine erlaubnispflichtige Tätigkeit mitgeteilt wurde. Ändert sich die Tätigkeit oder der Inhalt, ist diese Einordnung erneut zu prüfen.

Die bereitgestellten Rechtstexte sind keine Rechtsberatung und keine Garantie für Rechtskonformität. Vor Veröffentlichung wird eine abschließende rechtliche Prüfung empfohlen.

## Vor Veröffentlichung prüfen

- [ ] vollständige Firmenanschrift
- [ ] Geschäftsführer
- [ ] Registergericht
- [ ] Handelsregisternummer
- [ ] E-Mail-Adresse
- [ ] Telefonnummer, falls veröffentlicht
- [ ] Umsatzsteuer-ID, falls vorhanden
- [ ] finale Domain
- [ ] Datenschutzerklärung geprüft
- [ ] Tätigkeit der GmbH auf regulatorische Besonderheiten geprüft
- [ ] Impressum abschließend rechtlich geprüft
- [ ] Wirtschafts-Identifikationsnummer, falls vorhanden
- [ ] Pflichtangabe nach § 36 VSBG geprüft
- [ ] tatsächliche Hetzner-Logeinstellungen und Aufbewahrungsdauer geprüft
- [ ] zuständige Datenschutzaufsichtsbehörde ergänzt
- [ ] Auftragsverarbeitung mit Hetzner geprüft
- [ ] HTTPS, Weiterleitung und Security-Header im Zielhosting getestet
