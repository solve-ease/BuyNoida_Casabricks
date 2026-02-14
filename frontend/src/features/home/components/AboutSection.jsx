import { motion } from 'framer-motion'

const STATS = [
  { value: '150+', label: 'Actively verified and updated properties across key Noida sectors.' },
  { value: '20+', label: 'Strategic presence across Central Noida, Expressway, and near Delhi zones.' },
  { value: '95%', label: 'Buyers appreciate our visual-first, transparent property discovery process.' },
  { value: '24/7', label: 'Instant WhatsApp and callback assistance for faster property decisions.' },
]

function AboutSection() {
  return (
    <section id="about" className="bg-white px-4 py-16 md:py-20">
      <div className="mx-auto grid w-full max-w-7xl gap-12 lg:grid-cols-[1.2fr_1fr] lg:gap-16">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.2 }}
          transition={{ duration: 0.55 }}
          className="space-y-6"
        >
          <h2 className="text-4xl font-bold tracking-tight text-slate-900">About BuyNoida</h2>
          <p className="max-w-2xl text-lg leading-relaxed text-slate-600">
            BuyNoida is an innovative property discovery platform specifically focused on the vibrant city of Noida.
            It simplifies the process of buying plots by offering a guided search experience, providing visual insights,
            and presenting curated listings designed to enhance clarity and instill confidence in potential buyers.
          </p>

          <div className="grid grid-cols-2 gap-4 pt-2 sm:grid-cols-4">
            <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-center text-sm font-semibold text-slate-600">Noida Development Authority</div>
            <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-center text-sm font-semibold text-slate-600">RERA Approved</div>
            <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-center text-sm font-semibold text-slate-600">Asian Paints</div>
            <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-center text-sm font-semibold text-slate-600">Kajaria</div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 gap-7 sm:grid-cols-2">
          {STATS.map((item, index) => (
            <motion.article
              key={item.value}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.25 }}
              transition={{ delay: index * 0.08, duration: 0.5 }}
              className="rounded-2xl border border-slate-200 bg-slate-50 p-5"
            >
              <p className="text-5xl font-bold text-brand-ink">{item.value}</p>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">{item.label}</p>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  )
}

export default AboutSection
