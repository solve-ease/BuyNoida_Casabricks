import { Link } from 'react-router-dom'

function HomePage() {
  return (
    <section className="space-y-4">
      <p className="inline-flex rounded-md bg-emerald-100 px-2 py-1 text-xs font-medium text-emerald-700">
        Phase 0 active
      </p>
      <h2 className="text-2xl font-semibold">App shell is ready for feature implementation.</h2>
      <p className="max-w-3xl text-slate-600">
        This baseline replaces the legacy coming-soon UI and provides routing, configuration validation,
        logging, and API client scaffolding for upcoming phases.
      </p>
      <div className="flex flex-wrap gap-3">
        <Link to="/listings" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white">
          Open Listings Placeholder
        </Link>
        <Link to="/property/sample" className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700">
          Open Property Placeholder
        </Link>
      </div>
    </section>
  )
}

export default HomePage
