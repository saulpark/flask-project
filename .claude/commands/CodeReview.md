---
allowed-tools: Read(*), Write(*)
description: Perform code review of the code base
---

Mode $ARGUMENTS

If Mode is one of the following, adjust the review as described:

MODE == BUGS: Focus ONLY on logical or other bugs.

MODE == SECURITY: Focus ONLY on security issues.

MODE = PERFORMANCE: Focus ONLY performance issues.

MODE can also be set to a combination like "BUGS,SECURITY" etc => Perform the combined review in that case.

If MODE is set to anything else or nothing at all, perform a thorough, general code review.

Perform an in-depth code review of the entire codebase.

Carefully and thoroughly explore the codebase file-by-file to find potential issues and improvements.

Don't rush it, instead make sure you fully understand the code structure and architecture.

Update the results on the AUDIT.md file also updating it if any of the present issues is already resolved. Also, create a AUDIT_LOG.md file log where a summary of the issues created and solved on the AUDIT.md with the DATE of solution and the git user that pushed the solution to the issue.