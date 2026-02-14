import { Link, Outlet } from 'react-router-dom'

function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">CasaBricks</p>
            <h1 className="text-lg font-semibold">BuyNoida Frontend</h1>
          </div>
          <nav className="flex items-center gap-4 text-sm text-slate-700">
            <Link to="/" className="hover:text-slate-900">Home</Link>
            <Link to="/listings" className="hover:text-slate-900">Listings</Link>
            <Link to="/inquiry" className="hover:text-slate-900">Inquiry</Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}

export default AppLayout
