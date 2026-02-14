import { motion } from 'framer-motion'
import { Quote } from 'lucide-react'

const galleryImages = [
  'https://images.unsplash.com/photo-1616486029423-aaa4789e8c9a?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1617104551722-3b2d5136644c?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1617806118233-18e1de247200?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1616594039964-3d5d6fe2bd14?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1617098900591-3f90928e8c54?auto=format&fit=crop&w=900&q=80',
]

function GallerySection() {
  return (
    <section className="bg-[#eef2f7] px-4 py-14 md:py-20">
      <div className="mx-auto w-full max-w-7xl rounded-3xl border border-[#bfc7d8] bg-white p-4 shadow-sm md:p-8">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-12 md:grid-rows-2">
          <motion.img
            whileHover={{ y: -4 }}
            transition={{ duration: 0.28 }}
            src={galleryImages[0]}
            alt="Living room interior"
            className="h-56 w-full rounded-2xl object-cover md:col-span-4"
          />
          <motion.img
            whileHover={{ y: -4 }}
            transition={{ duration: 0.28 }}
            src={galleryImages[1]}
            alt="Modern stairway"
            className="h-[470px] w-full rounded-2xl object-cover md:col-span-4 md:row-span-2"
          />
          <motion.img
            whileHover={{ y: -4 }}
            transition={{ duration: 0.28 }}
            src={galleryImages[2]}
            alt="Bedroom interior"
            className="h-56 w-full rounded-2xl object-cover md:col-span-2"
          />
          <motion.img
            whileHover={{ y: -4 }}
            transition={{ duration: 0.28 }}
            src={galleryImages[3]}
            alt="Villa exterior"
            className="h-56 w-full rounded-2xl object-cover md:col-span-2"
          />
          <motion.img
            whileHover={{ y: -4 }}
            transition={{ duration: 0.28 }}
            src={galleryImages[4]}
            alt="Dark-tone lounge"
            className="h-48 w-full rounded-2xl object-cover md:col-span-2"
          />
          <motion.img
            whileHover={{ y: -4 }}
            transition={{ duration: 0.28 }}
            src={galleryImages[5]}
            alt="Bright minimal room"
            className="h-48 w-full rounded-2xl object-cover md:col-span-2"
          />
          <motion.div
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ duration: 0.45 }}
            className="flex h-48 flex-col justify-between rounded-2xl bg-gradient-to-br from-brand to-brand-dark p-5 text-white md:col-span-4"
          >
            <Quote size={22} />
            <p className="text-sm leading-relaxed text-white/90">
              “The visual-first approach helped us shortlist faster and decide confidently without overwhelming filters.”
            </p>
            <span className="text-sm font-semibold">— Verified Buyer, Noida Extension</span>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

export default GallerySection
