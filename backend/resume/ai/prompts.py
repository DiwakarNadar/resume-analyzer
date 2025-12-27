def resume_only_prompt(resume_text, ats_score):
    return f"""
You are an ATS expert.

Resume Text:
{resume_text[:1500]}

ATS Score: {ats_score}

Explain:
1. Why this score makes sense
2. Strengths of the resume
3. Actionable improvements

Do not invent experience.
"""


def resume_jd_prompt(resume_text, jd_text, semantic_result, ats_score):
    return f"""
You are an ATS evaluator.

Job Description:
{jd_text[:1000]}

Resume:
{resume_text[:1500]}

Semantic Match Result:
{semantic_result}

ATS Score: {ats_score}

Explain:
1. Fit for the role
2. Gaps based on JD
3. What to improve

Do not hallucinate skills.
"""
