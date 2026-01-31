"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { Check, Info, Skull, BookOpen, Gavel, Briefcase, Flame } from "lucide-react";

export const LENSES = [
    { id: "roast_master", name: "Drill Sergeant", icon: Skull, description: "Brutal honesty. No mercy." },
    { id: "nature_doc", name: "Nature Doc", icon: BookOpen, description: "Narrated like a wild animal hunt." },
    //   { id: "heist_movie", name: "Heist Movie", icon: Share2, description: "High stakes, intense music." },
    //   { id: "alien", name: "Alien Study", icon: User, description: "Confused observation of humans." },
    { id: "shakespeare", name: "Shakespeare", icon: Gavel, description: "Dramatic tragedy of your form." },
    { id: "corporate", name: "Corporate", icon: Briefcase, description: "Passive aggressive HR feedback." },
    { id: "hype_man", name: "Hype Man", icon: Flame, description: "Over-the-top excitement." },
];

interface LensSelectorProps {
    selectedLens: string;
    onSelectLens: (lensId: string) => void;
}

export function LensSelector({ selectedLens, onSelectLens }: LensSelectorProps) {
    return (
        <div className="w-full space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold font-oswald tracking-wide flex items-center gap-2 text-white">
                    <span className="w-1 h-6 bg-primary rounded-full" />
                    SELECT COMMENTARY STYLE
                </h2>
                <span className="text-xs text-white/40 font-mono">STEP 02</span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                {LENSES.map((lens) => {
                    const isSelected = selectedLens === lens.id;
                    const Icon = lens.icon;

                    return (
                        <motion.div
                            key={lens.id}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => onSelectLens(lens.id)}
                            className={cn(
                                "relative cursor-pointer overflow-hidden rounded-xl border-2 transition-all duration-300 h-full",
                                isSelected
                                    ? "border-primary bg-primary/10 shadow-[0_0_20px_rgba(var(--primary),0.3)]"
                                    : "border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10"
                            )}
                        >
                            {isSelected && (
                                <div className="absolute top-2 right-2 p-1 bg-primary rounded-full z-10">
                                    <Check className="w-3 h-3 text-white" />
                                </div>
                            )}

                            <div className="p-4 flex flex-col items-center text-center gap-3 h-full">
                                <Icon className={cn("w-10 h-10 mb-1 transition-colors", isSelected ? "text-primary" : "text-white")} />
                                <div>
                                    <div className="font-bold text-sm text-white">{lens.name}</div>
                                    <div className="text-[10px] text-white/50 leading-tight mt-1 line-clamp-2">
                                        {lens.description}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    );
                })}
            </div>
        </div>
    );
}
