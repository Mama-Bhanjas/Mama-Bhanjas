# 🧠 PIPELINE REFINEMENT SUMMARY

## 1. NER (Location Extraction) Fix 📍
**Issue**: The NER model was missing locations or being inaccurate for Nepali districts.
**Solution**: 
- Added a **comprehensive dictionary lookup** of 77+ Nepal districts and major cities (e.g., "Taplejung", "Jumla", "Parsa").
- The pipeline now consistently scans for these names *before* relying on the AI model.
- If "Kathmandu" or "Jhapa" appears in the text, it is **guaranteed** to be extracted as a location entity.

## 2. Verification Pipeline Refinement ✅
**Issue**: Real news without a "Trusted Source" match was defaulting to "Unknown" status.
**Solution**:
- Implemented **Content Dominance Rule**: If the AI model is extremely confident (>95%) that the text is real news, it overrides the "Unknown Source" penalty.
- Adjusted weights to rely 80% on content analysis when no URL is provided (up from 70%).
- **Result**: Legitimate citizen reports are now marked as "Likely Real" or "Verified" based on their content quality, even if the source is unknown.

## 3. Title Generation (Confirmed) 📝
- As implemented previously, titles are now auto-generated from summaries if missing.

---

**Status**: ✅ Pipelines Refined & Deployed.
