// API TYPES
export interface RoastResult {
  job_id: string;
  status: "processing" | "completed" | "failed";
  original_video_url?: string;
  processed_video_url?: string;
  meme_url?: string;
  transcript?: { timestamp: string; text: string }[];
}

// MOCK FUNCTIONS (To be replaced by real axios/fetch calls)
export const api = {
  // 1. Upload File & Start Job
  startRoast: async (file: File, lensId: string): Promise<{ job_id: string }> => {
    console.log("Uploading file:", file.name, "Lens:", lensId);
    return new Promise((resolve) => {
      setTimeout(() => resolve({ job_id: Date.now().toString() }), 1000);
    });
  },

  // 2. Poll for Status (Video replacement logic happens here)
  getRoastStatus: async (jobId: string): Promise<RoastResult> => {
    // Simulate "Processing" state for first 5 seconds
    const isProcessing = Math.random() < 0.3;

    if (isProcessing) {
      return {
        job_id: jobId,
        status: "processing",
        original_video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
      };
    }

    return {
      job_id: jobId,
      status: "completed",
      original_video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
      // This is the "New Video" (friend's work)
      processed_video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
      // This is the "Nano Banana" meme
      meme_url: "https://placehold.co/600x600/png?text=NANO+BANANA+MEME",
      transcript: [
        { timestamp: "00:02", text: "Look at that stance! Disgraceful." },
        { timestamp: "00:08", text: "You call that a swing? I call it a cry for help." },
        { timestamp: "00:15", text: "Even the ball looks embarrassed to be near you." }
      ]
    };
  },

  // 3. Get User Sessions (For Sidebar)
  getSessions: async () => {
    // In real app: return await axios.get("/api/sessions");
    const saved = localStorage.getItem("ragebait_sessions");
    return saved ? JSON.parse(saved) : [];
  }
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function generateMeme(videoId: string, caption: object, format: string) {
  const response = await fetch(`${API_BASE}/api/meme/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ video_id: videoId, caption, format }),
  });
  return response.json();
}
