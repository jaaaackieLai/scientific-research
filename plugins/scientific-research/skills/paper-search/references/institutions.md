# Acceptable universities and companies

Ranking source: QS World University Rankings 2027 (published 2026-06-18), taken from official data on topuniversities.com.
`=` means tied rank. Companies and non-university research institutes have no QS ranking and are marked `-`.

| Country/Region | University/Company | QS 2027 |
|---|---|---|
| USA | Massachusetts Institute of Technology (MIT) | 1 |
| USA | Stanford University | =2 |
| USA | Harvard University | 5 |
| USA | California Institute of Technology (Caltech) | 7 |
| USA | University of Pennsylvania (UPenn) | 15 |
| USA | Cornell University | =16 |
| USA | University of Chicago | 24 |
| USA | University of California, Berkeley | =20 |
| USA | Princeton University | 27 |
| USA | Columbia University | =43 |
| USA | University of California, Los Angeles (UCLA) | 49 |
| USA | University of Michigan-Ann Arbor | 51 |
| USA | Carnegie Mellon University | 55 |
| USA | New York University (NYU) | 58 |
| USA | University of Texas at Austin | 72 |
| USA | University of Illinois Urbana-Champaign (UIUC) | 74 |
| USA | University of California, San Diego (UCSD) | 81 |
| USA | University of Washington | =92 |
| USA | Purdue University | =100 |
| USA | Georgia Institute of Technology | =142 |
| USA | University of Southern California (USC) | 153 |
| USA | University of North Carolina at Chapel Hill (UNC) | =158 |
| USA | Michigan State University | 182 |
| USA | EleutherAI [research institute] | - |
| UK | Imperial College London | =2 |
| UK | University of Oxford | 4 |
| UK | University of Cambridge | 6 |
| UK | University College London (UCL) | =8 |
| UK | The University of Edinburgh | 35 |
| UK | Apollo Research [research institute] | - |
| Switzerland | ETH Zurich | =8 |
| Switzerland | EPFL | =22 |
| Singapore | National University of Singapore (NUS) | 10 |
| Singapore | Nanyang Technological University (NTU Singapore) | 12 |
| Hong Kong | The University of Hong Kong (HKU) | 11 |
| Hong Kong | The Chinese University of Hong Kong (CUHK) | 18 |
| Hong Kong | The Hong Kong University of Science and Technology (HKUST) | 33 |
| Mainland China | Peking University | 13 |
| Mainland China | Tsinghua University | 14 |
| Mainland China | Fudan University | 26 |
| Mainland China | Shanghai Jiao Tong University | 36 |
| Mainland China | Zhejiang University | 47 |
| Mainland China | University of Chinese Academy of Sciences (UCAS) | =360 |
| Germany | Technical University of Munich | 25 |
| Germany | Ludwig-Maximilians-Universität München (LMU) | 61 |
| Germany | Eberhard Karls Universität Tübingen | =230 |
| Germany | Technical University of Darmstadt | 250 |
| Germany | Max Planck Institute [research institute] | - |
| Canada | McGill University | 30 |
| Canada | University of Toronto | 32 |
| Canada | Université de Montréal | =162 |
| Canada | Mila [research institute, a collaboration of McGill and Université de Montréal] | - |
| France | Université PSL [includes ENS Paris] | 34 |
| France | INRIA [research institute] | - |
| Poland | IDEAS NCBR [research institute] | - |
| South Korea | Seoul National University | 38 |
| South Korea | KAIST | 65 |
| Japan | The University of Tokyo | 39 |
| Japan | Kyoto University | 64 |
| Taiwan | National Taiwan University (NTU) | 54 |
| Taiwan | National Tsing Hua University (NTHU) | =142 |
| Taiwan | National Yang Ming Chiao Tung University (NYCU) | =177 |
| Netherlands | University of Amsterdam | 60 |
| Australia | The University of Sydney | 28 |
| Australia | Australian National University (ANU) | 29 |
| Australia | Monash University | 31 |
| USA | Google DeepMind / Google Research | - |
| USA | Meta AI (FAIR) | - |
| USA | Microsoft Research | - |
| USA | OpenAI | - |
| USA | Anthropic | - |
| USA | NVIDIA Research | - |
| USA | Amazon Science | - |
| USA | Apple Machine Learning Research | - |
| USA | Adobe Research | - |
| Mainland China | ByteDance | - |
| Mainland China | Alibaba DAMO Academy | - |
| Mainland China | Tencent AI Lab | - |

## Matching rules
- Look at all institutions listed in the paper's author block; it passes if any one is in the table (companies and research institutes count too).
- When an institution name does not match (e.g. only a department or lab name is given), look up the university it belongs to.
- None of the authors' institutions are in the table → eliminated directly (SKILL.md threshold G4).
- The table is read directly by `scripts/match.py`. When adding entries, write names in the table format; if there are other common spellings or easily confused similar names, add them to `aliases.json` (the key must be exactly the same as the name in the table).
