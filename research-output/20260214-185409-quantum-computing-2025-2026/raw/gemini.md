# Research Task: Current State of Quantum Computing (2025–2026)

The period spanning 2025 through early 2026 marks a definitive inflection point in the trajectory of quantum information science, characterized by the industry's transition from experimental physics to high-performance engineering. Research indicates that 2025 was the year the "fault tolerance" barrier was credibly breached, not just in theory but in hardware implementation. While universal, large-scale commercial utility remains on the horizon (projected for the late 2020s), the immediate achievements of this period include the establishment of "four nines" (99.99%) gate fidelity in trapped ions, the verifiable demonstration of quantum advantage in specific sampling tasks by superconducting processors, and the operational deployment of logical qubits in neutral-atom arrays.

Leading hardware providers have converged on aggressive roadmaps that prioritize error correction and logical qubit scaling over raw physical qubit counts. Controversy remains regarding the precise definition of "quantum utility," yet verifiable milestones—such as Google’s computational speedup of 13,000x over classical supercomputers and JPMorgan Chase’s generation of certified quantum randomness—suggest that the industry has moved beyond hype into early operational relevance. The evidence leans toward a consolidation of capital around distinct modalities: superconducting circuits (Google, IBM), trapped ions (Quantinuum, IonQ), neutral atoms (QuEra, Atom Computing), and photonics (PsiQuantum), with significant government and private funding reinforcing these leaders.

## 1. Significant Quantum Computing Hardware Milestones (2025–2026)

The hardware landscape in 2025 and early 2026 was defined by the release of processors that fundamentally altered the error-correction landscape. The focus shifted decisively from "Noisy Intermediate-Scale Quantum" (NISQ) devices to "Early Fault-Tolerant" architectures.

### The Superconducting Breakthroughs: Willow and Nighthawk
In October 2025, Google Quantum AI achieved a historic milestone with the announcement of the **Willow** processor. This 105-qubit superconducting chip demonstrated verifiable quantum advantage by executing the "Quantum Echoes" algorithm (simulating out-of-time-order correlators) approximately 13,000 times faster than the world's most powerful classical supercomputers [cite: 1, 2]. Unlike previous "quantum supremacy" claims which were often contested or based on useless sampling tasks, the Willow demonstration involved verifiable benchmarks relevant to molecular modeling and nuclear magnetic resonance (NMR) spectroscopy [cite: 3]. Crucially, Willow demonstrated that error rates could be suppressed exponentially as the system scaled, a prerequisite for fault tolerance [cite: 4].

Following closely in November 2025, **IBM** unveiled its **Quantum Nighthawk** processor. While possessing 120 qubits—a modest number compared to their 1,000+ qubit Condor chip of 2023—Nighthawk represented a paradigm shift in connectivity. It introduced a square lattice topology with 218 tunable couplers, increasing inter-qubit connectivity by 20% compared to the previous Heron architecture [cite: 5]. This design allows for the execution of quantum circuits with 30% greater complexity, enabling the system to run algorithms requiring up to 5,000 two-qubit gates [cite: 6]. Simultaneously, IBM announced **Quantum Loon**, an experimental processor specifically architected to validate the hardware components necessary for the "Starling" fault-tolerant system targeted for 2029 [cite: 5].

### The Trapped-Ion Fidelity Record
**IonQ** claimed a pivotal achievement in October 2025 by demonstrating two-qubit gate fidelity exceeding **99.99%** (the "four nines" benchmark) on its trapped-ion hardware [cite: 7]. This milestone was achieved using a new "smooth gate" technique that bypassed the need for ground-state cooling, allowing for faster operation without sacrificing accuracy [cite: 7]. This level of fidelity is critical because it surpasses the threshold required for efficient error-correcting codes, theoretically allowing for a 10^10 performance increase in error-corrected operations compared to 99.9% systems [cite: 8].

**Quantinuum** responded in November 2025 with the launch of **Helios**, a 98-qubit trapped-ion quantum computer [cite: 9]. Helios represented a significant architectural evolution, utilizing a Quantum Charge-Coupled Device (QCCD) design that physically shuttles ions through a complex junction system. Notably, Helios switched data qubits to barium-137 ions (with ytterbium for sympathetic cooling) to improve gate error rates and scalability [cite: 10]. Quantinuum positioned Helios as the "world's most accurate" commercial system, integrating with NVIDIA's CUDA-Q platform for real-time error correction [cite: 11].

### The Rise of Neutral Atoms
The neutral-atom modality saw explosive growth in 2025. **QuEra Computing** launched **Gemini** in December 2025, a gate-model system featuring 260 physical qubits [cite: 12]. Unlike analog simulators, Gemini offers digital, programmable logic with all-to-all connectivity via dynamic qubit shuttling [cite: 13]. In collaboration with Harvard and MIT, QuEra demonstrated the operation of 48 to 96 logical qubits with error rates that improved as the system size increased, a definitive validation of scalable fault tolerance [cite: 14, 15].

Simultaneously, **Microsoft** and **Atom Computing** announced a commercial breakthrough in late 2025: the successful creation and entanglement of **24 logical qubits** on a neutral-atom platform [cite: 16]. This system, utilizing 112 physical ytterbium atoms, demonstrated the ability to detect and correct the loss of atoms in real-time—a unique failure mode of neutral-atom arrays—thereby ensuring computation continuity [cite: 16].

### Photonics and Cat Qubits
In the realm of superconducting circuits designed for specific stability, French startup **Alice & Bob** achieved a stunning milestone in September 2025: their "cat qubits" demonstrated resistance to bit-flip errors for over **one hour** [cite: 17, 18]. This shattered previous records of milliseconds or minutes, validating their approach of embedding error correction directly into the physical qubit design to reduce the hardware overhead for fault tolerance [cite: 19].

**PsiQuantum** continued its pursuit of utility-scale photonics, securing $1 billion in Series E funding to construct massive manufacturing and cryogenic facilities in Chicago and Brisbane, targeting a commercial system by 2027 [cite: 20, 21].

## 2. Leading Companies and Laboratories: Metrics and Status

The competitive landscape has stratified into top-tier "full-stack" providers and specialized hardware developers. The following analysis details the standing of key players as of early 2026.

### Google Quantum AI
*   **Architecture:** Superconducting Transmon Qubits.
*   **Current Flagship:** **Willow** (105 qubits) [cite: 2].
*   **Key Metrics:**
    *   Single-qubit gate fidelity: **99.97%** [cite: 22].
    *   Two-qubit gate fidelity: **99.88%** [cite: 22].
    *   Readout fidelity: **99.5%**.
*   **Status:** Google leads in demonstrated algorithmic speedup. The verified performance of Willow suggests they have successfully managed the noise-scale trade-off that plagued earlier large chips. Their roadmap is focused on reaching "Milestone 3": a long-lived logical qubit [cite: 3].

### IBM Quantum
*   **Architecture:** Superconducting Transmon Qubits.
*   **Current Flagship:** **Quantum Nighthawk** (120 qubits, high connectivity) [cite: 5].
*   **Key Metrics:**
    *   Circuit Depth: Capable of **5,000 two-qubit gates** [cite: 6].
    *   Error Decoding: <480 nanoseconds for real-time processing [cite: 23].
*   **Status:** IBM has pivoted from maximizing qubit count (e.g., the 1,121-qubit Condor) to maximizing *quality* and connectivity. The Nighthawk chip is the workhorse for "quantum advantage" demonstrations in 2026, while the experimental Loon chip prepares the ground for the 2029 "Starling" fault-tolerant system [cite: 24]. IBM maintains the largest fleet of cloud-accessible quantum systems.

### IonQ
*   **Architecture:** Trapped Ions (Ytterbium/Barium).
*   **Current Flagship:** **IonQ Tempo** (Development systems supporting ~100 qubits in 2025) [cite: 25].
*   **Key Metrics:**
    *   Two-qubit gate fidelity: **>99.99%** (World Record) [cite: 7].
    *   Physical Qubits: Roadmap targets 256 qubits in 2026 [cite: 26].
*   **Status:** IonQ has solidified its position as the leader in gate fidelity. The acquisition of Oxford Ionics provided crucial "Electronic Qubit Control" (EQC) technology, allowing them to replace optical controllers with chip-integrated electronics, a major step toward scalability [cite: 26]. Their roadmap projects scaling to millions of qubits by 2030 via photonic interconnects [cite: 27].

### Quantinuum
*   **Architecture:** Trapped Ions (QCCD).
*   **Current Flagship:** **Helios** (98 qubits) [cite: 9].
*   **Key Metrics:**
    *   Single-qubit gate fidelity: **99.9975%** [cite: 28].
    *   Two-qubit gate fidelity: **99.921%** across all pairs [cite: 28].
*   **Status:** Quantinuum holds the crown for the highest overall system volume and fidelity in a commercial general-purpose machine. Helios introduces "all-to-all" connectivity via ion shuttling, distinct from IonQ's photonic interconnect approach [cite: 10]. They are heavily integrated with NVIDIA's ecosystem for hybrid quantum-classical workflows [cite: 11].

### QuEra Computing
*   **Architecture:** Neutral Atoms (Rubidium).
*   **Current Flagship:** **Gemini** (260 physical qubits) [cite: 13].
*   **Key Metrics:**
    *   Logical Qubits: Demonstrated algorithms on **48 logical qubits**; validated architecture for up to 96 [cite: 14, 29].
    *   Two-qubit gate fidelity: **>99.2%** [cite: 13].
*   **Status:** QuEra has rapidly emerged as the leader in logical qubit implementation. Their partnership with Harvard and MIT has produced the most convincing demonstrations of quantum error correction to date. They are transitioning from research to industrial deployment, with systems installed at Japan's AIST [cite: 14, 30].

### Microsoft / Atom Computing
*   **Architecture:** Neutral Atoms (Ytterbium).
*   **Current Flagship:** Commercial system delivering **24 entangled logical qubits** [cite: 16].
*   **Key Metrics:**
    *   Physical gate fidelity: **99.6%** [cite: 16].
    *   Logical Qubit Count: 24 (entangled state) [cite: 31].
*   **Status:** This partnership combines Atom's hardware with Microsoft's virtualization (error correction) software. They are aggressively targeting commercial reliability, offering systems that can detect and correct atom loss in real-time [cite: 16].

## 3. Progress in Quantum Error Correction (QEC)

2025 is widely cited as the year fault tolerance transitioned from theory to engineering reality. The industry moved beyond simple error *detection* to active error *correction* and the successful operation of logical qubits (groups of physical qubits that act as a single, error-free unit).

### Logical Qubit Entanglement and Operation
The most significant QEC milestone was the entanglement of **24 logical qubits** by Microsoft and Atom Computing [cite: 16]. This demonstrated not only the creation of logical qubits but their ability to interact in a "cat state" (Greenberger-Horne-Zeilinger state) with error rates significantly below the break-even threshold. Furthermore, they demonstrated computation on **28 logical qubits** using the Bernstein-Vazirani algorithm, where the logical qubits produced more accurate solutions than the underlying physical qubits—a definitive proof of QEC gain [cite: 16].

### Scalable Architecture and Magic State Distillation
QuEra and its academic partners achieved a breakthrough by demonstrating **logical magic state distillation** [cite: 32]. Magic states are a resource required to perform non-Clifford gates (essential for universal quantum computing) in a fault-tolerant manner. QuEra also demonstrated that as they increased the size of their system (up to 96 logical qubits), the logical error rate decreased, validating the fundamental premise of fault tolerance [cite: 14]. They also solved the "atom loss" problem—where neutral atoms fly out of the trap—by replenishing qubits mid-computation, allowing continuous operation for over two hours [cite: 33].

### Bias-Preserving "Cat Qubits"
Alice & Bob's achievement of **1-hour bit-flip resistance** represents a different approach to QEC [cite: 17]. By using "cat qubits" that are inherently protected against bit-flips (one of the two main types of quantum errors), they drastically reduce the complexity of the error correction code required to fix the remaining phase-flips. This allows for fault tolerance with a 200-fold reduction in the number of physical qubits needed compared to standard surface codes [cite: 34].

### Real-Time Decoding
Effective QEC requires measuring errors and applying corrections faster than new errors can occur. IBM demonstrated the ability to decode quantum low-density parity-check (qLDPC) codes in under **480 nanoseconds** using classical hardware [cite: 23]. This 10x speedup in decoding is a critical enabling technology for the operation of their future fault-tolerant "Starling" system [cite: 35].

## 4. Near-Term Practical and Commercial Applications

While "universal" fault tolerance is years away, 2025 saw the emergence of applications delivering verifiable value in specific domains, often termed "quantum utility" or "commercial advantage."

### Certified Randomness in Finance
In March 2025, **JPMorgan Chase**, in collaboration with Quantinuum and US National Labs, demonstrated the first commercial application of a quantum computer for **certified randomness** [cite: 36]. Using Quantinuum's trapped-ion hardware, they generated cryptographic keys that are mathematically proven to be random—a feat impossible for classical deterministic computers. This has immediate utility in high-frequency trading, cryptography, and secure communications [cite: 37]. The randomness was verified by the Frontier supercomputer, confirming that the quantum output could not have been spoofed [cite: 38].

### GPS-Denied Navigation (Quantum Sensing)
**Q-CTRL** achieved a major milestone in April 2025 by demonstrating **quantum-assured navigation** on mobile platforms [cite: 39]. While distinct from computation, this application of quantum sensing allows vehicles to navigate without GPS by detecting minute variations in Earth's gravity and magnetic fields. In field trials, Q-CTRL's "Ironstone Opal" sensors outperformed conventional GPS backups by 50x, offering a jam-proof navigation solution for defense and maritime logistics [cite: 39, 40]. This is arguably the most "market-ready" quantum technology, with immediate defense contracts secured.

### Generative Quantum AI (GenQAI)
Quantinuum launched the **GenQAI** framework in 2025, which utilizes quantum computers to generate synthetic data for training classical AI models [cite: 41]. This hybrid approach addresses the "data scarcity" problem in fields like molecular discovery. By simulating quantum systems (e.g., hydrogen molecules) on the H2 and Helios processors, Quantinuum creates high-fidelity training datasets that improve the accuracy of classical AI models in predicting molecular behavior [cite: 42]. Partners like Merck and BMW are piloting this for drug discovery and materials science [cite: 11].

### Molecular Simulation and Chemistry
Google’s **Quantum Echoes** experiment on the Willow chip was verified against NMR experiments on molecules [cite: 1]. This demonstrated that quantum processors can now reliably predict the behavior of complex molecular interactions faster than classical supercomputers. While still in the research phase, this validates the hardware capability required for future drug discovery workflows. Similarly, **Goldman Sachs** and **Quantum Motion** developed quantum algorithms for pricing complex financial options, although widespread deployment awaits larger qubit counts [cite: 43].

## 5. Funding Trends and Industry Dynamics

### Capital Consolidation and Mega-Rounds
The financial landscape in 2025–2026 reflects a maturation of the market, with capital consolidating around proven "platform" winners.
*   **PsiQuantum** raised **$1 billion** (Series E) to build utility-scale facilities [cite: 20].
*   **Quantinuum** raised approximately **$300-$839 million** in late-stage funding [cite: 44, 45].
*   **QuEra** secured **$230 million** from investors including Google Quantum AI and SoftBank [cite: 14].
*   **Alice & Bob** raised **€100 million** ($104M) to advance cat qubits [cite: 46].
*   **Iceberg Quantum** emerged with a **$6 million** seed round for fault-tolerant architecture software [cite: 47].

Total global equity funding for quantum computing reached **$3.77 billion** in the first three quarters of 2025 alone, nearly triple the previous year's total [cite: 48].

### Geopolitical Shifts
A notable shift occurred in China's quantum sector. Tech giants **Alibaba** and **Baidu** exited the quantum hardware race in late 2024/early 2025, donating their labs to universities [cite: 49]. This signals a strategic pivot in China toward state-centralized development, with companies like **Origin Quantum** (delivering the "Wukong" computer) and government-backed entities leading the charge, rather than consumer internet firms [cite: 49]. Meanwhile, IBM and Google continue to drive the US ecosystem, with significant new government investments (e.g., the DOE Quantum Leadership Act of 2025) supporting infrastructure [cite: 50].

### Conclusion
By early 2026, the quantum computing industry has successfully navigated the "trough of disillusionment." The achievements of 2025—specifically Google's verifiable advantage, IonQ's four-nines fidelity, and the operational logical qubits from Microsoft/Atom and QuEra—provide the engineering validation required to justify the massive capital inflows. The focus has shifted definitively from asking *if* quantum computers can work to engineering *how* they can be scaled to fault tolerance, with hybrid quantum-classical applications providing the first bridge to commercial value.

**Sources:**
1. [theguardian.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFnV3PyzkmaxqGFNBcK8IJNQUulQh6tvf_2XlwjQt-tomGRe7Su2mt5k8S5kgZesipozUZdZ7WeuH7LOKgbOYytVwKaW4dItDvz21VNUsyZOKRGLARdciWsqPsQiTHfTmOZvC6zH0RQei3EenA5fRkT4QEgiZ59lsPLtlqM2p2LWWDzoHK68OJkVbd0HJ1zV9I2YB8o0Xvbck66ZthISeRd8vsZaqOjOpG5Qkws1E1dwcmhI_6wFBSOYNAL)
2. [techpowerup.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEsVGA9SNOWNnWDX9NUVTiYshgnro8yPR4HyURl9mVvC4ZvCD6R3ZZ-9BbalbmBjrmtzNVfj6H5D449WzoYiIy2Hng2gRHIpdmI3TDqkJIQCaCPCEsO6B1TAI7qdqA3vmk8ml9MAUdHuQtcLtuPyGBK98gy7QX1WI9jCOTfNQbSx2eMhpIRn9a80MlQmZB1qwzXKf7aEH9QPsFH3BiYx9HyIfRKwsawelZH348jvDnDqO-Hb84liobTlw==)
3. [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHytaJI3n0ajfZ6OaCXTqJoC5X0g9w-uVZ5dtPc5RL0kw-GXkgZw4110Ad9kGvstk_x_ndosNZ1WCpThxkLcltamk1qV6FLEOT46FjSyKIRXYOkgEPCrQ4rw0KcnlCtPdNe)
4. [wikipedia.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFhF_I_DM8Z3FwthPFRqqqCvLzQSC30YDQOQ9pxP5g6Yx4ZgKCwlFMeRzrkUZ_ma7l1lRaoJkV4N5fdbqP20IoltEHWiKiWVsZBa-ru81Lfvvsdt7ekeeOLI3DXPeX3qmnndt_h)
5. [postquantum.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFo3gH3ilrSTvoc1Y0IIxqrMKAXzD-s8ZhGkxiHjKxmqBCZyJ1zNSYMRVrL90SIE9-M-ipOSaNvGa8AtX-e4wflCvhf1jERi0a4D6VEet05GAviYWjo3_8AxZjtxB811sQOOswHXFc_cdtHdRQQg5A=)
6. [nextplatform.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGLzWLqHldMkzZJM4YsdeWfMyPeT2IszKdsjCJLNPE7UiofVaE_8ck74Bd8_1Buv47rLH8IZtu4242RioVVPx9M51FPmRLaFDdjBFEyNVl9eWQxcR4HuW3yN-p-vjXxuSUxF_Q0RfhDMCAR0iA74pevLecS5UTfioffCAaSuyuXToJ81gU5uBYv9Bvy-iep6L2bwI9F8eav5aWzizG-oQEYiC6N)
7. [postquantum.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQExF-xS89dQZxN3cA2sFemwnBlCK_fT9_tUFeAeNPCtfjIev_SsvkFOtV9W2sgorKCcJs6pzWN5fJcjTvEr6p-GXcebneuTWCl7afjd6ltK-_l36uRMig8bbBs3Sv14OIgCotwcPhLGEN4PQfocWIt1)
8. [oxionics.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHXL-vngqKQdt8EQgG4NrkdnDGmtZgjFdHL7Nzl2fSG1bbc4Z6G5G5qauh2F1QNJjikQYAMuk-NnnOpTczkd-hrj2TN93x0Y3x07wg6rWbUtqPznh8Rit5mKOyyVmiBBkD5anPeftfSRj4I-5TwPqFAdkuxDWp29vZlzS4HYSPgkxwjRES0KjYKu1R_xAiqdfz3aGrqD4PTYysjTLNmVGi2jHFxcnFtZm_XmwSfaFM5ooju_IUJ)
9. [oezratty.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEGWq9_UBxHwoj9lGYO4vaT-5TzoGypSMpc2TAaDvGxu_veSvExrX3aPilkGvK9OcQs4t_IkOBOUt-ZULgIIKFmEvoE8_i6uwVlvFm6fktgjrFkgNufzTzhTZol6BZ6Y9iiCoMa5de2-HNU1ZpCrbVebbXMNgLYn19k)
10. [postquantum.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQERXcdN06lAoMSohd_XOFRNHU403T19lwowsGH1lSwNTfu2hFDKthODMMMlnCbuMQawby_aYk6y_FVTFTdhH_7Hd2Pjl3QzQoYmn2LJuAtrwPI9A0mMzY9oTTTTdh_vNpJ3Bl3UJFUPDybj6Wwj-sk9dPz6muywDCVYPwWvwycW)
11. [quantinuum.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHs0p7FqA7SVfxS2bCj4XnsOqL2VE75gR1q4Ep_d7gC1zXtbKw154wpsujdKtWOqk77_VcVlpk-zU0qmkZ6yUVRGrTzv2KiHXqYPJdhUED1dfB9fS1ayPT1Ods6kkYrvh_x_BmyDPtJYlRGeqFVTKyVxq9cmmHAMgx8P_tAvivGZFnPKV0M97WguEHK-6d0EG7PcrE0G-GLQFK1sLyQij7aSiw4cPCXgtEEV02GdXiLIl6-Tmt1TJw6WMOv3LWxV1h2XrvHwEMIPoMMiEi22HcYjIilBblff-WudahJKfQWusLi3O2bkQDxAT8Jjsomeew=)
12. [quantumzeitgeist.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHRjADigcLJ8bIoHdHN9z2PrfNd2sC0ZL6HqqyAn18ASyFHzX_hg54iEey_zEEzAJjr2xzw_CAjsxHlIONuI5h1VtIcYhUQWzrq1t-q7pQpxFEVbz17S9vzWJ4dUNXD102IYYFU7RR8yxoPgdUdHRSobhC6q2W6YoIgNVoCdoA=)
13. [quera.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGKavAAth4e0mSapv0b4kNYONg-WRi-9Z5EqBLtA-CX0dbmCJttEpxOUf_btXzND_pcO_3rugcCqEc3aTLfUvA36lpVOON1fa8Ce3pMbLPuc8Fi)
14. [eenewseurope.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGLq-f9lWzuCmqUB2L-Yt-dclEaGHky6SJREqqU21cH-etInpP0j0nAPprB9BEZTeabm2Cj-L4ZKYT2d9o8mZoyOl-PE4YF0nD0OKG0_OeoZJQNvXHmwIg2_xfTfkaZBLQDap98fr5p3UVYiNOo0ykmvBGe-30VFsEjh7zUGPMHUzjF7kYMpKPX0CP1sY_E-89P8-FqFM5gJiwuPxAi4A==)
15. [substack.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE6p07QPDDGezB9_eZenvWCDUDAYhRD7F_4Nhmg7CJtvOsdEJunKH_L2EPdRNwMrnM4TpxXo0D04Bng0shnSupcmZkRiu94TuI8_P3gHorokXV-NwDaTfJY8vGqKRjQAs9TbdtqZdH81kayFLSXR_hcElSsACGg_ic2VZVnQ8w=)
16. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE47QIuzHagMWWESvjnB4ALphivJdbFLQJmovmotkfkmY_MZTx7o8k7Q8gbIdpCoryDntb8LGrawAnXj400n1pckWrL8d1bgQEcoA86een0L897eK53ovp7ohRVdT8kDehhaGRLPK0JL2D9fu9UL74MTrDQpbL2gBTVS9xrCRUVB8012_ER1_TiUtwFQxyDWDF8kF62fFfuaRje9exGidw9M-6Hfq5ns2VoeTetsajRvCBwY7B535jO3ZShQfFRYXonaOfTPVD8AoDF2YoU6afP2wk2GISQcM4NVd0wuMADOs7KH-A2QDbTeuQKz9cp7Q==)
17. [forbes.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGNU2dxFazeLLBbwzApKVzbrQTcemCdSf4fd9A7ezoay52yrA0TgJayZ_7eZeVHNu0hwI1XiBoeqYO-TdXYlKe4fKTVLHSLvsiOuq_KjDHyByUWuv6wVELP464AEW3-EMi5N93h1MgjVtZzz_V-7IDODUWEqCfMeh6Ua_xt7CgDZhepLmHf4iy0IZJvAOyVGmO7U2iJ4vMquDxht-0GZvGRCSxw_w==)
18. [quantumzeitgeist.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEGrqLJuPng9rGYgrPy07HEAPO-R5CjCVaeKwQ_0dIOQzTumUJ5zrm0gbvCG7jpvn1FT6s4zEoQF_JuX3d5qokkOBm1KX1YH8vVCCCwdG8eLx35iclvAfefc9surHTQ7zE3eFdwHkNzKiUkC_GX4eJ3EhkIQ0HfAprddsoGGXAtKACnsYag6oLZ76fsrOSeoNVDNzznZczPxV7uJubzuEziWAwtadz1-wIf)
19. [postquantum.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFqzEPi4FrRD5m-VJOfCsCKpkK_0yuyNJhJXYcTHlc0HG9RCPMCac2KkTrO75sciUT7i4ngPGxoV61PFbf34ccfqO-V9mrbDS29uqCnK4WgDd3_v-a4zrsJgLUHyucXvkWEuP8BRjZE6K7HkzlLC_Bi6YRKXOFrAg-l1iif9Q==)
20. [inc.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHz989qoiAbaDq5Z7TzZg7K6h0P9I-q4xlLpq2qrgASAhTJlopZG5uejrjNhruPT9cZEvrcIA3ZsKujmfkVGIF0YOzAX03U4fWodpRsdx7-vsWTMaaMPH1MkpZ1eAjMrSde0OrlfU5tT_H-147L9DYzMa0UvQkFOm0czrib5GclAdzWDMxSspgKaL9ootcD7bjMZbcaPnKHv8QluYwLj2cO3g9sJciEcjs=)
21. [psiquantum.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHjeuPi7CgiLR9D7yhsFpXpC_D40JrOCRV9zET_emQdiHf7ApONYjxOkCznnHt1T0bK62LUZSK7yK4yEgbsgI9kNhgTOPTaDvkg8FkRD5cdMoM=)
22. [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFOGuFvGe3oBWqGmGodvv9iugMtrNG9qsifuOxXVnADSlZ0JvoRGPq4o10GB4x6ddtlXsKd4qrWz757XkAGXNZs-Wy-ikcRq5kUsUJ9kQrj_4h2LITeAHIad9DVCrdfzENk)
23. [tomshardware.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHAOIeVnO4g_kkqxq4iLqdkS-bWpDy8cwvE_nWjsBWBiZHbY-cC56FHXWd7pilsQr-RpM4Juu42nGB6qwhmwn--jlm0OZtqvFqt18PlJuVALywuadY8EDNxQHGKOUN4Y1BWOAG4qvEOBHYez6tsTT5QsnurBg633VGFrhq3w24TJERrEgZ78csHyEIWTFmzsCEIFhJ6JNwgUaen2SEPIvWpaiooWLDE)
24. [livescience.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGMVH5QKqohinpUREKqCCOtBHSCjZD5d4slpjrxs_L_tX0Zog5r7erkSIbjBZ1AJT7z89Sk1qyc445kriV15zVNQkjC_5aF8m8-Dy_Pwd73GQh-_CDQDDj-K1n2P6g4Fr0BxhdySqU2NPNkkxHKiH-vPOxn3-9_E1ISXqJKAX0J6tFY-Z7c1kwcCHkqZQlXWo1_nP32mgmRYQaonSt5Lb6QsmXnc4mAIEAE_JxJoL8yzA_pDZoW8xMUGuD_X63-4Gcl9HKPElyTnWhbiWrzX9SHY4yBF8MlaiqJzeFBd_rmagI=)
25. [ionq.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGSJWKrerNz9oBGPZSqDfFbzICP9LG0dj6Pm5l8HOxM5bjlo-7jcxxeGVqOUgej3h7W_Oh80ShbOxQfts6vVVHj02sXNOe9vc95AyUwFczRqtfAw2dIoOZFlCMEKFWewcfRRyhPHMudSzajbwUN3NMCcrrxzanFEOxkaP96L7pKkcvJkE64FaYtYpA1ObRBCQ==)
26. [quantumcomputingreport.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQENUD0E9MYfSUsAdBR_Xmlm0a_36ogNevnvTit_uAOtw_cXUdhQhhIG6oepnaEAlhuasCNC_DFz8iRjdTuhA0s65oi4vMvo0NmvB-VQcI9JP_qVrDqO_fWkk3TX-6nkWZ3C56cA0zYTvdzCoNNVLcltGEuHF-khTfHO4wgFsCyvhw5auLKjWb-ZaABpc_msW9I6SZMlf_6R64VbCUVEG2AGEr-yZW2zR-16jKHcWh3y)
27. [postquantum.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEo7jaOnhclb4DQfqiPMOL4qd_QJqlzLnqXmQH5Pf-4BLhkon8PpGPWaLomt95Wth8ccWZQ0DBqQmpnrb9FVGzm9Hcq9rY5oOoPipyCVcvsuR-XU635aX138u4pb9-vmqkJgl4J6JQaI9wJeU-A)
28. [quantumcomputingreport.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF7nscjRDzLxWc0RcSe0OIpS6kbgfz52KYno5cAZjKjt_GdCmoyrEhp_mBDNozbU3B-yJ8vO1C8Pn1iuH6liTvW0VDEdvJ-8-XKAToI5HB-sh6B2yWZEqZ5UbcSSF0M2-gBe-4asEsGTuGZeEerZKhL87m3xFWtiVTfhbRmNhcurTUtBosXSBGl-3nFDoHpXDMQh9PbkNaIzBlduuKF6bVGGqp5dhrRY9g24vPd6EeERDHI0ggIxs0_Ph8_iyjT1A==)
29. [substack.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE_X3_ZwZFSoBiO_unWrIRhzhlLNJZoD-UfrEAvUBIxVxLpLj35BdQqX1qre5J3GL-xp3TTqIB_P4_l-AlCgjNnVW_ioo-jSSiAroactNHIUkSkhmYjKOMjyGtOZVxA3u4bfc4idTz9IOdIK9JTbO34VET31BNI)
30. [quera.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGOteVV2U5YWDBmVc3qiBwE7-2Mo3uWouzWXNDTc_ZrBKNN6hIN3T-GFnnaPyEhz4ibrftppAARy9jzlQCFNd2jgiktAMX2Umfree50RGG0d-bg6RGEn5LoEqJFRdl0FGcOpyk_aCB0ppfrh6VTCNhEL-KeJjT3tLWhMktlECb8fIyqu-L79hFUO5tX0ADc0KbP9ZLjaUdP-weg6d59A11BwSp4)
31. [coingeek.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEmb5cNFYlfU9eFGBRKKNorH-stdWUGe6SOzxQTmGU1itoG4vedFzJWLEizoVidavBCEN6PfqbW9uepkkWN-TSogEqu7UnMmIkzUtP1zy5XpOSl2hDRwFBTwHhmTdL4HI_X1i55LlKuBGWP6yRgdWgf1zZ096Z16KGY9sL5X4xT6vbxEjpCJIikd2c=)
32. [quera.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG3cwtkwcW0zJ2K-odRBYU1aRRfhWYmxJKj79bnPUU3CN-yC8pEvGgvhmzRUtxNiQNFIYY_YrBNQ4_DXAGUriaKiJi3evWPSN4XGB0dqPKCJJ0mYOB69tDeLgCXEfys3xjMC88WdoPtNVY78sv77KvnPqrEQXXzwfSrNIzqr_9aqri0vzzIedAqS7CYnkU4ozZn9GCKbiVBfIx_htGGM8BMYe74CFf99GR3_KSUOhuFiLHmLknh2nPeDyZfZ9xtIJA7_8jkKSLBy1Osd_e21cUOca2fHXeB7yLQGZrAmw==)
33. [prnewswire.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH3ib4ftDsQRKhfHfgcy-4A6SumALP3IF3bgseMNtHD2r__px_QT3M1YWoSCHdEhot_avSw29deTmqsAv1ESuELpioTcgDb5D_0UNg6iqJZgms6jlfO17HbSYf5GP1J8aob7NgHqitzLEgo12WmRlaVGi1f_fCXdG1mO8zYGA070_XQL8QCzYiQumCoKCt3r3d11lKnH7x3HIXx_AU_ESF84lGP9rs2PkUqw1BLFcexg-pGWHnr-xt1ghSJthVa_QksRd0Aq38EGmmGGHx0vlt1Sb370emX2jrx4wzUWdU5sOCvBbteGYSac0oyrQn2D9w=)
34. [alice-bob.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHo8SRxFnVMLRvIq6uny1rXadPbA7FuHyhdIf-aa4aCVsDA4RbYLX5QgqoJb3el2s-Dr530WFPnTMioBmIvKBv403GJDlLQwLLMebdLNZaQXckjnToNE1m2xT2nvV6WHu51pWeBtnxPvxWTJwGbQVp0_OGFBvEs1vFuOSkFZYMFD0YeMg==)
35. [quantumcomputingreport.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHmfG5Sxsp-TOjv7ktM86v866hC--KE8S4YWw9LS0_EPFYiMBFRw4xHjgLTDNNGTHaLoG637ONOD6MMCnV44wbPfVjr_CPSFyqDzwuN-wfqjl149H45HzO6yxnIK244j3bdJ488dfRtYv264fg-lSm99fZpBokpdb31mLe0aQFwlArqPfBN1X_xn0Htwj28KkXZdyGuor5RVBcXSPACZmFK8QF5YLdmnSQTriYGJ1do5N8=)
36. [marketsmedia.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH6aOeERSgzbePd37CkQ4SoTnYJQqBDzsOX4HPM0ohuM8Q15QHCmj8PJPW3j_Oy61QgV_BdDJFA4Y1gYjRlXfhfu-UdD1I1vpo7cMsL3bcXab4alfcj8x7zGRU8tjwmm92PgrABPr8xXlpMSQElzEzVWlULj6gQ02PtgpdTc1VdhibVN9zAVojyPlKq)
37. [jpmorganchase.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEVwRQho1FzKirtWlnedODHjVaJjUtyQk_Xl2f5ro70AyrflV-AJ9SkjizH3r91QAr7FHAPoVnGHti_WrpSV-bR8I7AkHeK96qvkJP4exmriyRyFfDo2B3mXZcQhpHKHsaTTs4MgRlLq3iFc0_aSdr9cUOlW7WyBSpJIT3_0og=)
38. [scottaaronson.blog](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGWQUg8PJ2Ly0z_Lk4xwYgjKXZFUcOj-dXi8dvOq20-9WQsMxH0S7QhdPVy-syAKaijx9iv_8oX-Yj_5VKZTduy65AsigeHfo67R2iKZohqe7SqdfWh0wyd)
39. [q-ctrl.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5lk62kP9J9w6NSGX687_X0jRMPulCsEJhrJNoRzynvlrcgO9xNVKRlLhf9_hgQsEAecKqdCiUn-8ymXXEJGVCRJ0dEtkXkNRNUl5-9xF5lftPAXwDdzG361tWnhJocifCeeY9ZXuusbLEBAbe0AiA4V7P72CbBMWKFPMwl45HK8Vt2x7EJU8wFEbzntja_1SlFa9A5HJweCM=)
40. [fiercesensors.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHLmGbyfcNhG8lGAFhF1CbaXg3bwFnomR7HSoIroHhwQCUXLuBtwKmVcI50pxyU-1KVarquDgzeAowtaJ8jq6WjPGvB8GUv33qouDSfLFko1PNQSSGxSZt03oMAEqEflyl1Yg1Qqdh31Gim3J6nTqmy8611lLOdCt719PrjgEOcQuHq-RwSOl9ZcrBBqDw1GF96LvzG7CNGQg==)
41. [prnewswire.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHa3MzlJOpIWyTKLDwgVMXO5Yog_GwfLwAqXNJG5CsVvBCBcrmTpbmq1xFzHm_B9xdEv_O6FFIQEkV6cIeB3xN_jswCnh_eWt-IsSYWw0gzahWAlwXSc0JehrzQ2OKEBQzeJNC8S9KJiFcj4neonLPny6886H-9PHlZws4Q7DLb7I02IbfvRVuDD0AfXl0BufMFLcoVejMj_diH4RwVcURg_BsFaUDNWj_yB0a9CcgfHt61-XKfsxf8wlHrI4kodqc7IE66OY_WcoOLtA==)
42. [quantumcomputingreport.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHPuIxBTqQlDlNy6dbhAc4EzUNtTPsfbd7mG-s4UiUcesQdgZg_aOYIgIwbJXLwwNtE29K76PZc-p_HkPT4vltyQqBhRtApXoLLDUJvzX1llsz-CHVHqMICuCHGEj9vQ58wG3YYQMfZrOchdTujgfyy7u_HXjAnruBfA_bvuFXNCNL1nV592VdBy2J1X4_xbSHnSEQMyp5t6SNmxS93Ft6_dLWxBSQ4pHo=)
43. [iotworldtoday.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEgFGDcdhtoUpv3W3qAC8Dnn1Ias5WKbP5k-b47wt-Ng7HSnjDGMwRXhOCmMAZZhBnFwKk6MOwxzvfLxHcsKw6Zb5vCuMFgX5wgpOtL8Y0qVo2nuAzo2zzybNZDEN96p-YJjw02yEZ9QMVL4JmFWWrrJy7JlCWLcUcw8eZMfXGkisUo48mZ8chSY_yODxmDw6LcbhXMS0kgorkCEA==)
44. [crispidea.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEVqDLT-Jv2EbwrQCTMJvPFiRVmvENGV89gL4UfafINjP2Q78a7h5tenux3FIQl3pI4bwnuuAsMfGBoHSdGhQ4urn8aRnqaEu6JRBLccPAbkdW0emUQUG07T3Q7imlGTME0OkUmxybpdW-fS2JW8Lu2Nu7_RE5xGTo=)
45. [tracxn.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGS15t7IBU6AV-CRySSMcGE2NBCw9ZeWGSLpBTJGC49tmD0fbDynsADZtWAj3Vc4zuMAcl3hqE-4Rv5ftRQfRZ3qcodv2xOzAYe97BEjoONeCEatOl4GL2IT8y0LF-NfWAjJqPqMZwDqndRPXATqg7Ib18uo2Qj7QA=)
46. [eutechfuture.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQETGvMKjjBfbm0DNbBzF3b8GhejA1WfaAicaYx7tU7NvomQzDff5d72fJOZH1ikXpnBR0CiulbNmTtXJ8sS7KZMJE0ZUuSII42gXOrubLIV9DYRyXipDLSM1i3aVt4wqhYrwHHj9P1dJHJD_jbvrtg3NJtGF-5ePej5soeVZmtsrlVQOrpZ5u-uyOBKb2_Y8eA1taSPAmEGmOh4WC4G6leSTXckqvablrFtlkZ-ow==)
47. [medianet.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHSbl90Uz2tblYcx-3IrN-zV8V6kbtKZ4vztcbusM2ZnAv41BD6GNQf9Mz-7XAhHq6RuHTBpqrKHFBcHZ3yL82DZ0k5C0T1jOLhqlu_8RDJAXewY0QVRObh0QYcQR1GvsI4g_FsKWGEz-cykyWbkS6fMjvPxBggeSz4qDQhFEESbuiH2hHAHP4Tc-0AxUhDtAnhw0sQdRXElaQvMCKV3cdx4fxkKM8a9MOBozderjI=)
48. [networkworld.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE73G9giocC6rpDq5kvjH7IusDFyQG5p1i1_kIuLt6j845hGNbFvXOwzLovYhDUV0RBy3qeb_k3UoT3RW3tZFwbf_-tqX9UGEBdT_s_oyts-htQAZ1h45tEOpplUY1r8uHgKWsEjRpUHHmtK2rfXJfIJIJn0KX1aBELWol4DLcZPPbEmQlIOf-1vA==)
49. [fanaticalfuturist.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEeKD1Li68W20Ab8UmSdB8eBCcCk6BDwIyLb2YbGCeRCF0W11BksGgMUZODLJXzWW74BUcRMmnWCenl4OStuPS9VfRep-FltK4f4ShvSG_EIPC4OTpGAj8IQ8EtwcaJnAb4W4NRBFq1rvh5cBdJ9R1XWh0d4KwIcLC7n0TDxQdJcHJRZThTc70O3UHlsx4N4l5qI3iPEb6B3bQyPWPqKbDQK7BfHQ==)
50. [spinquanta.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEgOQkrDgz9U04mDV3QpaG1zDTHu6-NsrHW9UzStAm1espW9qg-A7Mbd2ni0HXtl0CT7GMWXUxmnt5_4Rg_2tsiBRnnvvj8bBlMKiH_Zs7a9Ywe5m9OWwbYjOT-3bV5efzCSOvg_ey3UGgtMTRiivo4xZiX2y2VuJqvGJfnceM6zd7fG1GCPAWJweWNKdjhc9Pklyd1s2L3ROa1059-eeKavw==)
