"use client";

import React, { useState } from "react";
import { VideoUploader } from "@/components/VideoUploader";
import { LensSelector } from "@/components/LensSelector";
import { BrowserFeeds } from "@/components/BrowserFeeds"; // Import the new component
import { Button } from "@/components/ui/button";
import { Loader2, Zap } from "lucide-react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";

import { useSessions } from "@/lib/session-context";

export default function Home() {
  const router = useRouter();
  const { addSession } = useSessions(); // Use the hook
  const [file, setFile] = useState<File | null>(null);
  const [selectedLens, setSelectedLens] = useState<string>("roast_master");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    console.log("Generating with:", { file, selectedLens });

    // Create detailed title based on input
    const title = file ? `Analysis: ${file.name}` : `Roast: ${selectedLens}`;

    setTimeout(() => {
      addSession(title); // Add to sidebar
      setIsGenerating(false);
      router.push(`/result/${Date.now()}`); // Navigate to new ID
    }, 2000);
  };

  return (
    <div className="h-full flex flex-col p-6 max-w-[1600px] mx-auto">
      <header className="mb-12 text-center md:text-left">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl font-bold tracking-tight text-white mb-2 bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent"
        >
          Gemini 3 <span className="text-primary font-normal">SuperHack</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-xl text-white/60 font-light"
        >
          Multimodal Sports Analysis & Roast Agent
        </motion.p>
      </header>

      <div className="grid lg:grid-cols-12 gap-8 flex-1">
        {/* Left Column: Input (Video/URL) */}
        <div className="lg:col-span-4 space-y-8">
          <section className="bg-white/5 border border-white/10 rounded-2xl p-1 backdrop-blur-md h-full flex flex-col">
            <Tabs defaultValue="upload" className="w-full flex-1 flex flex-col">
              <TabsList className="w-full bg-transparent border-b border-white/5 justify-start h-14 p-0">
                <TabsTrigger value="upload" className="h-full px-8 data-[state=active]:bg-white/5 data-[state=active]:text-white data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none">
                  Upload
                </TabsTrigger>
                <TabsTrigger value="url" className="h-full px-8 data-[state=active]:bg-white/5 data-[state=active]:text-white data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none">
                  Paste URL
                </TabsTrigger>
              </TabsList>
              <div className="p-6 flex-1">
                <TabsContent value="upload" className="mt-0 h-full">
                  <VideoUploader onFileSelect={setFile} />
                </TabsContent>
                <TabsContent value="url" className="mt-0 space-y-4">
                  <div className="p-8 border-2 border-dashed border-white/10 rounded-xl bg-white/5 flex flex-col items-center justify-center text-center gap-4 min-h-[300px]">
                    <p className="text-white/60 max-w-sm">
                      Paste a link from Twitter, YouTube, or TikTok. Our Browser Agent will fetch it for you.
                    </p>
                    <div className="flex w-full max-w-md gap-2">
                      <Input placeholder="https://x.com/user/status/123..." className="bg-black/50 border-white/10" />
                      <Button variant="secondary">Fetch</Button>
                    </div>
                  </div>
                </TabsContent>
              </div>
            </Tabs>
          </section>
        </div>

        {/* Middle Column: Selection & Summary */}
        <div className="lg:col-span-5 space-y-8">
          <LensSelector
            selectedLens={selectedLens}
            onSelectLens={setSelectedLens}
          />

          <div className="bg-gradient-to-br from-primary/20 to-purple-900/20 border border-primary/20 rounded-2xl p-6 backdrop-blur-md">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-medium text-white">Analysis Ready</h3>
              <div className="flex items-center gap-2 text-xs text-primary font-mono uppercase">
                <Zap className="w-4 h-4 fill-primary" />
                Gemini-2.0-Flash
              </div>
            </div>

            <Button
              size="lg"
              className="w-full text-lg h-14 rounded-xl bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90 shadow-[0_0_30px_rgba(var(--primary),0.3)] transition-all hover:scale-[1.02]"
              disabled={!file && !isGenerating}
              onClick={handleGenerate}
            >
              {isGenerating ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Processing...
                </>
              ) : (
                "Bake the Roast"
              )}
            </Button>
          </div>
        </div>

        {/* Right Column: Live Browser Feeds */}
        <div className="lg:col-span-3">
          <BrowserFeeds />
        </div>
      </div>
    </div>
  );
}
