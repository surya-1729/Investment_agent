"use client";

import { Insight } from "@/lib/types";
import { ArrowDownRight, ArrowUpRight, Info } from "lucide-react";
import { cn } from "@/lib/utils";

type InsightCardProps = {
  insight: Insight;
};

export const InsightCard = ({ insight }: InsightCardProps) => {
  return (
    <article className="group relative overflow-hidden rounded-3xl border border-zinc-200/70 bg-white/80 p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-indigo-300/80 hover:shadow-xl">
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-white via-white/60 to-indigo-50 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
      <span className="inline-flex items-center gap-2 rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium uppercase tracking-wide text-zinc-600">
        {insight.kind}
      </span>
      <h3 className="mt-4 text-xl font-semibold text-zinc-900">{insight.title}</h3>
      <p className="mt-2 text-sm text-zinc-600">{insight.description}</p>

      <div className="mt-6 grid gap-4">
        {insight.metrics.map((metric) => (
          <div
            key={metric.label}
            className="flex items-start justify-between rounded-2xl border border-zinc-200/80 bg-white/80 p-4 transition-colors group-hover:border-indigo-200/90"
          >
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                {metric.label}
              </p>
              <p className="mt-1 text-lg font-semibold text-zinc-900">
                {metric.value}
              </p>
              {metric.hint ? (
                <span className="mt-1 inline-flex items-center gap-1 text-xs text-zinc-500">
                  <Info className="h-3 w-3" />
                  {metric.hint}
                </span>
              ) : null}
            </div>

            {metric.delta ? (
              <div
                className={cn(
                  "inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium",
                  metric.delta.isPositive
                    ? "bg-emerald-50 text-emerald-600"
                    : "bg-rose-50 text-rose-600"
                )}
              >
                {metric.delta.isPositive ? (
                  <ArrowUpRight className="h-3.5 w-3.5" />
                ) : (
                  <ArrowDownRight className="h-3.5 w-3.5" />
                )}
                {metric.delta.value}
              </div>
            ) : null}
          </div>
        ))}
      </div>
    </article>
  );
};
