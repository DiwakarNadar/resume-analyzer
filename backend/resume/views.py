import uuid
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Resume
from .serializers import ResumeUploadSerializer
from .supabase_client import upload_file_to_supabase, generate_signed_url
from .utils.text_extractor import extract_text_from_file
from .utils.resume_quality import calculate_resume_ats
from .utils.ats_engine import calculate_jd_ats

from resume.ai.rag_engine import run_rag
from resume.ai.prompts import resume_only_prompt, resume_jd_prompt
from resume.ai.llm_client import run_llm

class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response({"error": "File is required"}, status=400)

        ext = uploaded_file.name.split(".")[-1]
        supabase_path = f"{uuid.uuid4()}.{ext}"

        upload_file_to_supabase(
            uploaded_file.read(),
            supabase_path,
            uploaded_file.content_type,
        )

        resume = Resume.objects.create(
            original_file_name=uploaded_file.name,
            file=supabase_path,
        )

        return Response(
            ResumeUploadSerializer(resume).data,
            status=status.HTTP_201_CREATED,
        )

class ResumeOnlyATSView(APIView):
    def post(self, request, resume_id):
        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)

        # 1️⃣ Extract if missing
        if not resume.extracted_text:
            try:
                signed_url = generate_signed_url(resume.file, expires_in=120)
                resume.extracted_text = extract_text_from_file(signed_url)
                resume.save(update_fields=["extracted_text"])
            except Exception as e:
                return Response(
                    {"error": f"Text extraction failed: {str(e)}"},
                    status=400
                )

        # 2️⃣ Deterministic ATS
        base_result = calculate_resume_ats(resume.extracted_text)

        # 3️⃣ RAG grounding
        rag_result = run_rag(resume.extracted_text, None)

        # 4️⃣ LLM explanation (NON-BLOCKING)
        try:
            llm_feedback = run_llm(
                resume_only_prompt(
                    resume.extracted_text,
                    base_result["ats_score"]
                )
            )
        except Exception:
            llm_feedback = "LLM feedback unavailable at the moment."

        final_response = {
            **base_result,
            "rag_insights": rag_result,
            "llm_feedback": llm_feedback,
        }

        resume.ats_score = base_result["ats_score"]
        resume.skills = base_result["skills"]
        resume.analysis_result = final_response
        resume.save()

        return Response(final_response)

class ResumeJdATSView(APIView):
    def post(self, request, resume_id):
        jd = request.data.get("job_description")
        if not jd:
            return Response({"error": "Job description required"}, status=400)

        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)

        # 1️⃣ Extract if missing
        if not resume.extracted_text:
            try:
                signed_url = generate_signed_url(resume.file, expires_in=120)
                resume.extracted_text = extract_text_from_file(signed_url)
                resume.save(update_fields=["extracted_text"])
            except Exception as e:
                return Response(
                    {"error": f"Text extraction failed: {str(e)}"},
                    status=400
                )

        # 2️⃣ Deterministic ATS
        base_result = calculate_jd_ats(
            resume_text=resume.extracted_text,
            jd_text=jd,
        )

        # 3️⃣ RAG grounding
        rag_result = run_rag(resume.extracted_text, jd)

        # 4️⃣ LLM explanation (NON-BLOCKING)
        try:
            llm_feedback = run_llm(
                resume_jd_prompt(
                    resume.extracted_text,
                    jd,
                    rag_result,
                    base_result["ats_score"]
                )
            )
        except Exception:
            llm_feedback = "LLM feedback unavailable at the moment."

        final_response = {
            **base_result,
            "rag_insights": rag_result,
            "llm_feedback": llm_feedback,
        }

        resume.ats_score = base_result["ats_score"]
        resume.analysis_result = final_response
        resume.save()

        return Response(final_response)

