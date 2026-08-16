# FMEA

RPN = Severity × Occurrence × Detection

| Process | Failure Mode | Effect | Cause | Control | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---:|---:|---:|---:|---|
| Add book | Duplicate ISBN | Duplicate catalog entry | Repeated entry | UNIQUE constraint + validation | 7 | 4 | 3 | 84 | Prevent before insert |
| Issue | Unavailable book | Incorrect inventory | No copy available | Availability check | 9 | 3 | 2 | 54 | Block issue |
| Return | Repeat return | Inventory over-count | Duplicate action | Transaction status check | 8 | 3 | 2 | 48 | Block repeat return |
| Form entry | Invalid data | Bad record | User input | Poka-Yoke validation | 6 | 5 | 2 | 60 | Validate at source |
| Application | Unexpected exception | Operation failure | Runtime/database issue | Central error handler | 8 | 3 | 4 | 96 | Log + recover |
