import { useState } from 'react'
import { Heart, MapPin, Maximize, Car, Bath, Bed, Map, List, Home, Building2, Store, Trees, Waves, Star, X } from 'lucide-react'
import { motion } from 'framer-motion'

// Mock property data
const MOCK_PROPERTIES = [
  {
    id: 1,
    name: 'RedStone Station',
    price: 3094,
    location: '22 Crystal St, Noida',
    bedrooms: 6,
    area: 200,
    garages: 2,
    bathrooms: 3,
    hasPool: true,
    image: '/slider-img-1.png',
    images: ['/slider-img-1.png', '/slider-img-2.png', '/slider-img-3.png', '/slider-img-4.png', '/slider-img-5.png', '/slider-img-6.png', '/slider-img-7.png'],
    isPopular: true,
    has360: true,
    description: 'Nostrum reprehenderit maxime quaerat quis aperiam magnam molestiae. Similique porttitor dolore! Fugiat nisi tempora Lorem exceptetur officia.',
  },
  {
    id: 2,
    name: 'Crystal Heights Villa',
    price: 4200,
    location: '45 Sector 62, Noida',
    bedrooms: 5,
    area: 250,
    garages: 2,
    bathrooms: 4,
    hasPool: true,
    image: '/slider-img-2.png',
    images: ['/slider-img-2.png', '/slider-img-3.png', '/slider-img-4.png'],
    isPopular: false,
    has360: false,
  },
  {
    id: 3,
    name: 'Modern Estate',
    price: 2800,
    location: '12 Sector 18, Noida',
    bedrooms: 4,
    area: 180,
    garages: 1,
    bathrooms: 3,
    hasPool: false,
    image: '/slider-img-3.png',
    images: ['/slider-img-3.png', '/slider-img-4.png'],
    isPopular: true,
    has360: true,
  },
  {
    id: 4,
    name: 'Skyline Residence',
    price: 3500,
    location: '78 Greater Noida West',
    bedrooms: 6,
    area: 220,
    garages: 2,
    bathrooms: 4,
    hasPool: true,
    image: '/slider-img-4.png',
    images: ['/slider-img-4.png', '/slider-img-5.png', '/slider-img-6.png'],
    isPopular: false,
    has360: true,
  },
  {
    id: 5,
    name: 'Luxury Garden Villa',
    price: 5200,
    location: '34 Film City, Noida',
    bedrooms: 7,
    area: 300,
    garages: 3,
    bathrooms: 5,
    hasPool: true,
    image: '/slider-img-5.png',
    images: ['/slider-img-5.png', '/slider-img-6.png'],
    isPopular: true,
    has360: false,
  },
]

const PROPERTY_TYPES = [
  { id: 'home', label: 'Home', Icon: Home },
  { id: 'apartment', label: 'Apartment', Icon: Building2 },
  { id: 'commercial', label: 'Commercial', Icon: Store },
  { id: 'land', label: 'Land plot', Icon: Trees },
]

function ListingsPage() {
  const [viewMode, setViewMode] = useState('list')
  const [selectedProperty, setSelectedProperty] = useState(MOCK_PROPERTIES[0])
  const [propertyType, setPropertyType] = useState('home')
  const [priceRange, setPriceRange] = useState([500, 5000])
  const [rooms, setRooms] = useState(1)
  const [sortBy, setSortBy] = useState('price-high')
  const [hasGarage, setHasGarage] = useState(false)

  return (
    <div className="min-h-screen bg-page">
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-8 lg:px-6">
        {/* Left Sidebar - Filters */}
        <aside className="hidden w-72 flex-shrink-0 lg:block">
          <div className="sticky top-24 space-y-6">
            {/* Results Count */}
            <div>
              <h2 className="text-2xl font-bold text-slate-900">{MOCK_PROPERTIES.length} Results</h2>
              <p className="text-sm text-slate-500">in Noida</p>
            </div>

            {/* View Toggle */}
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('map')}
                className={`flex-1 rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                  viewMode === 'map' ? 'bg-slate-900 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'
                }`}
              >
                <Map className="mx-auto h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`flex-1 rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                  viewMode === 'list' ? 'bg-slate-900 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'
                }`}
              >
                <List className="mx-auto h-4 w-4" />
              </button>
            </div>

            {/* Sorting */}
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">Sorting</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-700 focus:border-brand focus:outline-none"
              >
                <option value="price-high">Price: high to low</option>
                <option value="price-low">Price: low to high</option>
                <option value="area-large">Area: largest first</option>
                <option value="area-small">Area: smallest first</option>
              </select>
            </div>

            {/* Property Type */}
            <div>
              <label className="mb-3 block text-sm font-semibold text-slate-700">Property type</label>
              <div className="grid grid-cols-2 gap-2">
                {PROPERTY_TYPES.map((type) => {
                  const IconComponent = type.Icon
                  return (
                    <button
                      key={type.id}
                      onClick={() => setPropertyType(type.id)}
                      className={`flex flex-col items-center gap-2 rounded-lg border-2 px-4 py-3 text-sm font-medium transition-all ${
                        propertyType === type.id
                          ? 'text-white'
                          : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'
                      }`}
                      style={propertyType === type.id ? { backgroundColor: 'var(--navy-blue)', borderColor: 'var(--navy-blue)' } : {}}
                    >
                      <IconComponent className="h-5 w-5" />
                      {type.label}
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Location */}
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">Location</label>
              <div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2.5">
                <MapPin className="h-4 w-4 text-slate-400" />
                <select className="flex-1 bg-transparent text-sm text-slate-700 focus:outline-none">
                  <option>Noida, India</option>
                  <option>Greater Noida</option>
                  <option>Noida Extension</option>
                </select>
              </div>
            </div>

            {/* Price Range */}
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">Per Area Unit Price</label>
              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <input
                  type="range"
                  min="500"
                  max="10000"
                  value={priceRange[1]}
                  onChange={(e) => setPriceRange([priceRange[0], Number(e.target.value)])}
                  className="w-full"
                />
                <div className="mt-3 flex justify-between text-sm text-slate-600">
                  <span>${priceRange[0]}<br /><span className="text-xs text-slate-400">min</span></span>
                  <span>${priceRange[1]}<br /><span className="text-xs text-slate-400">max</span></span>
                </div>
              </div>
            </div>

            {/* Rooms */}
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">Rooms</label>
              <div className="flex gap-2">
                {[1, 2, 3].map((num) => (
                  <button
                    key={num}
                    onClick={() => setRooms(num)}
                    className={`flex h-10 w-10 items-center justify-center rounded-lg border-2 text-sm font-medium transition-all ${
                      rooms === num
                        ? 'text-white'
                        : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'
                    }`}
                    style={rooms === num ? { backgroundColor: 'var(--navy-blue)', borderColor: 'var(--navy-blue)' } : {}}
                  >
                    {num}
                  </button>
                ))}
                <button
                  onClick={() => setRooms(4)}
                  className={`flex h-10 flex-1 items-center justify-center rounded-lg border-2 text-sm font-medium transition-all ${
                    rooms === 4
                      ? 'text-white'
                      : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'
                  }`}
                  style={rooms === 4 ? { backgroundColor: 'var(--navy-blue)', borderColor: 'var(--navy-blue)' } : {}}
                >
                  4+
                </button>
              </div>
            </div>

            {/* Additional Conveniences */}
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">Additional Conveniences</label>
              <label className="flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm">
                <input
                  type="checkbox"
                  checked={hasGarage}
                  onChange={(e) => setHasGarage(e.target.checked)}
                  className="h-4 w-4 rounded text-brand focus:ring-brand"
                />
                <span className="text-slate-700">Garage</span>
              </label>
            </div>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 space-y-4">
          {/* Header */}
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-slate-900">Search results ({MOCK_PROPERTIES.length})</h1>
          </div>

          {/* Property Cards */}
          <div className="space-y-4">
            {MOCK_PROPERTIES.map((property) => (
              <motion.div
                key={property.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="group relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md"
              >
                <div className="flex gap-4">
                  {/* Property Image */}
                  <div className="relative h-40 w-56 flex-shrink-0 overflow-hidden rounded-xl">
                    <img src={property.image} alt={property.name} className="h-full w-full object-cover" />
                    {property.isPopular && (
                      <span className="absolute left-3 top-3 rounded-full px-3 py-1 text-xs font-semibold text-white" style={{ backgroundColor: 'var(--navy-blue)' }}>
                        Popular
                      </span>
                    )}
                    {property.has360 && (
                      <span className="absolute bottom-3 right-3 flex h-8 w-8 items-center justify-center rounded-full bg-white text-xs font-bold text-slate-900">
                        360°
                      </span>
                    )}
                  </div>

                  {/* Property Info */}
                  <div className="flex flex-1 flex-col justify-between">
                    <div>
                      <div className="flex items-start justify-between">
                        <div>
                          <div className="flex items-center gap-2">
                            <h3 className="text-xl font-bold text-slate-900">${property.price.toLocaleString()}</h3>
                            <span className="text-sm text-slate-500">/ month</span>
                            <button className="ml-2 text-slate-400 transition-colors hover:text-red-500">
                              <Heart className="h-5 w-5" />
                            </button>
                          </div>
                          <h4 className="mt-1 font-semibold text-slate-900">{property.name}</h4>
                          <p className="mt-1 flex items-center gap-1 text-sm text-slate-500">
                            <MapPin className="h-4 w-4" />
                            {property.location}
                          </p>
                        </div>
                      </div>

                      {/* Property Features */}
                      <div className="mt-3 flex flex-wrap gap-3">
                        <span className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-1.5 text-sm text-slate-600">
                          <Bed className="h-4 w-4" />
                          {property.bedrooms}
                        </span>
                        <span className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-1.5 text-sm text-slate-600">
                          <Maximize className="h-4 w-4" />
                          {property.area}m²
                        </span>
                        <span className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-1.5 text-sm text-slate-600">
                          <Car className="h-4 w-4" />
                          {property.garages} Garage
                        </span>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="mt-4 flex items-center gap-3">
                      <button
                        onClick={() => setSelectedProperty(property)}
                        className="rounded-xl px-6 py-2.5 text-sm font-semibold text-white transition-all hover:-translate-y-0.5"
                        style={{ backgroundColor: 'var(--navy-blue)' }}
                        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgb(24, 56, 124)'}
                        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'var(--navy-blue)'}
                      >
                        View Details
                      </button>
                      <button className="flex items-center justify-center rounded-xl p-2.5">
                        <img src="/whatsapp-color-svgrepo-com.png" alt="WhatsApp" className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </main>

        {/* Right Sidebar - Property Detail */}
        {selectedProperty && (
          <aside className="hidden w-96 flex-shrink-0 xl:block">
            <div className="sticky top-24 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
              {/* Property Images */}
              <div className="relative h-64 bg-slate-100">
                <img src={selectedProperty.image} alt={selectedProperty.name} className="h-full w-full object-cover" />
                <button
                  onClick={() => setSelectedProperty(MOCK_PROPERTIES[0])}
                  className="absolute right-4 top-4 rounded-full bg-white p-2 shadow-md hover:bg-slate-50"
                >
                  <X className="h-5 w-5 text-slate-600" />
                </button>
                {selectedProperty.has360 && (
                  <span className="absolute bottom-4 right-4 flex h-10 w-10 items-center justify-center rounded-full bg-white text-sm font-bold">
                    360°
                  </span>
                )}
              </div>

              {/* Image Thumbnails */}
              <div className="flex gap-2 overflow-x-auto p-4">
                {selectedProperty.images.slice(0, 4).map((img, idx) => (
                  <div key={idx} className="relative h-16 w-20 flex-shrink-0 overflow-hidden rounded-lg">
                    <img src={img} alt="" className="h-full w-full object-cover" />
                  </div>
                ))}
                {selectedProperty.images.length > 4 && (
                  <div className="flex h-16 w-20 flex-shrink-0 items-center justify-center rounded-lg bg-slate-900 text-white">
                    +{selectedProperty.images.length - 4}
                  </div>
                )}
              </div>

              {/* Property Info */}
              <div className="p-4">
                <h3 className="text-xl font-bold text-slate-900">{selectedProperty.name}</h3>
                <p className="mt-1 flex items-center gap-1 text-sm text-slate-500">
                  <MapPin className="h-4 w-4" />
                  {selectedProperty.location}
                </p>

                <div className="mt-4 text-2xl font-bold" style={{ color: 'var(--navy-blue)' }}>
                  ${selectedProperty.price.toLocaleString()}
                  <span className="text-sm font-normal text-slate-500"> /month</span>
                </div>

                {/* Amenities */}
                <div className="mt-4 flex flex-wrap gap-2">
                  <span className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-2 text-sm">
                    <Bed className="h-4 w-4" />
                    {selectedProperty.bedrooms} Bedrooms
                  </span>
                  <span className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-2 text-sm">
                    <Maximize className="h-4 w-4" />
                    {selectedProperty.area}m²
                  </span>
                  <span className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-2 text-sm">
                    <Car className="h-4 w-4" />
                    {selectedProperty.garages} Garage
                  </span>
                  <span className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-2 text-sm">
                    <Bath className="h-4 w-4" />
                    {selectedProperty.bathrooms} Bathroom
                  </span>
                  {selectedProperty.hasPool && (
                    <span className="flex items-center gap-1.5 rounded-lg bg-slate-50 px-3 py-2 text-sm">
                      <Waves className="h-4 w-4" />
                      Pool
                    </span>
                  )}
                </div>

                {/* Description */}
                <div className="mt-4">
                  <h4 className="font-semibold text-slate-900">Property Details</h4>
                  <p className="mt-2 text-sm leading-relaxed text-slate-600">
                    {selectedProperty.description}
                  </p>
                </div>

                {/* Agent Info */}
                <div className="mt-4 flex items-center gap-3 rounded-lg bg-slate-50 p-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-200 text-sm font-semibold">
                    MJ
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-slate-900">Michael Josep</p>
                    <div className="flex items-center gap-1 text-xs">
                      <Star className="h-3 w-3 fill-amber-500 text-amber-500" />
                      <span className="text-slate-900">4.8</span>
                      <span className="text-slate-400">(15 review)</span>
                    </div>
                  </div>
                </div>

                {/* View Details Button */}
                <button
                  className="mt-4 w-full rounded-xl py-3 text-sm font-semibold text-white transition-all hover:-translate-y-0.5"
                  style={{ backgroundColor: 'var(--navy-blue)' }}
                  onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgb(24, 56, 124)'}
                  onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'var(--navy-blue)'}
                >
                  View Details
                </button>
              </div>
            </div>
          </aside>
        )}
      </div>
    </div>
  )
}

export default ListingsPage
