# import asyncio
# import logging
# import json
# from pathlib import Path
# from src.pipelines.orchestrator import run_pipeline

# logger = logging.getLogger(__name__)

# async def main():
#     logger.info(" Starting GOQii multi-agent pipeline...")

#     # Run pipeline
#     results = await run_pipeline()

#     clean_results = []
#     for r in results:
#         if isinstance(r, dict):
#             clean_results.append(r)
#         else:
#             try:
#                 parsed = json.loads(str(r))
#                 if isinstance(parsed, dict):
#                     clean_results.append(parsed)
#                 elif isinstance(parsed, list):
#                     clean_results.extend(parsed)
#             except Exception:
#                 clean_results.append({"raw_output": str(r)})

#     # Save as clean JSON
#     output_dir = Path("outputs")
#     output_dir.mkdir(exist_ok=True)
#     fp = output_dir / "health_news.json"
#     fp.write_text(json.dumps(clean_results, indent=2, ensure_ascii=False), encoding="utf-8")

#     logger.info(f"✅ Saved results to {fp}")

# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio
import json
import logging
from pathlib import Path
from src.pipelines.orchestrator import kickoff_crew

logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting GOQii multi-agent crew pipeline...")

    # Run the crew
    crew_output = await kickoff_crew()

    # Extract data
    if hasattr(crew_output, "raw"):
        results = crew_output.raw
    elif hasattr(crew_output, "results"):
        results = crew_output.results
    else:
        try:
            results = json.loads(str(crew_output))
        except Exception:
            results = {"output": str(crew_output)}

    # Save to /tmp (writable on HF Spaces)
    fp = Path("/tmp/health_news.json")
    fp.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info(f"✅ Saved results to {fp}")

    return results  # so UI can also read it directly

if __name__ == "__main__":
    asyncio.run(main())


