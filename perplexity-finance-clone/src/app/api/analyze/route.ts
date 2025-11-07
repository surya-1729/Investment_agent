import { NextResponse } from "next/server";
import {
  DataSource,
  Insight,
  OracleIQError,
  OracleIQResponse,
  TimelinePoint,
} from "@/lib/types";
import {
  formatCompactCurrency,
  formatCurrency,
  formatNumber,
  formatPercent,
  toDelta,
} from "@/lib/format";

const API_BASE = "https://www.alphavantage.co/query";
const API_KEY = process.env.ALPHAVANTAGE_API_KEY || "demo";

type AlphaParams = Record<string, string | number | undefined>;

type SymbolMatch = {
  symbol: string;
  name: string;
  region?: string;
  matchScore?: number;
};

class ApiError extends Error {
  status: number;
  type: OracleIQError["type"];

  constructor(message: string, status = 500, type: OracleIQError["type"] = "unknown") {
    super(message);
    this.status = status;
    this.type = type;
  }
}

const alphaFetch = async <T = unknown>(params: AlphaParams): Promise<T> => {
  const search = new URLSearchParams({
    ...Object.fromEntries(
      Object.entries(params).map(([key, value]) => [key, String(value)])
    ),
    apikey: API_KEY,
  });

  const response = await fetch(`${API_BASE}?${search.toString()}`, {
    headers: {
      "Content-Type": "application/json",
    },
    next: { revalidate: 0 },
  });

  if (!response.ok) {
    throw new ApiError(
      `Alpha Vantage responded with status ${response.status}`,
      502,
      "upstream"
    );
  }

  const json = (await response.json()) as Record<string, unknown>;

  if ("Note" in json) {
    throw new ApiError(
      "Upstream rate limit reached. Try again in a minute or upgrade your API plan.",
      429,
      "rate_limit"
    );
  }

  if ("Information" in json) {
    throw new ApiError(String(json.Information), 400, "upstream");
  }

  return json as T;
};

const findBestMatch = (payload: Record<string, unknown>): SymbolMatch | null => {
  const matches = payload?.bestMatches as Array<Record<string, string>> | undefined;
  if (!Array.isArray(matches) || matches.length === 0) return null;

  const [best] = matches;
  return {
    symbol: best["1. symbol"],
    name: best["2. name"],
    region: best["4. region"],
    matchScore: Number(best["9. matchScore"]),
  };
};

type OverviewPayload = {
  Symbol?: string;
  Name?: string;
  MarketCapitalization?: string;
  PERatio?: string;
  PEGRatio?: string;
  EPS?: string;
  DividendYield?: string;
  ProfitMargin?: string;
  ReturnOnEquityTTM?: string;
  Beta?: string;
  WeekHigh52?: string;
  WeekLow52?: string;
  AnalystTargetPrice?: string;
  Description?: string;
  Currency?: string;
  Sector?: string;
  Industry?: string;
};

type TimeSeriesPayload = {
  "Time Series (Daily)"?: Record<
    string,
    {
      "1. open": string;
      "2. high": string;
      "3. low": string;
      "4. close": string;
      "5. volume": string;
    }
  >;
};

type NewsItem = {
  title: string;
  url: string;
  summary: string;
  time_published: string;
  authors: string[];
  source: string;
  ticker_sentiment: Array<{
    ticker: string;
    ticker_sentiment_label: string;
    ticker_sentiment_score: string;
  }>;
};

type NewsPayload = {
  feed?: NewsItem[];
};

const buildTimeline = (series: TimeSeriesPayload): TimelinePoint[] => {
  const points = series?.["Time Series (Daily)"] ?? {};
  const entries = Object.entries(points);
  return entries
    .slice(0, 60)
    .map(([date, values]) => ({
      date,
      value: Number(values["4. close"]),
      volume: Number(values["5. volume"]),
    }))
    .filter((point) => !Number.isNaN(point.value))
    .reverse();
};

const normalizeNews = (payload: NewsPayload): DataSource[] => {
  if (!Array.isArray(payload.feed)) return [];
  return payload.feed.slice(0, 6).map((item) => ({
    name: `${item.source}: ${item.title}`,
    url: item.url,
    type: "news" as const,
    snippet: item.summary,
    publishedAt: item.time_published,
  }));
};

const computePriceInsights = (
  timeline: TimelinePoint[]
): { latest?: TimelinePoint; previous?: TimelinePoint } => {
  if (!timeline.length) return {};
  const latest = timeline[timeline.length - 1];
  const previous = timeline[timeline.length - 2];
  return { latest, previous };
};

const buildInsights = (
  overview: OverviewPayload,
  timeline: TimelinePoint[]
): Insight[] => {
  const { latest, previous } = computePriceInsights(timeline);
  const delta = toDelta(latest?.value, previous?.value);
  const latestVolume = latest?.volume;

  const valuationMetrics = [
    {
      label: "Market Cap",
      value: formatCompactCurrency(overview.MarketCapitalization),
    },
    {
      label: "P/E",
      value: formatNumber(overview.PERatio),
      hint: "Price-to-earnings ratio",
    },
    {
      label: "PEG",
      value: formatNumber(overview.PEGRatio),
    },
  ];

  const performanceMetrics = [
    {
      label: "Last Close",
      value: formatCurrency(latest?.value),
      delta:
        delta && latest?.value !== undefined
          ? {
              value: `${formatCurrency(latest.value - (previous?.value ?? 0))}`,
              isPositive: delta.isPositive,
            }
          : undefined,
    },
    {
      label: "Daily Change",
      value: delta ? formatPercent(delta.changePercent) : "–",
      delta: delta
        ? {
            value: `${formatPercent(delta.changePercent)}`,
            isPositive: delta.isPositive,
          }
        : undefined,
    },
    {
      label: "Volume",
      value: formatNumber(latestVolume, { fractionDigits: 0 }),
    },
  ];

  const qualityMetrics = [
    {
      label: "Return on Equity",
      value: formatPercent(Number(overview.ReturnOnEquityTTM) / 100),
    },
    {
      label: "Profit Margin",
      value: formatPercent(Number(overview.ProfitMargin) / 100),
    },
    {
      label: "Dividend Yield",
      value: formatPercent(Number(overview.DividendYield)),
    },
  ];

  const momentumMetrics = [
    {
      label: "52W High",
      value: formatCurrency(overview.WeekHigh52),
    },
    {
      label: "52W Low",
      value: formatCurrency(overview.WeekLow52),
    },
    {
      label: "Target Price",
      value: formatCurrency(overview.AnalystTargetPrice),
    },
  ];

  return [
    {
      title: "Valuation Snapshot",
      description:
        "Core valuation indicators benchmark the company against growth expectations and profitability.",
      metrics: valuationMetrics,
      kind: "valuation",
    },
    {
      title: "Price Performance",
      description:
        "Live market pricing and daily momentum assess the most recent move.",
      metrics: performanceMetrics,
      kind: "performance",
    },
    {
      title: "Quality & Income",
      description:
        "Operational efficiency and shareholder yield metrics describe fundamental quality.",
      metrics: qualityMetrics,
      kind: "quality",
    },
    {
      title: "Momentum Guardrails",
      description:
        "52-week bands and analyst targets contextualize upside and downside.",
      metrics: momentumMetrics,
      kind: "momentum",
    },
  ];
};

const buildSources = (
  overview: OverviewPayload,
  news: DataSource[],
  symbol: string
): DataSource[] => {
  const baseSources: DataSource[] = [
    {
      name: `Alpha Vantage overview (${symbol})`,
      url: "https://www.alphavantage.co/documentation/#company-overview",
      type: "fundamental",
    },
    {
      name: `Alpha Vantage daily prices (${symbol})`,
      url: "https://www.alphavantage.co/documentation/#daily",
      type: "market",
    },
  ];

  if (overview.Description) {
    baseSources.push({
      name: "Company description",
      snippet: overview.Description.slice(0, 240),
      type: "analytics",
    });
  }

  return [...baseSources, ...news];
};

const buildSummary = (
  overview: OverviewPayload,
  symbol: string,
  timeline: TimelinePoint[],
  news: DataSource[]
): string => {
  const { latest, previous } = computePriceInsights(timeline);
  const delta = toDelta(latest?.value, previous?.value);

  const direction = delta
    ? delta.isPositive
      ? "up"
      : "down"
    : undefined;

  const priceSentence =
    latest && delta
      ? `${overview.Name ?? symbol} (${symbol}) closed at ${formatCurrency(
          latest.value
        )}, ${direction} ${formatPercent(delta.changePercent)} on the session.`
      : `${overview.Name ?? symbol} (${symbol}) latest close is ${formatCurrency(
          latest?.value
        )}.`;

  const marketCapSentence = overview.MarketCapitalization
    ? `The company carries a market capitalization of ${formatCompactCurrency(
        overview.MarketCapitalization
      )} with a P/E of ${formatNumber(overview.PERatio)}.`
    : "";

  const qualitySentence =
    overview.ReturnOnEquityTTM || overview.DividendYield
      ? `Quality markers show ${
          overview.ReturnOnEquityTTM
            ? `ROE of ${formatPercent(
                Number(overview.ReturnOnEquityTTM) / 100
              )}`
            : ""
        }${
          overview.DividendYield
            ? ` and dividend yield near ${formatPercent(
                Number(overview.DividendYield)
              )}`
            : ""
        }.`
      : "";

  const newsSentence = news.length
    ? `Latest coverage: ${news[0].name.replace(/^[^:]+:\s?/, "")}.`
    : "";

  return [priceSentence, marketCapSentence, qualitySentence, newsSentence]
    .filter(Boolean)
    .join(" ");
};

export const maxDuration = 20;

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as { query?: string };
    const query = body?.query?.trim();

    if (!query) {
      throw new ApiError("Query is required", 400, "validation");
    }

    const searchPayload = await alphaFetch<Record<string, unknown>>({
      function: "SYMBOL_SEARCH",
      keywords: query,
    });

    const bestMatch = findBestMatch(searchPayload);
    if (!bestMatch?.symbol) {
      throw new ApiError(
        "No tradable symbols were found. Try a different ticker or company name.",
        404,
        "validation"
      );
    }

    const [overview, timeseries, newsPayload] = await Promise.all([
      alphaFetch<OverviewPayload>({
        function: "OVERVIEW",
        symbol: bestMatch.symbol,
      }),
      alphaFetch<TimeSeriesPayload>({
        function: "TIME_SERIES_DAILY",
        symbol: bestMatch.symbol,
      }),
      alphaFetch<NewsPayload>({
        function: "NEWS_SENTIMENT",
        tickers: bestMatch.symbol,
        limit: 12,
        sort: "LATEST",
      }),
    ]);

    const timeline = buildTimeline(timeseries);
    const news = normalizeNews(newsPayload);

    const insights = buildInsights(overview, timeline);
    const sources = buildSources(overview, news, bestMatch.symbol);
    const summary = buildSummary(overview, bestMatch.symbol, timeline, news);

    const payload: OracleIQResponse = {
      query,
      symbol: overview.Symbol ?? bestMatch.symbol,
      companyName: overview.Name ?? bestMatch.name,
      summary,
      insights,
      timeline,
      sources,
      news,
      generatedAt: new Date().toISOString(),
    };

    return NextResponse.json(payload);
  } catch (error) {
    if (error instanceof ApiError) {
      const payload: OracleIQError = {
        error: error.message,
        detail: error.message,
        type: error.type,
      };
      return NextResponse.json(payload, { status: error.status });
    }

    console.error("analyze route unexpected error", error);
    const payload: OracleIQError = {
      error: "Unexpected server error",
      type: "unknown",
    };
    return NextResponse.json(payload, { status: 500 });
  }
}
