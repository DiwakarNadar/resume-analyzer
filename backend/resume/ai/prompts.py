def resume_only_prompt(resume_text, ats_score):
    return f"""
You are an ATS resume reviewer.

ATS Score: {ats_score}

Resume summary:
{resume_text[:600]}

Give feedback in EXACTLY this format:

SUMMARY:
- point
- point
- point

STRENGTHS:
- point
- point

IMPROVEMENTS:
- point
- point

Rules:
- Max 1 sentence per point
- No extra text
"""



def resume_jd_prompt(resume_text, jd_text, semantic_result, ats_score):
    return f"""
You are an ATS evaluator.

Resume (partial):
{resume_text[:1200]}

Job Description:
{jd_text[:1200]}

Semantic Match:
{semantic_result}

ATS Score: {ats_score}

Return STRICT JSON only:

{{
  "summary": [3 short points],
  "strengths": [2 short points],
  "improvements": [2 actionable points]
}}

Rules:
- One sentence per point
- No markdown
- No explanations outside JSON
"""

