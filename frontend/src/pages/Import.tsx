import { useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import api from '../api/client'
import { Layout } from '../components/Layout'
import { Upload, CheckCircle, AlertCircle } from 'lucide-react'

export function Import() {
  const { user } = useAuth()
  const [avancementFile, setAvancementFile] = useState<File | null>(null)
  const [stayiairesFile, setStagiairesFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleImport = async (type: 'avancement' | 'stagiaire') => {
    const file = type === 'avancement' ? avancementFile : stayiairesFile
    if (!file) return

    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const { data } = await api.post(`/import/${type}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      setResult({ type, ...data })
      if (type === 'avancement') setAvancementFile(null)
      else setStagiairesFile(null)
    } catch (err: any) {
      setResult({ error: err.response?.data?.detail || 'Erreur import' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="max-w-2xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Import Excel</h1>

        <div className="space-y-6">
          {/* Avancement */}
          <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Avancement de Formation</h3>
                <p className="text-sm text-gray-600 mt-1">Fichier: AvancementProgramme*.xlsx</p>
              </div>
              <Upload className="text-gray-400" size={32} />
            </div>

            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={(e) => setAvancementFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-500 mb-4"
            />

            {avancementFile && (
              <p className="text-sm text-blue-600 mb-4">
                Fichier sélectionné: <strong>{avancementFile.name}</strong>
              </p>
            )}

            <button
              onClick={() => handleImport('avancement')}
              disabled={!avancementFile || loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
            >
              {loading ? 'Import...' : 'Importer'}
            </button>
          </div>

          {/* Stagiaires */}
          <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Stagiaires</h3>
                <p className="text-sm text-gray-600 mt-1">Fichier: lister.xlsx</p>
              </div>
              <Upload className="text-gray-400" size={32} />
            </div>

            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={(e) => setStagiairesFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-500 mb-4"
            />

            {stayiairesFile && (
              <p className="text-sm text-blue-600 mb-4">
                Fichier sélectionné: <strong>{stayiairesFile.name}</strong>
              </p>
            )}

            <button
              onClick={() => handleImport('stagiaire')}
              disabled={!stayiairesFile || loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
            >
              {loading ? 'Import...' : 'Importer'}
            </button>
          </div>
        </div>

        {/* Result */}
        {result && (
          <div className="mt-8">
            {result.error ? (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex space-x-4">
                <AlertCircle className="text-red-600 flex-shrink-0" size={24} />
                <div>
                  <h3 className="font-semibold text-red-900">Erreur d'import</h3>
                  <p className="text-red-700 mt-1">{result.error}</p>
                </div>
              </div>
            ) : (
              <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                <div className="flex space-x-4">
                  <CheckCircle className="text-green-600 flex-shrink-0" size={24} />
                  <div>
                    <h3 className="font-semibold text-green-900">Import réussi</h3>
                    <dl className="mt-2 text-sm text-green-700 space-y-1">
                      <dt>Lignes lues: {result.lignes_lues}</dt>
                      <dt>Lignes insérées: {result.lignes_inserees}</dt>
                      <dt>Lignes mises à jour: {result.lignes_mises_a_jour}</dt>
                      {result.erreurs?.length > 0 && (
                        <dt className="mt-4 text-red-600">
                          Erreurs: {result.erreurs.length}
                        </dt>
                      )}
                    </dl>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  )
}
