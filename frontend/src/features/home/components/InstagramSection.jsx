const instagramTiles = [
  '/slider-img-1.png',
  '/slider-img-2.png',
  '/slider-img-3.png',
  '/slider-img-4.png',
  '/slider-img-5.png',
  '/slider-img-6.png',
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
          <img src="/whatsapp-color-svgrepo-com.png" alt="WhatsApp" className="h-5 w-5" />
          Join Our WhatsApp Community
        </p>
      </div>
    </section>
  )
}

export default InstagramSection
