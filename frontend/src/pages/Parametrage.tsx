import { useState } from 'react'
import { Layout } from '../components/Layout'
import { Settings } from 'lucide-react'

export function Parametrage() {
  const [activeTab, setActiveTab] = useState<'salles' | 'groupes' | 'formateurs' | 'modules'>('salles')

  const tabs = [
    { id: 'salles' as const, label: 'Salles', icon: '🏫' },
    { id: 'groupes' as const, label: 'Groupes', icon: '👥' },
    { id: 'formateurs' as const, label: 'Formateurs', icon: '👨‍🏫' },
    { id: 'modules' as const, label: 'Modules', icon: '📚' },
  ]

  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Paramétrage</h1>

        <div className="flex space-x-2 mb-6 border-b border-gray-200">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 font-medium transition ${
                activeTab === tab.id
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-8">
          {activeTab === 'salles' && (
            <div>
              <h2 className="text-xl font-semibold mb-4">Gestion des Salles</h2>
              <p className="text-gray-600">Fonctionnalité à implémenter - CRUD salles avec MHS disponible</p>
            </div>
          )}
          {activeTab === 'groupes' && (
            <div>
              <h2 className="text-xl font-semibold mb-4">Gestion des Groupes</h2>
              <p className="text-gray-600">Fonctionnalité à implémenter - Édition et ajout post-import</p>
            </div>
          )}
          {activeTab === 'formateurs' && (
            <div>
              <h2 className="text-xl font-semibold mb-4">Gestion des Formateurs</h2>
              <p className="text-gray-600">Fonctionnalité à implémenter - Édition et ajout post-import</p>
            </div>
          )}
          {activeTab === 'modules' && (
            <div>
              <h2 className="text-xl font-semibold mb-4">Gestion des Modules</h2>
              <p className="text-gray-600">Fonctionnalité à implémenter - Masses horaires DRIF par module/filière</p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}
