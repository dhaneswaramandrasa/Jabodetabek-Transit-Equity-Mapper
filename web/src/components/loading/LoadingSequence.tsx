"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useAccessibilityStore } from "@/lib/store";

const STAGES = [
  { key: "resolving", label: "Locating your zone..." },
  { key: "fetching-pois", label: "Finding transit stops..." },
  { key: "fetching-transit", label: "Computing route options..." },
  { key: "analyzing", label: "Estimating mode probabilities..." },
] as const;

function CheckIcon() {
  return (
    <motion.svg
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className="w-5 h-5 text-emerald-400"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2.5}
        d="M5 13l4 4L19 7"
      />
    </motion.svg>
  );
}

function Spinner() {
  return (
    <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
  );
}

function PendingDot() {
  return <div className="w-5 h-5 rounded-full border-2 border-outline-variant/30" />;
}

export default function LoadingSequence() {
  const { appPhase, loadingStage } = useAccessibilityStore();

  if (appPhase !== "loading") return null;

  const stageIndex = STAGES.findIndex((s) => s.key === loadingStage);

  return (
    <AnimatePresence>
      <motion.div
        key="loading"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
        className="absolute inset-0 z-20 flex items-center justify-center"
      >
        <div className="absolute inset-0 bg-surface/60 backdrop-blur-sm" />

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1, duration: 0.4 }}
          className="relative glass-strong rounded-2xl p-8 max-w-sm w-full mx-4 shadow-xl"
        >
          <h3 className="text-lg font-semibold text-on-surface mb-6">
            Computing journey options...
          </h3>

          <div className="space-y-4">
            {STAGES.map((stage, idx) => {
              const isComplete = idx < stageIndex;
              const isCurrent = idx === stageIndex;
              const isPending = idx > stageIndex;

              return (
                <motion.div
                  key={stage.key}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 + idx * 0.1 }}
                  className="flex items-center gap-3"
                >
                  <div className="shrink-0">
                    {isComplete && <CheckIcon />}
                    {isCurrent && <Spinner />}
                    {isPending && <PendingDot />}
                  </div>
                  <span
                    className={`text-sm ${
                      isComplete
                        ? "text-emerald-400 font-medium"
                        : isCurrent
                        ? "text-primary font-medium"
                        : "text-on-surface/30"
                    }`}
                  >
                    {stage.label}
                  </span>
                </motion.div>
              );
            })}
          </div>

          {/* Progress bar */}
          <div className="mt-6 h-1 bg-white/8 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-primary rounded-full"
              initial={{ width: "0%" }}
              animate={{
                width:
                  stageIndex < 0
                    ? "0%"
                    : `${((stageIndex + 1) / STAGES.length) * 100}%`,
              }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
            />
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
