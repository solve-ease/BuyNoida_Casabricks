import { useEffect } from 'react'
import AboutSection from '../../features/home/components/AboutSection'
import GallerySection from '../../features/home/components/GallerySection'
import HeroSection from '../../features/home/components/HeroSection'
import InstagramSection from '../../features/home/components/InstagramSection'

function setMetaTag(name, content) {
  let metaTag = document.querySelector(`meta[name="${name}"]`)

  if (!metaTag) {
    metaTag = document.createElement('meta')
    metaTag.setAttribute('name', name)
    document.head.appendChild(metaTag)
  }

  metaTag.setAttribute('content', content)
}

function HomePage() {
  useEffect(() => {
    document.title = 'BuyNoida | Discover Noida Properties Visually'
    setMetaTag(
      'description',
      'BuyNoida helps you discover Noida properties through a guided visual-first experience with curated listings, property insights, and fast inquiry support.',
    )
  }, [])

  return (
    <>
      <HeroSection />
      <AboutSection />
      <GallerySection />
      <InstagramSection />
    </>
  )
}

export default HomePage
