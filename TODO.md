# SentinelScan — Development TODO

**Project:** Lightweight Endpoint Security Scanner  
**Platform:** Windows-first  
**Language:** Python  
**License:** MIT  
**Status:** Initial Development

---

## 1. Project Foundation

- [x] Initialize GitHub repository.
- [x] Select MIT License.
- [x] Establish initial project directory structure.
- [x] Implement basic system information collector using `platform`.

## 2. Endpoint Collectors

### 2.1 System Information — `collectors/system.py`

- [x] Collect hostname.
- [x] Collect operating system information.
- [x] Collect OS release and version.
- [x] Collect system architecture.
- [ ] Integrate `psutil` for CPU information.
- [ ] Collect total physical memory (RAM).
- [ ] Collect disk capacity and available storage.
- [ ] Collect system boot time.
- [ ] Implement exception handling.
- [ ] Add unit tests.

### 2.2 Application Inventory — `collectors/applications.py`

- [ ] Implement Windows Registry enumeration using `winreg`.
- [ ] Collect installed application names.
- [ ] Collect application versions.
- [ ] Collect software publishers.
- [ ] Collect installation directories.
- [ ] Collect installation dates when available.
- [ ] Support 32-bit and 64-bit Registry views.
- [ ] Handle missing Registry values.
- [ ] Prevent duplicate application entries.
- [ ] Test against installed applications.

### 2.3 Security Configuration — `collectors/security.py`

- [ ] Collect Microsoft Defender status.
- [ ] Check real-time protection.
- [ ] Collect security intelligence version.
- [ ] Check Windows Firewall profiles.
- [ ] Check BitLocker status.
- [ ] Check Windows Update status.
- [ ] Check User Account Control configuration.
- [ ] Check Secure Boot status.
- [ ] Check TPM availability and readiness.
- [ ] Handle administrator permission requirements.
- [ ] Handle unavailable or unsupported security features.

### 2.4 Runtime Information — Future Enhancement

- [x] Collect running processes.
- [ ] Collect active network connections.
- [ ] Identify listening ports.
- [ ] Collect startup applications.
- [ ] Monitor process resource consumption.

---

## 3. Installer Scanner — `scanners/installer.py`

- [ ] Identify supported installer formats (`.exe`, `.msi`).
- [ ] Calculate SHA-256 file hashes.
- [ ] Collect file size and timestamps.
- [ ] Extract executable metadata.
- [ ] Identify publisher information.
- [ ] Check digital signature validity.
- [ ] Flag unsigned or suspicious installers.
- [ ] Handle inaccessible and corrupted files.

---

## 4. Security Analysis — `analyzer/risk_engine.py`

- [ ] Establish a standardized security finding structure.
- [ ] Define severity levels (Critical, High, Medium, Low, Informational).
- [ ] Evaluate endpoint security configurations.
- [ ] Identify potentially outdated applications.
- [ ] Evaluate installer security indicators.
- [ ] Implement risk scoring.
- [ ] Generate actionable security recommendations.
- [ ] Distinguish confirmed issues from suspicious indicators.

---

## 5. Reporting — `reporters/`

### JSON Reporter — `json_report.py`

- [ ] Generate structured JSON reports.
- [ ] Include scan timestamp.
- [ ] Include endpoint information.
- [ ] Include application inventory.
- [ ] Include security findings.
- [ ] Include risk assessment results.

### HTML Reporter — `html_report.py`

- [ ] Create readable HTML reports.
- [ ] Display endpoint information.
- [ ] Display application inventory.
- [ ] Display security posture.
- [ ] Display findings by severity.
- [ ] Include recommendations.

---

## 6. Application Integration — `main.py`

- [ ] Integrate all collectors.
- [ ] Integrate installer scanning.
- [ ] Integrate the security analysis engine.
- [ ] Integrate report generation.
- [ ] Implement a centralized scanning workflow.
- [ ] Add command-line arguments.
- [ ] Implement application logging.
- [ ] Handle unexpected errors gracefully.

---

## 7. Testing and Quality Assurance

- [ ] Create unit tests for individual collectors.
- [ ] Test missing or inaccessible Registry entries.
- [ ] Test unavailable Windows security features.
- [ ] Test installer analysis.
- [ ] Test risk classification.
- [ ] Test JSON and HTML report generation.
- [ ] Perform end-to-end scanning tests.
- [ ] Verify results against Windows system tools.

---

## 8. Documentation and Release

- [ ] Write project README.
- [ ] Document installation instructions.
- [ ] Document dependencies.
- [ ] Document project architecture.
- [ ] Document supported Windows versions.
- [ ] Document known limitations.
- [ ] Add usage examples.
- [ ] Include sample security reports.
- [ ] Record a project demonstration.
- [ ] Prepare initial GitHub release.

---

## Future Enhancements

These are outside the initial MVP scope.

- [ ] Add Linux endpoint support.
- [ ] Add macOS endpoint support.
- [ ] Implement real-time file monitoring.
- [ ] Integrate threat intelligence sources.
- [ ] Add centralized endpoint management.
- [ ] Develop a graphical management dashboard.
- [ ] Introduce endpoint enrollment and remote scanning.

---

## Development Guidelines

1. Keep collectors responsible only for gathering information.
2. Use `return` instead of `print()` inside collector functions.
3. Maintain consistent data structures across modules.
4. Handle missing information and permission errors gracefully.
5. Keep detection logic separate from data collection.
6. Never automatically delete or quarantine files in the initial version.
7. Prioritize accuracy, transparency, and safe scanning behavior.

**Immediate Next Task:** Complete and test `applications.py`, followed by the implementation of `security.py`.

**MVP Goal:** Build a functional Windows endpoint scanner capable of collecting system information, inventorying installed applications, auditing security configurations, analyzing installers, and generating security assessment reports.