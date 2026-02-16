# Modern Ransomware Landscape (Late 2025-2026) — Research Report

## Executive Summary

The ransomware threat landscape underwent a fundamental structural transformation between late 2025 and early 2026. All three research providers agree on the core narrative: the era of dominant mega-syndicates has fractured into a highly fragmented ecosystem of smaller, agile groups. Attack volumes reached unprecedented levels — with estimates ranging from 7,200 to 7,679 reported incidents in 2025, representing a 32-47% increase over 2024 — even as ransom payment rates plummeted to historic lows of 23-25% and average payment sizes declined. This paradox of rising volume but falling revenue drove groups to innovate in both business models and extortion tactics.

The fragmentation was catalyzed by law enforcement disruptions of major operations (LockBit via Operation Cronos, ALPHV/BlackCat's exit scam, RansomHub's sudden collapse in April 2025) and accelerated by the emergence of 57 new ransomware groups and 27 new extortion groups during 2025, bringing the total number of distinct active groups to approximately 124 — a 46% increase over 2024. By Q3 2025, over 80 separate ransomware leak sites were active simultaneously. The ecosystem responded with structural innovation: DragonForce pioneered a "white-label cartel" model, SafePay demonstrated the viability of closed non-RaaS operations, and groups like Qilin absorbed displaced affiliates to become the most prolific operation globally with over 1,100 victims in 2025.

Tactically, the period saw the erosion of remaining "ethical" constraints (LockBit 5.0 explicitly permitted critical infrastructure targeting), the rise of data-only extortion as a standalone model, the blurring of nation-state and criminal operations (Chinese APT groups deploying Warlock ransomware via SharePoint zero-days), and an escalation to physical threats against executives. Despite notable law enforcement successes — Operation Checkmate (BlackSuit), Operation Phobos Aetor (8Base), and continued Scattered Spider arrests — overall attack volumes continued to rise, confirming that the affiliate-driven model is fundamentally resilient to infrastructure-focused disruption.

## Methodology

Synthesized from research conducted via: Claude (Anthropic), OpenAI Deep Research, Gemini Deep Research. Each provider independently researched the same topic domain. Claude's report provided strong analytical structure and assessment judgments but lacked URL-level citations. Gemini's report was concise with real citations via Google grounding (Vertex AI redirect URLs). OpenAI's report was the most extensive, with dense inline URL citations to primary sources.

Citation validation depth: 0 (none). All claims are reported as-stated by their source providers.

---

## Findings

### 1. Ecosystem Fragmentation and New Business Models

**The ransomware ecosystem underwent radical fragmentation in 2025, shattering the dominance of a few large RaaS platforms into a diverse landscape of 80+ simultaneously active operations.** [All providers]

Key statistics on fragmentation:
- 57 new ransomware groups and 27 new extortion groups emerged in 2025, bringing the total to ~124 active groups — a 46% year-over-year increase [Claude]
- Over 80 separate ransomware leak sites were active by Q3 2025 ([reliaquest.com](https://reliaquest.com/blog/threat-spotlight-ransomware-and-cyber-extortion-in-q3-2025/)) [OpenAI]
- Q4 2025 was the most active quarter on record, with over 2,287 observed victims [Gemini]
- Late May 2025 alone saw at least seven new gangs launch leak sites ([foresiet.com](https://foresiet.com/blog/new-ransomware-groups-emerge-in-may-2025/)) [OpenAI]

**Driving forces behind fragmentation** [All providers]:
1. Law enforcement disruptions of LockBit (Operation Cronos, Feb 2024) and ALPHV/BlackCat (exit scam, early 2025) eliminated dominant platforms
2. RansomHub's sudden collapse in April 2025 displaced hundreds of affiliates
3. Declining ransom payment rates (23-25%) forced groups to differentiate or die
4. Lowered barriers to entry through leaked source code (Babuk, LockBit builder, INC Ransom, VanHelsing)

**New business model innovations** [All providers]:
- **White-label cartel model (DragonForce):** Affiliates operate under their own branding while using DragonForce infrastructure, complicating attribution [All providers]
- **Closed non-RaaS operations (SafePay, Interlock):** Eliminating the affiliate layer entirely for tighter OPSEC and 100% profit retention [Gemini, Claude]
- **Multi-tier extortion services (Anubis):** Offering traditional RaaS (80% to affiliates), data-theft-only extortion (60%), and "access monetization" (50%) as distinct product lines [Claude]
- **Data-only extortion (World Leaks/Hunters International):** Skip encryption entirely, relying purely on data theft and leak threats ([flashpoint.io](https://flashpoint.io/blog/new-ransomware-as-a-service-raas-groups-to-watch-in-2025/)) [OpenAI]

**Revenue sharing evolution:** Fees vary from flat monthly rates to 20-40% revenue shares. DragonForce attracts affiliates with particularly low profit-share requirements. [Claude]

### 2. Emerging Threat Actor Profiles

#### Sinobi
- **Origin:** Mid-June 2025; traces technical lineage to INC Ransomware (Aug 2023), whose source code was sold for $300,000 and acquired by Lynx operators in July 2024 [Claude, OpenAI]
- **Model:** Closed, hybrid RaaS — small core team with carefully vetted affiliates; does not publicly recruit [Claude, OpenAI]
- **TTPs:** Stolen VPN credentials (CVE-2024-53704 exploitation), Curve25519 + AES-128-CTR encryption, Tor-based leak infrastructure across nine hidden services, extensive living-off-the-land (LotL/LOLBins) use, enterprise-aware stealth operations prioritizing control before monetization [All providers]
- **Notable Campaigns:** 61 incidents in October 2025 targeting U.S. construction, healthcare, and manufacturing; nearly all victims (92%) in the United States; focus on mid-market organizations with $10-50M annual revenue [Claude]
- **Status:** Active. ~138 victims by late 2025. Manufacturing bears highest sector risk at more than double the second-highest sector [All providers]

#### The Gentlemen
- **Origin:** July 2025; operators previously explored access to Qilin and LockBit panels before developing their own platform, indicating they "studied the market first" ([esecurityplanet.com](https://www.esecurityplanet.com/threats/these-gentlemen-arent-gentle-rapidly-evolving-ransomware-threat/)) [All providers]
- **Model:** RaaS / Private Affiliate Program [Gemini, OpenAI]
- **TTPs:** Cross-platform lockers (Windows, Linux, ESXi), XChaCha20 + Curve25519 encryption, Group Policy Object (GPO) manipulation for domain-wide deployment, BYOVD via ThrottleStop.sys driver (CVE-2025-7771) to disable EDR, AnyDesk and compromised RDP for remote access [All providers]
- **Notable Campaigns:** 48-63+ victims across 17+ countries within first months; Romanian energy provider incident (late December 2025); heavy focus on manufacturing and healthcare [All providers]
- **Status:** Active and expanding into 2026. CIS exclusion in targeting suggests Russian/Eastern European origin [Gemini]

#### DevMan
- **Origin:** April 2025; descended from Conti collective and DragonForce RaaS lineage ([halcyon.ai](https://www.halcyon.ai/threat-group/devman)) [OpenAI, Gemini]
- **Model:** Closed affiliate outfit partnering across multiple RaaS platforms (Qilin, Apos, RansomHub) [OpenAI]
- **TTPs:** Proprietary toolset migrated from C++ to Rust; exploits vulnerable internet-facing services (Exchange, ESXi); PsExec and RDP lateral movement [OpenAI]
- **Notable Campaigns:** 70-86 victims by Q3 2025; over 60% of victims in Asia and Africa (Taiwan, Thailand, China, Japan, Singapore) — unusual regional focus [OpenAI]
- **Status:** Active. Represents ransomware's globalization beyond traditional Eastern European base [OpenAI only]

#### DireWolf
- **Origin:** May 2025; no known ties to existing groups — entirely independent with bespoke malware ([halcyon.ai](https://www.halcyon.ai/threat-group/dire-wolf)) [OpenAI only]
- **Model:** Closed group, no affiliate program [OpenAI]
- **TTPs:** Custom Golang-based ransomware with Curve25519 + ChaCha20 encryption; highly tailored intrusions rather than mass attacks [OpenAI]
- **Notable Campaigns:** ~49 victims by mid-2025 spanning regulatory, logistics, and industrial sectors [OpenAI]
- **Status:** Active. Demonstrates new entrants can rapidly achieve enterprise-grade ransomware operations without inheriting code [OpenAI only]

#### Nova (aka RALord)
- **Origin:** Late March 2025 as "RALord," rebranded to Nova by April 2025 ([redpiranha.net](https://redpiranha.net/news/threat-intelligence-report-january-20-january-26-2026)) [OpenAI only]
- **Model:** Classic RaaS affiliate model [OpenAI]
- **TTPs:** Double extortion; flexible initial access vectors; continually updated malware [OpenAI]
- **Notable Campaigns:** 86+ victims across five continents by early 2026 ([threatlabsnews.xcitium.com](https://threatlabsnews.xcitium.com/blog/from-ralord-to-nova-how-this-raas-gang-is-wreaking-havoc-worldwide/)); targets included a French food production firm, a Dubai government entity, and media conglomerates [OpenAI]
- **Status:** Very active as of Q1 2026 [OpenAI only]

#### NightSpire
- **Origin:** Early 2025 (leak site live by March 12, 2025) [OpenAI only]
- **Model:** Evolved from data-extortion-only to full double-extortion mid-stream — a notable tactical pivot ([cyble.com](https://cyble.com/knowledge-hub/10-new-ransomware-groups-of-2025-threat-trend-2026/)) [OpenAI]
- **TTPs:** Initially pure data theft and leak threats; later added encryption. Uses ProtonMail, OnionMail, and Telegram for negotiations [OpenAI]
- **Notable Campaigns:** 90+ victims by late 2025 across healthcare, education, manufacturing, government, retail, and logistics; early victim included Nippon Ceramic (Japan, April 2025) [OpenAI]
- **Status:** Active. Exemplifies how data-only extortion groups often end up adding encryption for higher conversion rates [OpenAI only]

#### Warlock
- **Origin:** Mid-2025; uniquely tied to Chinese APT groups (Linen Typhoon, Violet Typhoon) — Microsoft tracks as Storm-2603 ([bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/microsoft-sharepoint-servers-also-targeted-in-ransomware-attacks/)) [OpenAI, Claude]
- **Model:** State-linked hybrid financial/espionage tool [OpenAI]
- **TTPs:** Exploited SharePoint zero-days (CVE-2025-49704/49706); web shells, Impacket, PsExec for lateral movement; GPO-based ransomware deployment [OpenAI]
- **Notable Campaigns:** Multiple government and enterprise networks globally from July 2025 onward [OpenAI, Claude]
- **Status:** Ongoing. Highlights the blurring of state-sponsored and criminal ransomware operations [OpenAI, Claude]

#### Interlock
- **Origin:** September 2024; gained significant traction in late 2025 [Gemini only]
- **Model:** Closed group / Opportunistic [Gemini]
- **TTPs:** Distinctive "ClickFix" social engineering — tricking users into running malicious PowerShell disguised as browser updates; cross-platform payloads including FreeBSD and Linux [Gemini]
- **Notable Campaigns:** City of St. Paul, MN (July/August 2025) — disrupted municipal services, required National Guard assistance; DaVita kidney dialysis breach (April 2025) impacting 200,000+ patients [Gemini]
- **Status:** Active [Gemini only]

#### TridentLocker
- **Origin:** Late November 2025 [Gemini only]
- **Model:** RaaS / Data Broker [Gemini]
- **TTPs:** Extensive anti-analysis (virtualization detection, timestomping); targets government contractors [Gemini]
- **Notable Campaigns:** Sedgwick Government Solutions (Dec 2025/Jan 2026) — compromised a federal contractor serving DHS and CISA, exfiltrated 3.4 GB [Gemini]
- **Status:** Active. High risk tolerance given willingness to target federal contractors [Gemini only]

#### Kazu
- **Origin:** Mid-2025 [Gemini only]
- **Model:** Double extortion using LockBit 5.0 variant [Gemini]
- **TTPs:** SmokeLoader for initial access; locale-checks to avoid CIS nations; focus on "Global South" (Latin America, SE Asia) [Gemini]
- **Notable Campaigns:** Manage My Health breach (Dec 2025) — New Zealand's largest patient portal, ~120,000 users impacted [Gemini]
- **Status:** Active. Represents sophisticated affiliate leveraging leaked LockBit builders [Gemini only]

### 3. Evolution of Established Actors

#### Qilin (Agenda) — The Dominant Force
**All three providers identify Qilin as the most prolific ransomware operation in 2025.** [All providers]

- **Rise:** Formerly "Agenda" (2022), Qilin claimed the top spot in April 2025 following RansomHub's collapse. Victim count grew from 45 (2023) to 179 (2024) to 1,138 (2025), including 190 victims in December and 115 in January 2026 [Claude]
- **Affiliate absorption:** Aggressively recruited displaced affiliates from LockBit, ALPHV/BlackCat, and RansomHub. Monthly victim average jumped from 36 (Q1) to 75 (Q3) — directly correlated with RansomHub's April closure [All providers]
- **Diverse affiliates:** Range from North Korean state actors (Moonstone Sleet) to Scattered Spider members, Devman, and Arkana [Claude]
- **Healthcare targeting:** 17 healthcare attacks in the first week of January 2026; Synnovis breach (2024) forced thousands of NHS cancellations; Covenant Health breach (May 2025) exposed 478,000 patient records [Claude, Gemini]
- **Technical:** Rust and C payloads with Safe Mode execution, automated negotiation tools, network propagation, and a "call lawyer" legal intimidation feature [Claude]
- **Status:** Active and dominant. Expect continued primacy into 2026, though scale increases law enforcement targeting risk [All providers]

#### DragonForce — The Ransomware Cartel
**All providers highlight DragonForce's innovative cartel model as a defining development of 2025.** [All providers]

- **Cartel pivot (March 2025):** Shifted from standard RaaS to white-label infrastructure provider. Affiliates operate under their own custom names (e.g., Devman, Mamona) while using DragonForce backend [All providers]
- **RansomHub absorption:** Following RansomHub's downtime, DragonForce claimed on RAMP forum that RansomHub "decided to move to our infrastructure." BlackLock also began collaborating after DragonForce defaced its leak site [Claude, OpenAI]
- **Scattered Spider connection:** Scattered Spider affiliates deploying DragonForce ransomware, including attacks on UK retailers (M&S, Co-op, Harrods) in April 2025 [All providers]
- **Data analysis service (August 2025):** Introduced risk audits generating extortion call scripts, letters to management, and pseudo-legal analysis reports [Claude]
- **BYOVD techniques:** Uses Bring Your Own Vulnerable Driver to disable EDR [Gemini]
- **Status:** Active and growing. White-label model complicates attribution and dilutes law enforcement targeting effectiveness [All providers]

#### LockBit — Diminished but Persistent
- **Operation Cronos (February 2024):** UK NCA took control of LockBit's site, compromised entire backend infrastructure, unmasked leadership, seized cryptocurrency and decryption keys [All providers]
- **Resurgence:** Resurfaced in September 2025 as LockBit 5.0 (also called "ChuongDong"), but with diminished impact — only 106 victims listed in December 2025 [Claude, OpenAI]
- **Rule changes:** LockBit 5.0 explicitly permitted affiliates to attack sectors previously off-limits (healthcare, critical infrastructure), interpreted as retaliation for law enforcement pressure ([reliaquest.com](https://reliaquest.com/blog/threat-spotlight-ransomware-and-cyber-extortion-in-q3-2025/)) [OpenAI]
- **Status:** Active but diminished. Remains to be seen whether it can regain market position [Claude, OpenAI]

#### INC Ransom — Healthcare Scourge
- **Scale:** 162 victims in 2024; over 300 in 2025; most deployed ransomware by victim count in July 2025 [Claude]
- **Healthcare focus:** 29% of attacks targeted healthcare in H1 2025 [Claude]
- **Code proliferation:** 48% function match with Lynx ransomware (rising to 70.8% for common functions), demonstrating how one group's tooling seeds successors (Lynx, Sinobi lineage) [Claude]
- **Affiliates:** GOLD IONIC (MITRE tracking); Storm-0494 for GootLoader initial access; Vanilla Tempest adopted INC as primary payload (August 2024) [Claude]
- **Status:** Active [Claude, Gemini]

#### RansomHub — Rise and Fall Case Study
- **Rise (Feb 2024-March 2025):** Replaced LockBit and BlackCat as frontrunner, courting displaced affiliates with lucrative payment splits; 230+ victims; estimated data stolen from 200+ organizations [All providers]
- **Collapse (April 1, 2025):** Operations abruptly halted. Client communication portal went offline. PRODAFT reported "many members leaving." Cause remains unclear — internal dispute, law enforcement, or exit scam [All providers]
- **Redistribution:** VanHelsing created by former affiliates; RansomBay moved to DragonForce systems; many affiliates migrated to Qilin (which nearly doubled activity in Q2 2025) [Claude, OpenAI]
- **Status:** Defunct. Epitomizes ecosystem volatility and transactional nature of affiliate loyalty [All providers]

### 4. RaaS Ecosystem Evolution

**The RaaS model fragmented but did not die — it adapted.** [All providers]

**Affiliate migration dynamics** [All providers]:
- Takedowns primarily target RaaS infrastructure and administrators, not affiliates who conduct intrusions
- When platforms are disrupted, affiliates migrate to alternatives or establish their own leak sites within days
- Multi-affiliate operators now work across RaaS platforms concurrently (e.g., DevMan participating in Qilin, DragonForce, Apos simultaneously) ([halcyon.ai](https://www.halcyon.ai/threat-group/devman)) [OpenAI]

**Business model innovations** [All providers]:
- **Competitive affiliate recruitment:** With fewer ransom payments to share, RaaS operators reintroduce premium services (data analysis, negotiation support, legal intimidation tools) to retain affiliates [Claude]
- **English-speaking RaaS:** Scattered Spider announced plans for "ShinySp1d3r RaaS" in Q3 2025 — the first English-speaking actor-led ransomware service ([reliaquest.com](https://reliaquest.com/blog/threat-spotlight-ransomware-and-cyber-extortion-in-q3-2025/)) [OpenAI]
- **Code leaks fueling proliferation:** VanHelsing RaaS source code leaked and sold in May 2025 ([cyble.com](https://cyble.com/blog/top-ransomware-groups-may-2025-safepay-devman-rise/)); INC Ransom source code sold for $300,000; LockBit builder widely available since 2022 [OpenAI, Claude]
- **Insider participation:** Two U.S. cybersecurity consultants pled guilty to running BlackCat affiliate operations, facing 20-year sentences ([itpro.com](https://www.itpro.com/security/cyber-crime/cybersecurity-experts-face-20-years-in-prison-following-ransomware-campaign)) [OpenAI]

**Payment ecosystem pressure** [Claude, OpenAI]:
- Ransom payment rates plummeted to 23-25% [Claude]
- Median payments dropped to ~$115k-$267k range [Gemini]
- Despite rising volumes, groups made less money in 2025 than 2024 in both total and average payments [Claude]
- Sanctions on mixers (Tornado Cash, ChipMixer) increased cost and risk of laundering proceeds [OpenAI]

### 5. Law Enforcement Operations and Impact

#### Major Operations

**Operation Cronos — LockBit (February 2024)** [All providers]
- UK NCA-led operation seized LockBit infrastructure, unmasked leadership, obtained decryption keys
- October 2024 follow-up: four arrests including a developer and bulletproof hosting administrator
- U.S. Treasury imposed sanctions on LockBit members
- Impact: LockBit eventually resurfaced as 5.0 in September 2025, but at significantly reduced capacity

**Operation Checkmate — BlackSuit/Royal (July 2025)** [All providers]
- Europol/FBI-led takedown seized four servers, nine domains, and ~$1,091,453 in cryptocurrency
- BlackSuit revealed as Conti > Quantum > Royal successor; responsible for 184+ victims and $500M+ in ransom demands ([cybernewscentre.com](https://www.cybernewscentre.com/5th-august-2025-cyber-update-global-blacksuit-ransomware-takedown/)) [OpenAI]
- Impact: Operators dispersed to INC ransomware and emerging "Chaos" group within weeks [Gemini, OpenAI]

**Operation Phobos Aetor — 8Base (February 2025)** [Gemini, OpenAI]
- Coordinated arrests of four Russian nationals in Thailand; seizure of dark web leak sites
- 8Base had attacked 1,000+ mostly SMBs using Phobos ransomware, stealing ~$16 million ([helpnetsecurity.com](https://www.helpnetsecurity.com/2025/02/11/8base-ransomware-group-leaders-arrested-leak-site-seized-phobos/)) [OpenAI]
- Impact: Operations ceased, but Phobos toolkit remained available to other affiliates [Gemini, OpenAI]

**Operation Endgame — Malware Droppers (May 2024)** [Claude]
- Europol-led multiagency effort: 100 servers and 2,000+ domains seized; four individuals arrested
- One individual earned at least $70M renting infrastructure for ransomware attacks [Claude]

**Interpol Global Sweeps (2025)** [OpenAI only]
- Operation Serengeti 2.0 (June-August 2025) and Operation Sentinel (October-November 2025)
- Sentinel: 574 arrests across 19 African nations, six ransomware variants decrypted, $3M recovered ([tomshardware.com](https://www.tomshardware.com/tech-industry/cyber-security/interpol-led-cybercrime-crackdown-results-in-574-arrests-in-19-african-nations-decrypts-six-ransomware-variants)) [OpenAI]

**Scattered Spider Arrests** [Claude, OpenAI]
- December 5, 2025: Remington Goy Ogletree (19, Texas) arrested — the seventh Scattered Spider member arrested [Claude]
- Despite arrests, operational tempo remains high [All providers]

**Bounties and Indictments** [OpenAI only]
- September 2025: $11 million reward for Ukrainian national Volodymyr Tymoshchuk ("deadface"/"farnetwork"), linked to LockerGoga ransomware ([pcgamer.com](https://www.pcgamer.com/gaming-industry/us-doj-puts-usd11-million-bounty-on-ransomware-king-allegedly-responsible-for-stealing-usd18-billion/)) [OpenAI]

#### Observable Behavioral Impact

**All providers agree: law enforcement achieved tactical successes but strategic impact remained limited.** [All providers]

Observable behavioral changes:
1. **Faster rebranding cycles:** Groups now preemptively rebrand to evade attribution. Brand "lifecycles" shortened significantly [All providers]
2. **Shift to decentralized models:** High-profile takedowns drove affiliates toward closed groups (SafePay) or decentralized cartels (DragonForce) to avoid single points of failure [Gemini, Claude]
3. **Trust erosion:** Compromising backend infrastructure sowed distrust between RaaS groups and affiliates, increasing friction in criminal communities [Claude]
4. **Retaliatory escalation:** LockBit 5.0 explicitly permitted critical infrastructure targeting, interpreted as retaliation for law enforcement pressure [OpenAI]
5. **Geographic caution:** Top actors doubled down on staying within friendly borders (primarily Russia) or using deep anonymity [OpenAI]
6. **Overall volume still rose:** Leak-site victims rose from ~5,400 (2024) to ~7,600 (2025) despite all enforcement actions ([techradar.com](https://www.techradar.com/pro/security/takedowns-and-arrests-didnt-slow-down-ransomware-in-2025)) [OpenAI]

### 6. Sector and Geographic Targeting

#### Sector Targeting [All providers]

| Sector | Share of Attacks | Key Details |
|--------|-----------------|-------------|
| Manufacturing | 14-22% | Most targeted sector across all reporting. Low downtime tolerance, legacy OT environments [All providers] |
| Technology/Professional Services | ~9-10% | Second tier; includes IT & ITES, BPO firms [Claude, OpenAI] |
| Construction | ~7% (rising) | Climbed to top three by Q2 2025 [OpenAI, Claude] |
| Healthcare | ~500+ victims in 2025 | Steady targeting despite some groups' nominal prohibitions. Qilin, INC Ransom disproportionately active here [All providers] |
| Retail/Wholesale | ~7% | Spiked in Q1 2025 due to Clop's file-transfer exploits [OpenAI, Claude] |
| Education | ~9% of INC attacks | Distributed campus networks with limited IT staffing [Claude, Gemini] |
| Government/Critical Infrastructure | Rising | 34% increase in critical infrastructure attacks year-over-year; new groups (Devman, Sinobi, Warlock, Gunra) actively targeting government and energy sectors [Claude, OpenAI] |

**Notable incidents:**
- Synnovis (UK pathology firm) — forced thousands of NHS appointment cancellations, blood supply shortages [Claude, Gemini]
- Ingram Micro (global IT distributor, July 2025) — SafePay threatened to leak 3.5 TB of data [Gemini]
- City of St. Paul, MN — required National Guard assistance for recovery [Gemini]
- DaVita kidney dialysis — 200,000+ patients impacted [Gemini]
- Manage My Health (New Zealand) — ~120,000 users [Gemini]
- Sedgwick Government Solutions — federal contractor serving DHS/CISA [Gemini]
- UK retailers (M&S, Co-op, Harrods) — Scattered Spider + DragonForce [Claude]

#### Geographic Distribution [All providers]

- **United States:** 47-67% of all attacks depending on reporting period. Remains primary target by overwhelming margin [All providers]
- **Germany:** Rose to #2 spot in 2025, partly attributed to SafePay focus on German organizations ([reliaquest.com](https://reliaquest.com/blog/ransomware-cyber-extortion-threat-intel-q2-2025/)) [OpenAI]
- **Canada:** ~4.5% of attacks [Claude]
- **United Kingdom, France, Italy, Australia:** Consistently in top targets [Claude, OpenAI]
- **APAC expansion:** DevMan concentrated 60%+ of victims in East/SE Asia; Kazu targeted New Zealand and SE Asia; The Gentlemen heavily targeted Brazil and Thailand [Gemini, OpenAI]
- **Global South emergence:** Latin America and Africa seeing increased activity from groups like Beast, Nova, and Kazu [Gemini, OpenAI]
- **Middle East:** Increasing targets (UAE, Saudi Arabia) due to growing wealth and digitization [OpenAI]
- **Geographic diversification forecast:** Recorded Future predicts 2026 will be the first year that new ransomware actors outside Russia outnumber those within it [Claude]

### 7. Tactical Adaptations

#### EDR Evasion [All providers]
- **BYOVD (Bring Your Own Vulnerable Driver):** Widespread adoption — dropping older signed drivers to disable endpoint security. The Gentlemen exploit ThrottleStop.sys; others use RTCore64 [All providers]
- **Living-off-the-land (LotL):** Extensive use of legitimate admin binaries (wmic, netsh, PowerShell, PsExec) to blend into normal operations [All providers]
- **Language diversification:** Golang (DireWolf), Rust (Qilin, DevMan), and Nim used to evade signature-based detection [OpenAI, Claude]
- **Shorter dwell times:** Some groups strike within hours of initial breach, overwhelming detection/quarantine capabilities [OpenAI]

#### Extortion Escalation [All providers]
- **Data-only extortion:** Growing use — skip encryption, focus on data theft for legal/compliance/reputational pressure. However, NightSpire's experience suggests groups often eventually add encryption for higher conversion [Claude, OpenAI]
- **Triple extortion:** Encryption + data leak + DDoS attacks on victim public infrastructure during negotiations ([techradar.com](https://www.techradar.com/pro/security/ransomware-gangs-are-now-expanding-to-physical-threats-in-the-real-world)) [OpenAI, Gemini]
- **Direct contact harassment:** Phone calls and emails to employees, executives, and even clients/partners to force negotiations [Gemini, OpenAI]
- **Physical threats:** ~46% of U.S. companies experiencing ransomware reported attackers threatened physical violence against executives ([ridgemarkinsurance.com](https://ridgemarkinsurance.com/ransomware-escalates-physical-threats-against-company-leaders/)) [OpenAI]
- **Legal intimidation:** Qilin introduced a "call lawyer" feature to pressure victims [Claude]
- **Data analysis service:** DragonForce's August 2025 service generates extortion call scripts and pseudo-legal analysis for affiliates [Claude]

#### Initial Access Evolution [All providers]
- **Credential-based intrusions:** Accounted for nearly half of initial access methods in 2025; identity compromise outpacing vulnerability exploitation as dominant vector [Claude, OpenAI]
- **Vulnerability exploitation:** Mass exploitation of file-transfer software (MOVEit, GoAnywhere, Cleo) by Clop; SharePoint zero-days (Warlock); SonicWall SSL VPN (Sinobi, CVE-2024-53704); SimpleHelp RMM (INC, CVE-2024-57726/57727/57728) [All providers]
- **Social engineering advancement:** ClickFix technique (fake browser updates prompting PowerShell execution) by Interlock [Gemini]; Scattered Spider's help desk impersonation and MFA fatigue attacks [All providers]
- **Insider recruitment:** Ransomware operators increasingly recruiting corporate insiders, including via gig work platforms. FBI advisory documented social engineering help desk scam via gig workers [Claude]
- **Supply chain attacks:** Nearly doubled in 2025 — 297 attacks claimed vs. 154 in 2024 (93% increase). Groups including RALord/Nova, Warlock, Sinobi, The Gentlemen, and BlackNevas targeting software supply chains [Claude]

#### Cross-Platform Targeting [All providers]
- Cross-platform ransomware (Windows + Linux + ESXi) has become the default rather than the exception
- Virtually every major group profiled supports ESXi targeting — encrypting hypervisors locks all virtual machines simultaneously
- Linux environments often lack robust EDR coverage found on Windows endpoints [Gemini, OpenAI]

#### AI Integration [Claude]
- Growing evidence of AI use for social engineering — overcoming language barriers, personalizing lures, crafting contextually appropriate phishing
- In controlled testing, AI-driven ransomware achieved full data exfiltration 100 times faster than human attackers [Claude only — single source, treat with caution]

---

## Areas of Disagreement

1. **Attack volume statistics:** Claude reports 7,200-7,515 victims in 2025; OpenAI cites 7,679 double-extortion incidents (citing neteye-blog.com); Gemini references Q4 2025 as 2,287 victims for that quarter alone. The discrepancies likely reflect different counting methodologies (leak site claims vs. confirmed incidents vs. double-extortion only). All agree on the directional trend of significant increase.

2. **US targeting share:** Claude states 55% of attacks targeted the US; OpenAI cites 67% for Q2 2025 (ReliaQuest data); Gemini places it at 47-52%. Differences likely reflect different time windows and data sources.

3. **Manufacturing targeting share:** Claude cites 14%; Gemini cites 20-22%; OpenAI confirms manufacturing as #1 but is less specific on percentage. All agree manufacturing is the most targeted sector.

4. **Group coverage divergence:** Each provider profiled substantially different emerging groups. OpenAI uniquely covered DevMan, DireWolf, Nova/RALord, NightSpire, Beast, and Warlock in depth. Gemini uniquely covered Interlock, TridentLocker, and Kazu. Claude provided the deepest coverage of INC Ransom and SafePay. All three covered Sinobi, The Gentlemen, DragonForce, and Qilin, allowing cross-validation on those actors.

5. **SafePay model characterization:** Gemini describes SafePay as explicitly non-RaaS with no affiliate recruitment. Claude agrees on its volume-focused, core-team-operated model. OpenAI describes it as an independent closed group. All agree it is non-traditional in structure, though they emphasize different aspects.

6. **DragonForce sub-brands:** Gemini specifically names Devman and Mamona as DragonForce white-label operations. OpenAI corroborates this. Claude mentions Devman as a Qilin affiliate, creating some ambiguity about whether DevMan's primary affiliation is with DragonForce or Qilin (likely both, given multi-platform participation).

7. **Germany as #2 target:** Only OpenAI (citing ReliaQuest) identifies Germany as the second-most targeted country. Claude lists Canada as #2 at 4.5%. This may reflect different time windows (Q2 2025 specifically vs. full-year).

---

## Gaps & Limitations

1. **Financial data is opaque:** None of the sources provide reliable data on actual ransom payments collected. The 23-25% payment rate and declining payment sizes are cited but precise dollar figures for 2025 total ransomware revenue are absent. Chainalysis data, typically the gold standard, was not directly cited by any provider.

2. **Attribution confidence is low:** Many "new" groups are assessed as rebrands or reconstitutions of older operations, but the exact lineage is often speculative. The Sinobi-Lynx-INC code relationship, The Gentlemen's predecessor identity, and DireWolf's claimed independence all lack definitive confirmation.

3. **State-actor nexus under-explored:** The Warlock/Storm-2603 case (Chinese APT deploying ransomware) and North Korean actors (Moonstone Sleet) operating as Qilin affiliates are mentioned but not deeply analyzed. The full extent of nation-state use of criminal ransomware infrastructure remains a major intelligence gap.

4. **Victim underreporting:** All statistics are based on leak-site claims and disclosed incidents. Actual attack volumes are certainly higher, as many victims pay and never appear on leak sites. The true scale of the problem is unknown.

5. **Defensive effectiveness data is absent:** No provider systematically analyzed which defensive measures were most effective against specific groups. Sector-specific resilience data is not covered.

6. **Cryptocurrency and payment infrastructure:** The mechanics of how groups are laundering proceeds post-Tornado Cash sanctions is not addressed in depth by any provider.

7. **Insurance industry impact:** The role of cyber insurance in enabling or constraining ransom payments — a significant factor in the ecosystem's economics — receives no meaningful coverage.

8. **Regulatory developments:** Proposed UK public sector ransom payment bans and similar policy initiatives in other jurisdictions are mentioned in passing (Claude) but not analyzed for likely impact.

9. **Non-English source intelligence:** All three providers appear to rely primarily on English-language sources. Intelligence from Russian-language forums, Chinese security research, and other non-English sources may contain significant additional detail on actor profiles and TTPs.

---

## References

Deduplicated citation list from all three reports, organized by source. URLs are provided where available (from OpenAI and Gemini reports). Claude's report cited sources generically without URLs.

### Threat Intelligence Vendors
- Cyble — "10 New Ransomware Groups of 2025" and related analyses: [cyble.com](https://cyble.com/knowledge-hub/10-new-ransomware-groups-of-2025-threat-trend-2026/)
- Cyble — "Top Ransomware Groups of May 2025": [cyble.com](https://cyble.com/blog/top-ransomware-groups-may-2025-safepay-devman-rise/)
- ReliaQuest — Q2 2025 Ransomware Threat Intel: [reliaquest.com](https://reliaquest.com/blog/ransomware-cyber-extortion-threat-intel-q2-2025/)
- ReliaQuest — Q3 2025 Ransomware and Cyber Extortion: [reliaquest.com](https://reliaquest.com/blog/threat-spotlight-ransomware-and-cyber-extortion-in-q3-2025/)
- Flashpoint — "New RaaS Groups to Watch in 2025": [flashpoint.io](https://flashpoint.io/blog/new-ransomware-as-a-service-raas-groups-to-watch-in-2025/)
- Halcyon — DevMan Threat Group: [halcyon.ai](https://www.halcyon.ai/threat-group/devman)
- Halcyon — DireWolf Threat Group: [halcyon.ai](https://www.halcyon.ai/threat-group/dire-wolf)
- Recorded Future (cited by Claude, no direct URL)
- Check Point Research (cited by Claude, no direct URL)
- GuidePoint Security: [guidepointsecurity.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGgpEyON4ySTCDyd2fu1wJrJSgFVkQA2LnDM7R4KZPXGI78Mgfq_NlHr5vhkGQOE9nubcJ0FjSzc0fYkFd4cM1lK1e5cCh39VCaCK5GxCGPJaiziKmXYmsiLtuWG-Cx03cYoRqwaQVh_j-WdXCKlLyKPizQE8xZrKg5Lr1xcl8KDx6GnA0Nvk1zGHeElRR6uVbFWN01RatxOWal5aBtnfYPyjBcMg==)
- Intel 471 (cited by Claude, no direct URL)
- Sophos (cited by Claude, no direct URL)
- PRODAFT (cited by Claude, no direct URL)
- NordStellar: [nordstellar.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFu1JjUupgYTvgbxUH_61zjk4gpZ3Zawsyt-q_qZZ7gza7iibpMHgtbneIuAy5Y-x-KLwfE8QX4bgNmXZLg9fiHuhCgTtofSh1tHIDLd_XugeAYlp6yPdEvSx0N64BuIGgtKDmSOQ==)

### Security News & Analysis
- BleepingComputer — SharePoint/Warlock attacks: [bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/microsoft-sharepoint-servers-also-targeted-in-ransomware-attacks/)
- TechRadar — "Takedowns and arrests didn't slow down ransomware in 2025": [techradar.com](https://www.techradar.com/pro/security/takedowns-and-arrests-didnt-slow-down-ransomware-in-2025)
- TechRadar — Physical threats in ransomware: [techradar.com](https://www.techradar.com/pro/security/ransomware-gangs-are-now-expanding-to-physical-threats-in-the-real-world)
- Neteye Blog — 2025 Ransomware Overview: [neteye-blog.com](https://www.neteye-blog.com/2026/01/ransomware-double-extortion-attack-2025-overview/)
- eSecurity Planet — The Gentlemen analysis: [esecurityplanet.com](https://www.esecurityplanet.com/threats/these-gentlemen-arent-gentle-rapidly-evolving-ransomware-threat/)
- CyberNewscentre — BlackSuit takedown: [cybernewscentre.com](https://www.cybernewscentre.com/5th-august-2025-cyber-update-global-blacksuit-ransomware-takedown/)
- Help Net Security — 8Base arrests: [helpnetsecurity.com](https://www.helpnetsecurity.com/2025/02/11/8base-ransomware-group-leaders-arrested-leak-site-seized-phobos/)
- Foresiet — New ransomware groups May 2025: [foresiet.com](https://foresiet.com/blog/new-ransomware-groups-emerge-in-may-2025/)
- RansomNews — The Gentlemen TTPs: [ransomnews.online](https://ransomnews.online/hub/ransomnews-thegentlemen.html)
- Xcitium ThreatLabs — Nova/RALord: [threatlabsnews.xcitium.com](https://threatlabsnews.xcitium.com/blog/from-ralord-to-nova-how-this-raas-gang-is-wreaking-havoc-worldwide/)
- Red Piranha — Nova threat intelligence: [redpiranha.net](https://redpiranha.net/news/threat-intelligence-report-january-20-january-26-2026)
- Ridgemark Insurance — Physical threats survey: [ridgemarkinsurance.com](https://ridgemarkinsurance.com/ransomware-escalates-physical-threats-against-company-leaders/)
- AlphaHunt Blog — Storm-2603/Warlock: [blog.alphahunt.io](https://blog.alphahunt.io/storm-2603-sharepoint-zero-day-exploitation-and-warlock-ransomware-a-hybrid-financial-and-espionage-threat/)
- Hackread — LockerGoga/EU Most Wanted: [hackread.com](https://hackread.com/lockergoga-ransomware-eu-most-wanted-list-doj-reward/)

### Government & Law Enforcement
- CISA (cited by Claude, no direct URL)
- FBI (cited by Claude, no direct URL)
- Axios — BlackSuit DOJ seizure: [axios.com](https://www.axios.com/2025/08/12/doj-blacksuit-ransomware-cryptocurrency-seizure)
- PCGamer — $11M ransomware bounty: [pcgamer.com](https://www.pcgamer.com/gaming-industry/us-doj-puts-usd11-million-bounty-on-ransomware-king-allegedly-responsible-for-stealing-usd18-billion/)
- AP News — Interpol Serengeti 2.0: [apnews.com](https://apnews.com/article/057fee9214a008eb2829a672b10e69b0)

### Vendor-Specific Research
- Arctic Wolf — Interlock analysis: [arcticwolf.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGKuVn7yd7r8xZ07eQTlBzrqVEZv1ggParfYnhMljpieFS7MPw219bbF5sKN5dAryc8iim8sQxzriJ4R95Dh8RJXOzG7QYbfjrYQz6d31EnH4HBkORMCyTSRoMyPN3Y7BVxxnIsGRIGizNkC6UEWH5drzodW2qA26IsMaHOJFbFi26He2lBkg==)
- Check Point: [checkpoint.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEoFkGZoKp8iUbfaIMY2O4hmY3mQbjAtQVQO1hujjNaI6dZCm644k3rZdk_G_9sb1ejqDdNfATTZNM757zRRg7nMOgK4RklvHwWm27bI0bp6Jig72Y39SKCMA9pPIWQHJiluWsYrG4M38s_42y12Wbu9cHRmX3maAGMX8SEsclQDJbVAsMHMLkRvA==)
- Trend Micro — The Gentlemen: [trendmicro.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGCFXhR-Tjmm9yrheLZXcx3bOQpNhMVuVo-s9-cGcx3G3TRBG-7kUgVlYn8Tw1LT8T6BHrg_I8fTU_JJJ7AgNzQaxxNaxIkzC0nebIAhozBZFf8G5ZSfNjsLnBSaQRqGb52sSlRTFG9Nw_GmNCrQ6_XoZYcPSWrPIUSKvSy3Cv1ia10Nlpd4Uce2UbgEA==)
- Cybereason — The Gentlemen: [cybereason.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG_4XE1ij2YeJD_M2ch8W4oQ7-DNho0FCtu_BabTP3moH2oeClGn4oZyrs1EdnEq8-KEtLEkUbs4aRIaFBRyBCG77RvMwhQz5lmcvUwGR3wLNd6HK00S15ahOZiaJGolNUI4p1E7si_VwyFYRf5RA==)
- ITPro — Cybersecurity experts ransomware guilty plea: [itpro.com](https://www.itpro.com/security/cyber-crime/cybersecurity-experts-face-20-years-in-prison-following-ransomware-campaign)
- Tom's Hardware — Interpol Operation Sentinel: [tomshardware.com](https://www.tomshardware.com/tech-industry/cyber-security/interpol-led-cybercrime-crackdown-results-in-574-arrests-in-19-african-nations-decrypts-six-ransomware-variants)
- SOCRadar: [socradar.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF1asvIZsKlvoMWwTnhp42pZRzAkwD43qizOfewY7o9KLlum8ObjsRqIfomYfu5ipXM_JArYX88zfFreklJIUMlTYJmHPTQf-Pzt0633qVSATSWfb0sbdb_cZCWp-eEcXrIZdtAqE0bytAFNh5rm2t9Q-3FcvmBlu5RkyPLx4fzFaQ=)
- Security and Technology Institute: [securityandtechnology.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFRtiNVBh-uKiL11TeTPyYAPMXK-kN45ZnMV2OLiCRhewePaKuSgc7q_KoAC_zrj-Ji2gl3ST2OEfG7glj9AJh16eXU1Bxz45-yxXhSsn5EwP1aIeQH2DTUFdareuqgMQGe6MVh8lvKp8UE6ZATTXc0XZZAAKuWdhjIUsQW5AgC)
- HIPAA Journal: [hipaajournal.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGsabZfkKA6-P-_jmmlTh1RnRubLjnyrabr6vwayTA-hezgXublIuJrNVgzAudBdnwYwVAMKV8YCGBDIoSNfUYIVsHcVgfFocZvpAlyyX6Gq4qG50jzM6njMCFXtEZEMtp2gUSgtU66ta_0ygETRUJNlHsq4U85b3h_mUr7p41z6w==)
- Acronis: [acronis.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEIvDn_wZGBQsSsURbC4ENJQ4qxb3mh4B0_5Zevwbri_cZdIQqXueF_oyHFrP5-edD_9pIfs1tBlwFoHG1fefO3DcHTKrD8iE_LjxGrZ5XYTS0NgwCdMwmLJUV_p_KxS-miNIc18ZgIci7T15qcbxdVVa3O7l4gxwd_jCSjhuxWmKDxESYntO7Df6qgvovGoXVGvZiP)

---

*Report synthesized: February 14, 2026*
*Sources: Claude (Anthropic), OpenAI Deep Research, Gemini Deep Research*
*Citation validation: None performed — all claims reported as-stated by source providers*
