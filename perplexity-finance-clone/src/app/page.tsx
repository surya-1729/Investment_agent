import Link from "next/link";
import Image from "next/image";
import {
  ArrowRight,
  LineChart,
  ShieldCheck,
  Layers,
  Timer,
  Sparkles,
  Globe,
} from "lucide-react";
import { SearchExperience } from "@/components/search-experience";

export default function Home() {
  const featureHighlights = [
    {
      icon: <Sparkles className="h-5 w-5 text-indigo-500" />,
      title: "Copilot summarisation",
      description:
        "Natural language answers distill multi-source financial data with bulletproof numerical accuracy.",
    },
    {
      icon: <ShieldCheck className="h-5 w-5 text-emerald-500" />,
      title: "Verifiable sources",
      description:
        "Every claim links back to fundamentals, market data, or news with full citation and timestamp.",
    },
    {
      icon: <Timer className="h-5 w-5 text-sky-500" />,
      title: "Under two seconds",
      description:
        "Edge-cached aggregation and streaming keep response latency incredibly low, even during market hours.",
    },
    {
      icon: <Layers className="h-5 w-5 text-amber-500" />,
      title: "Composable building blocks",
      description:
        "Embed the API, white-label the client, and orchestrate insights directly into your surfaces.",
    },
  ];

  const workflow = [
    {
      title: "Ingest & vectorise",
      body: "Company fundamentals, market trades, and news sentiment are normalised every minute into a vector lake.",
    },
    {
      title: "Reason & synthesise",
      body: "Semantic retrieval aligns your query with the right data slices before a structured reasoning pass.",
    },
    {
      title: "Cite & deliver",
      body: "Insights ship with citations, metrics, and charts that drop into your dashboards or client comms.",
    },
  ];

  const pricing = [
    {
      tier: "Starter",
      price: "$49",
      cadence: "per seat / month",
      highlight: "Perfect for independent analysts and boutique advisory teams.",
      features: [
        "400 questions per month",
        "Equity & ETF coverage",
        "Alpha Vantage (demo) key included",
        "Email support within 24h",
      ],
      cta: "Start free trial",
    },
    {
      tier: "Growth",
      price: "$149",
      cadence: "per seat / month",
      highlight: "Scale client delivery with advanced analytics and webhook pushes.",
      features: [
        "Unlimited questions",
        "Streaming responses",
        "Custom theming & embed SDK",
        "Slack + webhook alerts",
      ],
      cta: "Book a demo",
      popular: true,
    },
    {
      tier: "Scale",
      price: "Talk to us",
      cadence: "",
      highlight: "Purpose-built data residency, bespoke connectors, and SLAs.",
      features: [
        "Dedicated VPC deployment",
        "GraphQL + Snowflake bridges",
        "Fine-tuned reasoning models",
        "24/7 premium support",
      ],
      cta: "Contact sales",
    },
  ];

  const faqs = [
    {
      question: "Which data providers power OracleIQ?",
      answer:
        "We ship with Alpha Vantage out of the box and support Polygon, Intrinio, and Snowflake as bring-your-own-data connectors on Growth plans and beyond.",
    },
    {
      question: "Is this production-ready or a concept?",
      answer:
        "This is a full-stack SaaS scaffold inspired by Perplexity Finance. Swap in your branding, wire up authentication, and deploy to Vercel to go live in minutes.",
    },
    {
      question: "How do rate limits work?",
      answer:
        "Starter plans include the Alpha Vantage demo key for evaluation. Add your own key in the environment variables to unlock higher concurrency and remove demo limits.",
    },
    {
      question: "Can I integrate it into my existing platform?",
      answer:
        "Yes. Serverless API routes provide JSON responses while embeddable React primitives and web components are available for white-label delivery on Growth plans.",
    },
  ];

  return (
    <div className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top,var(--tw-gradient-stops))] from-indigo-100/70 via-white to-white" />
      <header className="relative mx-auto flex max-w-7xl flex-col gap-12 px-6 pb-24 pt-16 sm:px-10 lg:px-12">
        <nav className="flex items-center justify-between rounded-3xl border border-white/60 bg-white/80 px-6 py-4 shadow-xl shadow-zinc-300/30 backdrop-blur">
          <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-600 via-sky-500 to-emerald-500 text-white shadow-lg">
                <LineChart className="h-5 w-5" />
            </div>
            <div>
              <p className="text-base font-semibold text-zinc-900">OracleIQ Finance</p>
              <p className="text-xs text-zinc-500">Perplexity Finance reimagined</p>
            </div>
          </div>
          <div className="hidden items-center gap-6 text-sm font-medium text-zinc-600 md:flex">
            <a href="#product" className="transition hover:text-indigo-600">
              Product
            </a>
            <a href="#workflow" className="transition hover:text-indigo-600">
              Workflow
            </a>
            <a href="#pricing" className="transition hover:text-indigo-600">
              Pricing
            </a>
            <a href="#faq" className="transition hover:text-indigo-600">
              FAQ
            </a>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="#pricing"
              className="hidden rounded-full border border-zinc-200 px-4 py-2 text-sm font-medium text-zinc-700 transition hover:border-indigo-200 hover:text-indigo-600 md:inline-flex"
            >
              View plans
            </Link>
            <Link
              href="#experience"
              className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-indigo-600 via-sky-500 to-emerald-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-300/50 transition hover:shadow-indigo-400/60"
            >
              Launch console
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </nav>

        <div className="grid gap-14 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)]">
          <div className="space-y-8">
            <span className="inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-indigo-50/80 px-3 py-1 text-xs font-semibold text-indigo-600">
              <Globe className="h-3.5 w-3.5" />
              Ask the market anything
            </span>
            <h1 className="text-4xl font-bold tracking-tight text-zinc-900 sm:text-5xl md:text-6xl">
              The fastest way to deliver finance answers with provenance
            </h1>
            <p className="max-w-2xl text-lg text-zinc-600">
              OracleIQ Finance mirrors the Perplexity Finance experience with a
              Next.js SaaS stack. Ask a question, receive sourced fundamentals, price
              action, and news sentiment — all packaged for client-ready delivery.
            </p>

            <div className="grid gap-6 sm:grid-cols-3">
              <div className="rounded-3xl border border-zinc-200 bg-white/80 p-6 shadow-md shadow-zinc-200/60">
                <p className="text-3xl font-semibold text-zinc-900">45k+</p>
                <p className="mt-2 text-xs uppercase tracking-wide text-zinc-500">
                  Daily questions supported
                </p>
              </div>
              <div className="rounded-3xl border border-zinc-200 bg-white/80 p-6 shadow-md shadow-zinc-200/60">
                <p className="text-3xl font-semibold text-zinc-900">99.9%</p>
                <p className="mt-2 text-xs uppercase tracking-wide text-zinc-500">
                  Uptime on enterprise plans
                </p>
              </div>
              <div className="rounded-3xl border border-zinc-200 bg-white/80 p-6 shadow-md shadow-zinc-200/60">
                <p className="text-3xl font-semibold text-zinc-900">2.1s</p>
                <p className="mt-2 text-xs uppercase tracking-wide text-zinc-500">
                  Median response time
                </p>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-4">
              <Link
                href="#experience"
                className="inline-flex items-center gap-2 rounded-full bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-zinc-800"
              >
                Try the demo
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href="#pricing"
                className="inline-flex items-center gap-2 rounded-full border border-transparent bg-white/80 px-5 py-2.5 text-sm font-semibold text-zinc-700 shadow hover:border-zinc-200 hover:text-zinc-900"
              >
                Explore pricing
              </Link>
            </div>
          </div>

          <div className="relative">
            <div className="absolute -inset-6 rounded-[40px] bg-gradient-to-br from-indigo-200 via-white to-emerald-100 opacity-70 blur-2xl" />
            <div className="relative rounded-[36px] border border-white/70 bg-white/80 p-8 shadow-2xl shadow-indigo-200/50 backdrop-blur">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-indigo-600/90 text-white">
                  <Sparkles className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-zinc-900">
                    Guided analyst copilots
                  </p>
                  <p className="text-xs text-zinc-500">
                    Bring conversational insight to every stakeholder.
                  </p>
                </div>
              </div>
              <Image
                src="https://images.unsplash.com/photo-1556740749-887f6717d7e4?auto=format&fit=crop&w=1200&q=80"
                alt="Finance workspace illustration"
                width={640}
                height={420}
                className="mt-6 h-72 w-full rounded-[28px] object-cover"
              />
              <p className="mt-4 text-sm text-zinc-600">
                Prebuilt React and REST primitives let you embed the OracleIQ assistant
                into portals, CRMs, and research workflows.
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="relative mx-auto flex max-w-6xl flex-col gap-24 px-6 pb-32 sm:px-10 lg:px-12">
        <section
          id="product"
          className="grid gap-6 rounded-[40px] border border-white/70 bg-white/80 p-10 shadow-xl shadow-indigo-200/50 backdrop-blur-lg md:grid-cols-2"
        >
          <div className="space-y-4">
            <span className="rounded-full bg-zinc-900 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-white">
              Why teams switch
            </span>
            <h2 className="text-3xl font-semibold text-zinc-900">
              Everything Perplexity Finance offers, packaged for your brand
            </h2>
            <p className="text-sm text-zinc-600">
              OracleIQ Finance is a feature-complete clone scaffold that combines
              structured data retrieval, reasoning, and citation pipelines. Customise it
              for clients or internal desks without rebuilding the wheel.
            </p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {featureHighlights.map((feature) => (
              <div
                key={feature.title}
                className="rounded-3xl border border-zinc-200 bg-white/80 p-6 shadow-sm shadow-zinc-200/60 transition hover:border-indigo-200 hover:shadow-md"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-indigo-50">
                  {feature.icon}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-zinc-900">
                  {feature.title}
                </h3>
                <p className="mt-2 text-sm text-zinc-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </section>

        <div id="experience">
          <SearchExperience />
        </div>

        <section
          id="workflow"
          className="grid gap-8 rounded-[36px] border border-white/70 bg-white/75 p-10 shadow-lg shadow-indigo-100/40 backdrop-blur md:grid-cols-[0.7fr_1fr]"
        >
          <div>
            <span className="rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold text-indigo-600">
              Built for scale
            </span>
            <h2 className="mt-4 text-3xl font-semibold text-zinc-900">
              How OracleIQ keeps answers accurate
            </h2>
            <p className="mt-3 text-sm text-zinc-600">
              Blend deterministic data pipelines with semantic reasoning to produce
              explanations clients can act on.
            </p>
          </div>
          <div className="grid gap-6">
            {workflow.map((stage, index) => (
              <div
                key={stage.title}
                className="flex gap-4 rounded-3xl border border-zinc-200 bg-white/85 p-6 shadow-sm"
              >
                <div className="flex h-12 w-12 flex-none items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-600 to-sky-500 text-lg font-semibold text-white shadow-lg">
                  {index + 1}
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-zinc-900">{stage.title}</h3>
                  <p className="mt-2 text-sm text-zinc-600">{stage.body}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section
          id="pricing"
          className="rounded-[36px] border border-white/70 bg-white/80 p-10 shadow-xl shadow-indigo-200/40 backdrop-blur"
        >
          <div className="mx-auto max-w-3xl text-center">
            <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-600">
              Pricing
            </span>
            <h2 className="mt-4 text-3xl font-semibold text-zinc-900">
              Flexible pricing for research shops of every size
            </h2>
            <p className="mt-3 text-sm text-zinc-600">
              Start free, upgrade when you need white-labeled embeds, advanced data
              connectors, or bespoke infrastructure.
            </p>
          </div>

          <div className="mt-12 grid gap-6 lg:grid-cols-3">
            {pricing.map((plan) => (
              <div
                key={plan.tier}
                className={`relative flex flex-col gap-6 rounded-3xl border border-zinc-200 bg-white/85 p-8 shadow-lg shadow-zinc-200/50 ${
                  plan.popular
                    ? "border-indigo-400/80 shadow-indigo-200/60 ring-2 ring-indigo-200"
                    : ""
                }`}
              >
                {plan.popular ? (
                  <span className="absolute right-6 top-6 rounded-full bg-indigo-600 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-white">
                    Most popular
                  </span>
                ) : null}
                <div>
                  <p className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
                    {plan.tier}
                  </p>
                  <p className="mt-3 text-4xl font-semibold text-zinc-900">
                    {plan.price}
                    <span className="ml-2 text-base font-medium text-zinc-500">
                      {plan.cadence}
                    </span>
                  </p>
                  <p className="mt-3 text-sm text-zinc-600">{plan.highlight}</p>
                </div>
                <ul className="space-y-3 text-sm text-zinc-600">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-2">
                      <span className="mt-1 h-1.5 w-1.5 flex-none rounded-full bg-emerald-500" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/#contact"
                  className={`inline-flex items-center justify-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition ${
                    plan.popular
                      ? "bg-indigo-600 text-white shadow-lg shadow-indigo-300/50 hover:bg-indigo-700"
                      : "border border-zinc-200 bg-white text-zinc-700 hover:border-indigo-200 hover:text-indigo-600"
                  }`}
                >
                  {plan.cta}
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            ))}
          </div>
        </section>

        <section
          id="faq"
          className="grid gap-10 rounded-[32px] border border-white/60 bg-white/75 p-10 shadow-lg shadow-indigo-100/40 backdrop-blur md:grid-cols-[0.7fr_1fr]"
        >
          <div>
            <span className="rounded-full bg-zinc-900 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-white">
              FAQ
            </span>
            <h2 className="mt-4 text-3xl font-semibold text-zinc-900">
              Answers before you go live
            </h2>
            <p className="mt-3 text-sm text-zinc-600">
              Quick context for builders cloning the Perplexity Finance experience on
              Next.js and Tailwind.
            </p>
          </div>
          <div className="space-y-5">
            {faqs.map((faq) => (
              <div
                key={faq.question}
                className="rounded-3xl border border-zinc-200 bg-white/80 p-6 shadow-sm shadow-zinc-200/60"
              >
                <p className="text-sm font-semibold text-zinc-900">{faq.question}</p>
                <p className="mt-2 text-sm text-zinc-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="border-t border-white/40 bg-white/70">
        <div className="mx-auto flex max-w-6xl flex-col gap-6 px-6 py-12 text-sm text-zinc-500 sm:flex-row sm:items-center sm:justify-between sm:px-10">
          <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-600 via-sky-500 to-emerald-500 text-white">
                <LineChart className="h-5 w-5" />
            </div>
            <div>
              <p className="text-base font-semibold text-zinc-800">OracleIQ Finance</p>
              <p className="text-xs text-zinc-500">
                Clone-ready SaaS inspired by Perplexity Finance
              </p>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-4 text-xs text-zinc-500">
            <span>© {new Date().getFullYear()} OracleIQ Labs.</span>
            <Link href="mailto:hello@oracleiq.finance" className="hover:text-indigo-600">
              Contact
            </Link>
            <Link href="https://github.com" className="hover:text-indigo-600">
              GitHub
            </Link>
            <Link href="https://vercel.com" className="hover:text-indigo-600">
              Deploy to Vercel
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
