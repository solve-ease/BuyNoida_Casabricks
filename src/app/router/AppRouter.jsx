import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from '../layouts/AppLayout'
import HomePage from '../../pages/home/HomePage'
import InquiryPage from '../../pages/inquiry/InquiryPage'
import ListingsPage from '../../pages/listings/ListingsPage'
import PropertyDetailPage from '../../pages/property-detail/PropertyDetailPage'

function AppRouter() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/listings" element={<ListingsPage />} />
        <Route path="/property/:propertyId" element={<PropertyDetailPage />} />
        <Route path="/inquiry" element={<InquiryPage />} />
      </Route>
      <Route path="*" element={<Navigate replace to="/" />} />
    </Routes>
  )
}

export default AppRouter
