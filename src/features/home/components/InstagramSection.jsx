import { MessageCircle } from 'lucide-react'

const instagramTiles = [
  'https://images.unsplash.com/photo-1600607687644-c7f34b5d9f5a?auto=format&fit=crop&w=600&q=80',
  'https://images.unsplash.com/photo-1616047006789-b7afc78d8aaf?auto=format&fit=crop&w=600&q=80',
  'https://images.unsplash.com/photo-1615874959474-d609969a20ed?auto=format&fit=crop&w=600&q=80',
  '',
  '',
  'https://images.unsplash.com/photo-1617098474202-0d0d7f60f5f6?auto=format&fit=crop&w=600&q=80',
]

function InstagramSection() {
  return (
    <section className="bg-[#e9eef6] px-4 py-12 md:py-16">
      <div className="mx-auto w-full max-w-7xl rounded-2xl border border-dashed border-[#82b5ff] bg-[#edf3fc] p-5 md:p-8">
        <h3 className="text-center text-4xl font-bold tracking-tight text-slate-900">Explore BuyNoida on Instagram</h3>
        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-6">
          {instagramTiles.map((image, index) => (
            <div
              key={`${image}-${index}`}
              className="aspect-square overflow-hidden rounded-xl border border-slate-200 bg-slate-100"
            >
              {image ? <img src={image} alt="BuyNoida social post" className="h-full w-full object-cover" /> : null}
            </div>
          ))}
        </div>
        <p className="mt-5 inline-flex w-full items-center justify-center gap-2 text-center text-lg text-slate-600">
          <MessageCircle size={18} className="text-brand" />
          Join Our WhatsApp Community
        </p>
      </div>
    </section>
  )
}

export default InstagramSection
