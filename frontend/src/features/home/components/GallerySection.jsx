import { motion } from 'framer-motion'

// All 15 property images
const galleryImages = [
  '/slider-img-1.png',
  '/slider-img-2.png',
  '/slider-img-3.png',
  '/slider-img-4.png',
  '/slider-img-5.png',
  '/slider-img-6.png',
  '/slider-img-7.png',
  '/slider-img-8.jpg',
  '/slider-img-9.png',
  '/slider-img-10.png',
  '/slider-img-11.png',
  '/slider-img-12.png',
  '/slider-img-13.png',
  '/slider-img-14.png',
  '/slider-img-15.png',
]

// Pattern repeats: Box1 (3 imgs) -> Box2 (1 img) -> Box3 (3 imgs) -> repeat
const createGalleryBoxes = (images) => {
  const boxes = []
  let imageIndex = 0

  while (imageIndex < images.length) {
    // Box 1: 1 landscape on top + 2 squares below
    if (imageIndex < images.length) {
      boxes.push({
        type: 'type1',
        images: [
          images[imageIndex % images.length],
          images[(imageIndex + 1) % images.length],
          images[(imageIndex + 2) % images.length],
        ],
      })
      imageIndex += 3
    }

    // Box 2: 1 tall portrait image
    if (imageIndex < images.length) {
      boxes.push({
        type: 'type2',
        images: [images[imageIndex % images.length]],
      })
      imageIndex += 1
    }

    // Box 3: 2 images on top + 1 landscape below
    if (imageIndex < images.length) {
      boxes.push({
        type: 'type3',
        images: [
          images[imageIndex % images.length],
          images[(imageIndex + 1) % images.length],
          images[(imageIndex + 2) % images.length],
        ],
      })
      imageIndex += 3
    }
  }

  return boxes
}

function GallerySection() {
  const galleryBoxes = createGalleryBoxes(galleryImages)
  // Duplicate for seamless loop
  const duplicatedBoxes = [...galleryBoxes, ...galleryBoxes]

  return (
    <section className="overflow-hidden bg-[#eef2f7] py-14 md:py-20">
      <div className="relative">
        {/* Continuous scrolling animation from left to right */}
        <motion.div
          className="flex gap-4"
          animate={{
            x: ['0%', '-50%'],
          }}
          transition={{
            x: {
              repeat: Infinity,
              repeatType: 'loop',
              duration: 50,
              ease: 'linear',
            },
          }}
        >
          {duplicatedBoxes.map((box, boxIndex) => (
            <div key={boxIndex} className="flex-shrink-0">
              {/* Type 1: 1 landscape top + 2 squares bottom */}
              {box.type === 'type1' && (
                <div className="grid h-[470px] w-[320px] grid-rows-2 gap-3">
                  <motion.img
                    src={box.images[0]}
                    alt={`Property ${boxIndex}-1`}
                    className="h-full w-full rounded-2xl object-cover shadow-md"
                    whileHover={{ scale: 1.03 }}
                    transition={{ duration: 0.3 }}
                  />
                  <div className="grid grid-cols-2 gap-3">
                    <motion.img
                      src={box.images[1]}
                      alt={`Property ${boxIndex}-2`}
                      className="h-full w-full rounded-2xl object-cover shadow-md"
                      whileHover={{ scale: 1.03 }}
                      transition={{ duration: 0.3 }}
                    />
                    <motion.img
                      src={box.images[2]}
                      alt={`Property ${boxIndex}-3`}
                      className="h-full w-full rounded-2xl object-cover shadow-md"
                      whileHover={{ scale: 1.03 }}
                      transition={{ duration: 0.3 }}
                    />
                  </div>
                </div>
              )}

              {/* Type 2: 1 tall portrait image */}
              {box.type === 'type2' && (
                <motion.img
                  src={box.images[0]}
                  alt={`Property ${boxIndex}`}
                  className="h-[470px] w-[320px] rounded-2xl object-cover shadow-md"
                  whileHover={{ scale: 1.03 }}
                  transition={{ duration: 0.3 }}
                />
              )}

              {/* Type 3: 2 images top + 1 landscape bottom */}
              {box.type === 'type3' && (
                <div className="grid h-[470px] w-[320px] grid-rows-2 gap-3">
                  <div className="grid grid-cols-2 gap-3">
                    <motion.img
                      src={box.images[0]}
                      alt={`Property ${boxIndex}-1`}
                      className="h-full w-full rounded-2xl object-cover shadow-md"
                      whileHover={{ scale: 1.03 }}
                      transition={{ duration: 0.3 }}
                    />
                    <motion.img
                      src={box.images[1]}
                      alt={`Property ${boxIndex}-2`}
                      className="h-full w-full rounded-2xl object-cover shadow-md"
                      whileHover={{ scale: 1.03 }}
                      transition={{ duration: 0.3 }}
                    />
                  </div>
                  <motion.img
                    src={box.images[2]}
                    alt={`Property ${boxIndex}-3`}
                    className="h-full w-full rounded-2xl object-cover shadow-md"
                    whileHover={{ scale: 1.03 }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
              )}
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

export default GallerySection
