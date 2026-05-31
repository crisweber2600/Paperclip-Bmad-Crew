"""CLI for ZIP intake manifest and listing-intelligence workflow generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .intake import WorkflowEvidencePaths, build_asset_manifest, run_listing_intelligence_workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Build asset manifest v0 or final listing-intelligence record")
    parser.add_argument("--working-root", required=True, help="isolated output root for working copies and manifest")
    parser.add_argument("--intake-id", default=None, help="optional intake correlation id")
    parser.add_argument("--paperclip-issue-id", default=None)
    parser.add_argument("--paperclip-issue-identifier", default=None)
    parser.add_argument("--workflow", action="store_true", help="run full deterministic listing-intelligence workflow")
    parser.add_argument("--db-path", type=Path, default=None, help="SQLite path for final workflow persistence")
    parser.add_argument("--visual-analysis", type=Path, default=None, help="visual-analysis evidence JSON path")
    parser.add_argument("--marketplace-copy", type=Path, default=None, help="marketplace-copy evidence JSON path")
    parser.add_argument("--technical-estimate", type=Path, default=None, help="H2C technical-estimate evidence JSON path")
    parser.add_argument("zip_paths", nargs="+", help="source ZIP paths; opened read-only")
    args = parser.parse_args()

    if args.workflow:
        if not all([args.visual_analysis, args.marketplace_copy, args.technical_estimate]):
            parser.error("--workflow requires --visual-analysis, --marketplace-copy, and --technical-estimate")
        result = run_listing_intelligence_workflow(
            [Path(p) for p in args.zip_paths],
            Path(args.working_root),
            db_path=args.db_path,
            intake_id=args.intake_id,
            paperclip_issue_id=args.paperclip_issue_id,
            paperclip_issue_identifier=args.paperclip_issue_identifier,
            evidence_paths=WorkflowEvidencePaths(
                visual_analysis=args.visual_analysis,
                marketplace_copy=args.marketplace_copy,
                technical_estimate=args.technical_estimate,
            ),
        )
    else:
        result = build_asset_manifest(
            [Path(p) for p in args.zip_paths],
            Path(args.working_root),
            intake_id=args.intake_id,
            paperclip_issue_id=args.paperclip_issue_id,
            paperclip_issue_identifier=args.paperclip_issue_identifier,
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
