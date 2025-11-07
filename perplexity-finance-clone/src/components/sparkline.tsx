"use client";

import { TimelinePoint } from "@/lib/types";
import { memo } from "react";

type SparklineProps = {
  data: TimelinePoint[];
  stroke?: string;
  className?: string;
  strokeWidth?: number;
  showArea?: boolean;
};

const normalizePoints = (data: TimelinePoint[]) => {
  const prices = data.map((point) => point.value);
  const max = Math.max(...prices);
  const min = Math.min(...prices);
  const range = max - min || 1;

  return data.map((point, index) => {
    const x = (index / (data.length - 1 || 1)) * 100;
    const y = 100 - ((point.value - min) / range) * 100;
    return [x, y] as const;
  });
};

const SparklineComponent = ({
  data,
  stroke = "url(#spark-gradient)",
  className,
  strokeWidth = 2,
  showArea = true,
}: SparklineProps) => {
  if (!data.length) return null;
  const points = normalizePoints(data);
  const path = points.map(([x, y]) => `${x},${y}`).join(" ");
  const areaPath = `0,100 ${path} 100,100`;

  return (
    <svg
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      className={className ?? "h-24 w-full"}
    >
      <defs>
        <linearGradient
          id="spark-gradient"
          x1="0%"
          x2="100%"
          y1="0%"
          y2="0%"
        >
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="50%" stopColor="#0ea5e9" />
          <stop offset="100%" stopColor="#14b8a6" />
        </linearGradient>
        <linearGradient
          id="spark-area"
          x1="0%"
          x2="0%"
          y1="0%"
          y2="100%"
        >
          <stop offset="0%" stopColor="rgba(79, 70, 229, 0.35)" />
          <stop offset="100%" stopColor="rgba(14, 165, 233, 0.05)" />
        </linearGradient>
      </defs>

      {showArea && (
        <polyline
          points={areaPath}
          fill="url(#spark-area)"
          opacity={0.4}
          stroke="transparent"
        />
      )}

      <polyline
        points={path}
        fill="none"
        stroke={stroke}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={strokeWidth}
      />
    </svg>
  );
};

export const Sparkline = memo(SparklineComponent);
