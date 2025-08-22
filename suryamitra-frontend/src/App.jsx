import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'sonner'
import './App.css'

// Import components
import LoginPage from './components/LoginPage'
import AdminDashboard from './components/AdminDashboard'
import EmployerDashboard from './components/EmployerDashboard'
import JobSeekerManagement from './components/JobSeekerManagement'
import JobPostingManagement from './components/JobPostingManagement'
import CandidateMatching from './components/CandidateMatching'

// API base URL
const API_BASE_URL = 'http://localhost:5000/api'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for stored user session
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
    setLoading(false)
  }, [])

  const login = (userData) => {
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          {/* Public routes */}
          <Route 
            path="/login" 
            element={
              user ? (
                <Navigate to={user.role === 'admin' ? '/admin' : '/employer'} replace />
              ) : (
                <LoginPage onLogin={login} apiBaseUrl={API_BASE_URL} />
              )
            } 
          />
          
          {/* Protected routes */}
          {user ? (
            <>
              {/* Admin routes */}
              {user.role === 'admin' && (
                <>
                  <Route 
                    path="/admin" 
                    element={<AdminDashboard user={user} onLogout={logout} apiBaseUrl={API_BASE_URL} />} 
                  />
                  <Route 
                    path="/admin/job-seekers" 
                    element={<JobSeekerManagement user={user} onLogout={logout} apiBaseUrl={API_BASE_URL} />} 
                  />
                </>
              )}
              
              {/* Employer routes */}
              {user.role === 'employer' && (
                <>
                  <Route 
                    path="/employer" 
                    element={<EmployerDashboard user={user} onLogout={logout} apiBaseUrl={API_BASE_URL} />} 
                  />
                  <Route 
                    path="/employer/jobs" 
                    element={<JobPostingManagement user={user} onLogout={logout} apiBaseUrl={API_BASE_URL} />} 
                  />
                  <Route 
                    path="/employer/jobs/:jobId/matches" 
                    element={<CandidateMatching user={user} onLogout={logout} apiBaseUrl={API_BASE_URL} />} 
                  />
                </>
              )}
              
              {/* Default redirect based on role */}
              <Route 
                path="/" 
                element={<Navigate to={user.role === 'admin' ? '/admin' : '/employer'} replace />} 
              />
            </>
          ) : (
            <Route path="*" element={<Navigate to="/login" replace />} />
          )}
        </Routes>
        
        <Toaster />
      </div>
    </Router>
  )
}

export default App

