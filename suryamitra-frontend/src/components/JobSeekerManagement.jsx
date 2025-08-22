import { useState, useEffect } from 'react'
import Layout from './Layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { 
  Search, 
  Filter, 
  Plus, 
  Edit, 
  Trash2, 
  Download,
  Upload,
  Eye,
  Phone,
  Mail,
  MapPin,
  GraduationCap,
  Star
} from 'lucide-react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const JobSeekerManagement = ({ user, onLogout, apiBaseUrl }) => {
  const [jobSeekers, setJobSeekers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterState, setFilterState] = useState('all')
  const [filterCategory, setFilterCategory] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')

  // Mock data for demonstration
  const mockJobSeekers = [
    {
      id: 1,
      name: 'Ramya Nithya Sri S L',
      phone_number: '+91-9876543210',
      email: 'ramya.nithya@email.com',
      city: 'Coimbatore',
      state: 'TAMIL NADU',
      qualifications: 'ITI in Solar Technology',
      diploma_score: 95.00,
      experience_years: 2,
      category: 'Gen',
      gender: 'Female',
      training_result: 'Pass',
      placement_status: 'Placed',
      availability_status: 'available',
      skills: ['Solar Panel Installation', 'Electrical Wiring', 'System Maintenance']
    },
    {
      id: 2,
      name: 'Krishna Moorthi D',
      phone_number: '+91-9876543211',
      email: 'krishna.moorthi@email.com',
      city: 'Coimbatore',
      state: 'TAMIL NADU',
      qualifications: 'Diploma in Electrical Engineering',
      diploma_score: 94.37,
      experience_years: 3,
      category: 'OBC',
      gender: 'Male',
      training_result: 'Pass',
      placement_status: 'Placed',
      availability_status: 'available',
      skills: ['Solar Installation', 'Electrical Systems', 'Project Management']
    },
    {
      id: 3,
      name: 'Kavitha M',
      phone_number: '+91-9876543212',
      email: 'kavitha.m@email.com',
      city: 'Coimbatore',
      state: 'TAMIL NADU',
      qualifications: 'ITI in Electronics',
      diploma_score: 94.70,
      experience_years: 1,
      category: 'SC',
      gender: 'Female',
      training_result: 'Pass',
      placement_status: 'Placed',
      availability_status: 'available',
      skills: ['Solar Panel Maintenance', 'Electronics', 'Quality Control']
    },
    {
      id: 4,
      name: 'Jayapriya C',
      phone_number: '+91-9876543213',
      email: 'jayapriya.c@email.com',
      city: 'Coimbatore',
      state: 'TAMIL NADU',
      qualifications: 'Diploma in Mechanical Engineering',
      diploma_score: 87.59,
      experience_years: 2,
      category: 'OBC',
      gender: 'Female',
      training_result: 'Pass',
      placement_status: 'Placed',
      availability_status: 'available',
      skills: ['Mechanical Systems', 'Solar Installation', 'Technical Support']
    },
    {
      id: 5,
      name: 'Krishnaveni B',
      phone_number: '+91-9876543214',
      email: 'krishnaveni.b@email.com',
      city: 'Coimbatore',
      state: 'TAMIL NADU',
      qualifications: 'ITI in Electrical',
      diploma_score: 88.25,
      experience_years: 1,
      category: 'OBC',
      gender: 'Female',
      training_result: 'Pass',
      placement_status: 'Placed',
      availability_status: 'available',
      skills: ['Electrical Installation', 'Solar Systems', 'Safety Protocols']
    }
  ]

  useEffect(() => {
    fetchJobSeekers()
  }, [])

  const fetchJobSeekers = async () => {
    setLoading(true)
    try {
      // For demo, use mock data
      setTimeout(() => {
        setJobSeekers(mockJobSeekers)
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching job seekers:', error)
      setJobSeekers(mockJobSeekers)
      setLoading(false)
    }
  }

  const filteredJobSeekers = jobSeekers.filter(seeker => {
    const matchesSearch = seeker.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         seeker.city.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         seeker.qualifications.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesState = filterState === 'all' || seeker.state === filterState
    const matchesCategory = filterCategory === 'all' || seeker.category === filterCategory
    const matchesStatus = filterStatus === 'all' || seeker.placement_status === filterStatus

    return matchesSearch && matchesState && matchesCategory && matchesStatus
  })

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Placed':
        return <Badge variant="success">Placed</Badge>
      case 'Not Placed':
        return <Badge variant="destructive">Not Placed</Badge>
      default:
        return <Badge variant="secondary">Unknown</Badge>
    }
  }

  const getCategoryBadge = (category) => {
    const colors = {
      'Gen': 'bg-blue-100 text-blue-800',
      'OBC': 'bg-green-100 text-green-800',
      'SC': 'bg-yellow-100 text-yellow-800',
      'ST': 'bg-purple-100 text-purple-800'
    }
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[category] || 'bg-gray-100 text-gray-800'}`}>
        {category}
      </span>
    )
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
            <h1 className="text-2xl font-bold text-gray-900">Job Seeker Management</h1>
            <p className="text-gray-600">Manage Suryamitra trained candidates</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline">
              <Upload className="mr-2 h-4 w-4" />
              Import CSV
            </Button>
            <Button variant="outline">
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Candidate
            </Button>
          </div>
        </div>

        {/* Filters */}
        <Card>
          <CardHeader>
            <CardTitle>Search & Filter</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search candidates..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <Select value={filterState} onValueChange={setFilterState}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by State" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All States</SelectItem>
                  <SelectItem value="TAMIL NADU">Tamil Nadu</SelectItem>
                  <SelectItem value="ANDHRA PRADESH">Andhra Pradesh</SelectItem>
                  <SelectItem value="WEST BENGAL">West Bengal</SelectItem>
                  <SelectItem value="UTTAR PRADESH">Uttar Pradesh</SelectItem>
                </SelectContent>
              </Select>

              <Select value={filterCategory} onValueChange={setFilterCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="Gen">General</SelectItem>
                  <SelectItem value="OBC">OBC</SelectItem>
                  <SelectItem value="SC">SC</SelectItem>
                  <SelectItem value="ST">ST</SelectItem>
                </SelectContent>
              </Select>

              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="Placed">Placed</SelectItem>
                  <SelectItem value="Not Placed">Not Placed</SelectItem>
                  <SelectItem value="Unknown">Unknown</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Results Summary */}
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-600">
            Showing {filteredJobSeekers.length} of {jobSeekers.length} candidates
          </p>
        </div>

        {/* Job Seekers Table */}
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Candidate</TableHead>
                  <TableHead>Contact</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead>Qualifications</TableHead>
                  <TableHead>Score</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredJobSeekers.map((seeker) => (
                  <TableRow key={seeker.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium text-gray-900">{seeker.name}</div>
                        <div className="text-sm text-gray-500">{seeker.gender} • {seeker.experience_years} years exp</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="space-y-1">
                        <div className="flex items-center text-sm text-gray-600">
                          <Phone className="mr-1 h-3 w-3" />
                          {seeker.phone_number}
                        </div>
                        <div className="flex items-center text-sm text-gray-600">
                          <Mail className="mr-1 h-3 w-3" />
                          {seeker.email}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center text-sm text-gray-600">
                        <MapPin className="mr-1 h-3 w-3" />
                        {seeker.city}, {seeker.state}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm">
                        <div className="font-medium">{seeker.qualifications}</div>
                        <div className="text-gray-500">{seeker.skills.slice(0, 2).join(', ')}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <Star className="mr-1 h-4 w-4 text-yellow-400 fill-current" />
                        <span className="font-medium">{seeker.diploma_score}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      {getCategoryBadge(seeker.category)}
                    </TableCell>
                    <TableCell>
                      {getStatusBadge(seeker.placement_status)}
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button size="sm" variant="outline">
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {filteredJobSeekers.length === 0 && (
          <Card>
            <CardContent className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <Search className="mx-auto h-12 w-12" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No candidates found</h3>
              <p className="text-gray-600">Try adjusting your search or filter criteria.</p>
            </CardContent>
          </Card>
        )}
      </div>
    </Layout>
  )
}

export default JobSeekerManagement

