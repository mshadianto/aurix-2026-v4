# Sample PTCF Prompts for Demo
# Ready-to-use prompts for AI Chat demonstration

---

## 1. Credit Risk Audit Procedure

### PTCF Components:
- **Persona:** Senior Internal Auditor with 10 years experience in banking credit risk
- **Task:** Create comprehensive audit program for consumer loan origination
- **Context:** Mid-size commercial bank in Indonesia with NPL ratio of 4.5%, regulatory focus on POJK consumer protection
- **Format:** Detailed audit program with objectives, scope, procedures, and expected documentation

### Generated Prompt:
```
Anda adalah Senior Internal Auditor dengan pengalaman 10 tahun di bidang credit risk perbankan.

TUGAS:
Buatkan audit program komprehensif untuk proses consumer loan origination.

KONTEKS:
- Bank komersial menengah di Indonesia
- NPL ratio saat ini 4.5% (di atas appetite 3.5%)
- Fokus regulasi pada POJK perlindungan konsumen
- Volume kredit konsumer Rp 5 triliun per tahun
- 80% kredit adalah KPR dan KMG

FORMAT OUTPUT:
1. Audit Objectives (3-5 objectives)
2. Scope and Limitations
3. Key Risk Areas
4. Detailed Test Procedures (15-20 steps)
5. Sample Size Methodology
6. Expected Documentation
7. Key Regulatory References

Gunakan bahasa Indonesia yang formal dan profesional.
```

---

## 2. IT Security Assessment

### PTCF Components:
- **Persona:** IT Auditor with CISA certification specializing in cybersecurity
- **Task:** Develop security assessment checklist for core banking system
- **Context:** Bank implementing new core banking system, regulatory compliance required for BI and OJK
- **Format:** Security control checklist with testing procedures and pass/fail criteria

### Generated Prompt:
```
Anda adalah IT Auditor bersertifikasi CISA dengan spesialisasi cybersecurity.

TUGAS:
Kembangkan checklist security assessment untuk implementasi core banking system baru.

KONTEKS:
- Bank sedang implementasi core banking baru (Temenos T24)
- Go-live dijadwalkan Q2 2025
- Harus comply dengan PBI dan POJK tentang IT Risk
- Integrasi dengan 15 sistem existing
- Data migration 5 juta nasabah

FORMAT OUTPUT:
1. Security Control Categories (Access, Network, Application, Data)
2. Control Objectives per Category
3. Test Procedures (step-by-step)
4. Pass/Fail Criteria
5. Evidence Requirements
6. Regulatory Mapping (PBI/POJK reference)

Format sebagai tabel yang bisa di-copy ke Excel.
```

---

## 3. AML Compliance Review

### PTCF Components:
- **Persona:** Compliance Officer with expertise in AML/CFT regulations
- **Task:** Create AML transaction monitoring gap analysis framework
- **Context:** Bank recently received regulatory finding on AML monitoring, PPATK examination upcoming
- **Format:** Gap analysis matrix with current state, required state, and remediation actions

### Generated Prompt:
```
Anda adalah Compliance Officer dengan keahlian di regulasi AML/CFT.

TUGAS:
Buatkan framework gap analysis untuk AML transaction monitoring system.

KONTEKS:
- Bank menerima finding regulasi terkait AML monitoring
- Pemeriksaan PPATK dijadwalkan 3 bulan lagi
- Sistem monitoring saat ini coverage 65%
- Backlog alert 3,000+ dengan aging 60 hari
- STR filing compliance hanya 85%

FORMAT OUTPUT:
1. Gap Analysis Matrix:
   - Control Area
   - Regulatory Requirement (POJK/PPATK)
   - Current State
   - Gap Description
   - Risk Rating (H/M/L)
   - Remediation Action
   - Timeline
   - Owner

2. Quick Wins (dapat dicapai < 30 hari)
3. Medium Term (30-90 hari)
4. Long Term (> 90 hari)
5. Resource Requirements

Prioritaskan berdasarkan regulatory risk.
```

---

## 4. Fraud Investigation

### PTCF Components:
- **Persona:** Certified Fraud Examiner (CFE) with banking investigation experience
- **Task:** Develop investigation protocol for suspected internal fraud case
- **Context:** Anomaly detected in cash handling at branch, potential collusion between teller and supervisor
- **Format:** Step-by-step investigation protocol with evidence collection and interview guidelines

### Generated Prompt:
```
Anda adalah Certified Fraud Examiner (CFE) dengan pengalaman investigasi di perbankan.

TUGAS:
Kembangkan protokol investigasi untuk kasus dugaan fraud internal.

KONTEKS:
- Anomali terdeteksi di cash handling cabang X
- Dugaan kolusi antara teller dan supervisor
- Selisih kas Rp 500 juta dalam 6 bulan
- Pola: cash in tidak tercatat, tetapi balance tetap
- 2 karyawan sudah 5+ tahun di posisi yang sama

FORMAT OUTPUT:
1. Investigation Objectives
2. Preliminary Assessment Checklist
3. Evidence Collection Protocol:
   - Documentary evidence
   - Electronic evidence
   - Physical evidence
4. Interview Strategy:
   - Interview sequence (siapa duluan)
   - Key questions per role
   - Red flags to observe
5. Analysis Framework:
   - Transaction pattern analysis
   - Timeline reconstruction
   - Quantification methodology
6. Reporting Template
7. Preservation of Evidence Guidelines

Pastikan sesuai dengan hukum Indonesia dan best practices CFE.
```

---

## 5. Risk Assessment Report

### PTCF Components:
- **Persona:** Risk Management professional with experience in ERM implementation
- **Task:** Generate risk assessment report for new digital banking product
- **Context:** Bank launching mobile-only savings account for millennials, target 1 million customers year 1
- **Format:** Comprehensive risk assessment report with risk register and control recommendations

### Generated Prompt:
```
Anda adalah profesional Risk Management dengan pengalaman implementasi ERM.

TUGAS:
Buatkan risk assessment report untuk produk digital banking baru.

KONTEKS:
- Bank meluncurkan tabungan mobile-only untuk millennials
- Target 1 juta nasabah tahun pertama
- Full digital onboarding dengan e-KYC
- Integrasi dengan 10 e-commerce dan fintech
- Interest rate premium 1% di atas pasar

FORMAT OUTPUT:
1. Executive Summary
2. Product Overview
3. Risk Identification:
   - Credit Risk
   - Operational Risk
   - Compliance Risk
   - IT/Cyber Risk
   - Reputational Risk
   - Strategic Risk

4. Risk Register Table:
   | Risk ID | Category | Description | Likelihood | Impact | Score | Rating |
   
5. Control Recommendations per Risk
6. Residual Risk Assessment
7. Key Risk Indicators (KRI) for Monitoring
8. Risk Acceptance/Treatment Decision
9. Appendix: Risk Matrix Used

Sertakan pertimbangan POJK digital banking dan PBI e-KYC.
```

---

## 6. Operational Audit Working Paper

### PTCF Components:
- **Persona:** Internal Audit Manager reviewing branch operations
- **Task:** Create working paper template for branch cash operations audit
- **Context:** Annual audit of 50 branches, focus on cash handling and vault management
- **Format:** Standardized working paper template with test steps, sample size, and conclusion format

### Generated Prompt:
```
Anda adalah Internal Audit Manager yang me-review operasional cabang.

TUGAS:
Buatkan template working paper untuk audit operasional kas cabang.

KONTEKS:
- Audit tahunan 50 cabang
- Fokus: cash handling dan vault management
- Rata-rata cash holding Rp 2 milyar per cabang
- Standar: SOP Operasional Cabang v3.2
- Audit dilakukan 2 auditor per cabang, 3 hari

FORMAT OUTPUT:
1. Working Paper Header:
   - Audit Engagement Info
   - Preparer/Reviewer
   - Date Prepared/Reviewed

2. Audit Objective

3. Test Procedures Table:
   | Step | Procedure | Sample Size | Methodology | Result | W/P Ref |
   
4. Test Categories:
   - Cash counting verification
   - Dual control compliance
   - Vault access review
   - Cash in/out reconciliation
   - End of day procedures
   - Insurance coverage
   
5. Exception Log Template
6. Conclusion Format (3 options: Satisfactory/Needs Improvement/Unsatisfactory)
7. Follow-up Items Template

Buat dalam format yang bisa langsung digunakan auditor di lapangan.
```

---

## 7. Regulatory Compliance Checklist

### PTCF Components:
- **Persona:** Compliance Analyst specializing in banking regulations
- **Task:** Develop compliance checklist for POJK Consumer Protection requirements
- **Context:** New POJK 22/2023 on Consumer Protection, bank needs to assess current compliance
- **Format:** Detailed checklist with requirement mapping, compliance status, and evidence needed

### Generated Prompt:
```
Anda adalah Compliance Analyst yang spesialisasi di regulasi perbankan.

TUGAS:
Buatkan checklist kepatuhan untuk POJK Perlindungan Konsumen.

KONTEKS:
- POJK 22/POJK.01/2023 tentang Perlindungan Konsumen
- Bank perlu assessment kepatuhan saat ini
- Deadline kepatuhan penuh: Januari 2025
- Fokus area: informasi produk, penanganan pengaduan, data privasi

FORMAT OUTPUT:
1. Checklist Table:
   | Pasal | Requirement | Sub-requirement | Status | Evidence | Gap | Action Required |

2. Grouping by Category:
   - Informasi Produk dan Layanan
   - Perjanjian Baku
   - Penanganan Pengaduan
   - Perlindungan Data Konsumen
   - Edukasi Konsumen

3. Compliance Scoring:
   - Compliant
   - Partial
   - Non-Compliant
   - Not Applicable

4. Gap Summary dan Prioritization
5. Remediation Roadmap Template
6. Regulatory Reporting Requirements

Sertakan reference ke pasal spesifik di POJK.
```

---

## 8. Board Audit Committee Report

### PTCF Components:
- **Persona:** Chief Audit Executive presenting to Audit Committee
- **Task:** Prepare quarterly internal audit report for Audit Committee
- **Context:** Q3 2024 reporting, 15 audits completed, 3 critical findings, regulatory examination upcoming
- **Format:** Executive presentation format with key metrics, significant findings, and recommendations

### Generated Prompt:
```
Anda adalah Chief Audit Executive yang mempresentasikan ke Komite Audit.

TUGAS:
Siapkan laporan kuartalan Internal Audit untuk Komite Audit.

KONTEKS:
- Pelaporan Q3 2024
- 15 audit selesai dari 18 planned (83%)
- 3 finding critical, 8 high, 12 medium
- Closure rate finding: 75%
- Pemeriksaan OJK dijadwalkan Q1 2025

FORMAT OUTPUT:
1. Executive Summary (1 halaman)
   - Highlights
   - Key Concerns
   - Recommendations

2. Audit Activity Dashboard:
   - Plan vs Actual
   - Resource Utilization
   - Coverage Analysis

3. Significant Findings Summary:
   - Top 5 Findings dengan Root Cause
   - Management Response Status
   - Trend vs Previous Quarter

4. Finding Aging Analysis

5. Follow-up Status:
   - Open findings by age
   - Critical/High tracking
   - Overdue items

6. Regulatory Readiness Assessment
   - OJK exam preparation status
   - Key risk areas

7. Resource & Budget Update

8. Looking Forward (Q4 Plan)

Format profesional untuk presentasi dewan.
```

---

# End of Sample PTCF Prompts

## Tips Penggunaan:
1. Copy prompt yang sesuai dengan kebutuhan
2. Modifikasi context sesuai situasi aktual
3. Paste ke AI Chat di AURIX
4. Review dan edit output sesuai kebutuhan
5. Simpan sebagai template untuk penggunaan berulang
