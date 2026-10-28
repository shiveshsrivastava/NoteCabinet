# Abstention threshold tuning (dev split, 10 questions, 2 unanswerable)

Retriever: `hybrid+rerank`. Chosen threshold: **0.0101** (9/10 correct abstain/answer decisions; any value in [0.0000, 0.0202) behaves the same on dev).

| threshold interval | correct decisions |
|---|---|
| [0.0000, 0.0202) | 9/10 (90%) |
| [0.0202, 0.0410) | 8/10 (80%) |
| [0.0410, 0.3209) | 7/10 (70%) |
| [0.3209, 0.5514) | 6/10 (60%) |
| [0.5514, 0.5552) | 7/10 (70%) |
| [0.5552, 0.6832) | 7/10 (70%) |
| [0.6832, 0.8215) | 6/10 (60%) |
| [0.8215, 0.8439) | 5/10 (50%) |
| [0.8439, 0.9176) | 4/10 (40%) |
| [0.9176, 0.9693) | 3/10 (30%) |
| [0.9693, 1.0000) | 2/10 (20%) |

| id | type | top rerank score | model abstained | source note in top 5 |
|---|---|---|---|---|
| q002 | single | 0.844 | False | True |
| q013 | single | 0.683 | False | True |
| q014 | single | 0.821 | False | True |
| q025 | multi | 0.918 | False | True |
| q029 | multi | 0.321 | False | True |
| q041 | temporal | 0.020 | False | True |
| q042 | temporal | 0.041 | False | True |
| q047 | shorthand | 0.969 | False | True |
| q055 | unanswerable | 0.551 | False | n/a |
| q057 | unanswerable | 0.555 | True | n/a |
