import { Outlet } from 'react-router-dom'
import SiteFooter from '../../shared/components/layout/SiteFooter'
import SiteHeader from '../../shared/components/layout/SiteHeader'

function AppLayout() {
  return (
    <div className="min-h-screen bg-page text-slate-900">
      <SiteHeader />
      <main>
        <Outlet />
      </main>
      <SiteFooter />
    </div>
  )
}

export default AppLayout
