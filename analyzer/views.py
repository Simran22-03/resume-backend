from rest_framework.decorators import api_view
from rest_framework.response import Response
import traceback

  
from .services.pdf_reader import extract_text_from_pdf
from .services.gemini_service import (
    analyze_resume,
    ask_chatbot,
)


# ==========================================================
# Resume Analysis API
# ==========================================================

@api_view(["POST"])
def analyze_resume_view(request):
    try:
        resume = request.FILES.get("resume")
        job_description = request.data.get("job_description")

        if not resume:
            return Response(
                {"error": "Resume not uploaded."},
                status=400,
            )

        if not job_description:
            return Response(
                {"error": "Job description is required."},
                status=400,
            )

        resume_text = extract_text_from_pdf(resume)

        result = analyze_resume(
            resume_text,
            job_description,
        )

        return Response(result)

        except Exception as e:
        traceback.print_exc()

        return Response(
            {
                "success": False,
                "error": str(e),
            },
            status=500,
        )


# ==========================================================
# Resume Chatbot API
# ==========================================================

@api_view(["POST"])
def chatbot_view(request):

    question = request.data.get("question")
    analysis = request.data.get("analysis")

    if not question:
        return Response(
            {"error": "Question is required."},
            status=400,
        )

    if not analysis:
        return Response(
            {"error": "Analysis is required."},
            status=400,
        )

    result = ask_chatbot(
        question,
        analysis,
    )

    return Response(result)