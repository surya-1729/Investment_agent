"use client";

import { useCallback, useMemo, useState, useTransition } from "react";
import { Loader2, Sparkles, Wand2 } from "lucide-react";
import { OracleIQResponse } from "@/lib/types";
import { InsightCard } from "@/components/insight-card";
import { Sparkline } from "@/components/sparkline";
import { cn } from "@/lib/utils";

const TRENDING_QUERIES = [
  "NVDA hedge fund sentiment",
  "MSFT cash flow trend",
  "AAPL vs. QQQ year to date",
  "TSLA margin pressure outlook",
  "AMD valuation vs peers",
];

const DEFAULT_QUERY = TRENDING_QUERIES[0];

const toReadableDate = (input?: string) => {
  if (!input) return "";
  if (input.includes("-")) {
    return new Date(input).toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    });
  }

  if (input.length >= 15) {
    const year = input.slice(0, 4);
    const month = input.slice(4, 6);
    const day = input.slice(6, 8);
    const hour = input.slice(9, 11);
    const minute = input.slice(11, 13);
    const iso = `${year}-${month}-${day}T${hour}:${minute}:00Z`;
    return new Date(iso).toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    });
  }

  return input;
};

const NewsList = ({ data }: { data: OracleIQResponse["news"] }) => {
  if (!data.length) {
    return (
      <div className="rounded-2xl border border-zinc-200/70 bg-white/60 p-6 text-sm text-zinc-500">
        News sentiment is unavailable for this symbol right now.
      </div>
    );
  }

  return (
    <ul className="space-y-4">
      {data.map((item) => (
        <li
          key={item.url ?? item.name}
          className="rounded-2xl border border-zinc-200/80 bg-white/70 p-4 shadow-sm transition hover:border-indigo-200 hover:shadow-md"
        >
          <div className="flex items-center justify-between gap-4">
            <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">
              {toReadableDate(item.publishedAt)}
            </p>
            <span className="rounded-full bg-indigo-100/80 px-2.5 py-1 text-xs font-semibold text-indigo-600">
              News
            </span>
          </div>
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-2 block text-sm font-semibold text-zinc-900 transition hover:text-indigo-600"
          >
            {item.name}
          </a>
          {item.snippet ? (
            <p className="mt-2 text-sm text-zinc-600 line-clamp-3">{item.snippet}</p>
          ) : null}
        </li>
      ))}
    </ul>
  );
};

const SourcesRail = ({ data }: { data: OracleIQResponse["sources"] }) => {
  return (
    <div className="flex flex-wrap gap-2">
      {data.map((source) => (
        <a
          key={(source.url ?? source.name) + source.type}
          href={source.url}
          target={source.url ? "_blank" : undefined}
          rel={source.url ? "noopener noreferrer" : undefined}
          className={cn(
            "group inline-flex items-center gap-2 rounded-full border border-zinc-200/70 bg-white/70 px-3.5 py-2 text-xs font-medium text-zinc-600 transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700",
            !source.url && "pointer-events-none text-zinc-400"
          )}
        >
          <span
            className={cn(
              "h-2 w-2 rounded-full",
              source.type === "news"
                ? "bg-emerald-500"
                : source.type === "market"
                  ? "bg-indigo-500"
                  : source.type === "fundamental"
                    ? "bg-amber-500"
                    : "bg-sky-500"
            )}
          />
          {source.name}
        </a>
      ))}
    </div>
  );
};

export const SearchExperience = () => {
  const [query, setQuery] = useState(DEFAULT_QUERY);
  const [data, setData] = useState<OracleIQResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const runQuery = useCallback((input: string) => {
    const payload = input.trim();
    if (!payload) {
      setError("Enter a question about a company, ETF, or theme to get started.");
      return;
    }

    startTransition(async () => {
      try {
        setError(null);
        const response = await fetch("/api/analyze", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: payload }),
        });

        const json = await response.json();
        if (!response.ok) {
          setError(json.error ?? "Failed to retrieve analytics.");
          return;
        }

        setData(json as OracleIQResponse);
      } catch (err) {
        console.error(err);
        setError("Network error. Please try again.");
      }
    });
  }, []);

  const timeline = data?.timeline ?? [];
  const latestClose = timeline.length
    ? timeline[timeline.length - 1]?.value
    : undefined;

  const metaInsights = useMemo(
    () => [
      {
        label: "Tracked Markets",
        value: "1200+",
      },
      {
        label: "Insight Latency",
        value: "<2s",
      },
      {
        label: "Coverage",
        value: "US & ADRs",
      },
    ],
    []
  );

  return (
    <section className="relative mt-16 rounded-4xl border border-white/40 bg-white/70 p-10 shadow-2xl shadow-indigo-200/30 backdrop-blur-xl">
      <div className="absolute inset-x-0 top-0 -z-10 h-[420px] rounded-4xl bg-gradient-to-br from-indigo-200/40 via-sky-100/30 to-white/0 blur-3xl" />

      <header className="flex flex-wrap items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-600">
            <Sparkles className="h-3.5 w-3.5" />
            Ask anything in finance
          </div>
          <h2 className="mt-4 text-3xl font-semibold tracking-tight text-zinc-900 sm:text-4xl">
            Conversational insights in milliseconds
          </h2>
          <p className="mt-2 max-w-2xl text-sm text-zinc-600 sm:text-base">
            OracleIQ aligns Alpha Vantage fundamentals, daily prices, and news sentiment
            into a single response stream with citations you can trust.
          </p>
        </div>

        <div className="flex gap-6 rounded-3xl border border-indigo-100 bg-indigo-50/60 p-4 text-sm font-medium text-indigo-900">
          {metaInsights.map((stat) => (
            <div key={stat.label}>
              <p className="text-xs uppercase tracking-wide text-indigo-500">
                {stat.label}
              </p>
              <p className="text-lg font-semibold">{stat.value}</p>
            </div>
          ))}
        </div>
      </header>

      <form
        className="mt-10 flex flex-col gap-4 rounded-3xl border border-zinc-200/80 bg-white/80 p-4 shadow-lg shadow-zinc-200/40 sm:flex-row sm:items-center"
        onSubmit={(event) => {
          event.preventDefault();
          runQuery(query);
        }}
      >
        <div className="flex w-full flex-col">
          <label
            htmlFor="oracle-query"
            className="text-xs font-semibold uppercase tracking-wide text-zinc-500"
          >
            Question
          </label>
          <input
            id="oracle-query"
            name="query"
            className="mt-2 w-full rounded-2xl border border-transparent bg-white/90 px-4 py-3 text-base font-medium text-zinc-900 shadow-inner shadow-zinc-200/70 outline-none ring-0 transition focus:border-indigo-300 focus:shadow-indigo-100 focus-visible:ring-2 focus-visible:ring-indigo-200/60"
            placeholder="e.g. How is NVDA trading vs consensus targets?"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            disabled={isPending}
          />
        </div>
        <button
          type="submit"
          disabled={isPending}
          className="flex w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-br from-indigo-600 via-sky-500 to-emerald-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-300/40 transition hover:shadow-indigo-400/50 disabled:cursor-not-allowed disabled:opacity-70 sm:w-auto"
        >
          {isPending ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Analyzing
            </>
          ) : (
            <>
              <Wand2 className="h-4 w-4" />
              Run analysis
            </>
          )}
        </button>
      </form>

      <div className="mt-4 flex flex-wrap items-center gap-3 text-xs text-zinc-500">
        <span className="font-semibold uppercase tracking-wide text-zinc-600">
          Trending prompts:
        </span>
        {TRENDING_QUERIES.map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => {
              setQuery(item);
              runQuery(item);
            }}
            className="rounded-full border border-zinc-200 bg-white/60 px-3 py-1 text-xs font-medium text-zinc-600 transition hover:border-indigo-200 hover:text-indigo-600"
            disabled={isPending && item === query}
          >
            {item}
          </button>
        ))}
      </div>

      {error ? (
        <div className="mt-6 rounded-3xl border border-rose-200 bg-rose-50/80 px-6 py-4 text-sm font-medium text-rose-700 shadow-sm">
          {error}
        </div>
      ) : null}

      <div className="mt-12 grid gap-10 lg:grid-cols-[minmax(0,1.65fr)_minmax(0,1fr)]">
        <div className="space-y-10">
          <div className="rounded-3xl border border-zinc-200/70 bg-white/80 p-6 shadow-inner shadow-zinc-200/60">
            <header className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                  Summary
                </p>
                <h3 className="text-xl font-semibold text-zinc-900">
                  {data?.companyName ?? "Live multi-source synthesis"}
                </h3>
              </div>
              {latestClose ? (
                <div className="rounded-2xl bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700">
                  Last close: ${latestClose.toFixed(2)}
                </div>
              ) : null}
            </header>

            <p className="mt-4 text-sm leading-6 text-zinc-600">
              {data?.summary ??
                "We triangulate the ticker you ask about, match fundamentals, price action, and the latest sentiment to surface what matters. Try a question above to see it in action."}
            </p>

            <div className="mt-6 rounded-2xl border border-zinc-200/70 bg-white/70 p-4">
              {timeline.length ? (
                <Sparkline data={timeline} className="h-28 w-full" />
              ) : (
                <div className="flex h-28 items-center justify-center text-sm text-zinc-400">
                  Price history will appear once you run a query.
                </div>
              )}
            </div>

            {data ? <SourcesRail data={data.sources} /> : null}
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            {data?.insights
              ? data.insights.map((insight) => (
                  <InsightCard key={insight.title} insight={insight} />
                ))
              : Array.from({ length: 2 }).map((_, index) => (
                  <div
                    key={index}
                    className="h-64 animate-pulse rounded-3xl border border-dashed border-zinc-200 bg-white/40"
                  />
                ))}
          </div>
        </div>

        <aside className="space-y-6">
          <div className="rounded-3xl border border-zinc-200/70 bg-white/70 p-6 shadow-inner shadow-zinc-200/60">
            <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
              Latest news
            </p>
            {isPending && !data ? (
              <div className="mt-4 flex items-center gap-2 text-sm text-zinc-500">
                <Loader2 className="h-4 w-4 animate-spin" />
                Pulling press coverage
              </div>
            ) : (
              <NewsList data={data?.news ?? []} />
            )}
          </div>

          <div className="rounded-3xl border border-indigo-100 bg-indigo-50/70 p-6 text-sm text-indigo-900 shadow-inner shadow-indigo-100/80">
            <h4 className="text-sm font-semibold uppercase tracking-wide text-indigo-500">
              Build with OracleIQ API
            </h4>
            <p className="mt-3 text-sm text-indigo-900/80">
              Integrate actionable insights into your internal dashboards or client
              portals. GraphQL bridge and webhook streaming available on Scale plans.
            </p>
            <a
              href="#pricing"
              className="mt-4 inline-flex items-center gap-2 rounded-full bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-indigo-700"
            >
              Explore pricing
            </a>
          </div>
        </aside>
      </div>
    </section>
  );
};
