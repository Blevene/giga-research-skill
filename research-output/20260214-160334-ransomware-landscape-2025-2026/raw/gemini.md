# Research Task: Modern Ransomware Landscape — Threat Actor Analysis (Late 2025–2026)

### Executive Summary

The ransomware landscape between late 2025 and early 2026 has undergone a structural transformation, characterized by the fragmentation of monolithic Ransomware-as-a-Service (RaaS) models into "cartels" and highly specialized, closed-access groups. While the aggregate volume of attacks has increased—peaking in Q4 2025 with record-breaking victim counts [cite: 1, 2]—the ecosystem has shifted away from the "spray-and-pray" tactics of the early 2020s toward high-precision, "big game hunting" operations.

**Key Findings:**
*   **Fragmentation and Cartels:** The dominance of singular, massive RaaS brands (like LockBit) has waned following law enforcement pressure. In their place, a "cartel" model has emerged, pioneered by groups like **DragonForce**, offering white-label infrastructure to affiliates who operate under their own sub-brands [cite: 3, 4].
*   **The Rise of Closed Groups:** A significant deviation from the RaaS model is evident in the rise of **SafePay**, an independent operation that eschews affiliates entirely to maintain operational security and retain 100% of ransom revenues [cite: 5, 6].
*   **Emerging Threat Actors:** The period saw the rapid ascent of **The Gentlemen**, **Interlock**, **TridentLocker**, and **Kazu**, each displaying mature operational capabilities immediately upon emergence, suggesting they are comprised of veteran operators from dismantled groups [cite: 7, 8, 9].
*   **Law Enforcement Impact:** Coordinated international operations, specifically **Operation Checkmate** (targeting BlackSuit) and **Operation Phobos Aetor** (targeting 8Base), successfully dismantled infrastructure but ultimately accelerated the ecosystem's fracture into smaller, harder-to-track cells [cite: 10, 11, 12].

---

## 1. The Evolving Threat Landscape (2025–2026)

The transition from 2025 to 2026 marked a pivotal shift in cybercriminal economics. The "industrialization" of cybercrime reached a new maturity level, where the barriers to entry lowered for affiliates, yet the sophistication of top-tier operators increased.

### 1.1 Ecosystem Fragmentation and the "Cartel" Model
The traditional RaaS model, where a core developer rents lockers to hundreds of low-skilled affiliates, showed signs of strain due to law enforcement infiltration and trust issues. In response, a **"Ransomware Cartel"** model appeared.
*   **White-Labeling:** The most significant business innovation in late 2025 was the introduction of white-label services. **DragonForce** began allowing trusted affiliates to use its infrastructure to deploy payloads branded under different names (e.g., **Devman**, **Mamona**), complicating attribution and evading sanctions lists [cite: 4, 7].
*   **Closed Operations:** Conversely, groups like **SafePay** and **Interlock** adopted a "closed-shop" model. By eliminating the affiliate layer, these groups reduced the risk of operational security (OpSec) leaks and retained full profit margins, a reaction to the volatility of the RaaS market [cite: 5, 13].

### 1.2 Statistical Overview
*   **Attack Volume:** Q4 2025 was the most active quarter on record, with over 2,287 observed victims [cite: 1, 2].
*   **Sector Impact:** Manufacturing remained the most targeted sector (14-22% of attacks), followed closely by Healthcare and Construction [cite: 1, 9, 14].
*   **Financial Trends:** While attack volumes rose, some reports indicated a decline in average ransom payments (median payment dropped to ~$115k-$267k) as organizations improved backup resilience and refusal-to-pay rates increased [cite: 15, 16]. However, high-profile demands remained astronomical, such as the $50 million demand in the Synnovis attack [cite: 17].

---

## 2. Profile: The "New Guard" (Emerging Actors)

This section details the most significant ransomware groups that gained prominence between mid-2025 and early 2026.

### 2.1 SafePay
**Origin/Status:** First observed late 2024; surged to become a top-tier threat in mid-to-late 2025 [cite: 5, 6].
**Operational Model:** Independent / Closed Group (Non-RaaS). SafePay is notable for **not** recruiting affiliates, a strategic choice to minimize law enforcement visibility and maximize profit retention [cite: 5].
**TTPs & Capabilities:**
*   **Access:** Primarily exploits vulnerabilities in edge devices (VPN gateways, Remote Desktop Gateways) and leverages compromised credentials [cite: 18, 19].
*   **Encryption:** Uses a bespoke encryptor sharing code similarities with LockBit 3.0 and ALPHV. Known for extremely fast encryption timelines (often <24 hours from access to encryption) [cite: 5, 20].
*   **Extortion:** Standard double extortion (encryption + data theft).
**Notable Campaigns:**
*   **Ingram Micro (July 2025):** A massive attack on the global IT distributor, disrupting operations across the US, Europe, and Asia. SafePay threatened to leak 3.5 TB of data [cite: 19, 21].
**Analyst Assessment:** SafePay represents the "professionalization" of independent ransomware teams. Their refusal to adopt the RaaS model suggests a desire for longevity over rapid scaling.

### 2.2 The Gentlemen
**Origin/Status:** Emerged July/August 2025; highly active by Q4 2025 [cite: 8, 22].
**Operational Model:** RaaS / Private Affiliate Program.
**Attribution:** Linked to the threat actor alias "hastalamuerte" and "Zeta88" on underground forums. Operators previously sought access to Qilin and LockBit panels before developing their own [cite: 23].
**TTPs & Capabilities:**
*   **Targeting:** Focuses on enterprise environments with centralized Active Directory.
*   **Tooling:** Utilizes "The Gentlemen" locker (XChaCha20 + Curve25519 encryption) with variants for **Windows, Linux, and ESXi**.
*   **Tactics:** Known for modifying Group Policy Objects (GPO) to deploy ransomware domain-wide. They exfiltrate data *before* encryption to ensure leverage [cite: 8, 24].
**Notable Campaigns:**
*   Targeted 17+ countries within months of emergence, with a heavy focus on Manufacturing and Healthcare [cite: 3, 8].
**Analyst Assessment:** The Gentlemen's rapid maturity and use of "corporate" branding imply experienced operators. Their specific exclusion of CIS (Commonwealth of Independent States) targets suggests a Russian or Eastern European origin [cite: 25].

### 2.3 Interlock
**Origin/Status:** First observed September 2024; gained significant traction in late 2025 [cite: 13, 26].
**Operational Model:** Opportunistic / Closed Group.
**TTPs & Capabilities:**
*   **Initial Access (Social Engineering):** Distinctive use of the **"ClickFix"** technique—tricking users into running malicious PowerShell scripts disguised as browser or software updates (e.g., "Fix Chrome") [cite: 13, 27].
*   **Cross-Platform:** Developed payloads for **FreeBSD** and Linux, indicating a capability to target backend infrastructure beyond standard Windows servers [cite: 27, 28].
*   **Extortion:** Double extortion via their "Worldwide Secrets Blog" leak site.
**Notable Campaigns:**
*   **City of St. Paul, MN (July/August 2025):** A high-profile attack that disrupted municipal services and required National Guard assistance for recovery. Interlock stole 43GB of data [cite: 13, 29, 30].
*   **DaVita (April 2025):** Breach of a kidney dialysis provider, impacting 200,000+ patients [cite: 13].
**Analyst Assessment:** Interlock distinguishes itself through advanced social engineering (ClickFix) rather than zero-day exploits, making them dangerous to organizations with weak user awareness training.

### 2.4 TridentLocker
**Origin/Status:** Emerged late November 2025 [cite: 31].
**Operational Model:** RaaS / Data Broker.
**TTPs & Capabilities:**
*   **Targeting:** High focus on government contractors and entities managing regulated data.
*   **Tactics:** Extensive anti-analysis capabilities (virtualization detection, timestomping). Appends `.benzona` extension in some variants (possible code overlap or confusion in reporting with Benzona group) [cite: 9].
**Notable Campaigns:**
*   **Sedgwick Government Solutions (Dec 2025/Jan 2026):** Compromised a federal contractor serving the DHS and CISA. Exfiltrated 3.4 GB of data from an isolated file transfer system [cite: 31, 32].
**Analyst Assessment:** TridentLocker's willingness to target federal contractors (and arguably "poke the bear" of US law enforcement) suggests a high risk tolerance or political shielding.

### 2.5 Kazu
**Origin/Status:** Emerged mid-2025 [cite: 33].
**Operational Model:** Double Extortion.
**TTPs & Capabilities:**
*   **Technical:** Deploys **SmokeLoader** as an initial access tool. Ransomware payload identified as a **LockBit 5.0 variant**, utilizing locale-checks to avoid targeting CIS nations [cite: 9, 33].
*   **Geography:** Strong focus on the "Global South" (Latin America, SE Asia) and smaller developed nations (New Zealand) [cite: 33].
**Notable Campaigns:**
*   **Manage My Health (Dec 2025):** Breach of New Zealand’s largest patient portal, impacting ~120,000 users [cite: 34, 35].
**Analyst Assessment:** Kazu appears to be utilizing leaked or purchased builders (LockBit 5.0) rather than developing proprietary encryption, fitting the profile of a sophisticated affiliate striking out on their own.

---

## 3. Evolution of Established Actors

While new groups surged, established players adapted to survive law enforcement pressure.

### 3.1 DragonForce: The "Cartel" Pivot
**Status:** Active since 2023; rebranded late 2025.
**Evolution:** DragonForce shifted from a standard RaaS to a **"Ransomware Cartel"**.
*   **Business Model:** They now act as an infrastructure provider, allowing affiliates to "white-label" the ransomware. This spawned sub-variants like **Devman** and **Mamona**, which use DragonForce lockers but different branding to confuse defenders [cite: 4, 7, 36].
*   **Affiliations:** Strong links to **Scattered Spider** (the group behind the 2023 MGM attacks), creating a "Scattered Lapsus$ Hunters" ecosystem [cite: 29, 36].
*   **TTPs:** Uses **Bring Your Own Vulnerable Driver (BYOVD)** techniques to disable EDR [cite: 3].

### 3.2 Qilin: The Dominant Predator
**Status:** Surged in 2025 to become arguably the most prolific group following the decline of LockBit and RansomHub [cite: 14, 37].
**Notable Campaign:** The **Synnovis** attack (June 2024/2025 context) was a watershed moment, disrupting London hospitals for months and demanding $50 million. This cemented Qilin's reputation for ruthlessness [cite: 17, 38].
**Tactics:**
*   **Linux/ESXi Focus:** Highly effective Rust-based encryptors for virtualized environments.
*   **Recruitment:** Aggressively recruited displaced affiliates from disbanded groups like RansomHub [cite: 1].

---

## 4. Law Enforcement Actions & Impact

Law enforcement agencies (LEAs) conducted significant operations in 2025, forcing threat actors to decentralize.

### 4.1 Operation Checkmate (July 2025)
*   **Target:** **BlackSuit** (successor to Royal ransomware).
*   **Action:** A Europol/FBI-led takedown seized four servers and nine domains, confiscating over $1 million in cryptocurrency [cite: 10, 11, 39].
*   **Impact:** While the operation disrupted infrastructure, intelligence suggests BlackSuit operators quickly pivoted, with some elements rebranding or merging into the **Chaos** ransomware operation [cite: 11, 40]. The "whack-a-mole" dynamic persists.

### 4.2 Operation Phobos Aetor (February 2025)
*   **Target:** **8Base** and **Phobos** ransomware networks.
*   **Action:** Coordinated arrests of four suspects in Thailand and seizure of dark web leak sites [cite: 10, 12, 41].
*   **Significance:** 8Base was a high-volume group targeting SMBs. The arrests of personnel (not just server seizures) in Southeast Asia highlights the global reach of Western law enforcement.

### 4.3 Observable Impacts on Behavior
1.  **Reduced RaaS Reliability:** High-profile takedowns of central RaaS infrastructure (like LockBit and BlackSuit) have driven capable affiliates toward **closed groups** (SafePay) or **decentralized cartels** (DragonForce) to avoid "single point of failure" risks [cite: 5, 14].
2.  **Faster Rebranding:** The "lifecycle" of a ransomware brand has shortened. Groups like **Benzona** and **Minteye** appeared and disappeared or rebranded rapidly to shake off LEA tracking [cite: 9, 14].

---

## 5. Tactical Adaptations (TTPs)

Threat actors in late 2025/2026 have refined their tradecraft to bypass modern defenses (EDR/MDR).

### 5.1 "ClickFix" and Social Engineering
Groups like **Interlock** have moved away from relying solely on vulnerability exploitation (which is time-consuming) to user-interaction attacks.
*   **Technique:** Users visiting compromised sites are presented with a fake error (e.g., "Chrome Update Failed") and instructed to copy-paste a PowerShell script into their terminal to "fix" the issue. This bypasses many automated email filters and perimeter defenses [cite: 13, 27].

### 5.2 White-Labeling and Polymorphism
To confuse attribution and threat intelligence feeds, cartels like **DragonForce** provide builders that allow affiliates to generate unique binaries with custom extensions (e.g., `.devman`, `.mamona`) and ransom notes. This "white-labeling" prevents security vendors from easily clustering attacks under a single threat actor profile [cite: 4, 7].

### 5.3 Virtualization Targeting (ESXi)
Almost every major group profiled (**Qilin, DragonForce, The Gentlemen**) has prioritized **Linux/ESXi encryptors** [cite: 3, 17, 22].
*   **Why:** Enterprise servers often run on ESXi; encrypting the hypervisor locks all virtual machines simultaneously. Furthermore, Linux environments often lack the robust EDR coverage found on Windows endpoints.

### 5.4 Beyond Double Extortion
While data theft is standard, actors are escalating pressure:
*   **Direct Contact:** Groups like **The Gentlemen** and **SafePay** are increasingly contacting employees, executives, and even clients directly (via phone or email) to force negotiations [cite: 42].
*   **DDoS-as-a-Service:** Re-integration of DDoS attacks to paralyze victim websites during negotiations is returning (e.g., Chaos group) [cite: 43].

---

## 6. Target Demographics

### 6.1 Industry Sectors
*   **Manufacturing:** The most targeted sector (approx. 20-22% of attacks in 2025) due to its low tolerance for downtime and often legacy OT (Operational Technology) environments [cite: 9, 14].
*   **Healthcare:** despite some groups claiming to avoid it, Healthcare remains a primary target (e.g., Synnovis, DaVita, Manage My Health). **Qilin** specifically disproportionately targets this sector [cite: 1].
*   **Government/Critical Infrastructure:** A notable shift in late 2025 was the brazen targeting of government entities (City of St. Paul) and federal contractors (Sedgwick), suggesting a disregard for the "red lines" that previously deterred some groups [cite: 29, 31].

### 6.2 Geography
*   **United States:** Remains the primary target (~47-52% of all attacks) due to the perceived ability of victims to pay high ransoms [cite: 9, 14, 15].
*   **Global Expansion:** A significant rise in attacks in the **APAC** and **LATAM** regions.
    *   **Kazu** focuses on New Zealand, Thailand, and Colombia [cite: 33, 34].
    *   **The Gentlemen** heavily targeted Brazil and Thailand alongside the US [cite: 8, 24].
    *   **Benzona** activity observed in Romania and Côte d'Ivoire [cite: 44, 45].

---

### Conclusion
The ransomware ecosystem of 2026 is defined by its **resilience through decentralization**. The "mega-cartels" of the past have been replaced by a fluid network of white-label operations, closed specialist teams, and aggressive newcomers. For defenders, this means attribution is harder, and the threat surface has expanded to include aggressive social engineering (ClickFix) and deep infrastructure targeting (ESXi). Law enforcement successes, while operationally disruptive, have not yet curbed the global volume of attacks, driving the adversary to evolve faster than the defense.

**Sources:**
1. [hipaajournal.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGsabZfkKA6-P-_jmmlTh1RnRubLjnyrabr6vwayTA-hezgXublIuJrNVgzAudBdnwYwVAMKV8YCGBDIoSNfUYIVsHcVgfFocZvpAlyyX6Gq4qG50jzM6njMCFXtEZEMtp2gUSgtU66ta_0ygETRUJNlHsq4U85b3h_mUr7p41z6w==)
2. [guidepointsecurity.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGgpEyON4ySTCDyd2fu1wJrJSgFVkQA2LnDM7R4KZPXGI78Mgfq_NlHr5vhkGQOE9nubcJ0FjSzc0fYkFd4cM1lK1e5cCh39VCaCK5GxCGPJaiziKmXYmsiLtuWG-Cx03cYoRqwaQVh_j-WdXCKlLyKPizQE8xZrKg5Lr1xcl8KDx6GnA0Nvk1zGHeElRR6uVbFWN01RatxOWal5aBtnfYPyjBcMg==)
3. [nordstellar.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFu1JjUupgYTvgbxUH_61zjk4gpZ3Zawsyt-q_qZZ7gza7iibpMHgtbneIuAy5Y-x-KLwfE8QX4bgNmXZLg9fiHuhCgTtofSh1tHIDLd_XugeAYlp6yPdEvSx0N64BuIGgtKDmSOQ==)
4. [industrialcyber.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6F-gdoL3FHIUGMcdBbhntGqsTqCXDZwY01KyIFuwXVHFBj1owu4v5OFqMC1_kpTUBdVk4MhXnny2My-xR5cAx5FnhMpyWEAYb9YlqrjEKqvwsfHeaYP4yI53l6Ur01zZIOacKmK6X1Z2OJHKG_SLncCStap7_Lo67b5tbwYx--d6a3XDKO0FqutkEYQhYWzM-8iud7gvu5lAFr8IV5dFvEjaUEahZblX7bkmVxZMKttZX8PHSTs7ljO24o-doAlc_2pq3fTM=)
5. [halcyon.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHhideicaaGWNkpgLyIs65z_j-aFmFZdTVqGAOiuHjXFcKcpQlmJDpeXXtjQyyua2HD6lAvAYuApYvf-PdOOGHf05eR1JU-Ca5q9jYJOVKXMmB6rsEXxvNtq3A7Nvb-zoq-)
6. [acronis.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEIvDn_wZGBQsSsURbC4ENJQ4qxb3mh4B0_5Zevwbri_cZdIQqXueF_oyHFrP5-edD_9pIfs1tBlwFoHG1fefO3DcHTKrD8iE_LjxGrZ5XYTS0NgwCdMwmLJUV_p_KxS-miNIc18ZgIci7T15qcbxdVVa3O7l4gxwd_jCSjhuxWmKDxESYntO7Df6qgvovGoXVGvZiP)
7. [cyble.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFe_bqPqlINO9x2ihQv1ivWghjnQIaOncznVQbhPpKfLM9324BX8PGNYEwvYfgElRtGugBU4G_CTVuzCQUiDGE6vieXsGdkhkjj6b69Rpvyp_2T4U5dIq1sMtV-bIDAJxcmL798YCT1dNEvlbGiz9RIxASmVVq70piEqwKCH7EngvMEzjWsYq6rFw==)
8. [trendmicro.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGCFXhR-Tjmm9yrheLZXcx3bOQpNhMVuVo-s9-cGcx3G3TRBG-7kUgVlYn8Tw1LT8T6BHrg_I8fTU_JJJ7AgNzQaxxNaxIkzC0nebIAhozBZFf8G5ZSfNjsLnBSaQRqGb52sSlRTFG9Nw_GmNCrQ6_XoZYcPSWrPIUSKvSy3Cv1ia10Nlpd4Uce2UbgEA==)
9. [halcyon.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEao9bgZ8Y_-X4KRQnM00NLRP8883OIaU11-OtDerbp9q7jcBIgqJxDDlRlTI8kqGnCwer_vTKzmR_yVmuNy3lnakvmbIvUV9GgTQU83TVzSlPJUu4ifaMLWvl6F-x-VErv_eQE5MJJwwjIAjHuEVuM1zfHRiqSpQ_q4WiUW5K8NSR9eLLoZ05zsDfM_etZhFupAv1sO6nekCuF)
10. [socradar.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF1asvIZsKlvoMWwTnhp42pZRzAkwD43qizOfewY7o9KLlum8ObjsRqIfomYfu5ipXM_JArYX88zfFreklJIUMlTYJmHPTQf-Pzt0633qVSATSWfb0sbdb_cZCWp-eEcXrIZdtAqE0bytAFNh5rm2t9Q-3FcvmBlu5RkyPLx4fzFaQ=)
11. [securityandtechnology.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFRtiNVBh-uKiL11TeTPyYAPMXK-kN45ZnMV2OLiCRhewePaKuSgc7q_KoAC_zrj-Ji2gl3ST2OEfG7glj9AJh16eXU1Bxz45-yxXhSsn5EwP1aIeQH2DTUFdareuqgMQGe6MVh8lvKp8UE6ZATTXc0XZZAAKuWdhjIUsQW5AgC)
12. [securityaffairs.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGOGLRMQBUEnQ5KJYzvsOPEFt4yTSQx8ELqJ9dDXnTkuM6T4Z5mD9cbh7oq36U8wYOig0Mi5qUJQp4t5aPjwgvckhNal2IIYODyC15p1l5b3KmI1XTPVrwrPKhocHnTBWUHjkPo1lpE_jmcpSFi8v2QxsW7vl1pYs9YvOODGWr4ShfIDRL4cxsUH9hSfWAz49tG)
13. [arcticwolf.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGKuVn7yd7r8xZ07eQTlBzrqVEZv1ggParfYnhMljpieFS7MPw219bbF5sKN5dAryc8iim8sQxzriJ4R95Dh8RJXOzG7QYbfjrYQz6d31EnH4HBkORMCyTSRoMyPN3Y7BVxxnIsGRIGizNkC6UEWH5drzodW2qA26IsMaHOJFbFi26He2lBkg==)
14. [industrialcyber.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEKY-cNYBF8AZVKpQK92tILPitgxcFA2bWTEZB6NaVGlf-wltK3tuvk061gGT-Jb4eZ10R-GQt1MUONsIGXIVqe4l6s5XavJJsVdg5wnJnIsfMMvALRyoUibCSDHYHAmQotX1XIYMF37ZPm2iUH-fNE119XkTE62oZPr9hfgU1ReSuByh-uUjcoJEezzGrVGygiFua8lRYdeRVWmLLRfKyBW8olQmBJ-acKHKOG7VGUwTbLc7EnG5nT0ulwAidd6WPEuGfI5r4O_g==)
15. [techtarget.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHLYkUmj2T0m9Mb_ik8fVySgdCPvPQZVNcLVOygTW_X7JzAy8WKrRbiM9t5z4C0a-OMhyWG8xh6vWY421WSnO5hzgInegVnhxmMaGSuqWbSncdl0BPZ9Y5h-oVAFAziwfcEVAjo2GtnCwMCsoaCUYAtnIB3qG96XWaul-uT7b4Qz6lBfp79lCgJabC_DTv1)
16. [varonis.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEFTJQDbDuDZcX6q0ikObO-aEB2E3WAhDW7UugFth9n4RC4KhHOKjbDNKCRj3olWCHHhU6AOR6WwFjXmkaWLCt8Zwz1XlYqrfQNDM51BAdaekRk7t1JZ_jNPNRBSwlolBIfzmyn5nEqFQ==)
17. [checkpoint.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEoFkGZoKp8iUbfaIMY2O4hmY3mQbjAtQVQO1hujjNaI6dZCm644k3rZdk_G_9sb1ejqDdNfATTZNM757zRRg7nMOgK4RklvHwWm27bI0bp6Jig72Y39SKCMA9pPIWQHJiluWsYrG4M38s_42y12Wbu9cHRmX3maAGMX8SEsclQDJbVAsMHMLkRvA==)
18. [threatlocker.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGMGJqcC3l1P6gtjYazBSb7ewtCReDDDZvPrj-NFMwTB7i8VZqLs5oQUfcbGrYwm-iBX4dgtNVONGbiNUXFjwez-CuS9aLqsLhxelYeKF13KQtPI_Fv6lQYTCdgy763vWzyO44V0XCYnpLbR56fM_-QRJ-Tarzh0baH5PHTZqSzq_Fun1R3UnZtL3qKog69QrEJYnu3NQ==)
19. [blacksmithinfosec.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFTP3kHuc8nvEkzDVJEcq5wl4-TJWSCKDyzRRwftLKa-AFu6b9MoBIoump07F_BflKodPHPMzUl8NJz0Mno9b9kCVpca48aiP90rXGtgUTpvbEi7p-kLMJnOl4ScMa1SskLDFYy7p1xxlLooDyVgBKhy_oLildkZ-p0khjzInjbhZUEzl051-nty-beQUQww3upEN_BOAk=)
20. [checkpoint.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHnDpAABxhmjJpminQj6okjwwRiNKLpKJSUTkFdHLZM7F2JUUJRxEiaTxw_yFvrF3zpSqDiGdX0yFE178Zv0pz-c0-xxwwHpm9pLFHxFZ0FGTsN2BZDsBezbLUXwJ977HVT7exYQjEOOio_WD8uT8gfD3vTYZve-XK8tX7ATrklbNXtGxi3P9-1Qbhf)
21. [msspalert.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH6QUwYuBiaHK6ex_NKtaBN8z3HB79PjpxIx4eIlu0bmhDjg8CBOsGND5LkFXn5K59DCm_1_cDKDiqi8qjfSlcyxZGieZDAfbZjIthRKI1304cX2sboQzNR1RHVz0-d7f2VlDiz_V-H7N1ote4IBx0ws0e3dYM6mInwVUsC_AvRLB-_s94wb3j7GAJwf_nlucu3q04U)
22. [cybereason.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG_4XE1ij2YeJD_M2ch8W4oQ7-DNho0FCtu_BabTP3moH2oeClGn4oZyrs1EdnEq8-KEtLEkUbs4aRIaFBRyBCG77RvMwhQz5lmcvUwGR3wLNd6HK00S15ahOZiaJGolNUI4p1E7si_VwyFYRf5RA==)
23. [provendata.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHiyI2fjUkc_6VJ041LWcUN9nfjphsDvtqZWhNOquI6vyx50hKLgJwBx8cj3hA08qdMstNeUvxSN0wasJiAqaYMfgUQ1D25S8P-TsGguSpMg9yoHYMeDjsNNs0YOT28L5ZxrKdYtbOXyRF3kg==)
24. [socradar.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG9m-H8yAVy8pvTApeJSdLyzmifFeD10cDMIBn_-217soSSLsGKG8ooCdL3WUpEGL7xvzGvbMHChoTYnOQRVGz6GWyp2kouBLHux805D1vhE1L9GCHfmemg-h8K17Sl7wBfv0tdSy85GdAHIMs-dEKr0YofZUxq6XXm)
25. [gbhackers.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEQfM-ciTqouFpISe4GAdD2cFoqYWVFbaT6ObyYIYOw4113HUiPXu_k9ekcvly7qm26xVRuMemn5oZZCGeq3BQA2ftVUL0BFCxLn0rcx3v_UMpdZmNEg_h04tSwK_tNOucMado=)
26. [cyble.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFboWPuwqFzM7wIzrWbCWjcTO0iiAiZ4JHw60Vh_dJWr5Q3tC61dou3pur59XF6Q7UTOWdhaOqtJeFaKC38_7AK1f_8Bqh97xuYUmh5kCiCKZTLTVlQSbCCKFzjU4F_rJIdMN2VYggyqv-_g0BIEaPXnQiuqjeFGJ2n)
27. [socradar.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEgJeFffeVaIy2eKgJN6Rb0JkO7cM0Tb83wxB-_5O3FY8mGZs31utBkCmLp775zd-HR5Upq5_H_ki9d_YGYkl2RhRlXvSZjcCfm1HoeVKYW66SGkbXhmk2GHrLetMQdyfMxB1Cei9eWqpP9yZ2U1BPV3-vI-yY=)
28. [quorumcyber.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHMdUgIR6-YrnbsI5st-o4XNAsVySvL2mNbGfyanaPnZ_BY8yiZSqTXKL-VYrfwwSL4cWJTtTCbFdss1BVk58QZUSCOvLruO2zItUGSpyjDJ1paRdP2j029Y2lXAQCJDdbtOuWqFRmYefUL-X4zQ-KLolLRut5ev--UEQHfDQD1)
29. [integrity360.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYqkanfGfZ-7ploQWwNHjBoeeLv_FaYFR4i1yMbyso9hTOQNtg_e_KtHd4zmlCyiHXjzLRmiNQzanlzAnt9VI_V-2MXvqFY2xbwJ5dIhGu0nClGetZ4OmjoW1hAxsTaD6RJKB8CK7G3h2Pn93zW17uhCZvrip5o2mpnOgGpiLBCs-e_Iiy--5z_uUwdWPASRIHOv-5_w==)
30. [salvagedata.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEV6iGHIeu1Ohpcf3_J6hJkEWLfTY7fQYs8oah-LAoytBdFwCxhYFtQ6NGPCD6YZADNyjlbNPa2w-WxfaNlc4jJ1c3DDrmsos2Lm7COvxRgge928VdlD_LOmOm6r0oZJvVVSqJJE2AD7fcPg5jaDJv7Vg==)
31. [securityaffairs.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFQTy_ZEhvNvsbsnPBFKUE9Fc9QwIQP45yqLgLyFES7us13uGF982zUZX9YyL7ZN-fpFh9ZHIxc3xxnqzNCd771LmiBPJ8hpfi475tVboYiYuMYOAPq2X4Mn15w5OHDvTIm7Cc5mXSwtY-N5aQtNTHuwiankYM3SZMqrdKpB40D4Gc0fHPWokcEtq8VFtERPdqzai7CQ6i8F2iWafiank2edVhDO7_SiSDUk4WZvO0=)
32. [cyberpress.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHsY2uLovrCO6ZcLqjmR_2w9-ExjrCq6dhbsHlf717ZGmLUmQZFnP__1u8cAZ_mxIgv2_Kz4P0l9RcI1wRgIXUxUA3BdA6pqs6dS8nK8VsqhY_bYycEUFI_oFHH4VK-VzoRDhgR2I6R20maM1gmNudtIwvSGk8R)
33. [redpiranha.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFu1d6Tnb8zMZxN_Nm91wB6yDnFp_n-YAldEiXa71HCCOMR1SVSygA6m_30bN7W6NbNKdQcyTjrHWlYRroHpEBjn1V8spBgMlf7XnszAqHnxQr9WNGwz4sm-L2YBEHwAUlRkci___T8NGntGetUtqBnq0uKURQodroYcaj5SyGzIV8Z69Ua6cUP)
34. [rnz.co.nz](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEL8ui3xIdgQB25P1OhIWmpdeZA4KU5XE5llrae7KAHMOF9s4q_TIHZ3dzurP-bSSgTGWh25NNsyhJqFOF2Fv7TJDFP3SoCYor0DaDdDs525SPpuv9DfywioCOwPPKSemNWPaszIeO98OwQ07kRYT1ksnbHSguSO4vxV8IBLaIk9n0fGR7xOVV3mNx7Gak_mVrrNqkTJ-dbpbKReFoOtPR8XCiiWtqMXmYEsSQUgC1aPDc_t5C9fg7o)
35. [bankinfosecurity.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHm0e-FKLZZukCsFqchZ8uFe277kS5mnJrk7sCGsbJcBkdAq-IBDAVEnmwZmQ8ty0NzqUmHmROieYDELahNBqpYBDpm04RODWOl3raAxi2Gib0QqCZ-R6sbPy9x_5a_NJCQZ9km6-zLPqFcWZ8bU3fnl1_NyoqMFT_YGg0lLSfKGaxAKOq04LKMOfwpqOL27Q==)
36. [acronis.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGpCcqY1BRJy6XO3-d8Q3Y21ve5MR7naHSzqMgRPxpEpFFdZhVfndSW9JeBK8aPONWooSAzAYl8kmP_VRNSIOocqm7OvqWU4gq56-ecexIN_Cu-11zSFsyEdmVho8cWv-2ooIApWAFvIoSBBMLK9tugqKdeCeNEt07iuRLbhs3Ky8bUawoAZ1bpMoDh_3st7A==)
37. [industrialcyber.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEyOAbzT89vVbk8kWMW3DPCP1rsoSOmw6wEpxwphoOIS91eaqytTLBB3NQ_jgaTBCqYLN_GTf1MGFu7NxeTuHo9rubr9fWs6YBDSIxXHY-oroEeahJZzTMK2rnbXzmBq5z0VHpJpTbJEIAdMfOUDK5h2YOgp6ON0b8cusRKBi1DYX7sJErR6U1ZVLo0F3iUETl3XOuy3gU9jdOmpWzxwBaqqEWsyKISOUDc3xsfv8pNEToqP9hsawXrpGORwDy-p1NfFSA4PyZALCGyqTU=)
38. [blackfog.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHPMh4FIGQSZihui-tWmnOOu7dFRgfWWYHx9G5su_KSLOnW3AI96ubbsiZ6sbzEP9p8rnjC_xcBr0jLNFX99Prgr0441i-lF_cfrdyeGSwu1tnCC98UNxr2jVTxrL4Bb_JcZKwiRTOeOmsMC9xPqgK0wW1ohbw4eTpmuhMpUEWFUsA=)
39. [computerweekly.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEN-b8E84HUBXHtM14uUa603IzUQLTweIZiYPEz1uuiBAEmEzaWZNDBwr_qV-RHHPQNz_JzhGEVz1rB8q9J2ix4OEO09sJM65QhZmKOMo5GqT0FubwZHIk629_HpnHCIVPu3-BYajBXLebvhifStJN8If-zEENw7aXGJdZfQmaltu1FYGeYMl16YLq0fmJRNba7tDYXqPHymXyU3p7IC2s2)
40. [therecord.media](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF4BHb4ifeA1Gj-LMAfFYssYODpdXgm-RzREuu9DvXvSm9iEF5gHy4iuriBIxY4MlF9f3P2vEX00IalJbbUr5RrssZ7UurIjuGmHMyWpOmGjIe_v7_mceiqlQgrhYMD0jNVIBcV8AekaOm55c8=)
41. [cyberdaily.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFqLcFKmySqyh_yqjpe1QtLhs2rfy6JXhKD0W-hfiHF-qtDUVrN3j7XPjQSlqjX0k36xxCLapdYl-kmWDsz48D5hOmmstjzqSN_mR1Z9dFTRZBugB4ZSJ-gCkqwj-JgdGy0TO8NvoY1oEn5QbJKyl5mPdKsmPg-TCabgRff4z7kevK787UA9wNyVo29XvvDmCC8OawngaS6J1A=)
42. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFhCTmDfxa_4s1XyCEY-LCvVWsHnXl41G7ylWGIrzMR5Qwio_25cbe3CvrW42ymeup5yYd1RzrW81J_yRdJpUdYefdK0kQ1_M6al6zageY4xEr-YJG3PITTfzfcVejhzgmvMd1EuxK1kBURMiIJ9fyUfHTXJC19YU4Kr-O64qwgGIrk)
43. [recordedfuture.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGU787qq4l01SxRvdAEbc8diJPQzMf8a5OwwEwHbuafEvsbfqP6CP6yb_Tu-FHzfNJfax9pvmf6q96cWqCPDPG9p4JemuM5wY5q9ANgJjx3jf1xpehsDiXVpXHuPQOPBxp7iZmatSo4p72WvGgFVMxc4w==)
44. [broadcom.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGjp4wq4JHovD5kicx2k_f_UMO9Rhz4QwxsjrOxmCzKdH4lKAyjTKbdtdcbNQqz9exff87hFKyzA1NlTM8J_B3CDNnE8ZnIG1MdHBeSF_3AW9uY_qecOYaO3UZQ68hVYBU8GEcYZ7Sbm3Ns8RmOzjCNHTQBLlYufLc5QqM8iXdzNz8W3SK9QDpo3bUET9o=)
45. [redpiranha.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHosBGQFhS0ZvRadwbO8RlUlJqQiWgCGbn0igJi6LRLEHj94HbiXbHaxiXrgd0ZGVrvQCVN38gCwWDx_ZaK1nOKNgWGGJ69HgPA8rdndVreqhQkzdc-erwqsimpuyAZJTOoUbsnqqHtPNylWtiYzAMEZIKjDt3AEAh7vcxAD6hyryycuwgtcxdY)
