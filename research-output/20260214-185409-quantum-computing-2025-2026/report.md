# Current State of Quantum Computing (2025--2026) -- Research Report

## Executive Summary

The quantum computing industry reached a decisive inflection point during 2025 and early 2026, marking the transition from "Noisy Intermediate-Scale Quantum" (NISQ) devices to "Early Fault-Tolerant" architectures. Three developments define this era: the first credible demonstrations of below-threshold quantum error correction on real hardware, the emergence of practical quantum advantage on scientifically meaningful problems, and an unprecedented surge of capital -- nearly $3.77 billion in private equity funding in the first nine months of 2025 alone, nearly triple the $1.3 billion raised in all of 2024. Government commitments reached $10 billion globally by April 2025, driven by landmark national programs from Japan, the United States, and the European Union.

Hardware progress was substantial across multiple modalities. Google's 105-qubit Willow processor demonstrated exponential error suppression and a verified 13,000x speedup over classical supercomputers on a practical NMR simulation. IBM unveiled its Nighthawk processor emphasizing quality over quantity, while Quantinuum's Helios trapped-ion system achieved "better than break-even" error correction with a remarkable 2:1 physical-to-logical qubit ratio. IonQ crossed the "four nines" fidelity threshold (99.99% two-qubit gate fidelity), and neutral-atom platforms from QuEra and Microsoft/Atom Computing demonstrated operational logical qubits at scale.

Despite these achievements, fully fault-tolerant quantum computers capable of running million-operation algorithms remain years away -- most credible roadmaps target 2029--2030 for systems with hundreds of logical qubits. Near-term value is being delivered through hybrid quantum-classical approaches in drug discovery, financial modeling, optimization, and quantum sensing. The industry consensus, led by IBM's public prediction, is that verified quantum advantage on practical problems will be confirmed by the broader community before the end of 2026.

## Methodology

This report synthesizes research conducted independently via three AI research providers: **Claude** (Anthropic), **OpenAI**, and **Gemini** (Google). Each provider conducted web-based research on the same topic and questions, producing separate reports with inline citations. The synthesis process involved:

1. **Independent research**: Each provider queried current sources and produced a standalone report.
2. **Citation validation**: URL liveness checks were performed on all cited sources. Result: 126 alive, 22 dead (85% liveness rate). Citation validation depth: 1 (URL liveness check only; content accuracy not independently verified).
3. **Cross-referencing**: Claims were categorized by provider agreement level (Consensus, Majority, Unique).
4. **Confidence annotations**: Claims are tagged based on the number of independent providers corroborating them.

---

## Findings

### 1. Major Hardware Milestones

#### 1.1 Google Willow Processor

- **Consensus** [Claude, OpenAI, Gemini]: Google's Willow chip, a 105-qubit superconducting processor, achieved the first credible demonstration of below-threshold quantum error correction. As qubit arrays scaled from 3x3 to 5x5 to 7x7, the logical error rate decreased exponentially -- halving with each increase in code distance. This resolved a 30-year-old theoretical question about whether QEC could work in practice.

- **Majority** [OpenAI, Gemini]: Willow executed the "Quantum Echoes" algorithm (simulating out-of-time-order correlators relevant to NMR spectroscopy) approximately 13,000 times faster than the world's fastest classical supercomputer. This is characterized as the first practical, verifiable application of quantum computing that clearly outperformed classical methods.

- **Unique** [Claude only]: The original Willow benchmark (random circuit sampling) was described as completing in five minutes what would take a classical supercomputer 10^25 years. Willow achieved T1 coherence times of 68 microseconds, roughly a 5x improvement over the prior Sycamore generation.

- **Unique** [Gemini only]: Specific gate fidelity numbers: single-qubit gate fidelity of 99.97%, two-qubit gate fidelity of 99.88%, readout fidelity of 99.5%.

#### 1.2 IBM Quantum Nighthawk and Loon

- **Consensus** [Claude, OpenAI, Gemini]: IBM's Nighthawk processor (120 qubits) uses 218 next-generation tunable couplers in a square lattice topology, enabling circuits with up to 5,000 two-qubit gates -- 30% more complex than previous generations. IBM simultaneously introduced the experimental Loon processor, which validates all hardware components needed for their fault-tolerant "Starling" system targeted for 2029.

- **Consensus** [Claude, OpenAI, Gemini]: IBM's strategy has shifted from maximizing qubit count (their 1,121-qubit Condor demonstrated that larger is not always better, with 5x higher error rates than the smaller 127-qubit Eagle) toward maximizing quality, connectivity, and error correction capability.

- **Unique** [Claude only]: IBM's roadmap includes the Kookaburra processor (1,386 qubits), expandable to 4,158 qubits via multi-chip quantum communication links, planned for 2026. IBM also demonstrated real-time qLDPC error decoding in under 480 nanoseconds.

- **Unique** [Gemini only]: IBM's Nighthawk targets up to 7,500 gates by end of 2026 and 10,000 gates by 2027. The Starling system (2029) aims for 200 logical qubits running approximately 100 million error-corrected operations.

#### 1.3 Quantinuum Helios Trapped-Ion System

- **Consensus** [Claude, OpenAI, Gemini]: Quantinuum launched Helios in November 2025, positioning it as the most powerful and accurate commercial quantum computer available. It uses trapped-ion architecture with all-to-all connectivity and integrates with NVIDIA's CUDA-Q platform.

- **Majority** [OpenAI, Gemini]: Helios contains 98 physical barium-ion qubits configured into 48 fully error-corrected logical qubits, achieving "better than break-even" error correction with a 2:1 physical-to-logical qubit ratio -- far below the ~10:1 overhead previously expected. The system was used to simulate a superconducting metal, yielding a new scientific discovery about the material's atomic behavior.

- **Unique** [Gemini only]: Helios uses a Quantum Charge-Coupled Device (QCCD) architecture that physically shuttles ions through junction systems. Specific fidelity figures: single-qubit gate fidelity 99.9975%, two-qubit gate fidelity 99.921% across all qubit pairs.

#### 1.4 IonQ Record-Breaking Gate Fidelity

- **Consensus** [Claude, OpenAI, Gemini]: IonQ achieved two-qubit gate fidelity exceeding 99.99% (the "four nines" benchmark) in October 2025, making it the first and only quantum computing company to cross this threshold. This was accomplished using a novel "smooth" microwave-driven gate technique from its acquired partner Oxford Ionics.

- **Majority** [Claude, Gemini]: IonQ's roadmap projects 256-qubit systems in 2026, scaling to millions of physical qubits by 2030 via photonic interconnects. The current Tempo system targets 64 AQ (algorithmic qubits) with ~100 physical qubits.

- **Unique** [OpenAI only]: A separate research team demonstrated an even more extreme fidelity of 0.000015% error rate (1 error per 6.7 million operations) on a trapped-ion system using calcium-43 ions, approaching the physical limits imposed by quantum mechanics.

#### 1.5 Neutral-Atom Platforms

- **Consensus** [Claude, OpenAI, Gemini]: Neutral-atom quantum computing emerged as a competitive modality in 2025, with multiple teams demonstrating scalable architectures. Harvard and MIT researchers built a neutral-atom computer that ran continuously for over two hours using 3,000 ultracold atoms with a "conveyor belt" mechanism to replace lost atoms.

- **Unique** [Gemini only]: QuEra Computing launched Gemini in December 2025, a 260-qubit gate-model neutral-atom system offering digital programmable logic with all-to-all connectivity. Microsoft and Atom Computing announced the successful creation and entanglement of 24 logical qubits on a 112-atom ytterbium neutral-atom platform.

- **Unique** [OpenAI only]: Caltech scientists synchronized 6,100 neutral-atom qubits in a single system at room temperature -- the largest quantum array ever created.

#### 1.6 Other Notable Hardware Advances

- **Unique** [Gemini only]: French startup Alice & Bob demonstrated cat qubits with bit-flip resistance lasting over one hour, shattering previous records and enabling a 200-fold reduction in physical qubit overhead compared to standard surface codes.

- **Unique** [OpenAI only]: Quantum Motion (UK) unveiled the first quantum computer built using regular silicon CMOS chips, fabricated on a 300mm wafer, promising scalability using existing semiconductor infrastructure. Princeton researchers developed tantalum-on-silicon superconducting qubits with coherence times of 1.68ms -- 15x longer than Google's and IBM's current processors.

- **Unique** [Claude only]: Fujitsu and RIKEN announced a 256-qubit superconducting quantum computer in April 2025, with plans for 1,000 qubits by 2026. Chinese researchers crossed the fault-tolerance threshold with the Zuchongzhi 3.2 superconducting processor.

- **Majority** [OpenAI, Gemini]: D-Wave released its Advantage2 quantum annealer with approximately 4,400 superconducting qubits, offering higher connectivity and lower noise than its predecessor.

### 2. Quantum Error Correction Breakthroughs

#### 2.1 Below-Threshold Operation

- **Consensus** [Claude, OpenAI, Gemini]: The most significant QEC development of 2025 was the demonstration that adding more physical qubits to a logical qubit reduces rather than increases the overall error rate -- known as operating "below threshold." Google's Willow processor provided the most celebrated proof, with logical error decreasing by a factor of 2.14 when increasing code distance from five to seven using surface codes.

- **Majority** [OpenAI, Gemini]: Google achieved an effective logical error rate of approximately 0.1% per operation on their 101-qubit logical encoding -- a landmark indicating that fault-tolerant quantum computing is feasible in principle.

#### 2.2 Logical Qubit Operations at Scale

- **Majority** [OpenAI, Gemini]: Quantinuum's Helios achieved "better than break-even" error correction, where logical qubits had longer lifetimes and higher success rates than bare physical qubits, with an efficient 2:1 physical-to-logical ratio.

- **Unique** [Gemini only]: Microsoft and Atom Computing demonstrated entanglement of 24 logical qubits in a GHZ (cat) state with error rates below break-even. They also ran the Bernstein-Vazirani algorithm on 28 logical qubits, where logical qubits produced more accurate solutions than the underlying physical qubits.

#### 2.3 Magic State Distillation

- **Majority** [OpenAI, Gemini]: QuEra researchers achieved the first-ever demonstration of magic state distillation on logical qubits -- a milestone scientists had pursued for 20 years. Magic states are essential for performing non-Clifford gates required for universal fault-tolerant computing. Five imperfect magic states were distilled into one high-fidelity state using logical qubits of distance 3 and 5, published in Nature in July 2025.

#### 2.4 Algorithmic Fault Tolerance

- **Majority** [OpenAI, Gemini]: QuEra introduced "Algorithmic Fault Tolerance" (AFT), which restructures quantum algorithms to detect and correct errors during computation rather than relying on rigid check schedules. Simulations showed AFT could reduce QEC overhead by up to 100x while maintaining accuracy, published in Nature in late 2025.

#### 2.5 Novel Error Correction Approaches

- **Unique** [Claude only]: 120 peer-reviewed QEC papers were published in the first ten months of 2025, a dramatic surge from 36 in all of 2024. All seven main QEC code families have now been implemented on hardware. IBM's transition to qLDPC codes is expected to be followed by the wider industry in 2026.

- **Unique** [Claude only]: Microsoft's four-dimensional geometric codes require very few physical qubits per logical qubit, can check for errors in a single shot, and exhibit a 1,000-fold reduction in error rates.

- **Unique** [Gemini only]: Alice & Bob's cat qubits, inherently protected against bit-flips, require only phase-flip correction, enabling fault tolerance with 200x fewer physical qubits than standard surface codes.

### 3. Near-Term Commercial Applications

#### 3.1 Quantum Advantage Demonstrations

- **Majority** [OpenAI, Gemini]: Google's "Quantum Echoes" experiment on the Willow processor achieved a verified 13,000x speedup over classical supercomputers on an NMR molecular spin dynamics simulation. This is widely considered the first practical, verifiable demonstration of quantum computing outperforming classical methods on a scientifically meaningful problem.

- **Unique** [Gemini only]: JPMorgan Chase, in collaboration with Quantinuum and US National Labs, demonstrated the first commercial application of quantum computing for certified randomness generation in March 2025. The randomness was verified by the Frontier supercomputer.

#### 3.2 Drug Discovery and Chemistry

- **Unique** [Claude only]: A collaboration among IonQ, AstraZeneca, AWS, and NVIDIA achieved a 20x improvement in time-to-solution for the Suzuki-Miyaura reaction (used in pharmaceutical synthesis) using a hybrid quantum-classical approach. Insilico Medicine screened 100 million molecules using a quantum-enhanced pipeline, synthesizing 15 promising compounds with two showing biological activity against KRAS-G12D.

- **Unique** [Claude only]: IonQ and Ansys achieved a medical device simulation on a 36-qubit computer that outperformed classical HPC by 12% -- one of the first documented cases of practical quantum advantage in a real-world application.

#### 3.3 Financial Services

- **Consensus** [Claude, OpenAI, Gemini]: Financial institutions are actively deploying quantum computing. JPMorgan Chase achieved quantum streaming algorithms with theoretical exponential space advantage for large data set processing.

- **Unique** [OpenAI only]: HSBC used an IBM 127-qubit processor to optimize bond trading strategies, achieving a 34% improvement in bond price prediction compared to traditional techniques -- the first use of quantum computing for a trading optimization task.

#### 3.4 Optimization and Logistics

- **Unique** [Claude only]: IBM partnered with a commercial vehicle manufacturer to optimize deliveries across 1,200 New York City locations using hybrid quantum-classical methods.

- **Unique** [OpenAI only]: D-Wave reported "hundreds of early quantum and hybrid applications" in optimization, including route optimization for Save-On-Foods, railroad maintenance scheduling, and government infrastructure challenges across the UK, Canada, Japan, and Italy.

#### 3.5 Quantum Sensing and Navigation

- **Majority** [Claude, Gemini]: Q-CTRL achieved the first commercial quantum advantage in GPS-denied navigation, with quantum sensors outperforming conventional alternatives by 50x (later exceeding 100x). This has immediate defense and maritime applications.

#### 3.6 Generative Quantum AI

- **Unique** [Gemini only]: Quantinuum launched the GenQAI framework, which uses quantum computers to generate synthetic training data for classical AI models, addressing data scarcity in molecular discovery. Partners include Merck and BMW for drug discovery and materials science.

### 4. Funding Trends and Market Dynamics

#### 4.1 Private Investment

- **Consensus** [Claude, OpenAI, Gemini]: 2025 saw record-breaking private investment in quantum computing.

- **Majority** [Claude, Gemini]: The sector attracted $3.77 billion in equity funding in the first nine months of 2025, nearly triple the $1.3 billion raised in all of 2024. Q1 2025 alone exceeded $1.25 billion -- a 128% year-over-year increase.

- **Consensus** [Claude, OpenAI, Gemini]: Major funding rounds included PsiQuantum ($750M--$1B, combining government-backed and Series E funding), QuEra Computing ($230M from Google Ventures and SoftBank), and Quantum Machines ($170M Series C).

- **Unique** [Gemini only]: Alice & Bob raised approximately 100 million EUR. Quantinuum raised $300--$839M in late-stage funding.

#### 4.2 Government Funding

- **Consensus** [Claude, OpenAI, Gemini]: Government investment reached approximately $10 billion globally by April 2025, driven by national security and economic competitiveness concerns.

- **Unique** [Claude only]: Japan committed $7.4 billion, Spain invested 808 million EUR over its 2025--2030 quantum strategy, and the UK committed 670 million GBP over the next decade.

- **Unique** [OpenAI only]: A bipartisan US bill introduced in January 2026 would reauthorize the National Quantum Initiative for 2024--2029. The EU is formulating a "Quantum Chips Act." Spain built its first homegrown 5-qubit quantum computer for approximately 9 million EUR.

#### 4.3 Market Valuation

- **Unique** [Claude only]: The global quantum computing market reached $1.8--$3.5 billion in 2025, with projections indicating growth to $5.3 billion by 2029 (CAGR 32.7%) or as high as $20.2 billion by 2030 (CAGR 41.8%). McKinsey reports quantum companies generated $650--$750M in revenue in 2024, expected to surpass $1B in 2025.

- **Majority** [Claude, OpenAI]: Pure-play quantum stocks saw extraordinary returns: D-Wave surged over 3,700%, IonQ +700%, Rigetti +5,700% over trailing 12 months. D-Wave's market cap briefly exceeded $4.5 billion despite modest revenue (~$15M/quarter).

#### 4.4 Industry Consolidation

- **Unique** [Claude only]: IonQ pursued acquisitions exceeding $1 billion total, including Oxford Ionics ($1.075B), Lightsynq, Capella Space, ID Quantique, and Vector Atomic, building an integrated value chain.

- **Unique** [Gemini only]: A notable strategic shift occurred in China: Alibaba and Baidu exited quantum hardware research in late 2024/early 2025, donating their labs to universities, signaling a pivot toward state-centralized development.

### 5. Leading Companies and Ecosystem

#### 5.1 Competitive Landscape

- **Consensus** [Claude, OpenAI, Gemini]: The industry has stratified around four primary hardware modalities, each with clear leaders:
  - **Superconducting qubits**: Google (Willow, 105 qubits) and IBM (Nighthawk, 120 qubits)
  - **Trapped ions**: Quantinuum (Helios, 98 qubits) and IonQ (Tempo, ~100 qubits)
  - **Neutral atoms**: QuEra (Gemini, 260 qubits) and Atom Computing (1,225 qubits)
  - **Photonics**: PsiQuantum (targeting million-qubit scale)

- **Majority** [Claude, Gemini]: Quantinuum holds a multi-billion-dollar valuation (~$10B), formed from the merger of Honeywell Quantum Solutions and Cambridge Quantum.

#### 5.2 Technology Giants

- **Consensus** [Claude, OpenAI, Gemini]: Microsoft is pursuing topological qubits via the Majorana 1 chip, using "topoconductor" materials. In 2025, Microsoft collaborated with Quantinuum (12 logical qubit entanglement) and Atom Computing (24 logical qubit system).

- **Unique** [Claude only]: Amazon AWS launched the Ocelot chip in February 2025 to reduce error correction costs by up to 90%.

### 6. Expert Predictions and Outlook for 2026

- **Consensus** [Claude, OpenAI, Gemini]: IBM anticipates that verified quantum advantage will be confirmed by the wider community before the end of 2026. Multiple providers describe 2026 as a transition year from research promise to tangible deployment.

- **Majority** [Claude, OpenAI]: Google's leadership suggests truly useful, large-scale quantum computers could be "a few years" away if current trends continue.

- **Unique** [Claude only]: Jensen Huang (NVIDIA CEO) stated in January 2025 that quantum computing is "15 to 30 years from being truly useful," sparking industry-wide efforts to prove him wrong. Nobel laureate Frank Wilczek cautioned that "classical computers will remain superior for the foreseeable future."

- **Consensus** [Claude, OpenAI, Gemini]: Fully fault-tolerant quantum computers capable of running million-operation algorithms will not arrive before 2029--2030 at the earliest. Near-term systems (2026--2027) will have tens of logical qubits for specific applications.

---

## Areas of Disagreement

1. **Willow benchmark characterization**: Claude describes the Willow achievement primarily through the original random circuit sampling benchmark (5 minutes vs. 10^25 years for classical), while OpenAI and Gemini emphasize the later "Quantum Echoes" practical application (13,000x speedup on NMR simulation). These are likely distinct experiments on the same chip, not contradictions, but the framing differs significantly -- with the Quantum Echoes result being more practically meaningful.

2. **Microsoft Majorana credibility**: OpenAI's report explicitly notes that Microsoft's scientific paper "did not fully prove the existence of Majorana particles" and acknowledges skepticism. Claude presents the findings more neutrally, and Gemini treats it as a straightforward prototype. The level of scientific caution varies notably across providers.

3. **PsiQuantum funding magnitude**: Claude cites a $750 million government-backed round (March 2025), while OpenAI and Gemini report a $1 billion Series E. These appear to be different funding events that occurred close together, but the discrepancy is worth noting for precision.

4. **Helios detail level**: Claude's coverage of Quantinuum's Helios is notably less detailed than OpenAI and Gemini, which both report the 98-qubit / 48-logical-qubit achievement with 2:1 ratio. This represents an information gap in Claude's report rather than a factual disagreement.

5. **Market size estimates**: Claude provides a wide range ($1.8B--$3.5B for 2025 market size), while other providers do not specify. The range itself reflects genuine uncertainty in how the quantum computing market is defined and measured.

---

## Gaps & Limitations

### Research Gaps

- **Quantum software ecosystem**: None of the three providers provided substantial coverage of quantum programming frameworks (Qiskit, Cirq, PennyLane), compiler advances, or the software stack maturity required for practical deployment.

- **Quantum networking and internet**: Limited coverage of quantum communication, quantum key distribution (QKD) networks, and the emerging quantum internet infrastructure, despite active programs in China, Europe, and the US.

- **Workforce and talent**: Only briefly mentioned by Claude. The acute shortage of quantum engineers and the expansion of university programs deserve deeper analysis.

- **Environmental and energy considerations**: No provider addressed the energy consumption and cooling requirements of quantum systems, which are significant operational considerations for superconducting and some other modalities.

- **Quantum-AI convergence detail**: While Gemini mentions GenQAI and OpenAI notes quantum machine learning trends, the rapidly evolving intersection of quantum computing and AI deserves more focused analysis.

- **Standardization and benchmarking**: Claude mentions QuOps as an emerging metric, but none of the reports deeply examine the ongoing challenges of comparing quantum systems across different modalities and vendors.

### Methodological Limitations

- **Citation validation depth**: Only URL liveness was checked (Level 1). Content accuracy of cited sources was not independently verified against the claims made.
- **Dead links**: 22 of 148 total citations (15%) returned dead URLs, primarily among Gemini's Vertex AI Search redirect URLs. This affects the verifiability of Gemini's specific claims.
- **Provider bias**: Each AI provider may have preferential access to or awareness of certain sources. Google Gemini's citations route through Google's Vertex AI grounding infrastructure, which may introduce source selection bias.
- **Temporal coverage**: Reports reflect information available as of February 14, 2026. Developments after this date are not captured.
- **Single-provider claims**: Claims marked as "Unique" to one provider should be treated with lower confidence than consensus claims, as they lack independent corroboration from this research process.

---

## References

### Hardware and Processors

- IBM Nighthawk and Loon processors: [LiveScience - IBM unveils two new quantum processors](https://www.livescience.com/technology/computing/ibm-unveils-two-new-quantum-processors-including-one-that-offers-a-blueprint-for-fault-tolerant-quantum-computing-by-2029)
- Google Willow Quantum Echoes: [Tom's Hardware - Google's Quantum Echo Algorithm](https://www.tomshardware.com/tech-industry/quantum-computing/googles-quantum-echo-algorithm-shows-worlds-first-practical-application-of-quantum-computing-willow-105-qubit-chip-runs-algorithm-13-000x-faster-than-a-supercomputer)
- Google Willow error correction: [HuffPost ES - Willow chip](https://www.huffingtonpost.es/tecnologia/willow-nuevo-chip-cuantico-google-potencia-calculo-extraordinaria.html)
- Quantinuum Helios: [LiveScience - Most powerful quantum computer](https://www.livescience.com/technology/computing/this-is-easily-the-most-powerful-quantum-computer-on-earth-scientists-unveil-helios-a-record-breaking-quantum-system)
- IonQ gate fidelity record: [PostQuantum - IonQ Record 2025](https://postquantum.com/quantum-research/ionq-record-2025/)
- IonQ roadmap and AQ metrics: [IonQ Blog - AQ 35](https://www.ionq.com/blog/how-we-achieved-our-2024-performance-target-of-aq-35)

### Error Correction and Logical Qubits

- QuEra magic state distillation: [LiveScience - Magic state breakthrough](https://www.livescience.com/technology/computing/scientists-make-magic-state-breakthrough-after-20-years-without-it-quantum-computers-can-never-be-truly-useful)
- QuEra Algorithmic Fault Tolerance: [LiveScience - Quantum computing breakthrough could slash errors by 100 times](https://www.livescience.com/technology/computing/this-moves-the-timeline-forward-significantly-quantum-computing-breakthrough-could-slash-pesky-errors-by-up-to-100-times)
- IonQ 0.000015% error rate: [LiveScience - Error rate world record](https://www.livescience.com/technology/computing/scientists-hit-quantum-computer-error-rate-of-0-000015-percent-a-world-record-achievement-that-could-lead-to-smaller-and-faster-machines)
- Microsoft Majorana 1: [Le Monde - Microsoft quantum](https://www.lemonde.fr/sciences/article/2025/02/21/ordinateurs-quantiques-microsoft-jette-un-pave-dans-la-mare_6557701_1650684.html)

### Neutral Atoms and Novel Approaches

- Harvard/MIT 2-hour neutral-atom computer: [Tom's Hardware - Harvard quantum breakthrough](https://www.tomshardware.com/tech-industry/quantum-computing/harvard-researchers-hail-quantum-computing-breakthrough-with-machine-that-can-run-for-two-hours-atomic-loss-quashed-by-experimental-design-systems-that-can-run-forever-just-3-years-away)
- Caltech 6,100-qubit array: [LiveScience - Quantum record smashed](https://www.livescience.com/technology/computing/quantum-record-smashed-as-scientists-build-mammoth-6-000-qubit-system-and-it-works-at-room-temperature)
- Quantum Motion silicon CMOS: [LiveScience - First quantum computer built with regular silicon chips](https://www.livescience.com/technology/computing/scientists-unveil-worlds-first-quantum-computer-built-with-regular-silicon-chips)
- Princeton tantalum qubits: [LiveScience - Information lasts 15x longer](https://www.livescience.com/technology/computing/record-breaking-feat-means-information-lasts-15-times-longer-in-new-kind-of-quantum-processor-than-those-used-by-google-and-ibm)

### Applications

- HSBC bond trading: [Axios - AI HSBC quantum bonds](https://www.axios.com/2025/09/26/ai-hsbc-quantum-bonds)
- D-Wave optimization applications: [Axios - D-Wave government challenges](https://www.axios.com/sponsored/how-d-wavetm-is-solving-complex-government-challenges-today)
- JPMorgan certified randomness: [JPMorgan Chase](https://www.jpmorganchase.com)
- Q-CTRL GPS-denied navigation: [Q-CTRL](https://q-ctrl.com)

### Funding and Industry

- PsiQuantum $1B funding: [TechRadar - PsiQuantum million-qubit](https://www.techradar.com/pro/psiquantum-plans-to-build-worlds-first-large-scale-fault-tolerant-million-qubit-quantum-computers-for-solving-some-of-the-worlds-most-complex-scientific-problems)
- D-Wave stock performance: [Cinco Dias - D-Wave quantum](https://cincodias.elpais.com/companias/2025-05-20/la-empresa-de-computacion-cuantica-d-wave-quantum-se-dispara-en-bolsa-tras-poner-a-la-venta-su-nuevo-superordenador.html)
- IBM quantum advantage timeline: [ITPro - IBM targeting quantum advantage](https://www.itpro.com/technology/big-data/ibm-is-targeting-quantum-advantage-in-12-months-and-says-useful-quantum-computing-is-just-a-few-years-away)
- Google commercially viable timeline: [ITPro - Sundar Pichai quantum computing](https://www.itpro.com/technology/sundar-pichai-thinks-commercially-viable-quantum-computing-is-just-a-few-years-away)
- US NQI reauthorization: [Axios - Senators unveil bipartisan quantum bill](https://www.axios.com/2026/01/08/senators-unveil-bipartisan-quantum-bill)
- EU Quantum Chips Act: [Le Monde - Puces quantiques](https://www.lemonde.fr/economie/article/2025/03/02/puces-quantiques-l-europe-prepare-son-quantum-act-pour-reglementer-le-secteur_6572889_3234.html)

---

*Report generated: 2026-02-14*
*Research providers: Claude (Anthropic), OpenAI, Gemini (Google)*
*Citation validation: 126 alive / 22 dead (85% liveness)*
