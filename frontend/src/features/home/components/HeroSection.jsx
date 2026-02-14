import { motion } from 'framer-motion'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const BUDGET_OPTIONS = ['Under 75L', '75L-1.5Cr', '1.5Cr+']

function HeroSection() {
  const [selectedBudget, setSelectedBudget] = useState(BUDGET_OPTIONS[0])
  const navigate = useNavigate()

  const handleStartExploring = () => {
    navigate(`/listings?budget=${encodeURIComponent(selectedBudget)}`)
  }

  return (
    <section className="relative overflow-hidden bg-hero-gradient px-4 pb-20 pt-28 md:pt-32 lg:pb-28">
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-[#dfe5ef] to-transparent" />
      <div className="pointer-events-none absolute -left-32 bottom-8 h-60 w-[70vw] rounded-[100%] bg-wave-light/80 blur-3xl" />
      <img
        src="/home-img.png"
        alt="Modern property in Noida"
        className="pointer-events-none absolute bottom-0 right-0 hidden h-[70%] max-h-[540px] w-[48%] object-cover md:block"
      />

      <div className="relative mx-auto flex w-full max-w-7xl flex-col items-center">
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="text-center text-3xl font-medium tracking-tight text-slate-800 md:text-4xl"
        >
          Discover Noida Properties
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08, duration: 0.55 }}
          className="mt-2 text-center text-[68px] font-bold leading-[0.95] tracking-[0.03em] text-brand-ink sm:text-[92px] md:text-[140px] lg:text-[180px]"
          style={{ fontFamily: "'K2D', sans-serif", fontWeight: 700 }}
        >
          VISUALLY
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.16, duration: 0.5 }}
          className="mt-4 text-center text-lg text-slate-500"
        >
          Answer 3 quick questions and explore curated plots instantly
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.24, duration: 0.5 }}
          className="mt-6 flex flex-wrap items-center justify-center gap-3"
        >
          <button
            type="button"
            onClick={handleStartExploring}
            className="rounded-xl px-8 py-3 text-sm font-semibold text-white transition-all"
            style={{ backgroundColor: 'var(--navy-blue)' }}
          >
            Start Exploring
          </button>
          <Link
            to="/listings"
            className="rounded-xl border border-brand/45 bg-transparent px-8 py-3 text-sm font-semibold text-brand transition-colors hover:bg-brand/5"
          >
            View Listings
          </Link>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.32, duration: 0.55 }}
          className="mt-16 w-full max-w-xl rounded-2xl bg-white/10 p-6 "
        >
          <h2 className="text-center text-2xl font-semibold text-slate-800">What’s your budget?</h2>
          <div className="mt-7 grid grid-cols-1 gap-3 sm:grid-cols-3">
            {BUDGET_OPTIONS.map((option) => (
              <button
                key={option}
                type="button"
                onClick={() => setSelectedBudget(option)}
                className="inline-flex items-center justify-center gap-2 rounded-lg py-2 text-base font-medium text-slate-600"
              >
                <span
                  className={`h-5 w-5 rounded-full border-2 ${
                    selectedBudget === option ? 'border-brand bg-white' : 'border-slate-400 bg-transparent'
                  }`}
                >
                  <span
                    className={`m-0.5 block h-3 w-3 rounded-full ${
                      selectedBudget === option ? 'bg-brand' : 'bg-transparent'
                    }`}
                  />
                </span>
                {option}
              </button>
            ))}
          </div>
          <div className="mx-auto mt-4 flex w-28 justify-center gap-2">
            <span className="h-[3px] w-12 rounded-full bg-brand" />
            <span className="h-[3px] w-4 rounded-full bg-slate-300" />
            <span className="h-[3px] w-4 rounded-full bg-slate-300" />
          </div>
        </motion.div>
      </div>
    </section>
  )
}

export default HeroSection
