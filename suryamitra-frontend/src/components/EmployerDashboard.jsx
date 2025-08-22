import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Layout from './Layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Briefcase, 
  Users, 
  Target, 
  TrendingUp,
  Plus,
  Eye,
  RefreshCw,
  Star
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const EmployerDashboard = ({ user, onLogout, apiBaseUrl }) => {
  const [stats, setStats] = useState(null)
  const [recentMatches, setRecentMatches] = useState([])
  const [topCandidates, setTopCandidates] = useState([])
  const [loading, setLoading] = useState(true)

  // Mock data for demonstration
  const mockStats = {
    job_postings: {
      total: 5,
      active: 5
    },
    matches: {
      total: 0
    }
  }

  const mockRecentMatches = []

  const mockTopCandidates = [
    {
      id: 1,
      name: 'Ramya Nithya Sri S L',
      city: 'Coimbatore',
      state: 'TAMIL NADU',
      avg_match_score: 94.5,
      total_matches: 3
    },
    {
      id: 2,
      name: 'Krishna Moorthi D',
      city: 'Coimbatore', 
      state: 'TAMIL NADU',
      avg_match_score: 92.8,
      total_matches: 2
    },
    {
      id: 3,
      name: 'Kavitha M',
      city: 'Coimbatore',
      state: 'TAMIL NADU', 
      avg_match_score: 91.2,
      total_matches: 2
    }
  ]

  const mockJobPostings = [
    {
      id: 1,
      title: 'Solar Panel Installation Technician',
      city: 'Coimbatore',
      state: 'TAMIL NADU',
      salary_min: 18000,
      salary_max: 30000,
      status: 'active',
      created_at: '2025-01-21T10:00:00Z'
    },
    {
      id: 2,
      title: 'Solar System Maintenance Engineer',
      city: 'Vijayawada',
      state: 'ANDHRA PRADESH',
      salary_min: 20000,
      salary_max: 35000,
      status: 'active',
      created_at: '2025-01-21T10:00:00Z'
    }
  ]

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    setLoading(true)
    try {
      // For demo, use mock data
      setTimeout(() => {
        setStats(mockStats)
        setRecentMatches(mockRecentMatches)
        setTopCandidates(mockTopCandidates)
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      setStats(mockStats)
      setRecentMatches(mockRecentMatches)
      setTopCandidates(mockTopCandidates)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout user={user} onLogout={onLogout}>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout user={user} onLogout={onLogout}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Employer Dashboard</h1>
            <p className="text-gray-600">Find the perfect candidates for your job openings</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline" onClick={fetchDashboardData}>
              <RefreshCw className="mr-2 h-4 w-4" />
              Refresh
            </Button>
            <Button asChild>
              <Link to="/employer/jobs">
                <Plus className="mr-2 h-4 w-4" />
                Post New Job
              </Link>
            </Button>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Job Postings</CardTitle>
              <Briefcase className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.job_postings.active}</div>
              <p className="text-xs text-muted-foreground">
                Out of {stats?.job_postings.total} total
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Matches</CardTitle>
              <Target className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats?.matches.total}</div>
              <p className="text-xs text-muted-foreground">
                Candidates matched
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Available Candidates</CardTitle>
              <Users className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">47</div>
              <p className="text-xs text-muted-foreground">
                Suryamitra trained
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg. Match Score</CardTitle>
              <TrendingUp className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">85%</div>
              <p className="text-xs text-muted-foreground">
                Quality matches
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Recent Job Postings */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Your Job Postings</CardTitle>
                <CardDescription>Manage your active job listings</CardDescription>
              </div>
              <Button asChild variant="outline">
                <Link to="/employer/jobs">
                  <Eye className="mr-2 h-4 w-4" />
                  View All
                </Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockJobPostings.map((job) => (
                <div key={job.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{job.title}</h3>
                    <p className="text-sm text-gray-600">
                      {job.city}, {job.state} • ₹{job.salary_min.toLocaleString()} - ₹{job.salary_max.toLocaleString()}
                    </p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge variant="success">{job.status}</Badge>
                    <Button asChild size="sm" variant="outline">
                      <Link to={`/employer/jobs/${job.id}/matches`}>
                        <Target className="mr-2 h-4 w-4" />
                        View Matches
                      </Link>
                    </Button>
                  </div>
                </div>
              ))}
              
              {mockJobPostings.length === 0 && (
                <div className="text-center py-8">
                  <Briefcase className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No job postings</h3>
                  <p className="mt-1 text-sm text-gray-500">Get started by creating your first job posting.</p>
                  <div className="mt-6">
                    <Button asChild>
                      <Link to="/employer/jobs">
                        <Plus className="mr-2 h-4 w-4" />
                        Create Job Posting
                      </Link>
                    </Button>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Top Candidates */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Top Candidates</CardTitle>
              <CardDescription>Highest scoring candidates available for placement</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topCandidates.map((candidate, index) => (
                  <div key={candidate.id} className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-sm font-medium text-blue-600">#{index + 1}</span>
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {candidate.name}
                      </p>
                      <p className="text-sm text-gray-500">
                        {candidate.city}, {candidate.state}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Star className="h-4 w-4 text-yellow-400 fill-current" />
                      <span className="text-sm font-medium text-gray-900">
                        {candidate.avg_match_score}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Common tasks and shortcuts</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button className="w-full justify-start" variant="outline" asChild>
                <Link to="/employer/jobs">
                  <Plus className="mr-2 h-4 w-4" />
                  Create New Job Posting
                </Link>
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <Users className="mr-2 h-4 w-4" />
                Browse All Candidates
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <Target className="mr-2 h-4 w-4" />
                View All Matches
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <TrendingUp className="mr-2 h-4 w-4" />
                Download Reports
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  )
}

export default EmployerDashboard

