import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
import { Login } from './pages/Login'
import { Dashboard } from './pages/Dashboard'
import { Import } from './pages/Import'
import { Parametrage } from './pages/Parametrage'
import { Data } from './pages/Data'
import { Users } from './pages/admin/Users'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth()

  if (loading) return <div className="flex items-center justify-center h-screen">Chargement...</div>
  if (!isAuthenticated) return <Navigate to="/login" replace />

  return <>{children}</>
}

function AppRoutes() {
  const { isAuthenticated, loading } = useAuth()

  if (loading) return <div className="flex items-center justify-center h-screen">Chargement...</div>

  return (
    <Routes>
      <Route path="/login" element={isAuthenticated ? <Navigate to="/" replace /> : <Login />} />
      <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/import" element={<ProtectedRoute><Import /></ProtectedRoute>} />
      <Route path="/parametrage" element={<ProtectedRoute><Parametrage /></ProtectedRoute>} />
      <Route path="/data" element={<ProtectedRoute><Data /></ProtectedRoute>} />
      <Route path="/admin/users" element={<ProtectedRoute><Users /></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  )
}
