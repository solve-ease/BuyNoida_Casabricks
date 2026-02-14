import { useParams } from 'react-router-dom'

function PropertyDetailPage() {
  const { propertyId } = useParams()

  return (
    <section className="space-y-2">
      <h2 className="text-2xl font-semibold">Property Detail (Phase 3)</h2>
      <p className="text-slate-600">
        Placeholder for property <span className="font-medium text-slate-800">{propertyId}</span>. AI enhanced image disclosure and visual data modules will be added in later phases.
      </p>
    </section>
  )
}

export default PropertyDetailPage
