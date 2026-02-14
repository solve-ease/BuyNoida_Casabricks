import { AnimatePresence, motion } from 'framer-motion'
import { Home, Menu, X } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom'

const navLinkClass = ({ isActive }) =>
  `relative pb-1 text-sm font-medium transition-colors ${isActive ? 'text-brand' : 'text-slate-600 hover:text-slate-900'}`

function SiteHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isScrolled, setIsScrolled] = useState(false)
  const { pathname } = useLocation()

  const aboutHref = useMemo(() => (pathname === '/' ? '#about' : '/#about'), [pathname])

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <header className="fixed left-0 right-0 top-0 z-50 px-4 pt-4 transition-all duration-300">
      <div
        className={`mx-auto max-w-7xl rounded-2xl border transition-all duration-300 ${isScrolled
            ? 'border-white/40 bg-white/70 shadow-lg backdrop-blur-2xl'
            : 'border-slate-200/40 bg-white/60 backdrop-blur-md'
        }`}
      >
        <div className="flex items-center justify-between px-4 py-3 lg:px-6">
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
                    className="absolute -bottom-3 left-1/2 h-2 w-2 -translate-x-1/2 rounded-full border-2 border-white shadow-sm"
                    style={{ backgroundColor: 'var(--navy-blue)' }}
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
            className="rounded-xl px-6 py-2.5 text-sm font-semibold text-white transition-all hover:-translate-y-0.5"
            style={{color:'white', backgroundColor: 'var(--navy-blue)' }}
          >
            Contact Us
          </Link>
          <a
            href="https://wa.me/919999999999"
            target="_blank"
            rel="noreferrer"
            aria-label="Open WhatsApp"
            className="flex items-center justify-center rounded-xl p-2.5 transition-all"
            
          >
            <img src="/whatsapp-color-svgrepo-com.png" alt="WhatsApp" className="h-5 w-5" />
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
              className="border-t border-slate-200 bg-white/95 px-4 pb-4 pt-3 md:hidden"
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
                className="mt-1 inline-flex w-fit rounded-lg px-4 py-2 text-sm font-semibold text-white"
                style={{ backgroundColor: 'var(--navy-blue)' }}
              >
                Contact Us
              </Link>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
      </div>
    </header>
  )
}

export default SiteHeader
