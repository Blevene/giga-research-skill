# Comparison Matrix: Provider Report Analysis

## Topic Coverage

| Topic | Claude | OpenAI | Gemini |
|-------|--------|--------|--------|
| Google Willow chip | Yes | Yes | Yes |
| IBM Nighthawk processor | Yes | Yes | Yes |
| IBM Loon experimental processor | Yes | Yes | Yes |
| IBM Kookaburra multi-chip roadmap | Yes | No | No |
| Quantinuum Helios system | Yes | Yes | Yes |
| IonQ gate fidelity (99.99%) | Yes | Yes | Yes |
| IonQ Tempo / AQ metric | Yes | Yes | Yes |
| QuEra Gemini / neutral atoms | No | No | Yes |
| Microsoft/Atom Computing (24 logical qubits) | No | No | Yes |
| Alice & Bob cat qubits (1-hour bit-flip resistance) | No | No | Yes |
| Quantum Motion (silicon CMOS qubits) | No | Yes | No |
| Princeton tantalum qubits (1.68ms coherence) | No | Yes | No |
| D-Wave Advantage2 annealer | No | Yes | Yes |
| PsiQuantum photonic ($1B funding) | Yes | Yes | Yes |
| Harvard/MIT neutral-atom 2-hour runtime | Yes | Yes | Yes |
| Caltech 6,100-qubit neutral-atom array | No | Yes | No |
| Chinese CHIPX photonic chip | No | Yes | No |
| Microsoft Majorana 1 / topological qubits | Yes | Yes | Yes |
| Fujitsu/RIKEN 256-qubit system | Yes | No | No |
| China Zuchongzhi 3.2 | Yes | No | No |
| Atom Computing 1225-qubit system | Yes | No | No |
| Below-threshold QEC demonstration | Yes | Yes | Yes |
| Magic state distillation (QuEra) | No | Yes | Yes |
| Algorithmic Fault Tolerance (AFT) | No | Yes | Yes |
| qLDPC codes / IBM real-time decoding | Yes | No | Yes |
| QEC paper count surge (120 in 2025) | Yes | No | No |
| Drug discovery applications | Yes | No | No |
| Medical device simulation (IonQ/Ansys) | Yes | No | No |
| Financial services (JPMorgan) | Yes | Yes | Yes |
| HSBC bond trading optimization | No | Yes | No |
| Google Quantum Echoes (13,000x speedup) | No | Yes | Yes |
| Q-CTRL GPS-denied navigation | Yes | No | Yes |
| D-Wave optimization applications | No | Yes | No |
| Quantinuum GenQAI framework | No | No | Yes |
| Certified randomness (JPMorgan/Quantinuum) | No | No | Yes |
| IBM logistics optimization (NYC) | Yes | No | No |
| Private investment ($3.77B in 9 months) | Yes | No | Yes |
| Government funding ($10B global) | Yes | Yes | Yes |
| QuEra $230M funding round | Yes | No | Yes |
| Quantum Machines $170M funding | Yes | No | No |
| Classiq $110M funding | Yes | No | No |
| Alice & Bob ~100M EUR funding | No | No | Yes |
| Market valuation projections | Yes | No | No |
| Stock market performance | Yes | Yes | No |
| IonQ acquisitions ($1B+) | Yes | No | No |
| Jensen Huang "15-30 years" comment | Yes | No | No |
| QuOps metric standardization | Yes | No | No |
| Regional competition (NA, Asia, Europe) | Yes | Yes | No |
| UK quantum investment | Yes | No | No |
| US NQI reauthorization bill | No | Yes | No |
| EU Quantum Chips Act | No | Yes | No |
| Spain first quantum computer | No | Yes | No |
| Alibaba/Baidu exit from quantum | No | No | Yes |
| Expert predictions for 2026 | Yes | Yes | Yes |
| Post-quantum cryptography | No | Yes | No |

## Areas of Consensus (All 3 Providers Agree)

1. **Google Willow achieved below-threshold QEC**: All three confirm Google's 105-qubit Willow chip demonstrated exponential error suppression as qubit arrays scaled, crossing the fault-tolerance threshold. Claude and OpenAI cite 10^25 years / 13,000x classical speedup respectively for benchmark tasks.

2. **IBM Nighthawk (120 qubits, 5,000 two-qubit gates)**: All three report consistent specs: 120 qubits, 218 tunable couplers, 30% more circuit complexity, up to 5,000 two-qubit gates.

3. **IonQ achieved >99.99% two-qubit gate fidelity**: All providers confirm IonQ crossed the "four nines" benchmark, making it the first company to do so.

4. **Quantinuum Helios is a leading commercial system**: All three describe Helios as among the most powerful/accurate commercial quantum computers, with trapped-ion architecture.

5. **Error correction transitioned from theory to practice in 2025**: All providers agree 2025 was the year QEC moved from theoretical to hardware-validated.

6. **IBM targeting quantum advantage by end of 2026**: All three cite IBM's prediction of verified quantum advantage within 2026.

7. **Investment surge in 2025**: All three note unprecedented private and government funding, with Claude and Gemini both citing $3.77B in first three quarters.

8. **Microsoft pursuing topological qubits (Majorana)**: All three mention Microsoft's Majorana 1 chip, though with varying detail and skepticism levels.

9. **PsiQuantum raised ~$1B for photonic quantum computing**: All three providers report this major funding round.

10. **Neutral atoms emerging as competitive modality**: All three highlight neutral-atom platforms (QuEra, Atom Computing, Harvard/MIT) as a rising architecture.

## Areas of Disagreement or Conflicting Claims

1. **Google Willow speedup magnitude**:
   - Claude: "five minutes vs 10^25 years" (random circuit sampling benchmark)
   - OpenAI: "13,000x faster" (Quantum Echoes / NMR simulation, a different benchmark)
   - Gemini: Also cites "13,000x faster" for Quantum Echoes
   - *Note*: These appear to reference different benchmarks, not true contradictions. Claude references the original RCS claim while OpenAI and Gemini reference the later Quantum Echoes practical application.

2. **Quantinuum Helios qubit count and logical qubit achievement**:
   - Claude: Describes Helios with "all-to-all connectivity" but does not specify physical qubit count or logical qubit achievement
   - OpenAI: 98 physical qubits, 48 logical qubits with 2:1 physical-to-logical ratio, "better than break-even"
   - Gemini: 98 physical qubits, confirms 48 logical qubits, also references barium-137 ions
   - *Resolution*: OpenAI and Gemini are consistent; Claude's report is less detailed on Helios specifics.

3. **PsiQuantum funding amount**:
   - Claude: "$750 million government-backed funding round" (March 2025)
   - OpenAI: "$1 billion" (Series E)
   - Gemini: "$1 billion" (Series E)
   - *Note*: These may be different funding events. The $750M appears to be an Australian government-backed round, while $1B is the separate Series E.

4. **Microsoft Majorana 1 assessment**:
   - Claude: Presents Majorana findings matter-of-factly ("novel topoconductor materials")
   - OpenAI: Much more cautious, noting the paper "did not fully prove" Majorana particles; acknowledges skepticism
   - Gemini: Presents it neutrally but mentions it as a prototype with 8 topological qubits
   - *Significance*: OpenAI is notably more skeptical than the other two providers.

5. **Quantinuum valuation**:
   - Claude: "$10 billion" valuation
   - Gemini: "$300-$839 million" in late-stage funding (not valuation)
   - *Note*: These are different metrics (valuation vs. funding round) and not directly contradictory.

## Unique Insights by Provider

### Claude Only
- **Drug discovery detail**: Extensive coverage of IonQ-AstraZeneca-AWS-NVIDIA collaboration (20x improvement in Suzuki-Miyaura reaction), St. Jude KRAS research, Insilico Medicine hybrid pipeline
- **IonQ-Ansys medical device simulation**: 12% outperformance of classical HPC
- **QEC research paper surge**: 120 papers in first 10 months of 2025 vs. 36 in all of 2024
- **QuOps metric**: Growing recognition as the definitive benchmark for quantum progress
- **Jensen Huang controversy**: Nvidia CEO's "15-30 years" prediction and industry response
- **Fujitsu/RIKEN 256-qubit system**: Japan's expanding quantum hardware
- **IBM Kookaburra roadmap**: 1,386-qubit processor, expandable to 4,158 qubits
- **Stock market performance specifics**: D-Wave +3,700%, IonQ +700%, Rigetti +5,700%
- **IonQ acquisition spree**: $1B+ in acquisitions (Oxford Ionics, Lightsynq, ID Quantique, etc.)

### OpenAI Only
- **HSBC bond trading optimization**: 34% improvement in bond price prediction
- **Quantum Motion silicon CMOS qubits**: First quantum computer on regular silicon chips
- **Princeton tantalum qubits**: 1.68ms coherence, 15x longer than Google/IBM
- **Caltech 6,100-qubit neutral-atom array**: Largest quantum array at room temperature
- **Chinese CHIPX photonic chip**: "1,000x faster than NVIDIA GPUs" claim
- **D-Wave Advantage2 details**: ~4,400 qubits, optimization application detail (Save-On-Foods, railroad operators)
- **D-Wave CEO Alan Baratz letter**: Countering "always decades away" narrative
- **Photonic quantum computing detail**: Xanadu, PsiQuantum manufacturing plans
- **EU Quantum Chips Act**: European regulatory preparation
- **US NQI reauthorization**: Bipartisan bill for renewed federal quantum funding
- **Spain's first quantum computer**: 5-qubit system via Qilimanjaro
- **Post-quantum cryptography**: Standards being finalized for quantum-resistant encryption

### Gemini Only
- **QuEra Gemini system**: 260-qubit gate-model neutral-atom processor (December 2025)
- **Microsoft/Atom Computing 24 logical qubits**: Commercial breakthrough with entangled logical qubits
- **Alice & Bob cat qubits**: 1-hour bit-flip resistance, 200x reduction in physical qubit overhead
- **Certified randomness (JPMorgan/Quantinuum)**: First commercial QC application for cryptographic randomness
- **Quantinuum GenQAI framework**: Quantum-generated synthetic data for training classical AI
- **Iceberg Quantum**: Emerging fault-tolerant architecture software company
- **Alibaba/Baidu exit from quantum**: Strategic shift in China's quantum sector
- **Specific fidelity metrics**: Google Willow single-qubit 99.97%, two-qubit 99.88%; Quantinuum single-qubit 99.9975%, two-qubit 99.921%
- **IBM qLDPC decoding in <480 nanoseconds**: Real-time error correction speed achievement

## Depth and Quality Assessment

| Dimension | Claude | OpenAI | Gemini |
|-----------|--------|--------|--------|
| Hardware coverage breadth | High | Very High | High |
| Error correction depth | Medium | Very High | High |
| Application examples | High | High | Medium |
| Funding/market detail | Very High | Medium | High |
| Specific metrics/numbers | High | Very High | Very High |
| Skepticism/nuance | Medium | High | Medium |
| Regional/geopolitical | Medium | High | Medium |
| Novel/emerging approaches | Low | High | High |
| Overall word count | ~3,000 | ~6,000+ | ~4,000 |
| Citation quality | Inline quotes, no URLs | Full URLs with anchor text | Numbered cite refs with Vertex redirect URLs |
