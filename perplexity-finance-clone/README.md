# OracleIQ Finance · Perplexity Finance Clone SaaS

OracleIQ Finance is a polished SaaS starter inspired by the Perplexity Finance experience. It pairs a Next.js App Router front-end with serverless routes that orchestrate Alpha Vantage fundamentals, market data, and news sentiment into verifiable insights.

https://github.com/ - Replace with your repository URL

## ✨ Highlights

- **Conversational analytics** – Ask natural-language questions and receive sourced fundamentals, price action, and news sentiment in seconds.
- **Multi-source citations** – Responses carry Alpha Vantage fundamentals, pricing, and news links to keep downstream viewers confident.
- **Tailwind UI shell** – A refined marketing site with hero, feature grid, workflow story, pricing, and FAQ sections.
- **Ready-to-extend API** – `/api/analyze` aggregates Alpha Vantage endpoints and returns structured JSON for reuse in other surfaces.

## 🧱 Tech Stack

- [Next.js 15 App Router](https://nextjs.org/) with TypeScript
- Tailwind CSS (via `@tailwindcss/postcss`)
- React Server Components + Client Islands
- Alpha Vantage REST APIs (demo key fallback)
- ESLint (Next config), `clsx`, `tailwind-merge`, `lucide-react`

## 🚀 Getting Started

Clone and install dependencies:

```bash
git clone <repo-url>
cd perplexity-finance-clone
npm install
```

Run the development server:

```bash
npm run dev
# http://localhost:3000
```

### Required Environment Variables

Create `.env.local` in the project root:

```bash
ALPHAVANTAGE_API_KEY=your_alpha_vantage_key
```

- The Alpha Vantage demo key is used automatically if this variable is absent, but it is heavily rate limited (5 req/minute).
- Supplying your own key is recommended for interactive testing and production.

### Useful Commands

| Command            | Description                           |
| ------------------ | ------------------------------------- |
| `npm run dev`      | Start Next.js in development mode     |
| `npm run build`    | Create an optimized production build  |
| `npm start`        | Run the production build locally      |
| `npm run lint`     | Execute ESLint against the codebase   |

## 🗂️ Project Structure

```
src/
  app/
    api/analyze/route.ts      # Serverless aggregation of Alpha Vantage data
    layout.tsx                # Global layout, metadata, fonts
    page.tsx                  # Marketing + product experience
    globals.css               # Tailwind + custom design tokens
  components/
    search-experience.tsx     # Interactive finance copilot experience
    insight-card.tsx          # Metric cards rendered from API insights
    sparkline.tsx             # SVG-based price history chart
  lib/
    format.ts                 # Currency/percent/number formatting helpers
    types.ts                  # Shared API contract types
    utils.ts                  # Tailwind class merge helper
```

## 🧠 How `/api/analyze` Works

1. **Symbol discovery** – Calls `SYMBOL_SEARCH` to resolve user intent to a tradable ticker.
2. **Data aggregation** – Fetches company overview, daily time series, and news sentiment (Alpha Vantage).
3. **Insight synthesis** – Computes valuation, performance, quality, and momentum cards with formatted metrics.
4. **Cited response** – Returns a summary string, structured insights, timeline points, and linked sources.

Error handling covers missing symbols, upstream rate limits, and network issues with descriptive responses for the UI.

## 🧭 Next Steps & Extensions

- Add authentication (NextAuth, Clerk, or Supabase) and per-user quota tracking.
- Swap Alpha Vantage for Polygon, Finnhub, or a Snowflake warehouse via the same abstraction pattern.
- Stream responses (Server-Sent Events) for incremental reasoning output.
- Integrate persistence for saved queries, watchlists, and collaborative annotations.

## 📄 License

MIT – use it as a base for client demos, internal tools, or production SaaS deployments. Update branding, copy, and data providers to suit your needs.
