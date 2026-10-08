# Notes

- https://github.com/joaopalmeiro/template-python-uv-script
- https://huggingface.co/google/embeddinggemma-2
- https://ai.google.dev/gemma/docs/embeddinggemma/inference-embeddinggemma-with-sentence-transformers
- https://ai.google.dev/gemma/docs/embeddinggemma/fine-tuning-embeddinggemma-with-sentence-transformers
- "ImportError: EmbeddingGemma2Processor requires the PIL library but it was not found in your environment. You can install it with pip: `pip install pillow`. Please note that you may need to restart your runtime after installation."
  - https://github.com/huggingface/transformers/blob/v5.19.0/src/transformers/models/embedding_gemma2/processing_embedding_gemma2.py#L54
  - https://github.com/huggingface/transformers/blob/v5.19.0/src/transformers/utils/import_utils.py#L2916-L2930
  - https://github.com/huggingface/transformers/blob/v5.19.0/src/transformers/utils/import_utils.py#L2350: `("vision", (is_vision_available, VISION_IMPORT_ERROR)),`
  - https://github.com/huggingface/transformers/blob/v5.19.0/src/transformers/utils/import_utils.py#L2201
- https://github.com/huggingface/transformers/releases/tag/v5.19.0
- https://huggingface.co/docs/transformers/main/en/model_doc/embedding_gemma2
