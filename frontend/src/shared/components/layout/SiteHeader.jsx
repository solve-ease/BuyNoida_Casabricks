import { AnimatePresence, motion } from 'framer-motion'
import { Home, Menu, MessageCircle, X } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom'

const navLinkClass = ({ isActive }) =>
  `relative pb-1 text-sm font-medium transition-colors ${isActive ? 'text-brand' : 'text-slate-600 hover:text-slate-900'}`

function SiteHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { pathname } = useLocation()

  const aboutHref = useMemo(() => (pathname === '/' ? '#about' : '/#about'), [pathname])

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/70 bg-white/95 backdrop-blur-md">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-3 lg:px-6">
        <Link to="/" className="inline-flex items-center gap-2 text-slate-700 transition-colors hover:text-slate-900">
          <span className="rounded-full bg-slate-100 p-1.5">
            <Home size={14} strokeWidth={2.4} />
          </span>
          <span className="text-xl font-semibold tracking-tight">BuyNoida</span>
        </Link>

        <nav className="hidden items-center gap-7 md:flex">
          <NavLink to="/" className={navLinkClass}>
            {({ isActive }) => (
              <span className="relative">
                Home
                {isActive && (
                  <motion.span
                    layoutId="header-active-dot"
                    className="absolute -bottom-3 left-1/2 h-1.5 w-1.5 -translate-x-1/2 rounded-full bg-brand"
                  />
                )}
              </span>
            )}
          </NavLink>
          <a href={aboutHref} className="text-sm font-medium text-slate-600 transition-colors hover:text-slate-900">
            About
          </a>
        </nav>

        <div className="hidden items-center gap-3 md:flex">
          <Link
            to="/inquiry"
            className="rounded-xl bg-brand px-6 py-2.5 text-sm font-semibold text-white transition-all hover:-translate-y-0.5 hover:bg-brand-dark"
          >
            Contact Us
          </Link>
          <a
            href="https://wa.me/919999999999"
            target="_blank"
            rel="noreferrer"
            aria-label="Open WhatsApp"
            className="rounded-xl border border-slate-200 bg-white p-2.5 text-brand transition-colors hover:bg-slate-100"
          >
            <MessageCircle size={18} />
          </a>
        </div>

        <button
          type="button"
          aria-label="Toggle navigation menu"
          onClick={() => setIsMenuOpen((state) => !state)}
          className="rounded-xl border border-slate-200 bg-white p-2 text-slate-700 md:hidden"
        >
          {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="border-t border-slate-200 bg-white px-4 pb-4 pt-3 md:hidden"
          >
            <nav className="flex flex-col gap-3">
              <Link to="/" onClick={() => setIsMenuOpen(false)} className="text-sm font-medium text-slate-700">
                Home
              </Link>
              <a href={aboutHref} onClick={() => setIsMenuOpen(false)} className="text-sm font-medium text-slate-700">
                About
              </a>
              <Link
                to="/inquiry"
                onClick={() => setIsMenuOpen(false)}
                className="mt-1 inline-flex w-fit rounded-lg bg-brand px-4 py-2 text-sm font-semibold text-white"
              >
                Contact Us
              </Link>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}

export default SiteHeader
