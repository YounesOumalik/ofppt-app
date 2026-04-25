import React, { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/client'

export type Role = 'directeur_complexe' | 'directeur_etablissement' | 'gestionnaire_stagiaires' | 'formateur' | 'stagiaire'

export interface User {
  id: number
  email: string
  nom_complet: string
  role: Role
  code_efp: string | null
  actif: boolean
  formateur_matricule: string | null
  stagiaire_matricule: string | null
  cree_le: string
  dernier_login: string | null
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          const { data } = await api.get('/auth/me')
          setUser(data)
        } catch {
          localStorage.removeItem('token')
        }
      }
      setLoading(false)
    }
    checkAuth()
  }, [])

  const login = async (email: string, password: string) => {
    const { data } = await api.post('/auth/login', { email, password })
    localStorage.setItem('token', data.access_token)
    setUser(data.user)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
