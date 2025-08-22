import { useState, useEffect } from 'react'
import Layout from './Layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Users, 
  UserCheck, 
  UserX, 
  GraduationCap, 
  MapPin, 
  TrendingUp,
  RefreshCw,
  Brain
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const AdminDashboard = ({ user, onLogout, apiBaseUrl }) => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [trainingModel, setTrainingModel] = useState(false)

  // Mock data for demonstration
  const mockStats = {
    job_seekers: {
      total: 47,
      placed: 16,
      available: 31,
      placement_rate: 34.04,
      avg_diploma_score: 85.78,
      by_state: [
        { state: 'TAMIL NADU', count: 21 },
        { state: 'ANDHRA PRADESH', count: 11 },
        { state: 'WEST BENGAL', count: 9 },
        { state: 'UTTAR PRADESH', count: 6 }
      ],
      by_category: [
        { category: 'OBC', count: 32 },
        { category: 'Gen', count: 10 },
        { category: 'SC', count: 4 },
        { category: 'ST', count: 1 }
      ],
      by_gender: [
        { gender: 'Male', count: 29 },
        { gender: 'Female', count: 18 }
      ]
    },
    job_postings: {
      total: 5,
      active: 5
    },
    matches: {
      total: 0
    }
  }

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    setLoading(true)
    try {
      // For demo, use mock data
      // In real app: const response = await fetch(`${apiBaseUrl}/admin/statistics`)
      setTimeout(() => {
        setStats(mockStats)
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching stats:', error)
      setStats(mockStats)
      setLoading(false)
    }
  }

  const trainMLModel = async () => {
    setTrainingModel(true)
    try {
      // Simulate ML model training
      setTimeout(() => {
        setTrainingModel(false)
        // Show success message
      }, 3000)
    } catch (error) {
      console.error('Error training model:', error)
      setTrainingModel(false)
    }
  }

  const stateChartData = stats?.job_seekers.by_state || []
  const categoryChartData = stats?.job_seekers.by_category.map((item, index) => ({
    ...item,
    fill: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444'][index]
  })) || []

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
            <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="text-gray-600">Manage job seekers and monitor system performance</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline" onClick={fetchStats}>
              <RefreshCw className="mr-2 h-4 w-4" />
              Refresh
            </Button>
            <Button onClick={trainMLModel} disabled={trainingModel}>
              <Brain className="mr-2 h-4 w-4" />
              {trainingModel ? 'Training...' : 'Train ML Model'}
            </Button>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Job Seekers</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.job_seekers.total}</div>
              <p className="text-xs text-muted-foreground">
                Suryamitra trained candidates
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Placed Candidates</CardTitle>
              <UserCheck className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats?.job_seekers.placed}</div>
              <p className="text-xs text-muted-foreground">
                {stats?.job_seekers.placement_rate}% placement rate
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Available Candidates</CardTitle>
              <UserX className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{stats?.job_seekers.available}</div>
              <p className="text-xs text-muted-foreground">
                Ready for placement
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg. Diploma Score</CardTitle>
              <GraduationCap className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{stats?.job_seekers.avg_diploma_score}</div>
              <p className="text-xs text-muted-foreground">
                Out of 100
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* State Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>Candidates by State</CardTitle>
              <CardDescription>Distribution of job seekers across states</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stateChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="state" 
                    tick={{ fontSize: 12 }}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Category Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>Candidates by Category</CardTitle>
              <CardDescription>Social category distribution</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={categoryChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ category, count, percent }) => `${category}: ${count} (${(percent * 100).toFixed(0)}%)`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="count"
                  >
                    {categoryChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>System Status</CardTitle>
              <CardDescription>Current system performance</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Database Status</span>
                <Badge variant="success">Active</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">ML Model Status</span>
                <Badge variant="success">Trained</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">API Status</span>
                <Badge variant="success">Online</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Total Job Postings</span>
                <span className="text-sm text-gray-600">{stats?.job_postings.total}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Total Matches Generated</span>
                <span className="text-sm text-gray-600">{stats?.matches.total}</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Common administrative tasks</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button className="w-full justify-start" variant="outline">
                <Users className="mr-2 h-4 w-4" />
                View All Job Seekers
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <UserCheck className="mr-2 h-4 w-4" />
                Export Placement Report
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <TrendingUp className="mr-2 h-4 w-4" />
                Generate Analytics
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <Brain className="mr-2 h-4 w-4" />
                ML Model Performance
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  )
}

export default AdminDashboard

