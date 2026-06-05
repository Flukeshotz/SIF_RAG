# Dependency Map (Filtered)

Module → Imported By
---
**chunking.schema** | chunking/base_chunker.py, chunking/factsheet_chunker.py, chunking/isid_chunker.py, chunking/kim_chunker.py, chunking/regulatory_chunker.py, chunking/run.py, chunking/validator.py
> **HIGH IMPACT – DO NOT MOVE**

**db.qdrant_connection** | api/main.py, retrieval/search.py, scripts/audit_qdrant.py, scripts/ingest_qdrant.py, scripts/scrape_urls_to_qdrant.py, scripts/update_source_authority.py
> **HIGH IMPACT – DO NOT MOVE**

**processing.document_model** | processing/metadata_extractor.py, processing/pdf_parser.py, processing/run.py, processing/table_extractor.py, processing/validator.py, tests/test_processing.py
> **HIGH IMPACT – DO NOT MOVE**

**embeddings.model** | embeddings/generator.py, retrieval/embed_query.py, scripts/audit_qdrant.py, scripts/audit_vectors.py, scripts/scrape_urls_to_qdrant.py
> **HIGH IMPACT – DO NOT MOVE**

**chunking.base_chunker** | chunking/factsheet_chunker.py, chunking/isid_chunker.py, chunking/kim_chunker.py, chunking/regulatory_chunker.py
> **HIGH IMPACT – DO NOT MOVE**

**retrieval.embed_query** | retrieval/engine.py, scripts/generate_priority_audit.py, scripts/retrieval_benchmark.py, tests/test_retrieval.py
> **HIGH IMPACT – DO NOT MOVE**

**retrieval.search** | retrieval/engine.py, scripts/generate_priority_audit.py, scripts/retrieval_benchmark.py, tests/test_retrieval.py
> **HIGH IMPACT – DO NOT MOVE**

**core.config** | api/main.py, db/qdrant_connection.py, main.py
> **HIGH IMPACT – DO NOT MOVE**

**retrieval.engine** | api/main.py, scripts/evaluate_comprehensive.py, tests/test_generation.py
> **HIGH IMPACT – DO NOT MOVE**

**generation.prompts** | generation/llm.py, tests/test_generation.py
> **HIGH IMPACT – DO NOT MOVE**

**processing.metadata_extractor** | processing/run.py, tests/test_processing.py
> **HIGH IMPACT – DO NOT MOVE**

**processing.validator** | processing/run.py, tests/test_processing.py
> **HIGH IMPACT – DO NOT MOVE**

**retrieval.citations** | retrieval/engine.py, tests/test_generation.py
> **HIGH IMPACT – DO NOT MOVE**

**retrieval.context_builder** | retrieval/engine.py, tests/test_retrieval.py
> **HIGH IMPACT – DO NOT MOVE**

retrieval.query_router | scripts/retrieval_benchmark.py, scripts/validate_routing.py
**scripts.validate_corpus** | tests/test_corpus_inventory.py, tests/test_source_registry.py
> **HIGH IMPACT – DO NOT MOVE**

chunking.factsheet_chunker | chunking/run.py
chunking.isid_chunker | chunking/run.py
chunking.kim_chunker | chunking/run.py
chunking.regulatory_chunker | chunking/run.py
chunking.validator | chunking/run.py
core.logger | main.py
**generation.llm** | retrieval/engine.py
> **HIGH IMPACT – DO NOT MOVE**

**ingestion.downloader** | tests/test_downloader.py
> **HIGH IMPACT – DO NOT MOVE**

**ingestion.hashing** | tests/test_hashing.py
> **HIGH IMPACT – DO NOT MOVE**

**ingestion.registry** | tests/test_registry.py
> **HIGH IMPACT – DO NOT MOVE**

ingestion.run | jobs/refresh_corpus.py
jobs.refresh_corpus | jobs/scheduler.py
**jobs.scheduler** | api/main.py
> **HIGH IMPACT – DO NOT MOVE**

**main** | tests/conftest.py
> **HIGH IMPACT – DO NOT MOVE**

processing.pdf_parser | processing/run.py
processing.pdf_quality | processing/run.py
processing.table_extractor | processing/pdf_parser.py
registry.discovery | jobs/refresh_registry.py
