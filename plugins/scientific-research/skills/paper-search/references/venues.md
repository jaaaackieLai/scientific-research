# Acceptable journals and conferences

Only journals and conferences on this list are accepted. Anything not on the list is rejected, placed in the eliminated table, and noted as "venue not on the list".

## ML / AI
| Abbreviation | Full name | Type |
|---|---|---|
| NeurIPS | Conference on Neural Information Processing Systems | Conference |
| ICML | International Conference on Machine Learning | Conference |
| ICLR | International Conference on Learning Representations | Conference |
| AAAI | AAAI Conference on Artificial Intelligence | Conference |
| IJCAI | International Joint Conference on Artificial Intelligence | Conference |
| TPAMI | IEEE Transactions on Pattern Analysis and Machine Intelligence | Journal |
| TNNLS | IEEE Transactions on Neural Networks and Learning Systems | Journal |
| BigData | IEEE International Conference on Big Data | Conference |

## Security
| Abbreviation | Full name | Type |
|---|---|---|
| CCS | ACM Conference on Computer and Communications Security | Conference |
| NDSS | Network and Distributed System Security Symposium | Conference |
| S&P | IEEE Symposium on Security and Privacy | Conference |
| USENIX Security | USENIX Security Symposium | Conference |
| TDSC | IEEE Transactions on Dependable and Secure Computing | Journal |
| TIFS | IEEE Transactions on Information Forensics and Security | Journal |
| RAID | International Symposium on Research in Attacks, Intrusions and Defenses | Conference |

## Computer Vision
| Abbreviation | Full name | Type |
|---|---|---|
| ICCV | International Conference on Computer Vision | Conference |
| CVPR | Conference on Computer Vision and Pattern Recognition | Conference |
| ECCV | European Conference on Computer Vision | Conference |
| WACV | IEEE/CVF Winter Conference on Applications of Computer Vision | Conference |

## NLP
| Abbreviation | Full name | Type |
|---|---|---|
| ACL | Annual Meeting of the Association for Computational Linguistics | Conference |
| EMNLP | Conference on Empirical Methods in Natural Language Processing | Conference |
| NAACL | Annual Conference of the North American Chapter of the ACL | Conference |
| COLING | International Conference on Computational Linguistics | Conference |
| EACL | Conference of the European Chapter of the ACL | Conference |
| TACL | Transactions of the Association for Computational Linguistics | Journal |

## Graphics & Multimedia
| Abbreviation | Full name | Type |
|---|---|---|
| ACM MM | ACM International Conference on Multimedia | Conference |
| SIGGRAPH | ACM SIGGRAPH Conference | Conference |

## Medical
| Abbreviation | Full name | Type |
|---|---|---|
| TMI | IEEE Transactions on Medical Imaging | Journal |

## Agent
| Abbreviation | Full name | Type |
|---|---|---|
| AAMAS | International Conference on Autonomous Agents and Multiagent Systems | Conference |

## Data Mining
| Abbreviation | Full name | Type |
|---|---|---|
| KDD | ACM SIGKDD Conference on Knowledge Discovery and Data Mining | Conference |
| SDM | SIAM International Conference on Data Mining | Conference |

## Others
| Abbreviation | Full name | Type |
|---|---|---|
| WWW | The ACM Web Conference | Conference |
| KBS | Knowledge-Based Systems | Journal |

## Matching rules
- Only the main conference and the main journal count. Workshops, findings (e.g. Findings of ACL), and demo tracks of the same conference are not on the list.
- When a conference is renamed, the old name also counts, e.g. WWW was formerly the International World Wide Web Conference.
- The tables are read directly by `scripts/match.py`. When adding entries, write names in the table format; if there are other common spellings or easily confused similar names, add them to `aliases.json` (the key must be exactly the same as the name in the table).

## arXiv rules
1. First check whether there is a formally published version (see SKILL.md step 2). If so, match the formal version's journal or conference against this list.
2. No formal version:
   - Survey: acceptable only with citations ≥ 100
   - Non-survey: the authors must be academic authorities (defined in SKILL.md)
