const BASE_URL = "https://resume-analyzer-3l4w.onrender.com/api";

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/upload-resume/`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function getResumeATS(resumeId) {
  const res = await fetch(
    `${BASE_URL}/resume/${resumeId}/ats/resume/`,
    { method: "POST" }
  );

  if (!res.ok) throw new Error("ATS failed");
  return res.json();
}

export async function getResumeJdATS(resumeId, jobDescription) {
  const res = await fetch(
    `${BASE_URL}/resume/${resumeId}/ats/jd/`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description: jobDescription }),
    }
  );

  if (!res.ok) throw new Error("JD ATS failed");
  return res.json();
}
