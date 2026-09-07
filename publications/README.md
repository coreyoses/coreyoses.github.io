# Publication PDFs: what may be published, and what may not

Generated 2026-09-07 from the `open_access` field in
`data/publications_journal.json` and `data/publications_book.json`, which was
checked against Unpaywall on 2026-09-06. Regenerate with
`python3 functions/open_access_pdfs.py` (no arguments prints the publishable
names) if that field changes.

**This directory is the private full set. Keep every file here.** The rule below
governs only what leaves it: `make web-push` and `Makefile.s4e` run
`functions/open_access_pdfs.py --prune` on the *copies* they publish, never on
this directory.

## Publisher PDF, may be published (24)

Gold or hybrid open access. The published version of record carries a licence
(usually CC BY) that permits redistribution.

- `10.1016_j.actamat.2024.120117.pdf` : Fermi energy engineering of enhanced plasticity in high-entropy carbid
- `10.1021_cm503507h.pdf` : Materials Cartography: Representing and Mining Materials Space Using S
- `10.1021_prechem.5c00467.pdf` : Stabilizing Iodine in Pyrochlore: Toward New Nuclear Waste Forms
- `10.1038_ncomms15679.pdf` : Universal Fragment Descriptors for Predicting Properties of Inorganic 
- `10.1038_s41467-018-07160-7.pdf` : High-entropy high-hardness metal carbides discovered by entropy descri
- `10.1038_s41467-020-19597-w.pdf` : On-the-fly Closed-loop Autonomous Materials Discovery via Bayesian Act
- `10.1038_s41467-021-25979-5.pdf` : Settling the matter of the role of vibrations in the stability of high
- `10.1038_s41467-022-33497-1.pdf` : Plasmonic high-entropy carbides
- `10.1038_s41467-024-46753-3.pdf` : Materials Design for Hypersonics
- `10.1038_s41524-018-0085-8.pdf` : Machine learning modeling of superconducting critical temperature
- `10.1038_s41524-019-0192-1.pdf` : Coordination corrected <i>ab initio</i> formation enthalpies
- `10.1038_s41524-019-0206-z.pdf` : Unavoidable disorder and entropy in multi-component systems
- `10.1038_s41524-019-0226-8.pdf` : Predicting Superhard Materials via a Machine Learning Informed Evoluti
- `10.1038_s41524-020-0317-6.pdf` : Discovery of novel high-entropy ceramics via machine learning
- `10.1038_s41524-025-01594-6.pdf` : High entropy powering green energy: hydrogen, batteries, electronics, 
- `10.1038_s41586-023-06786-y.pdf` : Disordered enthalpy-entropy descriptor for high-entropy ceramics disco
- `10.1038_s41597-021-00974-z.pdf` : OPTIMADE: an API for exchanging materials data
- `10.1039_D4DD00039K.pdf` : Developments and applications of the OPTIMADE API for materials discov
- `10.1039_D5MH00356C.pdf` : Beyond the four core effects: revisiting thermoelectrics with a high-e
- `10.1088_2399-1984_ae19b0.pdf` : The search for high-entropy fuel-cell catalysts using disorder descrip
- `10.1088_2516-1075_ac572f.pdf` : Roadmap on Machine Learning in Electronic Structure
- `10.1103_PhysRevX.6.041061.pdf` : High-Throughput Computation of Thermal Conductivity of High-Temperatur
- `10.1126_sciadv.1602241.pdf` : Accelerated Discovery of New Magnets in the Heusler Alloy Family
- `10.3389_fphy.2022.815863.pdf` : Physics in the Machine: Integrating Physical Knowledge in Autonomous P

## Publisher PDF, may NOT be published (28)

Closed access. The version of record is the publisher's; hosting it publicly
would infringe. The public CV says these are available by email, which is the
normal and accepted practice.

- `10.1002_9783527802265.ch7.pdf` : Automated computation of materials properties  [arXiv 1805.05309]
- `10.1002_adma.202102904.pdf` : Entropy Landscaping of High-Entropy Carbides  [no arXiv version]
- `10.1002_anie.202205129.pdf` : The Microscopic Diamond Anvil Cell: Stabilization of Superhard, Superc  [arXiv 2204.03231]
- `10.1007_978-3-319-42913-7_63-2.pdf` : The AFLOW Fleet for Materials Discovery  [arXiv 1712.00422]
- `10.1007_978-3-319-50257-1_108-1.pdf` : Machine learning and high-throughput approaches to magnetism  [no arXiv version]
- `10.1016_j.actamat.2016.09.017.pdf` : A Computational High-Throughput Search for New Ternary Superalloys  [arXiv 1603.05967]
- `10.1016_j.actamat.2019.07.008.pdf` : Metallic glasses for biodegradable implants  [arXiv 1902.00485]
- `10.1016_j.actamat.2021.117051.pdf` : Carbon Stoichiometry and Mechanical Properties of High Entropy Carbide  [no arXiv version]
- `10.1016_j.actamat.2022.118594.pdf` : QH-POCC: taming tiling entropy in thermal expansion calculations of di  [arXiv 2212.00919]
- `10.1016_j.commatsci.2015.07.019.pdf` : The AFLOW Standard for High-Throughput Materials Science Calculations  [arXiv 1506.00303]
- `10.1016_j.commatsci.2017.04.036.pdf` : AFLUX: The LUX materials search API for the AFLOW data repositories  [arXiv 1612.05130]
- `10.1016_j.commatsci.2018.03.075.pdf` : AFLOW-ML: A RESTful API for machine-learning prediction of materials p  [arXiv 1711.10744]
- `10.1016_j.commatsci.2021.110450.pdf` : The AFLOW Library of Crystallographic Prototypes: Part 3  [arXiv 2012.05961]
- `10.1016_j.commatsci.2022.111808.pdf` : aflow.org: a web ecosystem of databases, software and tools  [arXiv 2207.09842]
- `10.1016_j.commatsci.2022.111889.pdf` : None  [arXiv 2208.03052]
- `10.1016_j.mtla.2023.101682.pdf` : Influence of Processing on the Microstructural Evolution and Multiscal  [no arXiv version]
- `10.1021_acs.chemmater.6b01449.pdf` : Modeling Off-Stoichiometry Materials with a High-Throughput Ab-Initio   [arXiv 1511.04373]
- `10.1021_acs.inorgchem.7b02462.pdf` : The structure and composition statistics of 6A binary and ternary stru  [arXiv 1703.04497]
- `10.1021_acs.jcim.8b00393.pdf` : AFLOW-CHULL: Cloud-oriented platform for autonomous phase stability an  [arXiv 1806.06901]
- `10.1021_jacs.4c11753.pdf` : Atomic Ordering-Induced Ensemble Variation in Alloys Governs Electroca  [no arXiv version]
- `10.1038_s41578-019-0170-8.pdf` : High-entropy ceramics  [no arXiv version]
- `10.1103_PhysRevMaterials.1.015401.pdf` : Combining the AFLOW GIBBS and elastic libraries to efficiently and rob  [arXiv 1611.05714]
- `10.1103_PhysRevMaterials.3.073801.pdf` : AFLOW-QHA3P: Robust and automated method to compute thermodynamic prop  [arXiv 1807.04669]
- `10.1103_PhysRevMaterials.5.043803.pdf` : Automated coordination corrected enthalpies with AFLOW-CCE  [arXiv 2101.02724]
- `10.1103_PhysRevMaterials.5.083608.pdf` : Tin-pest problem as a test of density functionals using high-throughpu  [arXiv 2010.07168]
- `10.1107_S2053273318003066.pdf` : AFLOW-SYM: platform for the complete, automatic and self-consistent sy  [arXiv 1802.07977]
- `10.1557_mrs.2018.207.pdf` : Data-driven design of inorganic materials with the Automatic Flow Fram  [arXiv 1803.05035]
- `10.1557_s43577-022-00281-x.pdf` : High-entropy ceramics: Propelling applications through disorder  [arXiv 2111.11519]

## arXiv preprints, may be published (3)

The author's own version, already public on arXiv. These are what the public CV
links as "PDF" for the closed articles that have one.

- `2207.09842.pdf` : aflow.org: a web ecosystem of databases, software and tools
- `2208.03052.pdf` : None
- `2212.00919.pdf` : QH-POCC: taming tiling entropy in thermal expansion calculations of di

## Files not covered by the lists above

- `10.1016_j.mtla.2023.101682_PRESS.pdf` : the in-press proof of the Materialia
  paper, kept for the record. Not publishable; the published version is listed
  above under its own DOI.

## The three copies, and which one counts

- **This directory** is the private full set (56 PDFs; 55 tracked in git, the
  2021 Comput. Mater. Sci. file is deliberately ignored because of its size).
- `output/s4e/src/media/publications/` is a working copy that `Makefile.s4e`
  rebuilds: it rsyncs the PDFs in, renders the PNG snapshots, then prunes the
  closed-access PDFs so only the publishable subset remains. Treat it as
  transient. Its PNGs are what `make web` copies back here for the CV's
  recent-papers strip.
- `entropy4energy.github.io/src/media/publications/` is what is actually live:
  open-access articles and arXiv preprints only.
