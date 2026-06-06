# SEO Audit Skill

Master orchestrator. Runs the full pipeline in order.

## Steps
1. Run extract agent: load CSV, detect all issues, save to outputs/issues.json
2. Run analyse agent: score and prioritize issues, generate recommendations
3. Run report agent: rewrite titles/metas, output HTML + PDF + PPTX
