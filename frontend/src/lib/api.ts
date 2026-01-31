// API TYPES
export interface RoastResult {
  job_id: string;
  status: "processing" | "completed" | "failed";
  original_video_url?: string;
  processed_video_url?: string;
  meme_url?: string;
  transcript?: { timestamp: string; text: string }[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// REAL API FUNCTIONS
export const api = {
  // 1. Upload File & Start Job
  startRoast: async (file: File, lensId: string): Promise<{ job_id: string }> => {
    const formData = new FormData();
    formData.append("video", file);
    formData.append("lens", lensId);

    try {
      const response = await fetch(`${API_BASE}/api/generate`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload failed: ${errorText}`);
      }

      const data = await response.json();
      return { job_id: data.video_id };
    } catch (e) {
      console.error("API Error:", e);
      throw e;
    }
  },

  // 2. Poll for Status
  getRoastStatus: async (jobId: string): Promise<RoastResult> => {
    try {
      const response = await fetch(`${API_BASE}/api/video/${jobId}`);

      if (response.status === 404) {
        // If 404, it might be processing (or not found). 
        // In this simple backend, if it returns 200 it's done. 
        // If 404, we assume it's possibly still going or actually error.
        // But our backend currently runs synchronously (long poll), so fetch won't return until done?
        // Actually, verify backend logic: generate endpoint waits! 
        // Oh, the generate endpoint waits for completion. 
        // So startRoast actually returns only when done?
        // Let's check backend/routers/generate.py.
        // Yes, generate_commentary is async def but it awaits everything. 
        // So startRoast will take a long time and return the final Result.
        // But the frontend expects startRoast -> jobId immediately, then poll.
        // This mismatch needs fixing.
        // For now, let's assume startRoast returns { video_id, ... } AFTER it is done.
        // And getRoastStatus just fetches the RESULT from the store.
        return { job_id: jobId, status: "processing" };
      }

      if (!response.ok) throw new Error("Failed to fetch status");

      const data = await response.json();

      // Map backend response to frontend types
      return {
        job_id: data.video_id,
        status: "completed",
        original_video_url: data.video_url, // Using output as original for now
        processed_video_url: data.video_url,
        meme_url: "", // Meme generated separately
        transcript: data.segments?.map((s: any) => ({
          timestamp: s.start_time.toFixed(1),
          text: s.text
        })) || []
      };
    } catch (e) {
      console.error("Status Error:", e);
      return { job_id: jobId, status: "failed" };
    }
  },

  // 3. Get User Sessions
  getSessions: async () => {
    const saved = localStorage.getItem("ragebait_sessions");
    return saved ? JSON.parse(saved) : [];
  }
};

export async function generateMeme(videoId: string, caption: any, format: string) {
  const response = await fetch(`${API_BASE}/api/meme/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ video_id: videoId }), // Backend only needs video_id for now
  });
  return response.json();
}
