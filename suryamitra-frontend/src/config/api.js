// API Configuration
const API_BASE_URL = 'http://localhost:5001/api'

// API endpoints
export const API_ENDPOINTS = {
  // Authentication
  LOGIN: '/auth/login',
  LOGOUT: '/auth/logout',
  
  // Admin endpoints
  ADMIN: {
    JOB_SEEKERS: '/admin/job-seekers',
    STATISTICS: '/admin/statistics',
    TRAIN_MODEL: '/admin/train-model'
  },
  
  // Employer endpoints
  EMPLOYER: {
    JOB_POSTINGS: '/employer/job-postings',
    MATCHES: '/employer/matches',
    DASHBOARD: '/employer/dashboard'
  }
}

// API utility functions
export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  }
  
  const config = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  }
  
  try {
    const response = await fetch(url, config)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}

// Authentication API
export const authAPI = {
  login: async (username, password) => {
    return apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
  },
  
  logout: async () => {
    return apiRequest('/auth/logout', {
      method: 'POST'
    })
  }
}

// Admin API
export const adminAPI = {
  getJobSeekers: async () => {
    return apiRequest(API_ENDPOINTS.ADMIN.JOB_SEEKERS)
  },
  
  getStatistics: async () => {
    return apiRequest(API_ENDPOINTS.ADMIN.STATISTICS)
  },
  
  trainModel: async () => {
    return apiRequest(API_ENDPOINTS.ADMIN.TRAIN_MODEL, {
      method: 'POST'
    })
  }
}

// Employer API
export const employerAPI = {
  getJobPostings: async () => {
    return apiRequest(API_ENDPOINTS.EMPLOYER.JOB_POSTINGS)
  },
  
  createJobPosting: async (jobData) => {
    return apiRequest(API_ENDPOINTS.EMPLOYER.JOB_POSTINGS, {
      method: 'POST',
      body: JSON.stringify(jobData)
    })
  },
  
  getMatches: async (jobId) => {
    return apiRequest(`${API_ENDPOINTS.EMPLOYER.MATCHES}/${jobId}`)
  },
  
  getDashboard: async () => {
    return apiRequest(API_ENDPOINTS.EMPLOYER.DASHBOARD)
  }
}

export default API_BASE_URL

