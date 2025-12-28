# Sample Findings for Demo
# Copy-paste into the application for demo purposes

## Finding 1: Inadequate Credit Documentation

**Title:** Inadequate Credit Documentation in Loan Origination

**Audit Area:** Credit Risk > Loan Origination

**Severity:** HIGH

**Status:** Open

**Due Date:** 2025-01-15

### 5Cs Details:

**Condition:**
During testing of 50 consumer loan files from Q3 2024, we identified that 35% (17 files) were missing one or more required supporting documents. Specifically:
- 8 files missing income verification documents
- 6 files missing collateral valuation reports
- 3 files missing KYC completion forms

**Criteria:**
According to Credit Policy Manual Section 4.2.1 and POJK No. 42/POJK.03/2017, all consumer loans must maintain complete documentation including:
- Income verification (slip gaji/SPT)
- Collateral valuation (for secured loans)
- Complete KYC documentation

**Cause:**
Root cause analysis revealed:
1. No systematic checklist verification before loan approval
2. Credit officers under pressure to meet monthly targets
3. Quality control only performed on sampled basis (10%)
4. No system enforcement blocking incomplete applications

**Consequence:**
If not addressed, this may result in:
- Potential loan losses estimated at Rp 5.2 billion (based on historical loss rates)
- Regulatory sanctions for non-compliance with POJK requirements
- Increased NPL due to inability to pursue legal collection
- Reputational risk from regulatory findings

**Corrective Action:**
1. Implement mandatory system checklist blocking loan approval until complete (Target: 30 days)
2. Increase QC sampling to 25% of new loans (Target: Immediate)
3. Provide refresher training to all credit officers (Target: 14 days)
4. Remediate existing files - complete missing documentation (Target: 60 days)
5. Monthly compliance reporting to Risk Committee (Target: Ongoing)

---

## Finding 2: System Access Control Weaknesses

**Title:** Inadequate Segregation of Duties in Core Banking System

**Audit Area:** IT/Cyber Risk > Access Control

**Severity:** CRITICAL

**Status:** In Progress

**Due Date:** 2024-12-31

### 5Cs Details:

**Condition:**
Review of core banking system access rights revealed:
- 12 users have both maker and checker access for fund transfer
- 5 IT administrators have production data access without approval
- 23 terminated employee accounts still active (avg 45 days post-termination)
- No periodic access recertification performed in 18 months

**Criteria:**
- Bank Indonesia Regulation PBI No. 9/15/PBI/2007 on Risk Management
- ISO 27001:2022 Control A.5.15 Access Control
- Internal IT Security Policy requiring quarterly access review
- Segregation of Duties Matrix approved by Risk Committee

**Cause:**
1. Manual access provisioning process without automated controls
2. HR-IT integration gap causing delayed termination notifications
3. Access review policy exists but not enforced
4. No automated SoD conflict detection in place

**Consequence:**
- Fraud risk: Users can initiate and approve own transactions
- Data breach risk: Unauthorized access to customer data
- Regulatory sanctions: Potential BI examination findings
- Financial loss exposure estimated at Rp 10-50 billion

**Corrective Action:**
1. Immediate removal of SoD conflicts (Target: 7 days) - COMPLETED
2. Disable all terminated employee accounts (Target: Immediate) - COMPLETED
3. Implement automated HR-IT integration (Target: 90 days) - IN PROGRESS
4. Deploy access governance tool with SoD detection (Target: 120 days)
5. Establish quarterly access certification process (Target: 60 days)

---

## Finding 3: AML Transaction Monitoring Gaps

**Title:** Insufficient AML Transaction Monitoring Coverage

**Audit Area:** Compliance Risk > AML/CFT

**Severity:** HIGH

**Status:** Open

**Due Date:** 2025-02-28

### 5Cs Details:

**Condition:**
Assessment of AML transaction monitoring system identified:
- Only 65% of transaction types covered by monitoring rules
- Cash transactions under Rp 100 million not monitored
- Cross-border wire transfers lack velocity checks
- 2,847 alerts in backlog (oldest 45 days)
- 15% of STRs filed after regulatory deadline

**Criteria:**
- POJK No. 23/POJK.01/2019 on Anti Money Laundering
- PPATK Regulation on Transaction Reporting
- Internal AML Policy requiring 100% coverage
- 14-day STR filing deadline from transaction date

**Cause:**
1. AML system not updated since 2019 implementation
2. New products launched without AML rule configuration
3. Insufficient AML analyst capacity (3 staff for 500+ daily alerts)
4. No escalation mechanism for aging alerts

**Consequence:**
- Regulatory sanctions including potential license revocation
- Reputational damage from enforcement actions
- Facilitation of money laundering activities
- Estimated regulatory penalty exposure: Rp 2-5 billion

**Corrective Action:**
1. Engage vendor for rule gap assessment (Target: 30 days)
2. Configure rules for uncovered transaction types (Target: 60 days)
3. Hire 2 additional AML analysts (Target: 45 days)
4. Clear alert backlog with prioritization framework (Target: 30 days)
5. Implement alert aging dashboard with auto-escalation (Target: 45 days)

---

## Finding 4: Business Continuity Plan Testing

**Title:** Inadequate BCP/DR Testing Frequency

**Audit Area:** Operational Risk > Business Continuity

**Severity:** MEDIUM

**Status:** Closed

**Due Date:** 2024-11-30

### 5Cs Details:

**Condition:**
Review of Business Continuity Management revealed:
- Last full DR test conducted 18 months ago (March 2023)
- Tabletop exercises performed annually (below quarterly requirement)
- Recovery time for core banking: 8 hours (target 4 hours)
- 3 critical systems have no documented recovery procedure
- Staff awareness survey shows only 45% know their BCP roles

**Criteria:**
- POJK No. 38/POJK.03/2016 on IT Risk Management
- ISO 22301:2019 Business Continuity Management
- Internal BCP Policy requiring quarterly testing
- RTO of 4 hours for critical systems

**Cause:**
1. BCP function understaffed (1 person for entire organization)
2. Business units prioritizing operational activities over testing
3. No executive sponsorship for BCP program
4. Budget constraints for DR site testing

**Consequence:**
- Extended outage during actual disaster event
- Regulatory findings during examination
- Customer impact and reputational damage
- Potential business losses during recovery

**Corrective Action:**
1. Hire additional BCP specialist (Target: 30 days) - COMPLETED
2. Schedule and complete full DR test (Target: 60 days) - COMPLETED
3. Document recovery procedures for 3 critical systems (Target: 45 days) - COMPLETED
4. Conduct BCP awareness training for all staff (Target: 30 days) - COMPLETED
5. Establish quarterly testing calendar for 2025 (Target: Immediate) - COMPLETED

---

## Finding 5: Vendor Risk Management

**Title:** Incomplete Third-Party Risk Assessments

**Audit Area:** Operational Risk > Vendor Management

**Severity:** MEDIUM

**Status:** Open

**Due Date:** 2025-03-31

### 5Cs Details:

**Condition:**
Vendor risk management review identified:
- 40% of critical vendors (8 of 20) lack current risk assessment
- Due diligence for 3 new vendors performed post-contract signing
- No ongoing monitoring of vendor performance against SLAs
- Business continuity requirements absent in 60% of contracts
- Concentration risk: 3 vendors handle 70% of IT infrastructure

**Criteria:**
- POJK No. 75/POJK.03/2016 on IT Outsourcing
- Internal Vendor Management Policy
- Risk Appetite Statement limiting vendor concentration
- Annual risk assessment requirement for critical vendors

**Cause:**
1. Decentralized vendor management across business units
2. No centralized vendor risk database
3. Procurement focused on cost vs risk considerations
4. Limited resources for ongoing vendor monitoring

**Consequence:**
- Operational disruption from vendor failures
- Data security incidents through third-party access
- Regulatory non-compliance findings
- Increased costs from vendor-related incidents

**Corrective Action:**
1. Complete risk assessment for 8 critical vendors (Target: 60 days)
2. Implement centralized vendor management system (Target: 90 days)
3. Update contract templates with BC and security requirements (Target: 30 days)
4. Develop vendor concentration reduction roadmap (Target: 45 days)
5. Establish quarterly vendor review process (Target: Immediate)

---

# End of Sample Findings
