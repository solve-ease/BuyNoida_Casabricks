import { Facebook, Home, Instagram, Linkedin, MessageCircle } from 'lucide-react'

function SiteFooter() {
  return (
    <footer className="bg-brand text-white">
      <div className="mx-auto flex w-full max-w-7xl flex-col items-center justify-between gap-4 px-4 py-5 md:flex-row md:px-6">
        <div className="flex items-center gap-4">
          <a href="#" aria-label="Instagram" className="opacity-90 transition-opacity hover:opacity-100"><Instagram size={18} /></a>
          <a href="#" aria-label="LinkedIn" className="opacity-90 transition-opacity hover:opacity-100"><Linkedin size={18} /></a>
          <a href="#" aria-label="Facebook" className="opacity-90 transition-opacity hover:opacity-100"><Facebook size={18} /></a>
          <a href="#" aria-label="WhatsApp" className="opacity-90 transition-opacity hover:opacity-100"><MessageCircle size={18} /></a>
        </div>

        <div className="inline-flex items-center gap-2 font-semibold">
          <Home size={14} />
          <span>BuyNoida</span>
        </div>

        <p className="text-xs text-white/85">© 2026 CasaBricks. All rights reserved.</p>
      </div>
    </footer>
  )
}

export default SiteFooter
