import { useEffect, useState } from 'react'
import { Layout } from '../../components/Layout'
import api from '../../api/client'
import { User, Role } from '../../auth/AuthContext'
import { Trash2, Edit2 } from 'lucide-react'

export function Users() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const { data } = await api.get('/admin/users')
        setUsers(data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchUsers()
  }, [])

  const handleDelete = async (id: number) => {
    if (!window.confirm('Désactiver cet utilisateur ?')) return
    try {
      await api.delete(`/admin/users/${id}`)
      setUsers(users.map(u => u.id === id ? { ...u, actif: false } : u))
    } catch (err) {
      console.error(err)
    }
  }

  if (loading) return <Layout><div>Chargement...</div></Layout>

  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Gestion Utilisateurs</h1>

        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Nom</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Rôle</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Statut</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-700 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {users.map(user => (
                <tr key={user.id} className={user.actif ? '' : 'bg-gray-50 opacity-50'}>
                  <td className="px-6 py-4 text-sm">{user.email}</td>
                  <td className="px-6 py-4 text-sm font-medium">{user.nom_complet}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                      {user.role.replace(/_/g, ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${user.actif ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                      {user.actif ? 'Actif' : 'Inactif'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right space-x-2">
                    <button className="p-2 hover:bg-gray-100 rounded transition">
                      <Edit2 size={16} className="text-gray-600" />
                    </button>
                    {user.actif && (
                      <button
                        onClick={() => handleDelete(user.id)}
                        className="p-2 hover:bg-red-100 rounded transition"
                      >
                        <Trash2 size={16} className="text-red-600" />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  )
}
