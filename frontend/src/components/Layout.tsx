import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { Menu, LogOut, Settings, Home, BarChart3, Upload, Users, Sliders } from 'lucide-react'
import { useState } from 'react'

export function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const menuItems = [
    { label: 'Tableau de bord', icon: Home, href: '/' },
    { label: 'Import Excel', icon: Upload, href: '/import' },
    { label: 'Paramétrage', icon: Sliders, href: '/parametrage' },
    { label: 'Consultation', icon: BarChart3, href: '/data' },
  ]

  if (user?.role === 'directeur_complexe' || user?.role === 'directeur_etablissement') {
    menuItems.push({ label: 'Admin Utilisateurs', icon: Users, href: '/admin/users' })
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 w-64 bg-blue-900 text-white transform transition-transform z-30 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 md:relative`}>
        <div className="p-6 border-b border-blue-800">
          <h1 className="text-2xl font-bold">OFPPT</h1>
          <p className="text-sm text-blue-200 mt-1">Gestion Centre Formation</p>
        </div>

        <nav className="p-4 space-y-2">
          {menuItems.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-800 transition"
              onClick={() => setSidebarOpen(false)}
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>
      </div>

      {/* Main */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="md:hidden">
            <Menu size={24} className="text-gray-700" />
          </button>

          <div className="flex items-center space-x-4">
            <div className="text-right hidden sm:block">
              <p className="font-medium text-gray-900">{user?.nom_complet}</p>
              <p className="text-sm text-gray-500">{user?.role.replace(/_/g, ' ')}</p>
            </div>
            <button
              onClick={handleLogout}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
              title="Déconnexion"
            >
              <LogOut size={20} className="text-gray-700" />
            </button>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>

      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 md:hidden z-20"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}
