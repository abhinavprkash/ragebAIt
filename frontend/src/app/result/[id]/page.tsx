"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ArrowLeft, Play, Pause, RefreshCw, MessageSquare, Share2, UploadCloud } from "lucide-react";
import Link from "next/link";
import { ShareButtons } from "@/components/ShareButtons";
import { Badge } from "@/components/ui/badge";

import { api, RoastResult } from "@/lib/api";
import { cn } from "@/lib/utils"; // Added cn import

export default function ResultPage() {
    const params = useParams();
    const id = params.id as string;

    const [status, setStatus] = useState<"processing" | "completed" | "failed">("processing");
    const [result, setResult] = useState<RoastResult | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);

    // Polling Logic
    useEffect(() => {
        let interval: NodeJS.Timeout;

        const checkStatus = async () => {
            const data = await api.getRoastStatus(id);
            setResult(data);
            setStatus(data.status);

            if (data.status === "completed") {
                clearInterval(interval);
            }
        };

        // Initial check
        checkStatus();
        // Poll every 3 seconds
        interval = setInterval(checkStatus, 3000);

        return () => clearInterval(interval);
    }, [id]);

    const activeVideoUrl = status === "completed" ? result?.processed_video_url : result?.original_video_url;

    const handleDownload = () => {
        if (activeVideoUrl) {
            const a = document.createElement('a');
            a.href = activeVideoUrl;
            a.download = `roast-${id}.mp4`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    };

    return (
        <div className="h-full flex flex-col p-6 max-w-[1800px] mx-auto space-y-6">

            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link href="/">
                        <Button variant="ghost" className="text-white hover:text-primary hover:bg-white/5">
                            <ArrowLeft className="w-4 h-4 mr-2" />
                            Back
                        </Button>
                    </Link>
                    <h1 className="text-2xl font-bold font-oswald text-white tracking-wide">SESSION RESULT</h1>
                </div>
                <div className="flex gap-2">
                    <Button className="bg-[#1DA1F2] hover:bg-[#1DA1F2]/90 text-white border-0">
                        <Share2 className="w-4 h-4 mr-2" />
                        Post to X (Browser Agent)
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1 min-h-0">

                {/* Left: Final Video (Commentary Added) */}
                <div className="lg:col-span-7 flex flex-col space-y-4">
                    <Card className="flex-1 bg-black border-white/10 relative overflow-hidden group shadow-2xl rounded-2xl">
                        <Badge className={cn("absolute top-4 left-4 z-10 transition-colors duration-500", status === "completed" ? "bg-green-600" : "bg-yellow-600 animate-pulse")}>
                            {status === "completed" ? "FINAL CUT READY" : "PROCESSING VIDEO..."}
                        </Badge>

                        {activeVideoUrl ? (
                            <video
                                id="main-video"
                                src={activeVideoUrl}
                                key={activeVideoUrl} // Force re-render on url change
                                className="w-full h-full object-contain"
                                onPlay={() => setIsPlaying(true)}
                                onPause={() => setIsPlaying(false)}
                                controls
                            />
                        ) : (
                            <div className="absolute inset-0 flex items-center justify-center text-white/30 animate-pulse">
                                <UploadCloud className="w-10 h-10 animate-bounce" />
                            </div>
                        )}
                    </Card>
                    <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10">
                        <div>
                            <div className="text-sm font-medium text-white">
                                {status === "completed" ? "AI Analysis Complete" : "Analyzing Frames..."}
                            </div>
                            <div className="text-xs text-white/50">Gemini 2.0 Flash + TTS</div>
                        </div>
                        <Button
                            variant="outline"
                            className="border-white/10 hover:bg-white/10"
                            onClick={handleDownload}
                            disabled={status !== "completed"}
                        >
                            {status === "completed" ? "Download Video" : "Waiting for Rendering..."}
                        </Button>
                    </div>
                </div>

                {/* Right: Meme & Commentary Log */}
                <div className="lg:col-span-5 flex flex-col space-y-6">

                    {/* Generated Meme Section */}
                    <div className="flex-1 min-h-[300px]">
                        <Card className="h-full bg-white/5 border-white/10 p-4 flex flex-col">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="font-bold font-oswald text-white tracking-wide flex items-center gap-2">
                                    <UploadCloud className="w-5 h-5 text-yellow-500" />
                                    GENERATED MEME
                                </h3>
                                <Badge variant="outline" className="border-yellow-500/50 text-yellow-500">Nano Banana</Badge>
                            </div>
                            <div className="flex-1 bg-black/40 rounded-lg overflow-hidden relative group flex items-center justify-center">
                                {status === "completed" && result?.meme_url ? (
                                    <div className="relative w-full h-full">
                                        <img src={result.meme_url} alt="Meme" className="w-full h-full object-contain" />
                                        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2 cursor-pointer">
                                            <Button variant="secondary">Regenerate</Button>
                                            <Button>Share Image</Button>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="text-center p-6 space-y-2">
                                        <UploadCloud className="w-8 h-8 text-white/20 mx-auto animate-pulse" />
                                        <p className="text-sm text-white/40">Cooking up a fresh roast...</p>
                                    </div>
                                )}
                            </div>
                        </Card>
                    </div>

                    {/* Roast Log (Transcript) */}
                    <div className="h-[250px]">
                        <Card className="h-full flex flex-col bg-white/5 border-white/10">
                            <div className="p-3 border-b border-white/10 flex justify-between items-center">
                                <h3 className="text-sm font-semibold text-white/70">Audio Transcript</h3>
                                {status === "processing" && <span className="text-xs text-primary animate-pulse">Generating...</span>}
                            </div>
                            <ScrollArea className="flex-1 p-4">
                                <div className="space-y-3 text-sm">
                                    {result?.transcript ? (
                                        result.transcript.map((line, i) => (
                                            <p key={i} className="text-white/90">
                                                <span className="text-primary font-mono mr-2">{line.timestamp}</span>
                                                {line.text}
                                            </p>
                                        ))
                                    ) : (
                                        <div className="space-y-3 opacity-30">
                                            <div className="h-4 w-3/4 bg-white/20 rounded animate-pulse" />
                                            <div className="h-4 w-1/2 bg-white/20 rounded animate-pulse delay-75" />
                                            <div className="h-4 w-5/6 bg-white/20 rounded animate-pulse delay-150" />
                                        </div>
                                    )}
                                </div>
                            </ScrollArea>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}
